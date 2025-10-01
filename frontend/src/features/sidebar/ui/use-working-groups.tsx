import * as React from "react";
import {
  fetchWorkingGroups as apiFetchWorkingGroups,
  createWorkingGroup as apiCreateWorkingGroup,
  deleteWorkingGroup as apiDeleteWorkingGroup,
} from "@/shared/api/working-groups";
import type { WorkingGroupItem } from "./types";

function mapResponse(json: any): WorkingGroupItem[] {
  const raw = (json?.result?.working_groups ?? json?.working_groups ?? json ?? []) as any[];
  return raw.map((it: any, i: number) => ({
    id: String(it.id ?? it.uuid ?? it.wg_id ?? i),
    name: String(it.name ?? it.title ?? `Группа ${i + 1}`),
    status: it.status ?? null,
  }));
}

export function useWorkingGroups() {
  const [groups, setGroups] = React.useState<WorkingGroupItem[] | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [creating, setCreating] = React.useState(false);
  const [deletingId, setDeletingId] = React.useState<string | null>(null);

  const load = React.useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const json = await apiFetchWorkingGroups();
      setGroups(mapResponse(json));
    } catch (e: any) {
      setGroups([]);
      setError(e?.message ?? "Не удалось загрузить рабочие группы");
    } finally {
      setLoading(false);
    }
  }, []);

  const create = React.useCallback(async (name: string) => {
    setCreating(true);
    try {
      const json: any = await apiCreateWorkingGroup({ name });
      const gAny = json?.result?.working_group ?? json?.working_group ?? json ?? null;
      const created: WorkingGroupItem | null = gAny ? {
        id: String(gAny.id ?? gAny.uuid ?? gAny.wg_id),
        name: String(gAny.name ?? gAny.title ?? name),
        status: gAny.status ?? null,
      } : null;

      if (created) setGroups((prev) => (prev ? [created, ...prev] : [created]));
      else await load();
    } finally {
      setCreating(false);
    }
  }, [load]);

  const remove = React.useCallback(async (id: string) => {
    setDeletingId(id);
    try {
      await apiDeleteWorkingGroup(id);
      setGroups((prev) => (prev ?? []).filter((g) => g.id !== id));
    } finally {
      setDeletingId(null);
    }
  }, []);

  return { groups, loading, error, load, create, creating, remove, deletingId };
}
