import * as React from "react";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/shared/ui/dialog";
import { Button } from "@/shared/ui/button";
import { Input } from "@/shared/ui/input";

export function CreateWorkingGroupDialog({
  open, onOpenChange, onCreate, creating,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCreate: (name: string) => Promise<void> | void;
  creating: boolean;
}) {
  const [name, setName] = React.useState("");

  const submit = async () => {
    const v = name.trim();
    if (!v) return;
    await onCreate(v);
    setName("");
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Новая рабочая группа</DialogTitle>
          <DialogDescription>Введите название новой рабочей группы.</DialogDescription>
        </DialogHeader>

        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="wg-name">Название</label>
          <Input id="wg-name" value={name} onChange={(e) => setName(e.target.value)} autoFocus />
        </div>

        <DialogFooter className="gap-2 sm:gap-0">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={creating}>Отмена</Button>
          <Button onClick={submit} disabled={creating || !name.trim()}>
            {creating ? "Создаю…" : "Создать"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
