import { Link } from "react-router-dom";
import { Users } from "lucide-react";
import { SidebarMenuButton, SidebarMenuItem } from "@/shared/ui/sidebar";
import {
  ContextMenu, ContextMenuTrigger, ContextMenuContent,
  ContextMenuItem, ContextMenuSeparator, ContextMenuLabel,
} from "@/shared/ui/context-menu";
import type { WorkingGroupItem } from "./types";

export function WorkingGroupRow({
  g, to, isActive, onClick, onRename, onDelete, deleting,
}: {
  g: WorkingGroupItem;
  to: string;
  isActive: boolean;
  onClick?: () => void;
  onRename: (g: WorkingGroupItem) => void; // пока заглушка
  onDelete: (g: WorkingGroupItem) => void; // откроет диалог
  deleting?: boolean;
}) {
  return (
    <SidebarMenuItem>
      <ContextMenu>
        <ContextMenuTrigger asChild>
          <SidebarMenuButton asChild isActive={isActive} tooltip={g.name} className="group">
            <Link to={to} onClick={onClick}>
              <Users className="mr-2 h-4 w-4" />
              <span className="truncate">{g.name}</span>
            </Link>
          </SidebarMenuButton>
        </ContextMenuTrigger>

        <ContextMenuContent>
          <ContextMenuLabel>{g.name}</ContextMenuLabel>
          <ContextMenuSeparator />
          <ContextMenuItem onClick={() => onRename(g)}>Переименовать</ContextMenuItem>
          <ContextMenuItem onClick={() => onDelete(g)} className="text-destructive" disabled={deleting}>
            {deleting ? "Удаляю…" : "Удалить"}
          </ContextMenuItem>
        </ContextMenuContent>
      </ContextMenu>
    </SidebarMenuItem>
  );
}
