import { forwardRef, type InputHTMLAttributes } from 'react'
import { cn } from '../../lib/utils'

export const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(({ className, ...props }, ref) => (
  <input ref={ref} className={cn('input', className)} {...props} />
))
Input.displayName = 'Input'
