
"use client";

import * as React from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/shared/ui/dialog";
import { ScrollArea, ScrollBar } from "@/shared/ui/scroll-area";
import { Button } from "@/shared/ui/button";
import { fetchWorkingGroupWorkerLogs } from "@/shared/api/working-groups";

type LogsDialogProps = {
    open: boolean;
    onOpenChange: (v: boolean) => void;
    accountId: string | null;
    username?: string | null;
};

export function LogsDialog({ open, onOpenChange, accountId, username }: LogsDialogProps) {
    const [loading, setLoading] = React.useState(false);
    const [logs, setLogs] = React.useState<
        { id: string; level: string; message: string; created_at: string }[]
    >([]);
    const [error, setError] = React.useState<string | null>(null);

    React.useEffect(() => {
        if (!open || !accountId) return;
        let cancelled = false;

        (async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await fetchWorkingGroupWorkerLogs({ accountIds: [accountId] });
                const normalized =
                    (data as any)?.result?.logs ??
                    (Array.isArray(data) ? data : (data as any)?.logs ?? []);
                if (!cancelled) setLogs(normalized ?? []);
            } catch (e) {
                if (!cancelled) setError(e instanceof Error ? e.message : "Не удалось загрузить логи");
            } finally {
                if (!cancelled) setLoading(false);
            }
        })();

        return () => {
            cancelled = true;
        };
    }, [open, accountId]);

    function levelClasses(level?: string) {
        const l = (level ?? "").toUpperCase();
        switch (l) {
            case "DEBUG":
                return {
                    text: "text-muted-foreground",
                    border: "border-gray-300 dark:border-gray-700",
                    bg: "",
                };
            case "INFO":
                return {
                    text: "text-foreground",
                    border: "border-zinc-300/70 dark:border-zinc-700/70",
                    bg: "",
                };
            case "WARNING":
            case "WARN":
                return {
                    text: "text-amber-600 dark:text-amber-400",
                    border: "border-amber-500/60 dark:border-amber-400/60",
                    bg: "bg-amber-50/40 dark:bg-amber-950/20",
                };
            case "ERROR":
            case "ERR":
                return {
                    text: "text-red-600 dark:text-red-400",
                    border: "border-red-500/60 dark:border-red-400/60",
                    bg: "bg-red-50/40 dark:bg-red-950/20",
                };
            default:
                return { text: "text-foreground", border: "border-transparent", bg: "" };
        }
    }

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-5xl">
                <DialogHeader>
                    <DialogTitle>Логи аккаунта</DialogTitle>
                    <DialogDescription>
                        {username ? `@${username} · ` : ""}Account ID: {accountId ?? "—"}
                    </DialogDescription>
                </DialogHeader>

                {loading && <div className="text-sm text-muted-foreground">Загрузка…</div>}
                {error && <div className="text-sm text-destructive">Ошибка: {error}</div>}

                {!loading && !error && (
                    <ScrollArea className="h-[50vh] w-full rounded-md border">
                        <ul className="p-3 space-y-2 font-mono text-xs">
                            {logs.length === 0 && <li className="text-muted-foreground">Пусто</li>}

                            {logs.map((l) => {
                                const cls = levelClasses(l.level as string);
                                return (
                                    <li
                                        key={l.id}
                                        // всегда переносим + сохраняем \n; длинные токены тоже ломаем
                                        className={`whitespace-pre-wrap break-all rounded-sm px-2 py-1 border-l-2 ${cls.text} ${cls.border} ${cls.bg}`}
                                    >
            <span className="mr-2 opacity-60 whitespace-nowrap">
              [{new Date(l.created_at).toLocaleString()}]
            </span>
                                        <span className="mr-2 uppercase whitespace-nowrap">
              {String(l.level)}
            </span>
                                        <span className="align-top">
              {l.message}
            </span>
                                    </li>
                                );
                            })}
                        </ul>
                    </ScrollArea>
                )}

                <div className="flex justify-end gap-2">
                    <Button variant="secondary" onClick={() => onOpenChange(false)}>Закрыть</Button>
                </div>
            </DialogContent>
        </Dialog>
    );
}
