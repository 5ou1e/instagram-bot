import { API_URL } from "@/shared/config/api";
import type { Proxy } from "@/types/proxy";

// актуальная форма ответа бэка
type ProxiesBackendResponse = {
  status: "success" | "error";
  result: {
    proxies: Proxy[];
    pagination: {
      page: number;
      page_size: number;
      count: number;
      total_count: number;
      total_pages: number;
    };
  };
};

// форма, которую ждёт таблица
type ProxiesListResponse = {
  rows: Proxy[];
  pageCount: number;
};

// GET /proxies?page=&page_size=
export async function fetchProxies(params: { pageIndex: number; pageSize: number }) {
  const { pageIndex, pageSize } = params;

  const res = await fetch(
    `${API_URL}/proxies?page=${pageIndex + 1}&page_size=${pageSize}`,
    { method: "GET" }
  );
  if (!res.ok) throw new Error("Не удалось получить список прокси");

  const data = (await res.json()) as ProxiesBackendResponse;

  // маппинг под таблицу
  return {
    rows: data.result.proxies,
    pageCount: data.result.pagination.total_pages ?? 1,
  } satisfies ProxiesListResponse;
}

// DELETE /proxies  body: { ids: string[] | null }
export async function deleteProxies(ids: string[] | null) {
  const res = await fetch(`${API_URL}/proxies`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ids }),
  });
  if (!res.ok) throw new Error("Не удалось удалить прокси");
  return res.json();
}

// POST /proxies  body: list[str]
export async function createProxies(lines: string[]) {
  const res = await fetch(`${API_URL}/proxies`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(lines), // сырой массив строк
  });
  if (!res.ok) throw new Error("Не удалось добавить прокси");
  return res.json();
}
