"use client";

import * as React from "react";
import { useEffect, useState } from "react";
import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";
import { MoreHorizontal, Trash2, Copy, Rows3, X, Download, Play, Rocket } from "lucide-react";
import {
  useReactTable,
  getCoreRowModel,
  type SortingState,
  type RowSelectionState,
} from "@tanstack/react-table";

import { toast } from "sonner";

import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuItem,
} from "@/shared/ui/dropdown-menu";
import { Button } from "@/shared/ui/button";
import { DataTable } from "@/shared/ui/data-table/data-table";
import { DataTableToolbar } from "@/shared/ui/data-table/data-table-toolbar";
import { DataTableSortList } from "@/shared/ui/data-table/data-table-sort-list";
import { DataTableActionBar } from "@/shared/ui/data-table/data-table-action-bar";
import { CustomTableActions } from "@/shared/ui/data-table/custom-table-actions";
import { DataTableFilterMenu } from "@/shared/ui/data-table/data-table-filter-menu";
import { DataTableAdvancedToolbar } from "@/shared/ui/data-table/data-table-advanced-toolbar";
import { DataTableFilterList } from "@/shared/ui/data-table/data-table-filter-list";

import { AddAccountWorkersDialog } from "@/features/working-group/ui/add-account-workers-dialog"
import { fetchWorkingGroupWorkers , createWorkingGroupWorkers, deleteWorkingGroupWorkers, startWorkingGroupWorkers } from "@/shared/api/working-groups";
import type { Worker } from "@/types/working-groups";
import { AccountWorkersTableColumns } from "./account-workers-table-columns";


import { WorkerRowContextMenu } from "./account-workers-table-row-context-menu";

import { LogsDialog } from "@/features/working-group/ui/account-worker-logs-dialog"; // путь подкорректируй

type Props = { wgId: string; initialPageSize?: number };

export default function AccountWorkersTable({ wgId, initialPageSize = 50 }: Props) {
  const qc = useQueryClient();



  // контролируемая таблица
  const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: initialPageSize });
  const [sorting, setSorting] = useState<SortingState>([{ id: "created_at", desc: true }]);
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({});

    const POLL_MS = 1000;

    const { data, isFetching, error, refetch } = useQuery({
        queryKey: ["wg_workers", wgId, pagination.pageIndex, pagination.pageSize, sorting],
        queryFn: () =>
            fetchWorkingGroupWorkers({
                groupId: wgId,
                pageIndex: pagination.pageIndex,
                pageSize: pagination.pageSize,
            }),
        keepPreviousData: true,
        enabled: !!wgId,
        refetchInterval: POLL_MS,             // ← опрос раз в 1 сек
        refetchIntervalInBackground: true,    // ← даже когда вкладка не активна (опционально)
        refetchOnWindowFocus: false,          // ← не дёргать лишний раз при фокусе
    });


  const rows = data?.rows ?? [];
  const pageCount = data?.pageCount ?? 1;

  const [columnPinning, setColumnPinning] = useState<ColumnPinningState>({
    left: ["select"],
    right: ["actions"],
  })

  // скрываем по умолчанию: account_id, password, last_action_time
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({
    id: false,
    account_id: false,
    password: false,
    last_action_time: false, // смотри, что accessorKey у тебя именно такой
    created_at: false,
  });

  const table = useReactTable<Worker>({
    data: rows,
    columns: AccountWorkersTableColumns,
    pageCount,
    state: {
      pagination, sorting, rowSelection,
      columnPinning, // 👈
      columnVisibility,
    },
    onPaginationChange: setPagination,
    onSortingChange: setSorting,
    onRowSelectionChange: setRowSelection,
    onColumnPinningChange: setColumnPinning,
    onColumnVisibilityChange: setColumnVisibility,
    enablePinning: true, // 👈 важно
    manualPagination: true,
    getCoreRowModel: getCoreRowModel(),
  })

  // === АКШЕНЫ ===
  const selected = table.getSelectedRowModel().rows.map((r) => r.original);
  const selectedIds = selected.map((w) => w.id);
  const hasSelection = selectedIds.length > 0;

  function copySelectedIds() {
    if (!hasSelection) return;
    navigator.clipboard.writeText(selectedIds.join("\n"));
  }

    // ── состояние модалки логов (глобально для таблицы)
    const [logDialog, setLogDialog] = React.useState<{
        open: boolean;
        accountId: string | null;
        username: string | null;
    }>({ open: false, accountId: null, username: null });

    const openLogs = React.useCallback((accountId: string, username?: string) => {
        setLogDialog({ open: true, accountId, username: username ?? null });
    }, []);

  async function deleteSelectedWorkers() {
    if (!hasSelection) return;
    if (!confirm(`Удалить выбранные (${selectedIds.length})?`)) return;
    await toast.promise(deleteWorkingGroupWorkers(wgId, selectedIds), {
      loading: "Удаляем…",
      success: "Удалено",
      error: (err) => (err instanceof Error ? err.message : "Ошибка удаления"),
    });

    table.resetRowSelection();
    await qc.invalidateQueries({ queryKey: ["wg_workers"] });

    await refetch();
  }

  async function deleteAllWorkers() {
    if (!confirm("Удалить все аккаунты во всех страницах?")) return;
    await deleteWorkingGroupWorkers(wgId, null)
    setPagination(p => ({ ...p, pageIndex: 0 }));
    await qc.invalidateQueries({ queryKey: ["wg_workers"] });
    await refetch();
  }

  async function startSelectedWorkers() {
    if (!hasSelection) return;
    if (!confirm(`Запустить выбранные (${selectedIds.length})?`)) return;
    await startWorkingGroupWorkers(wgId, selectedIds)
    await refetch();
  }

  return (
    <div className="space-y-3">
      {/* === ПАНЕЛЬ НАД ТАБЛИЦЕЙ === */}


      {error && <div className="text-destructive mb-2">{String(error)}</div>}

      {/* сама таблица */}
      <div className="relative">
          {isFetching && !data && (
              <div className="absolute inset-0 grid place-items-center bg-background/60 backdrop-blur-sm z-10 pointer-events-none">
                  Loading…
              </div>
          )}

      <DataTable
        table={table}
        rowContextMenu={(row) => (
          <WorkerRowContextMenu row={row} wgId={wgId} refetch={refetch} onOpenLogs={openLogs} />
        )}
      >
      <DataTableToolbar table={table}>
         <AddAccountWorkersDialog
           onAdd={async (lines) => {
             await createWorkingGroupWorkers(wgId, lines)
             await refetch()
           }}
         />
         {/*
        <DataTableFilterList table={table} />
        <DataTableFilterMenu table={table} />
        <DataTableSortList table={table} />
        */}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="outline" size="sm">
                      Действия <MoreHorizontal className="ml-2 h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end" className="w-56">
                    <DropdownMenuLabel>Массовые действия</DropdownMenuLabel>

                    <DropdownMenuItem disabled={!hasSelection} onClick={startSelectedWorkers}>
                      <Play className="mr-2 h-4 w-4" />
                      Запустить выбранные
                    </DropdownMenuItem>

                    <DropdownMenuItem onClick={deleteAllWorkers}>
                      <Trash2 className="mr-2 h-4 w-4" />
                      Удалить все
                    </DropdownMenuItem>

                    <DropdownMenuItem disabled={!hasSelection} onClick={deleteSelectedWorkers}>
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
      {/* Модалка — РЕНДЕРИМ ВНЕ МЕНЮ */}
      <LogsDialog
          open={logDialog.open}
          onOpenChange={(v) => setLogDialog((s) => ({ ...s, open: v }))}
          accountId={logDialog.accountId}
          username={logDialog.username}
      />
      </div>
    </div>
  );
}
