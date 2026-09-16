import { useEffect, useState, type FormEvent } from 'react'
import { Globe2, RadioTower } from 'lucide-react'
import type { Monitor, MonitorDraft, MonitorType } from '../lib/types'
import { Button } from './ui/button'
import { Dialog, DialogContent, DialogDescription, DialogTitle } from './ui/dialog'
import { Input } from './ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'

interface MonitorDialogProps {
  open: boolean
  monitor?: Monitor | null
  busy?: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (draft: MonitorDraft) => Promise<void>
}

const initialDraft: MonitorDraft = { name: '', url: '', type_of_request: 'https', interval_minutes: 5 }

export function MonitorDialog({ open, monitor, busy, onOpenChange, onSubmit }: MonitorDialogProps) {
  const [draft, setDraft] = useState(initialDraft)

  useEffect(() => {
    setDraft(monitor ? { name: monitor.name, url: monitor.url, type_of_request: monitor.type_of_request, interval_minutes: monitor.interval } : initialDraft)
  }, [monitor, open])

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    await onSubmit(draft)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogTitle>{monitor ? 'Настроить монитор' : 'Новый монитор'}</DialogTitle>
        <DialogDescription>{monitor ? 'Изменения применятся к следующим проверкам.' : 'Добавьте HTTP-сервис или DNS over HTTPS сервер.'}</DialogDescription>
        <form onSubmit={handleSubmit} className="form-stack">
          <label className="field-label">Название<Input autoFocus required maxLength={50} value={draft.name} placeholder="Например, Основной сайт" onChange={(event) => setDraft({ ...draft, name: event.target.value })} /></label>
          {!monitor && <label className="field-label">Тип проверки<Select value={draft.type_of_request} onValueChange={(value) => setDraft({ ...draft, type_of_request: value as MonitorType })}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="https"><span className="select-label"><Globe2 size={15} /> HTTPS</span></SelectItem><SelectItem value="dns"><span className="select-label"><RadioTower size={15} /> DNS over HTTPS</span></SelectItem></SelectContent></Select></label>}
          <label className="field-label">URL<Input required type="url" value={draft.url} placeholder={draft.type_of_request === 'https' ? 'https://example.com' : 'https://dns.google/resolve'} onChange={(event) => setDraft({ ...draft, url: event.target.value })} /></label>
          <label className="field-label">Интервал проверки, минут<Input required type="number" min={3} value={draft.interval_minutes} onChange={(event) => setDraft({ ...draft, interval_minutes: Number(event.target.value) })} /></label>
          <div className="dialog-actions"><Button type="button" variant="outline" onClick={() => onOpenChange(false)}>Отмена</Button><Button disabled={busy}>{busy ? 'Сохраняем…' : monitor ? 'Сохранить' : 'Создать монитор'}</Button></div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
