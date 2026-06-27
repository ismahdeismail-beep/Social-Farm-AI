'use client';
'use client';
import React, { useState } from 'react';
import { Settings, Users, Shield, Bell, Globe, Database, MessageSquare, Calendar, CreditCard, Key, Webhook, FileText, Save, RotateCcw, Plus, Trash2, Edit3, CheckCircle, AlertTriangle, Upload } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Switch } from '@/components/ui/Switch';
import { Label } from '@/components/ui/Label';
import { Input } from '@/components/ui/Input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/Select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';

interface SettingSection {
  id: string;
  label: string;
  icon: React.ReactNode;
  description: string;
}

const settingSections: SettingSection[] = [
  {
    id: 'workspace',
    label: 'Workspace Settings',
    icon: <Settings className='w-5 h-5' />,
    description: 'Manage workspace configuration and branding',
  },
  {
    id: 'users',
    label: 'User Management',
    icon: <Users className='w-5 h-5' />,
    description: 'Manage users, roles, and permissions',
  },
  {
    id: 'security',
    label: 'Security',
    icon: <Shield className='w-5 h-5' />,
    description: 'Security settings and compliance',
  },
  {
    id: 'notifications',
    label: 'Notification Settings',
    icon: <Bell className='w-5 h-5' />,
    description: 'Configure notification preferences',
  },
  {
    id: 'integrations',
    label: 'Integrations',
    icon: <Globe className='w-5 h-5' />,
    description: 'Connected social media platforms',
  },
  {
    id: 'api',
    label: 'API Configuration',
    icon: <Webhook className='w-5 h-5' />,
    description: 'API keys and webhooks',
  },
  {
    id: 'automation',
    label: 'Automation Defaults',
    icon: <MessageSquare className='w-5 h-5' />,
    description: 'Default automation settings',
  },
  {
    id: 'billing',
    label: 'Billing & Subscription',
    icon: <CreditCard className='w-5 h-5' />,
    description: 'Payment and subscription management',
  },
  {
    id: 'audit',
    label: 'Audit Logs',
    icon: <FileText className='w-5 h-5' />,
    description: 'View system activity logs',
  },
];

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState('workspace');
  const [isSaving, setIsSaving] = useState(false);
  const [settingsChanged, setSettingsChanged] = useState(false);

  const handleSave = async () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      setSettingsChanged(false);
      alert('Settings saved successfully!');
    }, 1000);
  };

  const renderSectionContent = () => {
    switch (activeSection) {
      case 'workspace':
        return (
          <div className='space-y-6'>
            <Card>
              <CardHeader>
                <CardTitle>Workspace Configuration</CardTitle>
                <CardDescription>Configure your workspace settings</CardDescription>
              </CardHeader>
              <CardContent className='space-y-4'>
                <div className='grid grid-cols-1 md:grid-cols-2 gap-4'> 
                  <div>
                    <Label>Workspace Name</Label>
                    <Input placeholder='Enter workspace name' className='mt-1' defaultValue='Social Farm AI' /> 
                  </div> 
                  <div>
                    <Label>Timezone</Label>
                    <Select defaultValue='utc'> 
                      <SelectTrigger className='mt-1'> 
                        <SelectValue /> 
                      </SelectTrigger> 
                      <SelectContent> 
                        <SelectItem value='utc'>UTC</SelectItem> 
                        <SelectItem value='est'>EST</SelectItem> 
                        <SelectItem value='pst'>PST</SelectItem> 
                        <SelectItem value='cet'>CET</SelectItem> 
                      </SelectContent> 
                    </Select> 
                  </div> 
                  <div>
                    <Label>Language</Label>
                    <Select defaultValue='en'> 
                      <SelectTrigger className='mt-1'> 
                        <SelectValue /> 
                      </SelectTrigger> 
                      <SelectContent> 
                        <SelectItem value='en'>English</SelectItem> 
                        <SelectItem value='es'>Spanish</SelectItem> 
                        <SelectItem value='fr'>French</SelectItem> 
                        <SelectItem value='de'>German</SelectItem> 
                      </SelectContent> 
                    </Select> 
                  </div> 
                  <div>
                    <Label>Date Format</Label>
                    <Select defaultValue='mdy'> 
                      <SelectTrigger className='mt-1'> 
                        <SelectValue /> 
                      </SelectTrigger> 
                      <SelectContent> 
                        <SelectItem value='mdy'>MM/DD/YYYY</SelectItem> 
                        <SelectItem value='dmy'>DD/MM/YYYY</SelectItem> 
                        <SelectItem value='ymd'>YYYY/MM/DD</SelectItem> 
                      </SelectContent> 
                    </Select> 
                  </div> 
                </div>
                <div>
                  <Label>Description</Label>
                  <Textarea placeholder='Enter workspace description' className='mt-1' rows={3} defaultValue='Enterprise social media management platform' /> 
                </div> 
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Branding</CardTitle>
                <CardDescription>Configure your workspace branding</CardDescription>
              </CardHeader>
              <CardContent className='space-y-4'> 
                <div className='grid grid-cols-1 md:grid-cols-2 gap-4'> 
                  <div>
                    <Label>Primary Color</Label>
                    <div className='flex gap-2 mt-1'> 
                      <Input type='color' defaultValue='#8b5cf6' className='w-12 h-10' /> 
                      <Input placeholder='#8b5cf6' defaultValue='#8b5cf6' /> 
                    </div> 
                  </div> 
                  <div>
                    <Label>Secondary Color</Label>
                    <div className='flex gap-2 mt-1'> 
                      <Input type='color' defaultValue='#3b82f6' className='w-12 h-10' /> 
                      <Input placeholder='#3b82f6' defaultValue='#3b82f6' /> 
                    </div> 
                  </div> 
                </div> 
                <div>
                  <Label>Logo Upload</Label>
                  <div className='mt-1 border-2 border-dashed border-[#1A2230] rounded-lg p-6 text-center hover:border-purple-500/50 transition-colors'> 
                    <Upload className='w-8 h-8 text-gray-400 mx-auto mb-2' /> 
                    <p className='text-sm text-gray-400'>Click to upload or drag and drop</p> 
                    <p className='text-xs text-gray-500 mt-1'>PNG, JPG (max 2MB)</p> 
                  </div> 
                </div> 
              </CardContent>
            </Card>
          </div>
        );

      case 'users':
        return (
          <div className='space-y-6'>
            <Card>
              <CardHeader>
                <CardTitle>User Management</CardTitle>
                <CardDescription>Manage users and their permissions</CardDescription>
              </CardHeader>
              <CardContent>
                <div className='space-y-4'> 
                  <div className='flex items-center justify-between p-4 bg-[#1A2230] rounded-lg'> 
                    <div className='flex items-center gap-3'> 
                      <Avatar fallback='JD' className='w-10 h-10' /> 
                      <div>
                        <h3 className='font-medium'>John Doe</h3>
                        <p className='text-sm text-gray-400'>john@company.com</p> 
                      </div> 
                    </div> 
                    <div className='flex items-center gap-4'> 
                      <Badge className='bg-green-500/20 text-green-400'>Admin</Badge> 
                      <Badge className='bg-blue-500/20 text-blue-400'>Active</Badge> 
                      <Button variant='secondary' size='sm'>Edit</Button> 
                    </div> 
                  </div> 
                  <div className='flex items-center justify-between p-4 bg-[#1A2230] rounded-lg'> 
                    <div className='flex items-center gap-3'> 
                      <Avatar fallback='AS' className='w-10 h-10' /> 
                      <div>
                        <h3 className='font-medium'>Alice Smith</h3>
                        <p className='text-sm text-gray-400'>alice@company.com</p> 
                      </div> 
                    </div> 
                    <div className='flex items-center gap-4'> 
                      <Badge className='bg-purple-500/20 text-purple-400'>Editor</Badge> 
                      <Badge className='bg-blue-500/20 text-blue-400'>Active</Badge> 
                      <Button variant='secondary' size='sm'>Edit</Button> 
                    </div> 
                  </div> 
                </div> 
                <Button className='mt-4'> 
                  <Plus className='w-4 h-4 mr-2' /> Add User 
                </Button> 
              </CardContent>
            </Card>
          </div>
        );

      case 'security':
        return (
          <div className='space-y-6'> 
            <Card>
              <CardHeader>
                <CardTitle>Security Settings</CardTitle>
                <CardDescription>Configure security and compliance settings</CardDescription>
              </CardHeader>
              <CardContent className='space-y-6'> 
                <div className='space-y-4'> 
                  <div className='flex items-center justify-between'> 
                    <div>
                      <h3 className='font-medium'>Two-Factor Authentication</h3> 
                      <p className='text-sm text-gray-400'>Require 2FA for all admin users</p> 
                    </div> 
                    <Switch defaultChecked /> 
                  </div> 
                  <div className='flex items-center justify-between'> 
                    <div>
                      <h3 className='font-medium'>Session Timeout</h3> 
                      <p className='text-sm text-gray-400'>Auto-logout after inactivity</p> 
                    </div> 
                    <Select defaultValue='30'> 
                      <SelectTrigger className='w-24'> 
                        <SelectValue /> 
                      </SelectTrigger> 
                      <SelectContent> 
                        <SelectItem value='15'>15 min</SelectItem> 
                        <SelectItem value='30'>30 min</SelectItem> 
                        <SelectItem value='60'>60 min</SelectItem> 
                        <SelectItem value='120'>120 min</SelectItem> 
                      </SelectContent> 
                    </Select> 
                  </div> 
                  <div className='flex items-center justify-between'> 
                    <div>
                      <h3 className='font-medium'>Password Policy</h3> 
                      <p className='text-sm text-gray-400'>Enforce strong password requirements</p> 
                    </div> 
                    <Switch defaultChecked /> 
                  </div> 
                  <div className='flex items-center justify-between'> 
                    <div>
                      <h3 className='font-medium'>IP Whitelist</h3> 
                      <p className='text-sm text-gray-400'>Restrict access to specific IP addresses</p> 
                    </div> 
                    <Switch /> 
                  </div> 
                </div> 
              </CardContent>
            </Card>
          </div>
        );

      case 'notifications':
        return (
          <div className='space-y-6'> 
            <Card>
              <CardHeader>
                <CardTitle>Notification Preferences</CardTitle>
                <CardDescription>Configure how you receive notifications</CardDescription>
              </CardHeader>
              <CardContent className='space-y-6'> 
                <div className='space-y-4'> 
                  <div className='flex items-center justify-between'> 
                    <div>
                      <h3 className='font-medium'>Email Notifications</h3> 
                      <p className='text-sm text-gray-400'>Receive notifications via email</p> 
                    </div> 
                    <Switch defaultChecked /> 
                  </div> 
                  <div className='flex items-center justify-between'> 
                    <div>
                      <h3 className='font-medium'>Push Notifications</h3> 
                      <p className='text-sm text-gray-400'>Receive browser push notifications</p> 
                    </div> 
                    <Switch defaultChecked /> 
                  </div> 
                  <div className='flex items-center justify-between'> 
                    <div>
                      <h3 className='font-medium'>SMS Notifications</h3> 
                      <p className='text-sm text-gray-400'>Receive critical alerts via SMS</p> 
                    </div> 
                    <Switch /> 
                  </div> 
                  <div>
                    <Label>Notification Frequency</Label>
                    <Select defaultValue='immediate'> 
                      <SelectTrigger className='mt-1'> 
                        <SelectValue /> 
                      </SelectTrigger> 
                      <SelectContent> 
                        <SelectItem value='immediate'>Immediate</SelectItem> 
                        <SelectItem value='hourly'>Hourly Digest</SelectItem> 
                        <SelectItem value='daily'>Daily Digest</SelectItem> 
                        <SelectItem value='weekly'>Weekly Digest</SelectItem> 
                      </SelectContent> 
                    </Select> 
                  </div> 
                </div> 
              </CardContent>
            </Card>
          </div>
        );

      case 'integrations':
        return (
          <div className='space-y-6'> 
            <Card>
              <CardHeader>
                <CardTitle>Social Media Integrations</CardTitle>
                <CardDescription>Connected social media platforms</CardDescription>
              </CardHeader>
              <CardContent className='space-y-4'> 
                <div className='space-y-3'> 
                  <div className='flex items-center justify-between p-4 bg-[#1A2230] rounded-lg'> 
                    <div className='flex items-center gap-3'> 
                      <div className='w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center'> 
                        <span className='text-white font-bold'>f</span> 
                      </div> 
                      <div>
                        <h3 className='font-medium'>Facebook</h3>
                        <p className='text-sm text-green-400'>Connected</p> 
                      </div> 
                    </div> 
                    <div className='flex items-center gap-2'> 
                      <Badge className='bg-green-500/20 text-green-400'>✓ Verified</Badge> 
                      <Button variant='secondary' size='sm'>Configure</Button> 
                      <Button variant='outline' size='sm'>Disconnect</Button> 
                    </div> 
                  </div> 
                  <div className='flex items-center justify-between p-4 bg-[#1A2230] rounded-lg'> 
                    <div className='flex items-center gap-3'> 
                      <div className='w-10 h-10 bg-pink-500 rounded-lg flex items-center justify-center'> 
                        <span className='text-white font-bold'>ig</span> 
                      </div> 
                      <div>
                        <h3 className='font-medium'>Instagram</h3>
                        <p className='text-sm text-red-400'>Error - Token expired</p> 
                      </div> 
                    </div> 
                    <div className='flex items-center gap-2'> 
                      <Badge className='bg-red-500/20 text-red-400'>Reconnect needed</Badge> 
                      <Button variant='secondary' size='sm'>Reconnect</Button> 
                    </div> 
                  </div> 
                  <div className='flex items-center justify-between p-4 bg-[#1A2230] rounded-lg'> 
                    <div className='flex items-center gap-3'> 
                      <div className='w-10 h-10 bg-black rounded-lg flex items-center justify-center'> 
                        <span className='text-white font-bold'>t</span> 
                      </div> 
                      <div>
                        <h3 className='font-medium'>TikTok</h3>
                        <p className='text-sm text-green-400'>Connected</p> 
                      </div> 
                    </div> 
                    <div className='flex items-center gap-2'> 
                      <Badge className='bg-green-500/20 text-green-400'>✓ Verified</Badge> 
                      <Button variant='secondary' size='sm'>Configure</Button> 
                    </div> 
                  </div> 
                </div> 
              </CardContent>
            </Card>
          </div>
        );

      case 'api':
        return (
          <div className='space-y-6'> 
            <Card>
              <CardHeader>
                <CardTitle>API Configuration</CardTitle>
                <CardDescription>Manage API keys and webhooks</CardDescription>
              </CardHeader>
              <CardContent className='space-y-4'> 
                <div>
                  <Label>API Key</Label>
                  <div className='flex gap-2 mt-1'> 
                    <Input placeholder='Enter API key' type='password' value='sk-****-****-****-****' readOnly /> 
                    <Button variant='outline'>Show</Button> 
                    <Button variant='outline'>Regenerate</Button> 
                  </div> 
                  <p className='text-xs text-gray-500 mt-1'>Your API key is securely stored</p> 
                </div> 
                <div>
                  <Label>Webhook URL</Label>
                  <Input placeholder='https://your-webhook-url.com' className='mt-1' defaultValue='https://api.socialfarm.ai/webhooks' /> 
                </div> 
                <div>
                  <Label>Webhook Secret</Label>
                  <Input placeholder='Enter webhook secret' className='mt-1' type='password' /> 
                </div> 
                <div className='flex items-center justify-between p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg'> 
                  <div>
                    <h3 className='font-medium'>Rate Limiting</h3>
                    <p className='text-sm text-gray-400'>API rate limits and quotas</p> 
                  </div> 
                  <Badge className='bg-blue-500/20 text-blue-400'>100/100 requests per hour</Badge> 
                </div> 
              </CardContent>
            </Card>
          </div>
        );

      case 'automation':
        return (
          <div className='space-y-6'> 
            <Card>
              <CardHeader>
                <CardTitle>Automation Defaults</CardTitle>
                <CardDescription>Configure default automation settings</CardDescription>
              </CardHeader>
              <CardContent className='space-y-6'> 
                <div className='space-y-4'> 
                  <div>
                    <Label>Default Automation Schedule</Label>
                    <Select defaultValue='business-hours'> 
                      <SelectTrigger className='mt-1'> 
                        <SelectValue /> 
                      </SelectTrigger> 
                      <SelectContent> 
                        <SelectItem value='business-hours'>Business Hours (9am-5pm)</SelectItem> 
                        <SelectItem value='always-on'>Always On</SelectItem> 
                        <SelectItem value='custom'>Custom Schedule</SelectItem> 
                      </SelectContent> 
                    </Select> 
                  </div> 
                  <div className='flex items-center justify-between'> 
                    <div>
                      <h3 className='font-medium'>Auto Approve Low-Risk Content</h3> 
                      <p className='text-sm text-gray-400'>Automatically approve content with low engagement risk</p> 
                    </div> 
                    <Switch /> 
                  </div> 
                  <div className='flex items-center justify-between'> 
                    <div>
                      <h3 className='font-medium'>Enable Error Retry</h3> 
                      <p className='text-sm text-gray-400'>Automatically retry failed automations</p> 
                    </div> 
                    <Switch defaultChecked /> 
                  </div> 
                  <div>
                    <Label>Retry Attempts</Label>
                    <Select defaultValue='3'> 
                      <SelectTrigger className='mt-1'> 
                        <SelectValue /> 
                      </SelectTrigger> 
                      <SelectContent> 
                        <SelectItem value='1'>1 attempt</SelectItem> 
                        <SelectItem value='2'>2 attempts</SelectItem> 
                        <SelectItem value='3'>3 attempts</SelectItem> 
                        <SelectItem value='5'>5 attempts</SelectItem> 
                      </SelectContent> 
                    </Select> 
                  </div> 
                </div> 
              </CardContent>
            </Card>
          </div>
        );

      case 'billing':
        return (
          <div className='space-y-6'> 
            <Card>
              <CardHeader>
                <CardTitle>Billing & Subscription</CardTitle>
                <CardDescription>Manage your subscription and billing</CardDescription>
              </CardHeader>
              <CardContent className='space-y-4'> 
                <div className='p-6 bg-gradient-to-r from-purple-500/20 to-blue-500/20 rounded-lg border border-purple-500/30'> 
                  <h3 className='text-lg font-medium mb-2'>Enterprise Plan</h3>
                  <p className='text-sm text-gray-400 mb-4'>Your current subscription includes unlimited automations</p>
                  <div className='flex items-center justify-between'> 
                    <div>
                      <p className='text-sm text-gray-400'>Next billing date</p>
                      <p className='font-medium'>2025-07-27</p> 
                    </div> 
                    <div>
                      <p className='text-sm text-gray-400'>Amount</p>
                      <p className='font-medium'>$999/month</p> 
                    </div> 
                    <Button variant='outline'>View Invoice</Button> 
                  </div> 
                </div> 
                <div className='space-y-3'> 
                  <h3 className='font-medium'>Usage This Month</h3> 
                  <div className='space-y-2'> 
                    <div className='flex items-center justify-between'> 
                      <span className='text-sm text-gray-400'>Posts Published</span> 
                      <span className='font-medium'>127/1000</span> 
                    </div> 
                    <div className='flex items-center justify-between'> 
                      <span className='text-sm text-gray-400'>API Calls</span> 
                      <span className='font-medium'>8,432/10,000</span> 
                    </div> 
                    <div className='flex items-center justify-between'> 
                      <span className='text-sm text-gray-400'>Storage Used</span> 
                      <span className='font-medium'>2.4GB/10GB</span> 
                    </div> 
                  </div> 
                </div> 
              </CardContent>
            </Card>
          </div>
        );

      case 'audit':
        return (
          <div className='space-y-6'> 
            <Card>
              <CardHeader>
                <CardTitle>Audit Logs</CardTitle>
                <CardDescription>View system activity and logs</CardDescription>
              </CardHeader>
              <CardContent>
                <div className='space-y-3'> 
                  <div className='flex items-center justify-between p-3 bg-[#1A2230] rounded-lg'> 
                    <div className='flex items-center gap-3'> 
                      <div className='w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center'> 
                        <CheckCircle className='w-4 h-4 text-green-400' /> 
                      </div> 
                      <div>
                        <h4 className='font-medium text-sm'>User Login</h4>
                        <p className='text-xs text-gray-400'>john.doe@company.com • 2025-06-27 14:30:00</p> 
                      </div> 
                    </div> 
                    <Badge className='bg-green-500/20 text-green-400 text-xs'>SUCCESS</Badge> 
                  </div> 
                  <div className='flex items-center justify-between p-3 bg-[#1A2230] rounded-lg'> 
                    <div className='flex items-center gap-3'> 
                      <div className='w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center'> 
                        <Upload className='w-4 h-4 text-blue-400' /> 
                      </div> 
                      <div>
                        <h4 className='font-medium text-sm'>Post Scheduled</h4>
                        <p className='text-xs text-gray-400'>TikTok • 2025-06-27 09:00:00</p> 
                      </div> 
                    </div> 
                    <Badge className='bg-blue-500/20 text-blue-400 text-xs'>COMPLETED</Badge> 
                  </div> 
                  <div className='flex items-center justify-between p-3 bg-[#1A2230] rounded-lg'> 
                    <div className='flex items-center gap-3'> 
                      <div className='w-8 h-8 bg-purple-500/20 rounded-lg flex items-center justify-center'> 
                        <AlertTriangle className='w-4 h-4 text-purple-400' /> 
                      </div> 
                      <div>
                        <h4 className='font-medium text-sm'>API Rate Limit Reached</h4>
                        <p className='text-xs text-gray-400'>2025-06-27 08:45:12</p> 
                      </div> 
                    </div> 
                    <Badge className='bg-red-500/20 text-red-400 text-xs'>ERROR</Badge> 
                  </div> 
                </div> 
              </CardContent>
            </Card>
          </div>
        );

      default:
        return <div>Select a section</div>;
    }
  };

  return (
    <div className='space-y-6'>
      <div className='flex justify-between items-center'> 
        <div>
          <h1 className='text-2xl font-bold'>Settings</h1>
          <p className='text-gray-400'>Manage your workspace configuration</p> 
        </div> 
        <div className='flex gap-2'> 
          <Button variant='outline' onClick={() => setSettingsChanged(false)}> 
            <RotateCcw className='w-4 h-4 mr-2' /> Reset 
          </Button> 
          <Button variant='primary' onClick={handleSave} disabled={!settingsChanged || isSaving}> 
            {isSaving ? 'Saving...' : ( 
              <><Save className='w-4 h-4 mr-2' /> Save Changes</> 
            )} 
          </Button> 
        </div> 
      </div>

      <div className='grid grid-cols-1 lg:grid-cols-4 gap-6'> 
        <Card className='lg:col-span-1'> 
          <CardHeader>
            <CardTitle>Settings Sections</CardTitle>
          </CardHeader>
          <CardContent className='p-2'> 
            {settingSections.map((section) => ( 
              <button 
                key={section.id} 
                onClick={() => setActiveSection(section.id)} 
                className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors text-left ${activeSection === section.id ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'text-gray-400 hover:text-white hover:bg-[#1A2230]'}`}
              > 
                <div className={`${activeSection === section.id ? 'text-purple-400' : 'text-gray-500'}`}> {section.icon} </div> 
                <div>
                  <div className='font-medium'>{section.label}</div> 
                  <div className='text-xs text-gray-500'>{section.description}</div> 
                </div> 
              </button> 
            ))} 
          </CardContent> 
        </Card>

        <Card className='lg:col-span-3'> 
          <CardHeader>
            <CardTitle>{settingSections.find((s) => s.id === activeSection)?.label}</CardTitle> 
            <CardDescription>{settingSections.find((s) => s.id === activeSection)?.description}</CardDescription> 
          </CardHeader>
          <CardContent>{renderSectionContent()}</CardContent> 
        </Card>
      </div> 
    </div>
  );
}
