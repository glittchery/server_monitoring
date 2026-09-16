import * as DropdownMenuPrimitive from '@radix-ui/react-dropdown-menu'
import type { ComponentProps } from 'react'
import { cn } from '../../lib/utils'

export const DropdownMenu = DropdownMenuPrimitive.Root
export const DropdownMenuTrigger = DropdownMenuPrimitive.Trigger
export function DropdownMenuContent({ className, ...props }: ComponentProps<typeof DropdownMenuPrimitive.Content>) { return <DropdownMenuPrimitive.Portal><DropdownMenuPrimitive.Content align="end" sideOffset={6} className={cn('dropdown-content', className)} {...props} /></DropdownMenuPrimitive.Portal> }
export function DropdownMenuItem({ className, ...props }: ComponentProps<typeof DropdownMenuPrimitive.Item>) { return <DropdownMenuPrimitive.Item className={cn('dropdown-item', className)} {...props} /> }
