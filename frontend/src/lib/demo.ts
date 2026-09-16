import type { Check, Monitor } from './types'

const now = Date.now()

export const demoMonitors: Monitor[] = [
  { id: 1, type_of_request: 'https', name: 'Основной сайт', url: 'https://akarmain.ru', interval: 5, next_check_at: new Date(now + 110000).toISOString(), user_id: 1 },
  { id: 2, type_of_request: 'https', name: 'Платёжный API', url: 'https://api.example.com', interval: 3, next_check_at: new Date(now + 45000).toISOString(), user_id: 1 },
  { id: 3, type_of_request: 'dns', name: 'Cloudflare DNS', url: 'https://cloudflare-dns.com/dns-query', interval: 10, next_check_at: new Date(now + 320000).toISOString(), user_id: 1 },
  { id: 4, type_of_request: 'https', name: 'Старый лендинг', url: 'https://legacy.example.com', interval: 15, next_check_at: new Date(now + 520000).toISOString(), user_id: 1 },
]

const responses = [142, 118, 131, 126, 155, 122, 119, 168, 137, 129, 124, 116]
export const demoChecks: Check[] = demoMonitors.flatMap((monitor) =>
  responses.map((time, index) => ({
    id: monitor.id * 100 + index,
    monitor_id: monitor.id,
    status_code: monitor.id === 4 && index < 3 ? 503 : 200,
    response_time_ms: String(time + monitor.id * 9),
    success: !(monitor.id === 4 && index < 3),
    reason: monitor.id === 4 && index < 3 ? 'Service Unavailable' : 'OK',
    created_at: new Date(now - index * 60 * 60 * 1000).toISOString(),
  })),
)
