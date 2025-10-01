import { flexRender, type Table as TanstackTable, type Row } from "@tanstack/react-table";
import type * as React from "react";

import { DataTablePagination } from "@/shared/ui/data-table/data-table-pagination";
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/shared/ui/table";
import { getCommonPinningStyles } from "@/shared/lib/data-table";
import { cn } from "@/shared/lib/utils";

// 👉 импорт контекстного меню shadcn
import {
  ContextMenu,
  ContextMenuTrigger,
  ContextMenuContent,
} from "@/shared/ui/context-menu";

interface DataTableProps<TData> extends React.ComponentProps<"div"> {
  table: TanstackTable<TData>;
  actionBar?: React.ReactNode;
  // 👉 новый проп: функция, которая вернёт JSX пунктов меню для конкретной строки
  rowContextMenu?: (row: Row<TData>) => React.ReactNode;
}

export function DataTable<TData>({
  table,
  actionBar,
  rowContextMenu,
  children,
  className,
  ...props
}: DataTableProps<TData>) {
  return (
    <div className={cn("flex w-full h-[800px] flex-col gap-2.5", className)} {...props}>
      {children}

      <div className="flex flex-2/3 flex-col overflow-hidden rounded-md border">
        <Table className="table-fixed w-full">
          <TableHeader className="sticky top-0 z-10 bg-background shadow-md">
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead
                    key={header.id}
                    colSpan={header.colSpan}
                    className="whitespace-nowrap"
                    style={{ ...getCommonPinningStyles({ column: header.column }) }}
                  >
                    {header.isPlaceholder
                      ? null
                      : flexRender(header.column.columnDef.header, header.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>

          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => {
                const rowEl = (
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() ? "selected" : undefined}
                    className={row.getIsSelected() ? "bg-muted" : undefined} // fallback
                    // 👉 при правом клике выделяем строку (так привычнее)
                    onContextMenu={(e) => {
                      // если хочешь поддержать мультивыделение по Ctrl — проверь e.ctrlKey/e.metaKey
                      if (!row.getIsSelected()) {
                        table.resetRowSelection();
                        row.toggleSelected(true);
                      }
                    }}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell
                        key={cell.id}
                        className="p-0"
                        style={{ ...getCommonPinningStyles({ column: cell.column }) }}
                      >
                        <div className="px-3 py-2 truncate" title={String(cell.getValue?.() ?? "")}>
                          {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </div>
                      </TableCell>
                    ))}
                  </TableRow>
                );

                // 👉 если прокинули rowContextMenu — оборачиваем строку в ContextMenu
                return rowContextMenu ? (
                  <ContextMenu key={row.id}>
                    <ContextMenuTrigger asChild>{rowEl}</ContextMenuTrigger>
                    <ContextMenuContent className="w-56">
                      {rowContextMenu(row)}
                    </ContextMenuContent>
                  </ContextMenu>
                ) : (
                  rowEl
                );
              })
            ) : (
              <TableRow>
                <TableCell colSpan={table.getAllColumns().length} className="h-24 text-center">
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <div className="flex flex-col gap-2.5">
        <DataTablePagination table={table} />
        {actionBar && table.getFilteredSelectedRowModel().rows.length > 0 && actionBar}
      </div>
    </div>
  );
}
