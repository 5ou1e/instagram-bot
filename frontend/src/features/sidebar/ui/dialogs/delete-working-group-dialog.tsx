import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/shared/ui/dialog";
import { Button } from "@/shared/ui/button";
import type { WorkingGroupItem } from "../types";

export function DeleteWorkingGroupDialog({
  target, deleting, onCancel, onConfirm,
}: {
  target: WorkingGroupItem | null;
  deleting: boolean;
  onCancel: () => void;
  onConfirm: (target: WorkingGroupItem) => void;
}) {
  return (
    <Dialog open={!!target} onOpenChange={(o) => !o && onCancel()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Удалить рабочую группу «{target?.name}» ?</DialogTitle>
          <DialogDescription>
            Подтвердите действие
          </DialogDescription>
        </DialogHeader>

        <DialogFooter className="gap-2 sm:gap-0">
          <Button variant="outline" onClick={onCancel} disabled={deleting}>Отмена</Button>
          <Button variant="destructive" onClick={() => target && onConfirm(target)} disabled={deleting}>
            {deleting ? "Удаляю…" : "Удалить"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
