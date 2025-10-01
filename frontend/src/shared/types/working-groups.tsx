// types/working-groups.ts

export type ActionStatistics = {
  follows: number
  follows_blocks: number
  authorizations: number
}

export type Worker = {
  id: string
  account_id: string
  working_group_id: string
  username: string
  password: string | null
  email_username: string | null
  email_password: string | null
  proxy: string | null
  action_statistics: ActionStatistics
  status: string | null
  last_log_message: string | null
  last_action_time: string | null
  password_changed_datetime: string | null
  created_at: string | null
  attached_to_task: string | null
  android_device: string | null
  work_state: string // e.g. "IDLE"
}

export type WorkersResponse = {
  status: "success"
  result: {
    workers: Worker[]
    pagination: {
      page: number
      page_size: number
      count: number
      total_count: number
      total_pages: number
    }
  }
}
