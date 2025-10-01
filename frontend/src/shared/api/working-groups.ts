import type { Worker, WorkersResponse } from "@/shared/types/working-groups"
import { API_URL } from "@/shared/config/api";



export async function fetchWorkingGroups() {
  const res = await fetch(`${API_URL}/working_groups/`)
  if (!res.ok) throw new Error('Не удалось загрузить рабочие группы')
  return res.json()
}

export async function fetchWorkingGroup(id: string) {
  const res = await fetch(`${API_URL}/working_groups/${id}/`) // поставь слеш по необходимости
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`fetchWorkingGroup(${id}): ${res.status} ${text}`)
  }
  return res.json()
}


export async function createWorkingGroup({ name }: { name: string }) {
  const res = await fetch(`${API_URL}/working_groups/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name }), // <-- передаем имя группы
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error('Не удалось создать рабочую группу: ' + text)
  }

  return res.json()
}


export async function deleteWorkingGroup(id: string) {
  const res = await fetch(`${API_URL}/working_groups/${id}`, {
    method: 'DELETE',
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error('Не удалось удалить рабочую группу: ' + text);
  }

  return true;
}

export async function fetchWorkingGroupWorkers(args: {
  groupId: string
  pageIndex: number
  pageSize: number
}): Promise<{ rows: Worker[]; pageCount: number; total: number }> {
  const { groupId, pageIndex, pageSize } = args
  const params = new URLSearchParams({
    page: String(pageIndex + 1),
    page_size: String(pageSize),
  })

  const res = await fetch(
    `${API_URL}/working_groups/${groupId}/workers/?${params.toString()}`,
    { cache: "no-store" }
  )
  if (!res.ok) throw new Error(await res.text())

  const json = (await res.json()) as WorkersResponse
  const rows = json.result.workers
  const { total_pages, total_count } = json.result.pagination

  return { rows, pageCount: Math.max(1, total_pages), total: total_count }
}


export async function createWorkingGroupWorkers(
  groupId: string,
  worker_strings: string[],
): Promise<void> {
  const res = await fetch(`${API_URL}/working_groups/${groupId}/workers/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ worker_strings, format: "IAM_MOB" }),
  });

  const text = await res.text();
  let data: any = null;
  try { data = text ? JSON.parse(text) : null; } catch {}

  if (!res.ok) {
    const err = data?.error ?? data?.message ?? text ?? `${res.status} ${res.statusText}`;
    throw new Error(typeof err === "string" ? err : JSON.stringify(err));
  }
}

export async function deleteWorkingGroupWorkers(
  wgId: string,
  workerIds?: string[] | null,   // ← необязательный параметр
): Promise<void> {
  const body =
    workerIds && workerIds.length > 0
      ? JSON.stringify({ worker_ids: workerIds })
      : null

  const res = await fetch(`${API_URL}/working_groups/${wgId}/workers/`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body, // ← если null, body не уйдёт
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Ошибка при удалении воркеров: ${text}`)
  }
}


export async function startWorkingGroupWorkers(
  wgId: string,
  workerIds?: string[],
): Promise<void> {
  const body = JSON.stringify({ worker_ids: workerIds });

  const res = await fetch(`${API_URL}/working_groups/${wgId}/start_workers/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Ошибка при запуске аккаунтов: ${text}`)
  }
}



export type AccountWorkerLogType = "info" | "warning" | "error" | string;

export async function fetchWorkingGroupWorkerLogs(opts: {
    accountIds?: string[];              // -> account_ids=...&account_ids=...
    types?: AccountWorkerLogType[];     // -> types=...&types=...
}) {
    const qs = new URLSearchParams();
    opts.accountIds?.forEach((id) => qs.append("account_ids", id));
    opts.types?.forEach((t) => qs.append("types", t));

    const res = await fetch(`${API_URL}/logs/?${qs.toString()}`, {
        method: "GET",
    });

    if (!res.ok) {
        const txt = await res.text().catch(() => "");
        throw new Error(`Не удалось загрузить логи: ${res.status} ${txt}`);
    }
    return res.json(); // ApiResponse<GetLogsQueryResult> или {logs:[]} — компонент обрабатывает оба варианта
}

