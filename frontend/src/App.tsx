import { useEffect, useMemo, useRef, useState, type FormEvent } from 'react'
import {
  Activity, ArrowLeft, ArrowRight, Check as CheckIcon, CheckCircle2, Clock3, CloudCog, Globe2, LayoutDashboard,
  LoaderCircle, LogOut, Menu, Moon, MoreHorizontal, Pencil, Play, Plus, RadioTower,
  RefreshCw, Search, Server, Settings, Settings2, ShieldCheck, Sun, Trash2, TriangleAlert, XCircle,
} from 'lucide-react'
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { toast } from 'sonner'
import { api, ApiError } from './lib/api'
import { demoChecks, demoMonitors } from './lib/demo'
import type { Check, Monitor, MonitorDraft } from './lib/types'
import { Badge } from './components/ui/badge'
import { Button } from './components/ui/button'
import { Card, CardContent, CardHeader } from './components/ui/card'
import { Dialog, DialogContent, DialogDescription, DialogTitle } from './components/ui/dialog'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from './components/ui/dropdown-menu'
import { Input } from './components/ui/input'
import { MonitorDialog } from './components/monitor-dialog'
import { Toaster } from './components/ui/sonner'

type Session = 'loading' | 'guest' | 'authenticated' | 'demo'
type AuthMode = 'login' | 'register'
type NavSection = 'overview' | 'monitors'
type ThemeMode = 'light' | 'dark' | 'system'

function formatTime(date: string) {
  return new Intl.DateTimeFormat('ru', { hour: '2-digit', minute: '2-digit' }).format(new Date(date))
}

function relativeTime(date: string) {
  const minutes = Math.max(1, Math.round((new Date(date).getTime() - Date.now()) / 60000))
  return minutes <= 1 ? 'меньше чем через минуту' : `через ${minutes} мин.`
}

function responseNumber(value: string | null) {
  if (!value) return null
  const match = value.match(/[\d.]+/)
  return match ? Number(match[0]) : null
}

function Logo() {
  return <div className="brand"><span className="brand-mark"><Activity size={18} strokeWidth={2.5} /></span><span>Pulse</span></div>
}

function AuthScreen({ onAuthenticated, onDemo }: { onAuthenticated: (username: string) => void; onDemo: () => void }) {
  const [mode, setMode] = useState<AuthMode>('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function submit(event: FormEvent) {
    event.preventDefault()
    setBusy(true)
    setError('')
    try {
      if (mode === 'login') await api.login(username, password)
      else await api.register(username, password)
      onAuthenticated(username)
    } catch (cause) {
      setError(cause instanceof ApiError ? cause.message : 'API недоступен. Можно открыть демо-режим.')
    } finally { setBusy(false) }
  }

  return <main className="auth-layout">
    <section className="auth-story">
      <Logo />
      <div className="auth-copy"><Badge>Мониторинг без шума</Badge><h1>Ваши сервисы<br />всегда на виду.</h1><p>Проверяйте сайты и DNS, замечайте сбои раньше пользователей и храните всю историю в одном месте.</p></div>
      <div className="signal-card"><div className="signal-head"><span><span className="status-dot" />Все системы работают</span><span>99,98%</span></div><div className="signal-bars">{Array.from({ length: 28 }, (_, index) => <i key={index} className={index === 21 ? 'warn' : ''} style={{ height: 14 + ((index * 13) % 26) }} />)}</div><div className="signal-foot"><span>Последние 24 часа</span><span>Обновлено сейчас</span></div></div>
      <p className="auth-foot">HTTPS & DNS over HTTPS · история проверок · быстрые уведомления</p>
    </section>
    <section className="auth-panel"><div className="auth-form-wrap"><div className="mobile-logo"><Logo /></div><span className="eyebrow">{mode === 'login' ? 'С возвращением' : 'Начнём'}</span><h2>{mode === 'login' ? 'Войдите в аккаунт' : 'Создайте аккаунт'}</h2><p className="muted">{mode === 'login' ? 'Продолжите следить за своими сервисами.' : 'Настройте первый монитор за пару минут.'}</p>
      <form className="form-stack auth-form" onSubmit={submit}><label className="field-label">Имя пользователя<Input required maxLength={50} autoComplete="username" placeholder="yourname" value={username} onChange={(event) => setUsername(event.target.value)} /></label><label className="field-label">Пароль<Input required type="password" autoComplete={mode === 'login' ? 'current-password' : 'new-password'} placeholder="Не менее 8 символов" value={password} onChange={(event) => setPassword(event.target.value)} /></label>{error && <div className="form-error"><TriangleAlert size={16} />{error}</div>}<Button className="auth-submit" disabled={busy}>{busy && <LoaderCircle className="spin" size={16} />}{mode === 'login' ? 'Войти' : 'Создать аккаунт'}<ArrowRight size={16} /></Button></form>
      <div className="auth-switch">{mode === 'login' ? 'Нет аккаунта?' : 'Уже есть аккаунт?'} <button onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError('') }}>{mode === 'login' ? 'Зарегистрироваться' : 'Войти'}</button></div>
      <div className="or"><span>или</span></div><Button variant="outline" className="demo-button" onClick={onDemo}><Play size={15} />Открыть демо</Button>
    </div></section>
  </main>
}

function Sidebar({ demo, accountName, active, theme, onThemeChange, onNavigate, onLogout }: { demo: boolean; accountName?: string; active: NavSection; theme: ThemeMode; onThemeChange: (theme: ThemeMode) => void; onNavigate: (section: NavSection) => void; onLogout: () => void }) {
  const [settingsOpen, setSettingsOpen] = useState(false)
  return <aside className="sidebar"><div><Logo /><nav><button className={active === 'overview' ? 'active' : ''} onClick={() => onNavigate('overview')}><LayoutDashboard size={17} />Обзор</button><button className={active === 'monitors' ? 'active' : ''} onClick={() => onNavigate('monitors')}><Activity size={17} />Мониторы</button></nav></div><div className="sidebar-bottom">{demo && <div className="demo-note"><Play size={15} /><div><strong>Демо-режим</strong><span>Данные хранятся локально</span></div></div>}{accountName && <div className="account-name"><span>{demo ? 'Демо-аккаунт' : 'Аккаунт'}</span><strong>{accountName}</strong></div>}<div className="sidebar-settings">{settingsOpen && <SettingsMenu accountName={accountName} theme={theme} onThemeChange={(value) => { onThemeChange(value); setSettingsOpen(false) }} onLogout={onLogout} />}<button className={settingsOpen ? 'settings-trigger active' : 'settings-trigger'} onClick={() => setSettingsOpen((value) => !value)} aria-expanded={settingsOpen}><Settings size={17} />Настройки</button></div></div></aside>
}

function SettingsMenu({ accountName, theme, onThemeChange, onLogout }: { accountName?: string; theme: ThemeMode; onThemeChange: (theme: ThemeMode) => void; onLogout: () => void }) {
  const options = [{ value: 'light' as const, label: 'Светлая', icon: Sun }, { value: 'dark' as const, label: 'Тёмная', icon: Moon }, { value: 'system' as const, label: 'Как в системе', icon: Settings2 }]
  return <div className="settings-menu">{accountName && <div className="menu-account"><span>Аккаунт</span><strong>{accountName}</strong></div>}<p>Оформление</p>{options.map((option) => <button key={option.value} onClick={() => onThemeChange(option.value)}><option.icon size={16} /><span>{option.label}</span>{theme === option.value && <CheckIcon className="menu-check" size={16} />}</button>)}<div className="settings-separator" /><button className="settings-logout" onClick={onLogout}><LogOut size={16} /><span>Выйти из аккаунта</span></button></div>
}

function MetricCard({ label, value, hint, icon, status }: { label: string; value: string; hint: string; icon: React.ReactNode; status?: 'good' | 'bad' }) {
  return <Card className="metric"><CardHeader><span>{label}</span><span className="metric-icon">{icon}</span></CardHeader><CardContent><strong className={status === 'bad' ? 'text-danger' : ''}>{value}</strong><small className={status === 'good' ? 'text-success' : ''}>{hint}</small></CardContent></Card>
}

function StatusBadge({ success }: { success: boolean }) {
  return <Badge className={success ? 'badge-success' : 'badge-danger'}><span />{success ? 'Работает' : 'Сбой'}</Badge>
}

interface DashboardProps { demo: boolean; accountName?: string; initialMonitors: Monitor[]; onLogout: () => void }

function Dashboard({ demo, accountName, initialMonitors, onLogout }: DashboardProps) {
  const [monitors, setMonitors] = useState(initialMonitors)
  const [checks, setChecks] = useState<Check[]>(demo ? demoChecks : [])
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState<Monitor | null>(null)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editing, setEditing] = useState<Monitor | null>(null)
  const [deleteTarget, setDeleteTarget] = useState<Monitor | null>(null)
  const [busy, setBusy] = useState(false)
  const [mobileNav, setMobileNav] = useState(false)
  const [activeSection, setActiveSection] = useState<NavSection>('overview')
  const [highlightedSection, setHighlightedSection] = useState<NavSection | null>(null)
  const highlightTimer = useRef<number | null>(null)
  const [theme, setTheme] = useState<ThemeMode>(() => (localStorage.getItem('pulse-theme') as ThemeMode | null) || 'system')
  const [resolvedDark, setResolvedDark] = useState(false)

  useEffect(() => {
    const media = window.matchMedia('(prefers-color-scheme: dark)')
    const apply = () => { const dark = theme === 'dark' || (theme === 'system' && media.matches); setResolvedDark(dark); document.documentElement.classList.toggle('dark', dark) }
    apply(); localStorage.setItem('pulse-theme', theme); media.addEventListener('change', apply)
    return () => media.removeEventListener('change', apply)
  }, [theme])
  useEffect(() => {
    if (!demo && monitors.length) Promise.all(monitors.map((monitor) => api.checks(monitor.id).catch(() => []))).then((groups) => setChecks(groups.flat()))
  }, [demo, monitors.length])
  useEffect(() => () => {
    if (highlightTimer.current !== null) window.clearTimeout(highlightTimer.current)
  }, [])

  const monitorState = (id: number) => checks.filter((check) => check.monitor_id === id).sort((a, b) => +new Date(b.created_at) - +new Date(a.created_at))[0]
  const healthy = monitors.filter((monitor) => monitorState(monitor.id)?.success !== false).length
  const responseValues = checks.filter((check) => check.success).map((check) => responseNumber(check.response_time_ms)).filter((value): value is number => value !== null)
  const average = responseValues.length ? Math.round(responseValues.reduce((a, b) => a + b, 0) / responseValues.length) : 0
  const filtered = monitors.filter((monitor) => `${monitor.name} ${monitor.url}`.toLowerCase().includes(query.toLowerCase()))

  async function saveMonitor(draft: MonitorDraft) {
    setBusy(true)
    try {
      if (editing) {
        if (!demo) await api.updateMonitor(editing.id, { name: draft.name, url: draft.url, interval_minutes: draft.interval_minutes })
        setMonitors((items) => items.map((item) => item.id === editing.id ? { ...item, name: draft.name, url: draft.url, interval: draft.interval_minutes } : item))
        toast.success('Настройки монитора сохранены')
      } else {
        if (!demo) await api.createMonitor(draft)
        const created: Monitor = { id: Date.now(), user_id: 1, next_check_at: new Date(Date.now() + draft.interval_minutes * 60000).toISOString(), interval: draft.interval_minutes, name: draft.name, url: draft.url, type_of_request: draft.type_of_request }
        if (demo) setMonitors((items) => [created, ...items]); else setMonitors(await api.monitors())
        toast.success('Монитор добавлен')
      }
      setDialogOpen(false); setEditing(null)
    } catch (cause) { toast.error(cause instanceof Error ? cause.message : 'Не удалось сохранить монитор') }
    finally { setBusy(false) }
  }

  async function removeMonitor() {
    if (!deleteTarget) return
    setBusy(true)
    try { if (!demo) await api.deleteMonitor(deleteTarget.id); setMonitors((items) => items.filter((item) => item.id !== deleteTarget.id)); setChecks((items) => items.filter((item) => item.monitor_id !== deleteTarget.id)); if (selected?.id === deleteTarget.id) setSelected(null); toast.success('Монитор удалён'); setDeleteTarget(null) }
    catch (cause) { toast.error(cause instanceof Error ? cause.message : 'Не удалось удалить монитор') }
    finally { setBusy(false) }
  }

  async function runCheck(monitor: Monitor) {
    const toastId = toast.loading('Запускаем проверку…')
    try {
      if (!demo) { await api.runCheck(monitor.id); const fresh = await api.checks(monitor.id); setChecks((items) => [...items.filter((item) => item.monitor_id !== monitor.id), ...fresh]) }
      else { const fresh: Check = { id: Date.now(), monitor_id: monitor.id, status_code: 200, response_time_ms: String(90 + Math.round(Math.random() * 80)), success: true, reason: 'OK', created_at: new Date().toISOString() }; setChecks((items) => [fresh, ...items]) }
      toast.success('Проверка завершена', { id: toastId })
    } catch (cause) { toast.error(cause instanceof Error ? cause.message : 'Проверка не выполнена', { id: toastId }) }
  }

  function navigate(section: NavSection) {
    setActiveSection(section)
    setMobileNav(false)
    setHighlightedSection(null)
    window.requestAnimationFrame(() => {
      window.requestAnimationFrame(() => setHighlightedSection(section))
    })
    if (highlightTimer.current !== null) window.clearTimeout(highlightTimer.current)
    highlightTimer.current = window.setTimeout(() => setHighlightedSection(null), 1100)
    if (window.matchMedia('(max-width: 760px)').matches) {
      document.getElementById(section)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  return <div className="app-shell">
    <Sidebar demo={demo} accountName={accountName} active={activeSection} theme={theme} onThemeChange={setTheme} onNavigate={navigate} onLogout={onLogout} />
    {mobileNav && <><button className="mobile-nav-overlay" aria-label="Закрыть меню" onClick={() => setMobileNav(false)} /><div className="mobile-nav"><div className="mobile-nav-head"><Logo /><Button size="icon" variant="ghost" onClick={() => setMobileNav(false)}><XCircle size={20} /></Button></div><button className={activeSection === 'overview' ? 'active' : ''} onClick={() => navigate('overview')}><LayoutDashboard size={17} />Обзор</button><button className={activeSection === 'monitors' ? 'active' : ''} onClick={() => navigate('monitors')}><Activity size={17} />Мониторы</button><div className="mobile-settings">{accountName && <div className="menu-account"><span>Аккаунт</span><strong>{accountName}</strong></div>}<p>Оформление</p>{[{ value: 'light' as const, label: 'Светлая', icon: Sun }, { value: 'dark' as const, label: 'Тёмная', icon: Moon }, { value: 'system' as const, label: 'Как в системе', icon: Settings2 }].map((option) => <button key={option.value} onClick={() => setTheme(option.value)}><option.icon size={16} />{option.label}{theme === option.value && <CheckIcon className="menu-check" size={16} />}</button>)}<button className="settings-logout" onClick={onLogout}><LogOut size={16} />Выйти из аккаунта</button></div></div></>}
    <main className="main"><header className="topbar"><Button className="menu-button" size="icon" variant="ghost" onClick={() => setMobileNav(true)}><Menu size={19} /></Button><div className="top-status"><span className="status-dot" />Система мониторинга работает</div><div className="top-actions"><button className="icon-plain" aria-label="Сменить тему" onClick={() => setTheme(resolvedDark ? 'light' : 'dark')}>{resolvedDark ? <Sun size={18} /> : <Moon size={18} />}</button><Button onClick={() => { setEditing(null); setDialogOpen(true) }}><Plus size={16} />Добавить монитор</Button></div></header>
      <div className="content"><div className="page-heading scroll-section" id="overview"><div><span className="eyebrow">Рабочее пространство</span><h1>Обзор сервисов</h1><p>Состояние и производительность ваших систем в реальном времени.</p></div><div className="last-updated"><RefreshCw size={14} />Обновлено только что</div></div>
        <section className={`metrics-grid${highlightedSection === 'overview' ? ' nav-highlight' : ''}`}><MetricCard label="Всего мониторов" value={String(monitors.length)} hint="активные проверки" icon={<Server size={18} />} /><MetricCard label="Работают" value={String(healthy)} hint={healthy === monitors.length ? 'Все системы в норме' : 'Требуется внимание'} status={healthy === monitors.length ? 'good' : 'bad'} icon={<CheckCircle2 size={18} />} /><MetricCard label="Средний ответ" value={average ? `${average} мс` : '—'} hint="за последние 24 часа" icon={<Clock3 size={18} />} /><MetricCard label="Аптайм" value={checks.length ? `${((checks.filter((c) => c.success).length / checks.length) * 100).toFixed(2)}%` : '—'} hint="за последние 24 часа" status="good" icon={<ShieldCheck size={18} />} /></section>
        <Card className={`monitor-card scroll-section${highlightedSection === 'monitors' ? ' nav-highlight' : ''}`} id="monitors"><div className="monitor-toolbar"><div><h2>Мониторы</h2><p>{monitors.length} сервисов под наблюдением</p></div><div className="search"><Search size={16} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Поиск сервиса…" /></div></div>
          <div className="monitor-list"><div className="monitor-row monitor-labels"><span>Сервис</span><span>Статус</span><span>Ответ</span><span>Следующая проверка</span><span /></div>{filtered.length ? filtered.map((monitor) => { const state = monitorState(monitor.id); return <button className="monitor-row" key={monitor.id} onClick={() => setSelected(monitor)}><span className="service-cell"><span className="service-icon">{monitor.type_of_request === 'https' ? <Globe2 size={19} /> : <RadioTower size={19} />}</span><span><strong>{monitor.name}</strong><small>{monitor.url.replace(/^https?:\/\//, '')}</small></span></span><span><StatusBadge success={state?.success !== false} /></span><span className="response-cell">{responseNumber(state?.response_time_ms ?? null) ? `${responseNumber(state?.response_time_ms ?? null)} мс` : '—'}</span><span className="next-cell">{relativeTime(monitor.next_check_at)}<small>каждые {monitor.interval} мин.</small></span><span onClick={(event) => event.stopPropagation()}><DropdownMenu><DropdownMenuTrigger asChild><Button size="icon" variant="ghost"><MoreHorizontal size={18} /></Button></DropdownMenuTrigger><DropdownMenuContent><DropdownMenuItem onSelect={() => runCheck(monitor)}><Play size={15} />Проверить сейчас</DropdownMenuItem><DropdownMenuItem onSelect={() => { setEditing(monitor); setDialogOpen(true) }}><Pencil size={15} />Изменить</DropdownMenuItem><DropdownMenuItem className="danger-item" onSelect={() => setDeleteTarget(monitor)}><Trash2 size={15} />Удалить</DropdownMenuItem></DropdownMenuContent></DropdownMenu></span></button> }) : <div className="empty"><CloudCog size={28} /><h3>Ничего не найдено</h3><p>Попробуйте изменить запрос или добавьте новый монитор.</p></div>}</div>
        </Card>
      </div>
    </main>
    {selected && <MonitorDetails monitor={selected} checks={checks.filter((item) => item.monitor_id === selected.id)} onClose={() => setSelected(null)} onRun={() => runCheck(selected)} onEdit={() => { setEditing(selected); setDialogOpen(true) }} />}
    <MonitorDialog open={dialogOpen} monitor={editing} busy={busy} onOpenChange={(open) => { setDialogOpen(open); if (!open) setEditing(null) }} onSubmit={saveMonitor} />
    <Dialog open={Boolean(deleteTarget)} onOpenChange={(open) => !open && setDeleteTarget(null)}><DialogContent className="confirm-dialog"><span className="danger-icon"><Trash2 size={20} /></span><DialogTitle>Удалить «{deleteTarget?.name}»?</DialogTitle><DialogDescription>Монитор и вся история его проверок будут удалены без возможности восстановления.</DialogDescription><div className="dialog-actions"><Button variant="outline" onClick={() => setDeleteTarget(null)}>Отмена</Button><Button variant="destructive" disabled={busy} onClick={removeMonitor}>{busy ? 'Удаляем…' : 'Удалить'}</Button></div></DialogContent></Dialog>
  </div>
}

function MonitorDetails({ monitor, checks, onClose, onRun, onEdit }: { monitor: Monitor; checks: Check[]; onClose: () => void; onRun: () => void; onEdit: () => void }) {
  const sorted = [...checks].sort((a, b) => +new Date(b.created_at) - +new Date(a.created_at))
  const latest = sorted[0]
  const chart = [...sorted].reverse().slice(-12).map((check) => ({ time: formatTime(check.created_at), value: responseNumber(check.response_time_ms), success: check.success }))
  return <div className="details-backdrop" onMouseDown={(event) => event.target === event.currentTarget && onClose()}><aside className="details-panel"><header><Button size="icon" variant="ghost" onClick={onClose}><ArrowLeft size={19} /></Button><div><span className="eyebrow">Детали монитора</span><h2>{monitor.name}</h2></div><Button size="icon" variant="ghost" onClick={onEdit}><Pencil size={17} /></Button></header><div className="details-body"><div className="details-status"><div><StatusBadge success={latest?.success !== false} /><h3>{latest?.success === false ? 'Сервис недоступен' : 'Сервис работает стабильно'}</h3><p>{monitor.url}</p></div><Button onClick={onRun}><Play size={15} />Проверить</Button></div><div className="details-stats"><div><span>Последний ответ</span><strong>{responseNumber(latest?.response_time_ms ?? null) ? `${responseNumber(latest?.response_time_ms ?? null)} мс` : '—'}</strong></div><div><span>Код ответа</span><strong>{latest?.status_code ?? '—'}</strong></div><div><span>Интервал</span><strong>{monitor.interval} мин.</strong></div></div><div className="chart-block"><div className="section-title"><div><h3>Время ответа</h3><p>Последние 12 проверок</p></div><Activity size={17} /></div>{chart.length ? <ResponsiveContainer width="100%" height={190}><AreaChart data={chart} margin={{ top: 10, right: 5, bottom: 0, left: -24 }}><defs><linearGradient id="responseGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="currentColor" stopOpacity={0.22} /><stop offset="95%" stopColor="currentColor" stopOpacity={0} /></linearGradient></defs><XAxis dataKey="time" tickLine={false} axisLine={false} tick={{ fontSize: 11 }} /><YAxis tickLine={false} axisLine={false} tick={{ fontSize: 11 }} /><Tooltip contentStyle={{ borderRadius: 10, border: '1px solid var(--border)', background: 'var(--popover)', fontSize: 12 }} formatter={(value) => [`${value} мс`, 'Ответ']} /><Area type="monotone" dataKey="value" stroke="currentColor" strokeWidth={2} fill="url(#responseGradient)" /></AreaChart></ResponsiveContainer> : <div className="chart-empty">Пока нет данных для графика</div>}</div><div className="history"><div className="section-title"><div><h3>История проверок</h3><p>Последние события</p></div></div>{sorted.slice(0, 6).map((check) => <div className="history-row" key={check.id}>{check.success ? <CheckCircle2 className="check-good" size={17} /> : <XCircle className="check-bad" size={17} />}<span><strong>{check.success ? 'Проверка успешна' : check.reason}</strong><small>{new Date(check.created_at).toLocaleString('ru')}</small></span><span><strong>{check.status_code ?? '—'}</strong><small>{responseNumber(check.response_time_ms) ? `${responseNumber(check.response_time_ms)} мс` : 'нет ответа'}</small></span></div>)}</div></div></aside></div>
}

export function App() {
  const [session, setSession] = useState<Session>('loading')
  const [monitors, setMonitors] = useState<Monitor[]>([])
  const [accountName, setAccountName] = useState(() => localStorage.getItem('pulse-account-name') || '')

  useEffect(() => { api.monitors().then((items) => { setMonitors(items); setSession('authenticated') }).catch(() => setSession('guest')) }, [])
  const screen = useMemo(() => {
    if (session === 'loading') return <div className="app-loading"><span className="brand-mark"><Activity size={20} /></span><LoaderCircle className="spin" size={20} /></div>
    if (session === 'guest') return <AuthScreen onAuthenticated={(username) => { localStorage.setItem('pulse-account-name', username); setAccountName(username); api.monitors().then((items) => { setMonitors(items); setSession('authenticated') }) }} onDemo={() => { setAccountName('Гость'); setMonitors(demoMonitors); setSession('demo') }} />
    return <Dashboard demo={session === 'demo'} accountName={accountName} initialMonitors={monitors} onLogout={() => { localStorage.removeItem('pulse-account-name'); setAccountName(''); setSession('guest'); setMonitors([]) }} />
  }, [session, monitors, accountName])
  return <>{screen}<Toaster /></>
}
