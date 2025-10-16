"use client";

import * as React from "react";
import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  useReactTable,
  getCoreRowModel,
  type SortingState,
  type RowSelectionState,
  type ColumnPinningState,
  type VisibilityState,
} from "@tanstack/react-table";
import { MoreHorizontal, Trash2, Copy, Plus } from "lucide-react";
import { toast } from "sonner";

import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuItem,
} from "@/shared/ui/dropdown-menu";
import { Button } from "@/shared/ui/button";
import { DataTable } from "@/shared/ui/data-table/data-table";
import { DataTableToolbar } from "@/shared/ui/data-table/data-table-toolbar";

import { ProxiesTableColumns } from "./proxies-table-columns";
import { AddProxiesDialog } from "@/features/proxies/ui/add-proxies-dialog";
import { fetchProxies, deleteProxies, createProxies } from "@/shared/api/proxies";
import type { Proxy } from "@/types/proxy";

type Props = { initialPageSize?: number };

export default function ProxiesTable({ initialPageSize = 50 }: Props) {
  const qc = useQueryClient();

  const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: initialPageSize });
  const [sorting, setSorting] = useState<SortingState>([{ id: "created_at", desc: true }]);
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({});

  const POLL_MS = 1000;

  const { data, isFetching, error, refetch } = useQuery({
    queryKey: ["proxies", pagination.pageIndex, pagination.pageSize, sorting],
    queryFn: () =>
      fetchProxies({
        pageIndex: pagination.pageIndex,
        pageSize: pagination.pageSize,
      }),
    keepPreviousData: true,
    refetchInterval: POLL_MS,
    refetchIntervalInBackground: true,
    refetchOnWindowFocus: false,
  });

  const rows: Proxy[] = data?.rows ?? [];
  const pageCount = data?.pageCount ?? 1;

  const [columnPinning, setColumnPinning] = useState<ColumnPinningState>({
    left: ["select"],
    right: [],
  });

  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({
    password: true,
    created_at: true,
  });

  const table = useReactTable<Proxy>({
    data: rows,
    columns: ProxiesTableColumns,
    pageCount,
    state: { pagination, sorting, rowSelection, columnPinning, columnVisibility },
    onPaginationChange: setPagination,
    onSortingChange: setSorting,
    onRowSelectionChange: setRowSelection,
    onColumnPinningChange: setColumnPinning,
    onColumnVisibilityChange: setColumnVisibility,
    enablePinning: true,
    manualPagination: true,
    getCoreRowModel: getCoreRowModel(),
  });

  const selected = table.getSelectedRowModel().rows.map((r) => r.original);
  const selectedIds = selected.map((p) => p.id);
  const hasSelection = selectedIds.length > 0;

  const copySelectedIds = () => {
    if (!hasSelection) return;
    navigator.clipboard.writeText(selectedIds.join("\n"));
  };

  const deleteSelected = async () => {
    if (!hasSelection) return;
    if (!confirm(`Удалить выбранные прокси (${selectedIds.length})?`)) return;

    await toast.promise(deleteProxies(selectedIds), {
      loading: "Удаляем…",
      success: "Удалено",
      error: (e) => (e instanceof Error ? e.message : "Ошибка удаления"),
    });

    table.resetRowSelection();
    await qc.invalidateQueries({ queryKey: ["proxies"] });
    await refetch();
  };

  const deleteAll = async () => {
    if (!confirm("Удалить все прокси?")) return;

    await toast.promise(deleteProxies(null), {
      loading: "Удаляем…",
      success: "Все прокси удалены",
      error: (e) => (e instanceof Error ? e.message : "Ошибка удаления"),
    });

    setPagination((p) => ({ ...p, pageIndex: 0 }));
    await qc.invalidateQueries({ queryKey: ["proxies"] });
    await refetch();
  };

  return (
    <div className="space-y-3">
      {error && <div className="text-destructive mb-2">{String(error)}</div>}

      <div className="relative">
        {isFetching && !data && (
          <div className="absolute inset-0 grid place-items-center bg-background/60 backdrop-blur-sm z-10 pointer-events-none">
            Loading…
          </div>
        )}

        <DataTable table={table}>
          <DataTableToolbar table={table}>
            <AddProxiesDialog
              onAdd={async (lines) => {
                await toast.promise(createProxies(lines), {
                  loading: "Добавляем…",
                  success: "Добавлено",
                  error: (e) => (e instanceof Error ? e.message : "Ошибка добавления"),
                });
                await qc.invalidateQueries({ queryKey: ["proxies"] });
                await refetch();
              }}
            >
              <Button size="sm">
                <Plus className="mr-2 h-4 w-4" />
                Добавить прокси
              </Button>
            </AddProxiesDialog>

            <div className="ml-auto" />

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" size="sm">
                  Действия <MoreHorizontal className="ml-2 h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>Массовые действия</DropdownMenuLabel>

                <DropdownMenuItem onClick={deleteAll}>
                  <Trash2 className="mr-2 h-4 w-4" />
                  Удалить все
                </DropdownMenuItem>

                <DropdownMenuItem disabled={!hasSelection} onClick={deleteSelected}>
                  <Trash2 className="mr-2 h-4 w-4" />
                  Удалить выбранные
                </DropdownMenuItem>

                <DropdownMenuItem disabled={!hasSelection} onClick={copySelectedIds}>
                  <Copy className="mr-2 h-4 w-4" />
                  Копировать ID выбранных
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </DataTableToolbar>
        </DataTable>
      </div>
    </div>
  );
}
