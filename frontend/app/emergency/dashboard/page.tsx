import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, Bell, CheckCircle, Clock, Database, Download, TrendingUp, Users, Wifi, WifiOff, AlertCircle, Shield, Settings, BarChart2 } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { Progress } from '@/components/ui/Progress';
import { ScrollArea } from '@/components/ui/ScrollArea';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/Alert';

interface SystemStatus {
  status: 'healthy' | 'degraded' | 'offline';
  lastCheck: string;
  uptime: number;
  version: string;
}

interface AutomationModule {
  id: string;
  name: string;
  status: 'active' | 'inactive' | 'error';
  executions: number;
  success_rate: number;
  last_execution: string;
  errors: number;
}

interface Notification {
  id: string;
  type: 'info' | 'warning' | 'error' | 'success';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
}

const EmergencyDashboard = () => {
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({ status: 'offline', lastCheck: '', uptime: 0, version: '0.3.0' });
  const [automationModules, setAutomationModules] = useState<AutomationModule[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isSystemHealthy, setIsSystemHealthy] = useState(true);
  const [isWebSocketConnected, setIsWebSocketConnected] = useState(false);

  useEffect(() => {
    fetchSystemStatus();
    fetchAutomationModules();
    fetchNotifications();
    
    // WebSocket connection for real-time updates
    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8080'}/emergency`);
    
    ws.onopen = () => {
      console.log('Emergency WebSocket connected');
      setIsWebSocketConnected(true);
      ws.send(JSON.stringify({ type: 'join_emergency' }));
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'system_update') {
        setSystemStatus(data.payload);
      } else if (data.type === 'automation_update') {
        setAutomationModules(data.payload);
      } else if (data.type === 'notification') {
        setNotifications(prev => [{ id: Date.now().toString(), ...data.payload, read: false }, ...prev]);
      }
    };
    
    ws.onerror = (error) => {
      console.error('Emergency WebSocket error:', error);
      setIsWebSocketConnected(false);
    };
    
    ws.onclose = () => {
      console.log('Emergency WebSocket disconnected');
      setIsWebConnection(false);
      // Attempt to reconnect after 5 seconds
      setTimeout(() => {
        // Reconnect logic will be handled by the main WS implementation
      }, 5000);
    };
    
    return () => ws.close();
  }, []);

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch('/api/health');
      const data = await response.json();
      setSystemStatus(data);
      setIsSystemHealthy(data.status === 'healthy');
    } catch (error) {
      console.error('Failed to fetch system status:', error);
      setSystemStatus({ status: 'offline', lastCheck: new Date().toISOString(), uptime: 0, version: 'unknown' });
      setIsSystemHealthy(false);
    }
  };

  const fetchAutomationModules = async () => {
    try {
      const response = await fetch('/api/automation/modules');
      const data = await response.json();
      setAutomationModules(data);
    } catch (error) {
      console.error('Failed to fetch automation modules:', error);
    }
  };

  const fetchNotifications = async () => {
    try {
      const response = await fetch('/api/notifications?unread=true');
      const data = await response.json();
      setNotifications(data);
    } catch (error) {
      console EDF.error('Failed to fetch notifications:', error);
    }
  };

  const getSystemStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'degraded':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'offline':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getModuleStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-500/20 text-green-400';
      case 'error':
        return 'bg-red-500/20 text-red-400';
      case 'inactive':
        return 'bg-gray-500/20 text-gray-400';
      default:
        return 'bg-gray-500/20 text-gray-400';
    }
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle className='w-4 h-4 text-green-400' />;
      case 'warning':
        return <AlertTriangle className='w-4 h-4 text-yellow-400' />;
      case 'error':
        return <AlertCircle className='w-4 h-4 text-red-400' />;
      case 'info':
        return <AlertCircle className='w-4 h-4 text-blue-400' />;
      default:
        return <Bell className='w-4 h-4 text-gray-400' />;
    }
  };

  return (
    <div className='min-h-screen bg-gray-900 text-white p-6'>
      {/* Emergency Header */}
      <div className='flex justify-between items-center mb-8'>
        <div>
          <h1 className='text-3xl font-bold flex items-center gap-3'>🚨 EMERGENCY DASHBOARD</h1>
          <p className='text-gray-400 mt-2'>Critical System Status & Recovery Operations</p>
        </div>
        <div className='flex items-center gap-4'> 
          <div className={`px-4 py-2 rounded-lg border ${getSystemStatusColor(systemStatus.status)}`}> 
            <div className='text-sm font-semibold'>SYSTEM STATUS</div>
            <div className='text-xs'>{systemStatus.status.toUpperCase()}</div>
          </div>
          <div className='px-4 py-2 bg-gray-800 rounded-lg'>
            <div className='text-sm font-semibold'>UPTIME</div>
            <div className='text-xs'>{systemStatus.uptime}%</div>
          </div>
          <div className='px-4 py-2 bg-gray-800 rounded-lg'> 
            <div className='text-sm font-semibold'>VERSION</div>
            <div className='text-xs'>{systemStatus.version}</div>
          </div>
          <button 
            onClick={() => window.location.reload()}
            className='px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors'
          >
            🔄 REFRESH SYSTEM
          </button>
        </div>
      </div>

      {/* Emergency Alert */}
      {!isSystemHealthy && (
        <Alert className='mb-8 border-red-500 bg-red-500/10'>
          <AlertTriangle className='h-4 w-4' />
          <AlertTitle>SYSTEM HEALTH ALERT</AlertTitle>
          <AlertDescription>
            Critical system issues detected. Recovery operations are in progress. 
            Some features may be temporarily unavailable.
          </AlertDescription>
        </Alert>
      )}

      {/* Connection Status */}
      <div className='flex items-center gap-4 mb-6'> 
        {isWebSocketConnected ? (
          <div className='flex items-center gap-2 px-3 py-2 bg-green-500/20 rounded-lg'> 
            <Wifi className='w-4 h-4 text-green-400' />
            <span className='text-sm text-green-400'>WEBSOCKET CONNECTED</span>
          </div>
        ) : (
          <div className='flex items-center gap-2 px-3 py-2 bg-red-500/20 rounded-lg'> 
            <WifiOff className='w-4 h-4 text-red-400' />
            <span className='text-sm text-red-400'>WEBSOCKET DISCONNECTED</span>
          </div>
        )}
        <div className='text-sm text-gray-400'>
          Last updated: {new Date().toLocaleString()}
        </div>
      </div>

      {/* Main Dashboard Grid */}
      <div className='grid grid-cols-1 lg:grid-cols-3 gap-6'>
        {/* System Status Card */}
        <Card className='lg:col-span-1'>
          <CardHeader>
            <CardTitle className='flex items-center gap-2'> 
              <Database className='w-5 h-5' /> System Status
            </CardTitle>
            <CardDescription>Core infrastructure health</CardDescription>
          </CardHeader>
          <CardContent>
            <div className='space-y-4'>
              <div className='flex items-center justify-between'> 
                <span className='text-sm text-gray-400'>API Gateway</span>
                <Badge className={getSystemStatusColor(systemStatus.status)}> 
                  {systemStatus.status}
                </Badge>
              </div>
              <div className='flex items-center justify-between'> 
                <span className='text-sm text-gray-400'>Worker Pool</span>
                <Badge className='bg-green-500/20 text-green-400'>ACTIVE</Badge>
              </div>
              <div className='flex items-center justify-between'> 
                <span className='text-sm text-gray-400'>Cache Layer</span> 
                <Badge className='bg-green-500/20 text-green-400'>OPTIMAL</Badge>
              </div>
              <div className='flex items-center justify-between'> 
                <span className='text-sm text-gray-400'>Message Queue</span>
                <Badge className='bg-green-500/20 text-green-400'>RUNNING</Badge>
              </div>
            </div>
            <div className='mt-4 pt-4 border-t border-gray-800'> 
              <div className='text-sm text-gray-400 mb-2'>System Health Score</div> 
              <Progress value={isSystemHealthy ? 95 : 30} className='h-2' /> 
            </div>
          </CardContent>
        </Card>

        {/* Automation Modules Status */}
        <Card className='lg:col-span-2'> 
          <CardHeader>
            <CardTitle className='flex items-center gap-2'> 
              <Activity className='w-5 h-5' /> Automation Modules
            </CardTitle>
            <CardDescription>Core automation workflow status</CardDescription>
          </CardHeader>
          <CardContent>
            {automationModules.length === 0 ? ( 
              <div className='text-center py-8'> 
                <div className='text-gray-500 mb-2'>Loading automation modules...</div> 
                <div className='w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto' />
              </div>
            ) : (
              <div className='grid grid-cols-1 md:grid-cols-2 gap-4'> 
                {automationModules.map((module) => (
                  <div key={module.id} className='p-4 bg-gray-800 rounded-lg border border-gray-700'> 
                    <div className='flex items-center justify-between mb-2'> 
                      <h3 className='font-semibold'>{module.name}</h3> 
                      <Badge className={getModuleStatusColor(module.status)}> 
                        {module.status}
                      </Badge> 
                    </div> 
                    <div className='space-y-2 text-sm text-gray-400'> 
                      <div className='flex justify-between'> 
                        <span>Executions:</span> 
                        <span className='font-medium text-white'>{module.executions}</span> 
                      </div> 
                      <div className='flex justify-between'> 
                        <span>Success Rate:</span> 
                        <span className='font-medium text-green-400'>{module.success_rate}%</span> 
                      </div> 
                      <div className='flex justify-between'> 
                        <span>Last Execution:</span> 
                        <span>{module.last_execution}</span> 
                      </div> 
                      <div className='flex justify-between'> 
                        <span>Errors:</span> 
                        <span className='font-medium text-red-400'>{module.errors}</span> 
                      </div> 
                    </div> 
                  </div> 
                ))} 
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Notifications Section */}
      <Card className='mt-6'> 
        <CardHeader>
          <CardTitle className='flex items-center gap-2'> 
            <Bell className='w-5 h-5' /> Critical Notifications
          </CardTitle>
          <CardDescription>Unread alerts and system messages</CardDescription>
        </CardHeader>
        <CardContent>
          {notifications.length === 0 ? ( 
            <div className='text-center py-8'> 
              <div className='text-green-400 mb-2'>✅ NO CRITICAL NOTIFICATIONS</div> 
              <div className='text-sm text-gray-500'>All systems operational</div> 
            </div>
          ) : ( 
            <div className='space-y-3'> 
              {notifications.map((notification) => (
                <div key={notification.id} className='p-4 bg-gray-800 rounded-lg border-l-4 border-gray-600 hover:bg-gray-750 transition-colors'> 
                  <div className='flex items-start gap-3'> 
                    <div className='mt-1'> {getNotificationIcon(notification.type)} </div> 
                    <div className='flex-1'> 
                      <div className='flex items-center justify-between mb-1'> 
                        <h4 className='font-medium text-sm'>{notification.title}</h4> 
                        <span className='text-xs text-gray-500'> 
                          {new Date(notification.timestamp).toLocaleTimeString()}
                        </span> 
                      </div> 
                      <p className='text-sm text-gray-400'> {notification.message}</p> 
                    </div> 
                  </div> 
                </div> 
              ))} 
            </div>
          )}
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card className='mt-6'> 
        <CardHeader>
          <CardTitle>Emergency Operations</CardTitle>
          <CardDescription>Quick system recovery and diagnostic actions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className='grid grid-cols-1 md:grid-cols-3 gap-4'> 
            <button 
              onClick={() => fetchSystemStatus()}
              className='p-4 bg-gray-800 rounded-lg hover:bg-gray-750 transition-colors text-left'
            > 
              <div className='font-semibold mb-1'>🔍 System Diagnostic</div> 
              <div className='text-sm text-gray-400'>Check system health</div> 
            </button> 
            <button 
              onClick={() => fetchAutomationModules()}
              className='p-4 bg-gray-800 rounded-lg hover:bg-gray-750 transition-colors text-left'
            > 
              <div className='font-semibold mb-1'>🔄 Auto Modules</div> 
              <div className='text-sm text-gray-400'>Refresh automation status</div> 
            </button> 
            <button 
              onClick={() => fetchNotifications()}
              className='p-4 bg-gray-800 rounded-lg hover:bg-gray-750 transition-colors text-left'
            > 
              <div className='font-semibold mb-1'>📋 Notifications</div> 
              <div className='text-sm text-gray-400'>Fetch unread alerts</div> 
            </button> 
            <button 
              onClick={() => window.location.href = '/api/docs'}
              className='p-4 bg-gray-800 rounded-lg hover:bg-gray-750 transition-colors text-left'
            > 
              <div className='font-semibold mb-1'>📚 API Docs</div> 
              <div className='text-sm text-gray-400'>View API documentation</div> 
            </button> 
            <button 
              onClick={() => window.location.href = '/automation/dashboard'}
              className='p-4 bg-gray-800 rounded-lg hover:bg-gray-750 transition-colors text-left'
            > 
              <div className='font-semibold mb-1'>📊 Automation Dashboard</div> 
              <div className='text-sm text-gray-400'>View automation metrics</div> 
            </button> 
            <button 
              onClick={() => window.location.href = '/ai'}
              className='p-4 bg-gray-800 rounded-lg hover:bg-gray-750 transition-colors text-left'
            > 
              <div className='font-semibold mb-1'>🤖 AI Command Center</div> 
              <div className='text-sm text-gray-400'>Access AI orchestration</div> 
            </button> 
          </div> 
        </CardContent>
      </Card>

      {/* Recovery Status */}
      <Card className='mt-6'> 
        <CardHeader>
          <CardTitle>Recovery Operations Status</CardTitle>
          <CardDescription>Current emergency recovery progress</CardDescription>
        </CardHeader>
        <CardContent>
          <div className='space-y-4'> 
            <div className='flex items-center justify-between'> 
              <span className='text-sm text-gray-400'>✅ Emergency Dashboard Active</span> 
              <Badge className='bg-green-500/20 text-green-400'>ONLINE</Badge> 
            </div> 
            <div className='flex items-center justify-between'> 
              <span className='text-sm text-gray-400'>WebSocket Connection</span> 
              <Badge classnName={`bg-${isWebSocketConnected ? 'green' : 'red'}-500/20 text-${isWebSocketConnected ? 'green' : 'red'}-400`}> 
                {isWebSocketConnected ? 'CONNECTED' : 'DISCONNECTED'}
              </Badge> 
            </div> 
            <div className='flex items-center justify-between'> 
              <span className='text-sm text-gray-400'>System Recovery Mode</span> 
              <Badge className='bg-blue-500/20 text-blue-400'>EMERGENCY</Badge> 
            </div> 
            <div className='flex items-center justify-between'> 
              <span className='text-sm text-gray-400'>Data Persistence</span> 
              <Badge className='bg-green-500/20 text-green-400'>ACTIVE</Badge> 
            </div> 
            <div className='flex items-center justify-between'> 
              <span className='text-sm text-gray-400'>API Connectivity</span> 
              <Badge className='bg-green-500/20 text-green-400'>OPERATIONAL</Badge> 
            </div> 
          </div> 
        </CardContent>
      </Card>
    </div>
  );
};

export default EmergencyDashboard;
