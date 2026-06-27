import React from 'react';
import { clsx } from 'clsx';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'interactive' | 'bordered' | 'glass' | 'elevated';
  padding?: 'none' | 'xs' | 'sm' | 'md' | 'lg' | 'xl';
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  (
    {
      className,
      variant = 'default',
      padding = 'md',
      ...props
    },
    ref
  ) => {
    const variants = {
      default:
        'bg-[#121822] border border-[#1A2230] rounded-xl shadow-sm hover:shadow-md transition-all duration-200',
      interactive:
        'bg-[#121822] border border-[#1A2230] rounded-xl shadow-sm hover:shadow-lg hover:bg-[#1E2230] hover:border-purple-500/30 cursor-pointer transform hover:-translate-y-1 transition-all duration-200',
      bordered: 'bg-[#0B0F14] border-2 border-[#334155] rounded-xl shadow-sm',
      glass:
        'bg-[#1A2230]/80 backdrop-blur-md border border-white/10 rounded-xl shadow-lg',
      elevated: 'bg-[#121822] rounded-xl shadow-xl border border-[#1A2230]/50',
    };

    const paddings = {
      none: '',
      xs: 'p-3',
      sm: 'p-4',
      md: 'p-6',
      lg: 'p-8',
      xl: 'p-10',
    };

    return (
      <div ref={ref} className={clsx(variants[variant], paddings[padding], className)} {...props} />
    );
  }
);

Card.displayName = 'Card';

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardHeader = React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ className, children, ...props }, ref) => (
    <div
      ref={ref}
      className={clsx('pb-4 border-b border-[#1A2230] mb-4', className)}
      {...props}
    >
      {children}
    </div>
  )
);

CardHeader.displayName = 'CardHeader';

export interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardContent = React.forwardRef<HTMLDivElement, CardContentProps>(
  ({ className, children, ...props }, ref) => (
    <div ref={ref} className={clsx('', className)} {...props}>
      {children}
    </div>
  )
);

CardContent.displayName = 'CardContent';

export interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardFooter = React.forwardRef<HTMLDivElement, CardFooterProps>(
  ({ className, children, ...props }, ref) => (
    <div
      ref={ref}
      className={clsx('pt-4 border-t border-[#1A2230] mt-4', className)}
      {...props}
    >
      {children}
    </div>
  )
);

CardFooter.displayName = 'CardFooter';

export interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {}

export const CardTitle = React.forwardRef<HTMLHeadingElement, CardTitleProps>(
  ({ className, children, ...props }, ref) => (
    <h3
      ref={ref}
      className={clsx('text-lg font-semibold leading-none tracking-tight', className)}
      {...props}
    >
      {children}
    </h3>
  )
);

CardTitle.displayName = 'CardTitle';

export interface CardDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {}

export const CardDescription = React.forwardRef<HTMLParagraphElement, CardDescriptionProps>(
  ({ className, children, ...props }, ref) => (
    <p
      ref={ref}
      className={clsx('text-sm text-gray-400', className)}
      {...props}
    >
      {children}
    </p>
  )
);

CardDescription.displayName = 'CardDescription';
