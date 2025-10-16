"use client";

import * as React from "react";
import { useState } from "react";
import { Button } from "@/shared/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogTrigger,
} from "@/shared/ui/dialog";
import { Textarea } from "@/shared/ui/textarea";

type Props = {
  children?: React.ReactNode;
  onAdd: (lines: string[]) => Promise<void> | void;
};

export function AddProxiesDialog({ children, onAdd }: Props) {
  const [open, setOpen] = useState(false);
  const [raw, setRaw] = useState("");

  async function handleAdd() {
    const lines = raw
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);

    await onAdd(lines);
    setRaw("");
    setOpen(false);
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>Добавить прокси</DialogTitle>
        </DialogHeader>

        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">
            По одному на строку. Форматы:
            {" "}
            <code className="font-mono">host:port</code> или{" "}
            <code className="font-mono">host:port:username:password</code>
          </p>
          <Textarea
            rows={10}
            value={raw}
            onChange={(e) => setRaw(e.target.value)}
            placeholder={"1.2.3.4:8080\n5.6.7.8:3128:user:pass"}
          />
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            Отмена
          </Button>
          <Button onClick={handleAdd} disabled={!raw.trim()}>
            Добавить
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
