import * as React from "react";
import { useMatch, useNavigate } from "react-router-dom";
import { ChevronDown, Plus, AlertCircle } from "lucide-react";
import { Button } from "@/shared/ui/button";
import { ScrollArea } from "@/shared/ui/scroll-area";
import { Skeleton } from "@/shared/ui/skeleton";
import { SidebarGroup, SidebarGroupLabel, SidebarMenu } from "@/shared/ui/sidebar";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/shared/ui/collapsible";

import { ROUTES, linkToWorkingGroup } from "@/shared/routes";
import type { AppSidebarProps, WorkingGroupItem } from "../types";
import { useWorkingGroups } from "../use-working-groups";
import { WorkingGroupRow } from "../working-group-row";
import { CreateWorkingGroupDialog } from "../dialogs/create-working-group-dialog";
import { DeleteWorkingGroupDialog } from "../dialogs/delete-working-group-dialog";

export function WorkingGroupsSection({ currentGroupId, onGroupSelect }: AppSidebarProps) {

  const { groups, loading, error, load, create, creating, remove, deletingId } = useWorkingGroups();
  const wgMatch = useMatch(ROUTES.WORKING_GROUP);
  const activeGroupId = currentGroupId ?? wgMatch?.params.wgId;
  const navigate = useNavigate();

  const [open, setOpen] = React.useState(true);
  React.useEffect(() => {
    const saved = typeof window !== "undefined" ? localStorage.getItem("sidebar.wg.open") : null;
    if (saved !== null) setOpen(saved === "1");
  }, []);
  React.useEffect(() => {
    if (typeof window !== "undefined") localStorage.setItem("sidebar.wg.open", open ? "1" : "0");
  }, [open]);

  const [createOpen, setCreateOpen] = React.useState(false);
  const [deleteTarget, setDeleteTarget] = React.useState<WorkingGroupItem | null>(null);
  const onConfirmDelete = async (g: WorkingGroupItem) => {
    await remove(g.id);
    setDeleteTarget(null);
    if (activeGroupId === g.id) navigate(ROUTES.HOME, { replace: true });
  };

  const didInit = React.useRef(false);
  React.useEffect(() => {
    if (didInit.current) return;
    didInit.current = true;
    load();
  }, [load]);

  return (
    <>
      <SidebarGroup>
        <Collapsible open={open} onOpenChange={setOpen} className="w-full">
          {/* header row */}
          <div className="flex items-center justify-between gap-2 px-2 w-full">
            <div className="flex items-center gap-1">

              <SidebarGroupLabel>Рабочие группы</SidebarGroupLabel>
            </div>

            <div className="flex items-center gap-1">
              <Button
                size="icon"
                variant="ghost"
                className="h-7 w-7 rounded-md"
                title="Добавить группу"
                aria-label="Добавить группу"
                onClick={() => setCreateOpen(true)}
              >
                <Plus className="h-4 w-4" />
              </Button>
              <CollapsibleTrigger asChild>
                <Button
                  size="icon"
                  variant="ghost"
                  className="h-7 w-7 rounded-md transition-transform data-[state=closed]:-rotate-90"
                  aria-label={open ? "Свернуть" : "Развернуть"}
                  title={open ? "Свернуть" : "Развернуть"}
                >
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </CollapsibleTrigger>
            </div>
          </div>

          {/* content */}
          <CollapsibleContent className="w-full">
            <ScrollArea className="px-1">
              <SidebarMenu className="w-full">
                {loading && (
                  <div className="space-y-2 p-2">
                    <Skeleton className="h-7 w-full rounded-xl" />
                    <Skeleton className="h-7 w-5/6 rounded-xl" />
                    <Skeleton className="h-7 w-4/6 rounded-xl" />
                  </div>
                )}

                {/* ...error/empty... */}

                {!loading && !error && groups?.map((g) => (
                  <WorkingGroupRow
                    key={g.id}
                    g={g}
                    to={linkToWorkingGroup(g.id)}
                    isActive={activeGroupId === g.id}
                    onClick={() => onGroupSelect?.(g)}
                    onRename={(gg) => alert(`Переименовать «${gg.name}» — заглушка`)}
                    onDelete={(gg) => setDeleteTarget(gg)}
                    deleting={deletingId === g.id}
                  />
                ))}
              </SidebarMenu>
            </ScrollArea>
          </CollapsibleContent>
        </Collapsible>
      </SidebarGroup>

      <CreateWorkingGroupDialog
        open={createOpen}
        onOpenChange={setCreateOpen}
        onCreate={create}
        creating={creating}
      />

      <DeleteWorkingGroupDialog
        target={deleteTarget}
        deleting={!!deletingId}
        onCancel={() => setDeleteTarget(null)}
        onConfirm={onConfirmDelete}
      />
    </>
  );
}
