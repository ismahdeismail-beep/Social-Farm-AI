'use client';
import React, { useState, useEffect } from 'react';
import { Bell, CheckCircle, AlertTriangle, Activity, Clock, Trash2, Archive, Search, Filter, BellRing, BellOff, Check, X, Settings, Calendar, TrendingUp, Users, MessageSquare, FileText, Image, Video, Play } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Switch } from '@/components/ui/Switch';
import { Label } from '@/components/ui/Label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/Select';
import { Input } from '@/components/ui/Input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/Dialog';
import { Textarea } from '@/components/ui/Textarea';

interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error' | 'approval' | 'system';
  status: 'unread' | 'read' | 'archived';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  platform: string;
  source: string;
  actionUrl?: string;
  createdAt: string;
  expiresAt?: string;
  actionRequired?: boolean;
}

interface NotificationStats {
  total: number;
  unread: number;
  archived: number;
  urgent: number;
  approvalRequests: number;
  systemAlerts: number;
}

const notificationStats: NotificationStats = {
  total: 47,
  unread: 12,
  archived: 8,
  urgent: 3,
  approvalRequests: 5,
  systemAlerts: 2,
};

const recentNotifications: Notification[] = [
  {
    id: 'notif-001',
    title: 'Approval Required',
    message: 'Your LinkedIn post scheduled for tomorrow requires approval',
    type: 'approval',
    status: 'unread',
    priority: 'high',
    platform: 'LinkedIn',
    source: 'Auto Engagement Workflow',
    actionUrl: '/automation/workflows/wf-004',
    createdAt: '2025-06-27 10:30:00',
    actionRequired: true,
  },
  {
    id: 'notif-002',
    title: 'Trend Detected',
    message: 'New viral trend detected for your industry. Create content now!',
    type: 'info',
    status: 'unread',
    priority: 'medium',
    platform: 'TikTok',
    source: 'Trend Monitor',
    actionUrl: '/automation/modules/trend-monitoring',
    createdAt: '2025-06-27 09:15:00',
    actionRequired: true,
  },
  {
    id: 'notif-003',
    title: 'System Alert',
    message: 'Worker health degraded. Some automations may be delayed',
    type: 'warning',
    status: 'unread',
    priority: 'urgent',
    platform: 'System',
    source: 'Automation Dashboard',
    createdAt: '2025-06-27 08:45:00',
    actionRequired: true,
  },
  {
    id: 'notif-004',
    title: 'Post Published Successfully',
    message: 'Your TikTok post "Farm Life Updates" has been published',
    type: 'success',
    status: 'unread',
    priority: 'low',
    platform: 'TikTok',
    source: 'Auto Publish Module',
    actionUrl: '/analytics',
    createdAt: '2025-06-27 07:00:00',
    actionRequired: false,
  },
  {
    id: 'notif-005',
    title: 'Content Ready for Review',
    message: 'AI generated content for Instagram is ready for approval',
    type: 'approval',
    status: 'read',
    priority: 'high',
    platform: 'Instagram',
    source: 'AI Writer Module',
    actionUrl: '/content-studio',
    createdAt: '2025-06-26 15:30:00',
    actionRequired: true,
  },
];

export default function NotificationCenterPage() {
  const [notifications, setNotifications] = useState<Notification[]>(recentNotifications);
  const [stats, setStats] = useState<NotificationStats>(notificationStats);
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('all');

  const getNotificationIcon = (type: Notification['type']) => {
    switch (type) {
      case 'success':
        return <CheckCircle className='w-5 h-5 text-green-400' />;
      case 'warning':
        return <AlertTriangle className='w-5 h-5 text-yellow-400' />;
      case 'error':
        return <AlertTriangle className='w-5 h-5 text-red-400' />;
      case 'approval':
        return <Check className='w-5 h-5 text-blue-400' />;
      case 'system':
        return <Activity className='w-5 h-5 text-purple-400' />;
      default:
        return <Bell className='w-5 h-5 text-gray-400' />;
    }
  };

  const getNotificationColor = (type: Notification['type']) => {
    switch (type) {
      case 'success':
        return 'bg-green-500/20 border-green-500/30 text-green-400';
      case 'warning':
        return 'bg-yellow-500/20 border-yellow-500/30 text-yellow-400';
      case 'error':
        return 'bg-red-500/20 border-red-500/30 text-red-400';
      case 'approval':
        return 'bg-blue-500/20 border-blue-500/30 text-blue-400';
      case 'system':
        return 'bg-purple-500/20 border-purple-500/30 text-purple-400';
      default:
        return 'bg-gray-500/20 border-gray-500/30 text-gray-400';
    }
  };

  const getPriorityColor = (priority: Notification['priority']) => {
    switch (priority) {
      case 'urgent':
        return 'border-l-4 border-red-500';
      case 'high':
        return 'border-l-4 border-orange-500';
      case 'medium':
        return 'border-l-4 border-yellow-500';
      case 'low':
        return 'border-l-4 border-green-500';
    }
  };

  const filteredNotifications = notifications.filter((notif) => {
    const matchesFilter = filter === 'all' || 
      (filter === 'unread' ? notif.status === 'unread' : notif.status === 'archived');
    const matchesSearch = notif.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      notif.message.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = selectedType === 'all' || notif.type === selectedType;
    return matchesFilter && matchesSearch && matchesType;
  });

  const markAsRead = (id: string) => {
    setNotifications(prev => prev.map(notif =>
      notif.id === id ? { ...notif, status: 'read' as const } : notif
    ));
    setStats(prev => ({ ...prev, unread: prev.unread - 1 }));
  };

  const markAsArchived = (id: string) => {
    setNotifications(prev => prev.map(notif =>
      notif.id === id ? { ...notif, status: 'archived' as const } : notif
    ));
    setStats(prev => ({ ...prev, unread: prev.unread - 1, archived: prev.archived + 1 }));
  };

  const deleteNotification = (id: string) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
    const deleted = notifications.find(n => n.id === id);
    if (deleted) {
      setStats(prev => {
        const newStats = { ...prev };
        if (deleted.status === 'unread') newStats.unread = Math.max(0, newStats.unread - 1);
        if (deleted.status === 'archived') newStats.archived = Math.max(0, newStats.archived - 1);
        newStats.total = Math.max(0, newStats.total - 1);
        return newStats;
      });
    }
  };

  const clearAllRead = () => {
    setNotifications(prev => prev.map(notif => ({ ...notif, status: 'read' as const })));
    setStats(prev => ({ ...prev, unread: 0 }));
  };

  const clearAllArchived = () => {
    setNotifications(prev => prev.map(notif =>
      notif.status === 'archived' ? { ...notif, status: 'read' as const } : notif
    ));
    setStats(prev => ({ ...prev, archived: 0 }));
  };

  return (
    <div className='space-y-6'>
      <div className='flex justify-between items-center'>
        <div>
          <h1 className='text-2xl font-bold'>Notification Center</h1>
          <p className='text-gray-400'>Manage your notifications and alerts</p>
        </div>
        <div className='flex gap-2'> 
          <Button variant='outline' size='sm' onClick={clearAllRead} disabled={stats.unread === 0}>
            <Check className='w-4 h-4 mr-2' /> Mark All Read
          </Button>
          <Button variant='outline' size='sm' onClick={clearAllArchived} disabled={stats.archived === 0}>
            <Archive className='w-4 h-4 mr-2' /> Clear Archived
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className='grid grid-cols-1 md:grid-cols-5 gap-4'>
        <Card>
          <CardHeader className='pb-2'>
            <CardTitle className='text-sm font-medium text-gray-400'>Total</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold'>{stats.total}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='pb-2'>
            <CardTitle className='text-sm font-medium text-gray-400'>Unread</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold text-blue-400'>{stats.unread}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='pb-2'>
            <CardTitle className='text-sm font-medium text-gray-400'>Archived</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold text-gray-400'>{stats.archived}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='pb-2'>
            <CardTitle className='text-sm font-medium text-gray-400'>Urgent</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold text-red-400'>{stats.urgent}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className='pb-2'>
            <CardTitle className='text-sm font-medium text-gray-400'>Approvals</CardTitle>
          </CardHeader>
          <CardContent>
            <div className='text-2xl font-bold text-purple-400'>{stats.approvalRequests}</div>
          </CardContent>
        </Card>
      </div>

      <div className='grid grid-cols-1 lg:grid-cols-4 gap-6'>
        {/* Filters */}
        <Card className='lg:col-span-1'>
          <CardHeader>
            <CardTitle>Filters</CardTitle>
          </CardHeader>
          <CardContent className='space-y-4'>
            <div>
              <Label className='text-sm font-medium'>Status</Label>
              <Select value={filter} onValueChange={setFilter}>
                <SelectTrigger className='mt-1'>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value='all'>All Notifications</SelectItem>
                  <SelectItem value='unread'>Unread Only</SelectItem>
                  <SelectItem value='archived'>Archived Only</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label className='text-sm font-medium'>Type</Label>
              <Select value={selectedType} onValueChange={setSelectedType}>
                <SelectTrigger className='mt-1'>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value='all'>All Types</SelectItem>
                  <SelectItem value='info'>Info</SelectItem>
                  <SelectItem value='success'>Success</SelectItem>
                  <SelectItem value='warning'>Warning</SelectItem>
                  <SelectItem value='error'>Error</SelectItem>
                  <SelectItem value='approval'>Approval</SelectItem>
                  <SelectItem value='system'>System</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label className='text-sm font-medium'>Search</Label>
              <Input
                placeholder='Search notifications...'
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className='mt-1'
              />
            </div>

            <div className='pt-4 border-t border-[#1A2230]'>
              <div className='text-sm font-medium text-gray-400 mb-2'>Quick Actions</div>
              <div className='space-y-2'>
                <Button variant='outline' size='sm' className='w-full justify-start'>
                  <BellRing className='w-4 h-4 mr-2' /> Enable Sound
                </Button>
                <Button variant='outline' size='sm' className='w-full justify-start'>
                  <BellOff className='w-4 h-4 mr-2' /> Disable All
                </Button>
                <Button variant='outline' size='sm' className='w-full justify-start'>
                  <Settings className='w-4 h-4 mr-2' /> Notification Settings
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Notification List */}
        <Card className='lg:col-span-3'>
          <CardHeader>
            <CardTitle>Notifications ({filteredNotifications.length})</CardTitle>
          </CardHeader>
          <CardContent className='space-y-3'>
            {filteredNotifications.length === 0 ? (
              <div className='text-center py-12'>
                <Bell className='w-16 h-16 text-gray-500 mx-auto mb-4' />
                <h3 className='text-lg font-medium mb-2'>No notifications found</h3>
                <p className='text-gray-500'>Try adjusting your filters or search query</p>
              </div>
            ) : (
              filteredNotifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`p-4 rounded-lg border transition-all hover:bg-[#1A2230] cursor-pointer ${getPriorityColor(notification.priority)}`}
                >
                  <div className='flex items-start gap-4'> 
                    <div className={`p-2 rounded-lg border ${getNotificationColor(notification.type)}`}> 
                      {getNotificationIcon(notification.type)} 
                    </div>
                    <div className='flex-1 min-w-0'> 
                      <div className='flex items-center justify-between mb-1'> 
                        <h4 className='font-medium truncate'>{notification.title}</h4> 
                        <Badge variant='secondary' className='text-xs ml-2'> 
                          {notification.platform} 
                        </Badge> 
                      </div> 
                      <p className='text-sm text-gray-400 truncate'>{notification.message}</p> 
                      <div className='flex items-center justify-between mt-2 text-xs text-gray-500'> 
                        <span>{notification.createdAt}</span> 
                        <div className='flex items-center gap-2'> 
                          {notification.actionRequired && ( 
                            <Badge variant='secondary' className='text-xs bg-blue-500/20 text-blue-400'> 
                              Action Required 
                            </Badge> 
                          )} 
                          <button 
                            onClick={() => notification.status === 'unread' && markAsRead(notification.id)} 
                            className='text-gray-400 hover:text-white' 
                          > 
                            <Check className='w-3 h-3' /> 
                          </button> 
                          <button 
                            onClick={() => markAsArchived(notification.id)} 
                            className='text-gray-400 hover:text-white' 
                          > 
                            <Archive className='w-3 h-3' /> 
                          </button> 
                          <button 
                            onClick={() => deleteNotification(notification.id)} 
                            className='text-gray-400 hover:text-red-400' 
                          > 
                            <Trash2 className='w-3 h-3' /> 
                          </button> 
                        </div> 
                      </div> 
                    </div> 
                  </div> 
                </div> 
              )) 
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
