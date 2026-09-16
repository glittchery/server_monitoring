import * as SelectPrimitive from '@radix-ui/react-select'
import { Check, ChevronDown } from 'lucide-react'
import type { ComponentProps } from 'react'
import { cn } from '../../lib/utils'

export const Select = SelectPrimitive.Root
export function SelectTrigger({ className, children, ...props }: ComponentProps<typeof SelectPrimitive.Trigger>) { return <SelectPrimitive.Trigger className={cn('select-trigger', className)} {...props}>{children}<SelectPrimitive.Icon><ChevronDown size={16} /></SelectPrimitive.Icon></SelectPrimitive.Trigger> }
export const SelectValue = SelectPrimitive.Value
export function SelectContent({ className, ...props }: ComponentProps<typeof SelectPrimitive.Content>) { return <SelectPrimitive.Portal><SelectPrimitive.Content className={cn('select-content', className)} position="popper" sideOffset={5} {...props}><SelectPrimitive.Viewport>{props.children}</SelectPrimitive.Viewport></SelectPrimitive.Content></SelectPrimitive.Portal> }
export function SelectItem({ className, children, ...props }: ComponentProps<typeof SelectPrimitive.Item>) { return <SelectPrimitive.Item className={cn('select-item', className)} {...props}><SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText><SelectPrimitive.ItemIndicator><Check size={14} /></SelectPrimitive.ItemIndicator></SelectPrimitive.Item> }
