import type { Check, Monitor, MonitorDraft } from './types'

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api'

class ApiError extends Error {
  status: number
  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { credentials: 'include', ...init })
  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new ApiError(body?.detail || 'Не удалось выполнить запрос', response.status)
  }
  return response.json()
}

const query = (values: object) => {
  const params = new URLSearchParams()
  Object.entries(values as Record<string, string | number | undefined>).forEach(([key, value]) => value !== undefined && params.set(key, String(value)))
  return params.toString()
}

export const api = {
  login: (username: string, password: string) =>
    request('/auth/login?' + query({ username, password }), { method: 'POST' }),
  register: (username: string, password: string) =>
    request('/auth/register?' + query({ username, password }), { method: 'POST' }),
  monitors: () => request<Monitor[]>('/monitors/user_monitors'),
  createMonitor: (draft: MonitorDraft) =>
    request('/monitors/create_new?' + query(draft), { method: 'POST' }),
  updateMonitor: (id: number, draft: Partial<MonitorDraft>) =>
    request(`/monitors/${id}?` + query({ id, ...draft }), { method: 'PATCH' }),
  deleteMonitor: (id: number) => request(`/monitors/${id}`, { method: 'DELETE' }),
  runCheck: (id: number) => request('/checks?' + query({ monitor_id: id }), { method: 'POST' }),
  checks: (id: number) => request<Check[]>(`/monitors/${id}/checks?` + query({ monitor_id: id })),
}

export { ApiError }
