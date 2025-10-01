// AddAccountWorkersDialog.tsx
import { toast } from "sonner";
import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter, DialogTrigger } from "@/shared/ui/dialog";
import { Button } from "@/shared/ui/button";
import { Textarea } from "@/shared/ui/textarea";

export function AddAccountWorkersDialog({
  onAdd,
}: {
  onAdd: (accounts: string[]) => Promise<void>;
}) {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAdd() {
    const lines = value
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);

    if (!lines.length) {
      toast.info("Добавь хотя бы одну строку");
      return;
    }

    setLoading(true);
    try {
      await toast.promise(onAdd(lines), {
        loading: "Добавляем аккаунты…",
        success: "Аккаунты успешно добавлены",
        error: (err) =>
          err instanceof Error ? err.message : "Неизвестная ошибка",
      });
      // если onAdd прошёл — очищаем и закрываем
      setValue("");
      setOpen(false);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">Добавить аккаунты</Button>
      </DialogTrigger>

      <DialogContent className="sm:max-w-4xl min-h-[70vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>Добавить аккаунты</DialogTitle>
          <DialogDescription>
            Вставь список аккаунтов (по одному на строку).
          </DialogDescription>
        </DialogHeader>

        <Textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="username:password\nusername2:password2"
          className="flex-1 resize-none"
        />

        <DialogFooter className="mt-4">
          <Button variant="outline" onClick={() => setOpen(false)} disabled={loading}>
            Отмена
          </Button>
          <Button onClick={handleAdd} disabled={loading}>
            {loading ? "Добавление…" : "Добавить"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
