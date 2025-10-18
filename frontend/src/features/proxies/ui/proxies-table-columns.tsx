"use client";

import type { ColumnDef } from "@tanstack/react-table";
import { DataTableColumnHeader } from "@/shared/ui/data-table/data-table-column-header";
import { Checkbox } from "@/shared/ui/checkbox";
import type { Proxy } from "@/types/proxy";

const fmtDate = (iso?: string | null) => (iso ? new Date(iso).toLocaleString() : "—");
const mask = (s?: string | null) => (s && s.trim() ? s : "—");

export const ProxiesTableColumns: ColumnDef<Proxy>[] = [
  {
    id: "select",
    enablePinning: true,
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
  {
    accessorKey: "protocol",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Protocol" />,
    enableSorting: false,
    size: 50,
    cell: ({ getValue }) => <span className="uppercase">{String(getValue() ?? "—")}</span>,
  },

  {
    accessorKey: "host",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Host" />,
    enableSorting: false,
        size: 100,
  },
  {
    accessorKey: "port",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Port" />,
    enableSorting: false,
    size: 60,
    cell: ({ getValue }) => <span className="font-mono">{String(getValue() ?? "—")}</span>,
  },
  {
    accessorKey: "username",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Username" />,
    enableSorting: false,
    cell: ({ getValue }) => <span>{mask(getValue() as string | null)}</span>,
    size: 200,
  },
  {
    accessorKey: "password",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Password" />,
    enableSorting: false,
    cell: ({ getValue }) => {
      const v = getValue() as string | null;
      return <span className="font-mono break-all">{v ?? "—"}</span>; // ← показываем как есть
    },
  },
  {
    accessorKey: "created_at",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Добвлен" />,
    enableSorting: false,
    cell: ({ getValue }) => <span>{fmtDate(getValue() as string | null)}</span>,
  },
];
