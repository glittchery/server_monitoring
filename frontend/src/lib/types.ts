export type MonitorType = 'https' | 'dns'

export interface Monitor {
  id: number
  type_of_request: MonitorType
  name: string
  url: string
  interval: number
  next_check_at: string
  user_id: number
}

export interface Check {
  id: number
  monitor_id: number
  status_code: number | null
  response_time_ms: string | null
  success: boolean
  reason: string
  created_at: string
}

export interface MonitorDraft {
  name: string
  url: string
  type_of_request: MonitorType
  interval_minutes: number
}
