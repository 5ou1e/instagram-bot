"use client"

import type { ColumnDef } from "@tanstack/react-table"
import { MoreHorizontal } from "lucide-react"

import { DataTableColumnHeader } from "@/shared/ui/data-table/data-table-column-header"
import { Badge } from "@/shared/ui/badge"
import { Checkbox } from "@/shared/ui/checkbox"
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "@/shared/ui/dropdown-menu"

import type { Worker } from "@/types/working-groups"

const fmtDate = (iso?: string | null) => (iso ? new Date(iso).toLocaleString() : "—")

export const AccountWorkersTableColumns: ColumnDef<Worker>[] = [
  // ── PIN LEFT ──────────────────────────────────────────────────────────────
  // Колонка выбора — закреплена слева
  {
    id: "select",
    enablePinning: true, // <- разрешаем пиннинг
    size: 32,
    header: ({ table }) => (
      <div className="w-9 text-center">
        <Checkbox
          key={`all-${table.getIsAllPageRowsSelected() ? "1" : "0"}`}
          checked={table.getIsAllPageRowsSelected()}
          onCheckedChange={(v) => table.toggleAllPageRowsSelected(!!v)}
          aria-label="Выбрать все на странице"
        />
      </div>
    ),
    cell: ({ row }) => (
      <div className="w-9 text-center">
        <Checkbox
          key={`${row.id}-${row.getIsSelected() ? "1" : "0"}`}
          checked={row.getIsSelected()}
          onCheckedChange={(v) => row.toggleSelected(!!v)}
          aria-label="Выбрать строку"
          onClick={(e) => e.stopPropagation()}
        />
      </div>
    ),
    enableSorting: false,
    enableHiding: false,
  },

  // ── DATA ──────────────────────────────────────────────────────────────────
  {
    accessorKey: "id",
    header: ({ column }) => <DataTableColumnHeader column={column} title="ID" />,
    enableSorting: false,
    enableColumnFilter: true,
  },
  {
    accessorKey: "account_id",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Account ID" />,
    enableSorting: false,
    cell: ({ getValue }) => <span className="font-mono">{String(getValue() ?? "—")}</span>,
  },
  {
    accessorKey: "username",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Username" />,
    enableSorting: false,
    enableColumnFilter: true,
    size: 100,
  },
  {
    accessorKey: "password",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Password" />,
    enableSorting: false,
  },
  {
    accessorKey: "work_state",
    header: ({ column }) => <DataTableColumnHeader column={column} title="State" />,
    cell: ({ getValue }) => <Badge variant="outline">{String(getValue() ?? "—")}</Badge>,
    enableSorting: false,
    enableColumnFilter: true,
    size: 50,
  },
  {
    accessorKey: "last_log_message",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Лог" />,
    cell: ({ getValue }) => <span>{(getValue() as string) ?? "—"}</span>,
    enableSorting: false,
    size: 400,
  },
  {
    id: "stats",
    header: "Stats",
    enableSorting: false,
    cell: ({ row }) => {
      const s = row.original.action_statistics
      return (
        <div className="text-xs text-muted-foreground">
          Follows: {s.follows} · Blocks: {s.follows_blocks} · Auth: {s.authorizations}
        </div>
      )
    },
  },
  {
    accessorKey: "last_action_time",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Last action" />,
    enableSorting: false,
    cell: ({ getValue }) => <span>{fmtDate(getValue() as string | null)}</span>,
  },
  {
    accessorKey: "created_at",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Created" />,
    enableSorting: false,
    cell: ({ getValue }) => <span>{fmtDate(getValue() as string | null)}</span>,
  },

  // ── PIN RIGHT (ACTIONS) ───────────────────────────────────────────────────
  // Колонка действий — закреплена справа и всегда последняя
  {
    id: "actions",
    enablePinning: true, // <- разрешаем пиннинг
    size: 48,
    enableSorting: false,
    header: "", // пустой заголовок
    cell: ({ row }) => {
      const w = row.original
      return (
        <div className="flex justify-end pr-1">
          <DropdownMenu>
            <DropdownMenuTrigger
              asChild
              onClick={(e) => e.stopPropagation()} // чтобы клик не трогал селект строки
            >
              <button
                className="inline-flex h-8 w-8 items-center justify-center rounded-md hover:bg-muted"
                aria-label="Actions"
              >
                <MoreHorizontal className="h-4 w-4" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-44">
              <DropdownMenuItem onClick={() => console.log("Start", w.id)}>
                Start (stub)
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => console.log("Stop", w.id)}>
                Stop (stub)
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => navigator.clipboard.writeText(w.id)}>
                Copy ID
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      )
    },
  },
]
