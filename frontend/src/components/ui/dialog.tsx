import * as DialogPrimitive from '@radix-ui/react-dialog'
import { X } from 'lucide-react'
import type { ComponentProps } from 'react'
import { cn } from '../../lib/utils'

export const Dialog = DialogPrimitive.Root
export const DialogTrigger = DialogPrimitive.Trigger
export const DialogClose = DialogPrimitive.Close
export function DialogContent({ className, children, ...props }: ComponentProps<typeof DialogPrimitive.Content>) {
  return <DialogPrimitive.Portal><DialogPrimitive.Overlay className="dialog-overlay" /><DialogPrimitive.Content className={cn('dialog-content', className)} {...props}>{children}<DialogPrimitive.Close className="dialog-x" aria-label="Закрыть"><X size={18} /></DialogPrimitive.Close></DialogPrimitive.Content></DialogPrimitive.Portal>
}
export const DialogTitle = ({ className, ...props }: ComponentProps<typeof DialogPrimitive.Title>) => <DialogPrimitive.Title className={cn('dialog-title', className)} {...props} />
export const DialogDescription = ({ className, ...props }: ComponentProps<typeof DialogPrimitive.Description>) => <DialogPrimitive.Description className={cn('dialog-description', className)} {...props} />
