import React from 'react';
import { clsx } from 'clsx';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className = '',
      label,
      error,
      helperText,
      leftIcon,
      rightIcon,
      fullWidth = true,
      ...props
    },
    ref
  ) => {
    const widthClass = fullWidth ? 'w-full' : '';
    const hasIcon = leftIcon || rightIcon;

    return (
      <div className={`${widthClass}`}>
        {label && (
          <label className='block text-sm font-medium text-gray-300 mb-2'>{label}</label>
        )}
        <div className='relative'>
          {leftIcon && (
            <div className='absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500'>{leftIcon}</div>
          )}
          <input
            ref={ref}
            className={clsx(
              'w-full px-4 py-3 bg-[#121822] border rounded-lg text-white placeholder-gray-500',
              'focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
              'disabled:opacity-50 disabled:cursor-not-allowed',
              'transition-all duration-200',
              leftIcon ? 'pl-10' : '',
              rightIcon ? 'pr-10' : '',
              error ? 'border-red-500' : 'border-[#1A2230] hover:border-gray-600',
              hasIcon ? '' : '',
              className
            )}
            {...props}
          />
          {rightIcon && (
            <div className='absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500'>{rightIcon}</div>
          )}
        </div>
        {(error || helperText) && (
          <p className={clsx('mt-2 text-sm', error ? 'text-red-400' : 'text-gray-500')}>{error || helperText}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
