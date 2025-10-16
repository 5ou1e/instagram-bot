"use client";

import * as React from "react";
import { Button } from "@/shared/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/shared/ui/dialog";
import { Label } from "@/shared/ui/label";
import { Textarea } from "@/shared/ui/textarea";
import { toast } from "sonner";

// ⚠️ Импорт API подправь под свой путь:
import { setAccountsComments } from "@/shared/api/accounts";
// если у тебя это в другом модуле, укажи корректный импорт

type Props = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  accountIds: string[];
  onSuccess?: () => void;    // вызовем после удачной установки
};

export function SetAccountsCommentDialog({ open, onOpenChange, accountIds, onSuccess }: Props) {
  const [comment, setComment] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  // если диалог закрыли — чистим поле
  React.useEffect(() => {
    if (!open) setComment("");
  }, [open]);

  async function handleSubmit() {
    if (!accountIds?.length) return;
    if (!comment.trim()) {
      toast.error("Введите комментарий");
      return;
    }
    setLoading(true);
    try {
      await toast.promise(
        setAccountsComments(accountIds, comment),
        {
          loading: "Устанавливаем комментарий…",
          success: "Комментарий установлен",
          error: (e) => (e instanceof Error ? e.message : "Ошибка при установке комментария"),
        }
      );
      onOpenChange(false);
      onSuccess?.();
    } finally {
      setLoading(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={(v) => !loading && onOpenChange(v)}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>Установить комментарий для аккаунтов ({accountIds.length})</DialogTitle>
        </DialogHeader>

        <div className="space-y-2">
          <Label htmlFor="comment">Комментарий</Label>
          <Textarea
            id="comment"
            placeholder="…"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            disabled={loading}
            rows={4}
          />
        </div>

        <DialogFooter className="gap-2">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={loading}>
            Отмена
          </Button>
          <Button onClick={handleSubmit} disabled={loading || !comment.trim()}>
            Установить
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
