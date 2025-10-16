export type Proxy = {
  id: string;
  protocol: string; // <- опционально
  host: string;
  port: number;         // было `integer` — в TS это number
  username: string | null;
  password: string | null;

  // опционально, если есть на бэке
  created_at?: string | null;
};