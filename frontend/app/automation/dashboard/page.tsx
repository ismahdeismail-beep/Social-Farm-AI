'use client';
import React, { useState, useEffect } from 'react';
import { Activity, CheckCircle, Clock, AlertTriangle, Play, Pause, Square, TrendingUp, Users, Calendar, Settings, BarChart2, Bell, Trash2, RotateCcw, Eye, History, Filter, Search, Grid, List } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Progress } from '@/components/ui/Progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { Switch } from '@/components/ui/Switch';
import { Label } from '@/components/ui/Label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/Select';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/DropdownMenu';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/Dialog';

interface AutomationStats {
  totalExecutions: number;
  successRate: number;
  failureRate: number;
  pendingExecutions: number;
  processingQueue: number;
}

interface Execution {
  id: string;
  automationName: string;
  platform: string;
  status: 'success' | 'failed' | 'pending' | 'processing';
  startTime: string;
  endTime?: string;
  executionTime: number;
  postsCreated?: number;
  errors?: string;
}

const automationStats: AutomationStats = {
  totalExecutions: 1247,
  successRate: 94,
  failureRate: 6,
  pendingExecutions: 12,
  processingQueue: 8,
};

const recentExecutions: Execution[] = [
  {
    id: 'exec-001',
    automationName: 'Daily Instagram Poster',
    platform: 'Instagram',
    status: 'success',
    startTime: '2025-06-27 09:00:00',
    endTime: '2025-06-27 09:15:00',
    executionTime: 15,
    postsCreated: 3,
  },
  {
    id: 'exec-002',
    automationName: 'Auto Commenter',
    platform: 'TikTok',
    status: 'processing',
    startTime: '2025-06-27 10:30:00',
    endTime: undefined,
    executionTime: 0,
    postsCreated: 0,
    errors: 'API rate limit approaching',
  },
  {
    id: 'exec-003',
    automationName: 'Trend Monitor - Twitter',
    platform: 'Twitter',
    status: 'failed',
    startTime: '2025-06-27 08:00:00',
    endTime: '2025-06-27 08:45:00',
    executionTime: 45,
    postsCreated: 0,
    errors: 'Token expired',
  },
  {
    id: 'exec-004',
    automationName: 'Auto Engagement - LinkedIn',
    platform: 'LinkedIn',
    status: 'success',
    startTime: '2025-06-27 11:15:00',
    endTime: '2025-06-27 11:20:00',
    executionTime: 5,
    postsCreated: 12,
  },
  {
    id: 'exec-005',
    automationName: 'Content Recycling',
    platform: 'Facebook',
    status: 'pending',
    startTime: '2025-06-27 12:00:00',
    endTime: undefined,
    executionTime: 0,
    postsCreated: 0,
  },
];

export default function AutomationDashboardPage() {
  const [executions, setExecutions] = useState<Execution[]>(recentExecutions);
  const [stats, setStats] = useState<AutomationStats>(automationStats);
  const [healthStatus, setHealthStatus] = useState<'healthy' | 'degraded' | 'offline'>('healthy');

  const getStatusIcon = (status: Execution['status']) => {
    switch (status) {
      case 'success':
        return <CheckCircle className='w-5 h-5 text-green-400' />;
      case 'failed':
        return <AlertTriangle className='w-5 h-5 text-red-400' />;
      case 'processing':
        return <Activity className='w-5 h-5 text-blue-400 animate-pulse' />;
      case 'pending':
        return <Clock className='w-5 h-5 text-yellow-400' />;
    }
  };

  const getStatusColor = (status: Execution['status']) => {
    switch (status) {
      case 'success':
        return 'bg-green-500/20 text-green-400';
      case 'failed':
        return 'bg-red-500/20 text-red-400';
      case 'processing':
        return 'bg-blue-500/20 text-blue-400';
      case 'pending':
        return 'bg-yellow-500/20 text-yellow-400';
    }
  };

  const getHealthStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-500/20 text-green-400';
      case 'degraded':
        return 'bg-yellow-500/20 text-yellow-400';
      case 'offline':
        return 'bg-red-500/20 text-red-400';
      default:
        return 'bg-gray-500/20 text-gray-400';
    }
  };

  return (
    <div className='space-y-6'>
      <div className='flex justify-between items-center'>
        <div>
          <h1 className='text-2xl font-bold'>Automation Dashboard</h1>
          <p className='text-gray-400'>Monitor and manage your automation workflows</p>
        </div>
        <div className='flex gap-2'>
          <Button variant='outline' size='sm'>
            <History className='w-4 h-4 mr-2' /> View History
          </Button>
          <Button variant='primary' size='sm'>
            <Settings className='w-4 h-4 mr-2' /> Automation Settings
          </Button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6'>
        <Card>
          <CardHeader className='pb-2'>
            <CardTitle className='text-sm font-medium text-gray-400'>Total Executions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='flex items-center justify-between'>
              <div className='text-2xl font-bold'>{stats.totalExecutions.toLocaleString()}</div>
              <Activity className='w-8 h-8 text-purple-400' />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='pb-2'>
            <CardTitle className='text-sm font-medium text-gray-400'>Success Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='flex items-center justify-between'>
              <div className='text-2xl font-bold'>{stats.successRate}%</div>
              <CheckCircle className='w-8 h-8 text-green-400' />
            </div>
            <Progress value={stats.successRate} className='mt-2' />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='pb-2'>
            <CardTitle className='text-sm font-medium text-gray-400'>Failure Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='flex items-center justify-between'>
              <div className='text-2xl font-bold'>{stats.failureRate}%</div>
              <AlertTriangle className='w-8 h-8 text-red-400' />
            </div>
            <Progress value={stats.failureRate} className='mt-2' />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='pb-2'>
            <CardTitle className='text-sm font-medium text-gray-400'>Pending</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='flex items-center justify-between'>
              <div className='text-2xl font-bold'>{stats.pendingExecutions}</div>
              <Clock className='w-8 h-8 text-yellow-400' />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='pb-2'>
            <CardTitle className='text-sm font-medium text-gray-400'>Processing Queue</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='flex items-center justify-between'>
              <div className='text-2xl font-bold'>{stats.processingQueue}</div>
              <Play className='w-8 h-8 text-blue-400' />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className='grid grid-cols-1 lg:grid-cols-3 gap-6'>
        {/* Worker Status */}
        <Card className='lg:col-span-1'>
          <CardHeader>
            <CardTitle>Worker Status</CardTitle>
            <CardDescription>System health and performance</CardDescription>
          </CardHeader>
          <CardContent className='space-y-4'>
            <div className='flex items-center justify-between'>
              <span className='text-sm text-gray-400'>Health Status</span>
              <Badge className={getHealthStatusColor(healthStatus)}>{healthStatus}</Badge>
            </div>
            <div className='space-y-2'>
              <div className='flex items-center justify-between'>
                <span className='text-sm text-gray-400'>Active Workers</span>
                <span className='font-medium'>8/8</span>
              </div>
              <Progress value={100} className='h-2' />
            </div>
            <div className='space-y-2'>
              <div className='flex items-center justify-between'>
                <span className='text-sm text-gray-400'>CPU Usage</span>
                <span className='font-medium'>45%</span>
              </div>
              <Progress value={45} className='h-2' />
            </div>
            <div className='space-y-2'>
              <div className='flex items-center justify-between'>
                <span className='text-sm text-gray-400'>Memory Usage</span>
                <span className='font-medium'>62%</span>
              </div>
              <Progress value={62} className='h-2' />
            </div>
            <div className='space-y-2'>
              <div className='flex items-center justify-between'>
                <span className='text-sm text-gray-400'>Queue Length</span>
                <span className='font-medium'>23/100</span>
              </div>
              <Progress value={23} className='h-2' />
            </div>
          </CardContent>
        </Card>

        {/* Execution Timeline */}
        <Card className='lg:col-span-2'>
          <CardHeader>
            <CardTitle>Execution Timeline</CardTitle>
            <CardDescription>Recent automation executions</CardDescription>
          </CardHeader>
          <CardContent>
            <div className='space-y-4'>
              {executions.map((execution) => (
                <div key={execution.id} className='flex items-center gap-4'>
                  <div className='flex-shrink-0'>{getStatusIcon(execution.status)}</div>
                  <div className='flex-grow min-w-0'>
                    <div className='flex items-center justify-between'>
                      <p className='text-sm font-medium truncate'>{execution.automationName}</p>
                      <Badge className={getStatusColor(execution.status)}>{execution.status}</Badge>
                    </div>
                    <div className='flex items-center gap-4 text-xs text-gray-500'>
                      <span>{execution.platform}</span>
                      <span>{execution.startTime}</span>
                      {execution.endTime && <span>{execution.executionTime}s</span>}
                      {execution.errors && <span className='text-red-400'>{execution.errors}</span>}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
