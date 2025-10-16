import { API_URL } from "@/shared/config/api";


export async function setAccountsComments(accountIds: string[], comment: string) {

  const res = await fetch(`${API_URL}/accounts/comment`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ account_ids: accountIds, comment: comment }),
  });

  if (!res.ok) throw new Error('Не удалось установить комментарий аккаунтам')
  return res.json()
}
