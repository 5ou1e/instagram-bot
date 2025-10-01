"use client";

import * as React from "react";
import type { Row } from "@tanstack/react-table";
import { toast } from "sonner";
import { ContextMenuItem, ContextMenuSeparator } from "@/shared/ui/context-menu";
import type { Worker } from "@/types/working-groups";
import { startWorkingGroupWorkers, deleteWorkingGroupWorkers } from "@/shared/api/working-groups";

type Props = {
    row: Row<Worker>;
    wgId: string;
    refetch: () => Promise<unknown> | unknown;
    onOpenLogs: (accountId: string, username?: string) => void; // 👈 новый проп
};

export function WorkerRowContextMenu({ row, wgId, refetch, onOpenLogs }: Props) {
    const w = row.original;

    async function handleStart() {
        await startWorkingGroupWorkers(wgId, [w.id]);
        await refetch();
    }

    async function handleDelete() {
        await toast.promise(deleteWorkingGroupWorkers(wgId, [w.id]), {
            loading: "Удаляем…",
            success: "Удалено",
            error: (e) => (e instanceof Error ? e.message : "Ошибка удаления"),
        });
        await refetch();
    }

    const copy = (text: string) => navigator.clipboard.writeText(text);

    return (
        <>
            <ContextMenuItem onSelect={handleStart}>Запустить</ContextMenuItem>
            <ContextMenuItem onSelect={handleDelete}>Удалить</ContextMenuItem>

            <ContextMenuSeparator />

            <ContextMenuItem onSelect={() => copy(w.id)}>Копировать ID</ContextMenuItem>
            <ContextMenuItem onSelect={() => copy(w.username)}>Копировать username</ContextMenuItem>

            <ContextMenuSeparator />

            <ContextMenuItem onSelect={() => onOpenLogs(w.account_id, w.username)}>
                Открыть лог
            </ContextMenuItem>
        </>
    );
}
