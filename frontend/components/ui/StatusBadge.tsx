import React from 'react';
import { cn } from '@/lib/utils';

interface StatusBadgeProps {
  status: 'healthy' | 'degraded' | 'disconnected';
  label: string;
}

export function StatusBadge({ status, label }: StatusBadgeProps) {
  const getColors = () => {
    switch (status) {
      case 'healthy':
        return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'degraded':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'disconnected':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  return (
    <span className={cn('px-2 py-1 rounded-full text-xs font-medium border', getColors())}>
      {label}
    </span>
  );
}
