import React, { useState } from 'react';
import { Play, Plus, Trash2, Settings, Activity, Clock, CheckCircle, AlertTriangle, ChevronRight, GripVertical, Save, Eye, Users, Calendar, BarChart2, TrendingUp, Target, Bell, Filter as FilterIcon, Search } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Switch } from '@/components/ui/Switch';
import { Label } from '@/components/ui/Label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/Select';
import { Input } from '@/components/ui/Input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';

interface Workflow {
  id: string;
  name: string;
  description: string;
  platform: string;
  status: 'active' | 'inactive' | 'draft';
  lastRun: string;
  nextRun: string;
  triggers: string[];
  actions: string[];
  approvals: number;
  pendingApprovals: number;
}

const workflows: Workflow[] = [
  {
    id: 'wf-001',
    name: 'Daily Instagram Poster',
    description: 'Automated posting of daily content to Instagram',
    platform: 'Instagram',
    status: 'active',
    lastRun: '2025-06-27 09:00:00',
    nextRun: '2025-06-28 09:00:00',
    triggers: ['Schedule', 'Manual'],
    actions: ['Post', 'Track Performance'],
    approvals: 5,
    pendingApprovals: 0,
  },
  {
    id: 'wf-002',
    name: 'Auto Commenter',
    description: 'AI-powered commenting on TikTok videos',
    platform: 'TikTok',
    status: 'active',
    lastRun: '2025-06-27 10:30:00',
    nextRun: '2025-06-27 11:30:00',
    triggers: ['On Video Upload', 'Schedule'],
    actions: ['Comment', 'Engage'],
    approvals: 3,
    pendingApprovals: 1,
  },
  {
    id: 'wf-003',
    name: 'Trend Monitor - Twitter',
    description: 'Monitor Twitter trends and create posts',
    platform: 'Twitter',
    status: 'inactive',
    lastRun: '2025-06-25 14:00:00',
    nextRun: null,
    triggers: ['Keyword Alert', 'Schedule'],
    actions: ['Analyze', 'Create Post'],
    approvals: 2,
    pendingApprovals: 0,
  },
  {
    id: 'wf-004',
    name: 'Auto Engagement - LinkedIn',
    description: 'Automated engagement and networking on LinkedIn',
    platform: 'LinkedIn',
    status: 'draft',
    lastRun: null,
    nextRun: null,
    triggers: ['Manual'],
    actions: ['Like', 'Comment', 'Connect'],
    approvals: 0,
    pendingApprovals: 0,
  },
];

export default function WorkflowBuilderPage() {
  const [workflowsList, setWorkflowsList] = useState<Workflow[]>(workflows);
  const [selectedWorkflow, setSelectedWorkflow] = useState<string | null>(null);
  const [showNewWorkflow, setShowNewWorkflow] = useState(false);

  const getStatusColor = (status: Workflow['status']) => {
    switch (status) {
      case 'active':
        return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'inactive':
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
      case 'draft':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
    }
  };

  const handleCreateWorkflow = () => {
    setShowNewWorkflow(true);
  };

  return (
    <div className='space-y-6'>
      <div className='flex justify-between items-center'>
        <div>
          <h1 className='text-2xl font-bold'>Workflow Builder</h1>
          <p className='text-gray-400'>Create and manage your automation workflows</p>
        </div>
        <Button onClick={handleCreateWorkflow} variant='primary'>
          <Plus className='w-4 h-4 mr-2' /> New Workflow
        </Button>
      </div>

      <Tabs defaultValue='workflows' className='space-y-4'>
        <TabsList>
          <TabsTrigger value='workflows'>Workflows</TabsTrigger>
          <TabsTrigger value='templates'>Templates</TabsTrigger>
          <TabsTrigger value='analytics'>Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value='workflows'>
          {showNewWorkflow ? (
            <Card className='border-dashed border-purple-500/50 bg-purple-500/10'>
              <CardContent className='p-8 text-center'>
                <div className='w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4'>
                  <Plus className='w-8 h-8 text-purple-400' />
                </div>
                <h3 className='text-lg font-medium mb-2'>Create New Workflow</h3>
                <p className='text-gray-500 mb-4'>Set up your automated workflow with triggers, actions, and approvals</p>
                <div className='space-y-4 text-left max-w-md mx-auto'>
                  <div>
                    <Label>Workflow Name</Label>
                    <Input placeholder='Enter workflow name' className='mt-1' />
                  </div>
                  <div>
                    <Label>Description</Label>
                    <Input placeholder='Enter description' className='mt-1' />
                  </div>
                  <div>
                    <Label>Platform</Label>
                    <Select>
                      <SelectTrigger className='mt-1'>
                        <SelectValue placeholder='Select platform' />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value='instagram'>Instagram</SelectItem>
                        <SelectItem value='tiktok'>TikTok</SelectItem>
                        <SelectItem value='linkedin'>LinkedIn</SelectItem>
                        <SelectItem value='twitter'>Twitter</SelectItem>
                        <SelectItem value='facebook'>Facebook</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Trigger</Label>
                    <Select>
                      <SelectTrigger className='mt-1'>
                        <SelectValue placeholder='Select trigger' />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value='schedule'>Schedule</SelectItem>
                        <SelectItem value='manual'>Manual</SelectItem>
                        <SelectItem value='keyword'>Keyword Alert</SelectItem>
                        <SelectItem value='upload'>Video Upload</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <div className='flex gap-2 mt-6 justify-center'>
                  <Button variant='secondary' onClick={() => setShowNewWorkflow(false)}>Cancel</Button>
                  <Button variant='primary'>Create Workflow</Button>
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
              {workflowsList.map((workflow) => (
                <Card key={workflow.id} className='hover:border-purple-500/50 transition-all cursor-pointer' onClick={() => setSelectedWorkflow(workflow.id)}>
                  <CardHeader>
                    <div className='flex items-start justify-between'>
                      <div className='flex-1'>
                        <CardTitle className='text-lg'>{workflow.name}</CardTitle>
                        <CardDescription className='mt-1'>{workflow.description}</CardDescription>
                      </div>
                      <Badge className={getStatusColor(workflow.status)}>{workflow.status}</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className='space-y-3'>
                      <div className='flex items-center justify-between text-sm'>
                        <span className='text-gray-400'>Platform</span>
                        <span className='font-medium'>{workflow.platform}</span>
                      </div>
                      <div className='flex items-center justify-between text-sm'>
                        <span className='text-gray-400'>Status</span>
                        <div className='flex items-center gap-1'>
                          <CheckCircle className='w-3 h-3 text-green-400' /> {workflow.lastRun}
                        </div>
                      </div>
                      <div className='flex items-center justify-between text-sm'>
                        <span className='text-gray-400'>Approvals</span>
                        <span className='font-medium'>{workflow.pendingApprovals}/{workflow.approvals}</span>
                      </div>
                      <div className='flex items-center justify-between text-sm'>
                        <span className='text-gray-400'>Triggers</span>
                        <div className='flex gap-1'>
                          {workflow.triggers.map((trigger, idx) => (
                            <Badge key={idx} variant='secondary' className='text-xs'>{trigger}</Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                    <div className='mt-4 pt-4 border-t border-[#1A2230] flex gap-2'>
                      <Button variant='secondary' size='sm' className='flex-1'>Edit</Button>
                      <Button variant='outline' size='sm' className='flex-1'>View</Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value='templates'>
          <Card>
            <CardHeader>
              <CardTitle>Templates</CardTitle>
              <CardDescription>Start with pre-built workflow templates</CardDescription>
            </CardHeader>
            <CardContent>
              <div className='text-center py-20'>
                <p className='text-gray-500'>Templates library coming soon...</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value='analytics'>
          <Card>
            <CardHeader>
              <CardTitle>Workflow Analytics</CardTitle>
              <CardDescription>Performance metrics and insights</CardDescription>
            </CardHeader>
            <CardContent>
              <div className='text-center py-20'>
                <p className='text-gray-500'>Analytics dashboard coming soon...</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {selectedWorkflow && (
        <Card className='fixed bottom-0 left-0 right-0 rounded-none border-t border-[#1A2230] z-40'>
          <CardContent className='p-4'>
            <div className='flex items-center justify-between'>
              <div className='flex items-center gap-4'>
                <div className='w-2 h-2 bg-green-400 rounded-full animate-pulse' />
                <span className='text-sm font-medium'>Workflow Selected: {selectedWorkflow}</span>
              </div>
              <div className='flex gap-2'>
                <Button variant='outline' size='sm'>Configure</Button>
                <Button variant='outline' size='sm'>Test Run</Button>
                <Button variant='secondary' size='sm'>Export</Button>
                <Button variant='primary' size='sm'>Deploy</Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
