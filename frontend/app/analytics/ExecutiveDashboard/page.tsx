'use client';
import React from 'react';
import { useState } from 'react';
import { Calendar, Clock, TrendingUp, Target, Hash, MessageSquare, Play, Image, Video, FileText, Users, BarChart2, Settings, Bell, Search, Plus, Filter, X, CheckCircle, AlertCircle, Clock as ClockIcon, MapPin, Calendar as CalendarIcon, TrendingUp as TrendingIcon, Users as UsersIcon, FileText as FileTextIcon, Star, Heart, Share2, MessageCircle, ThumbsUp, Eye, Bookmark, Download, Upload, Edit, Trash2, MoreVertical, Award, DollarSign, Globe, Smartphone, Monitor, Tablet } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';

export default function Dashboard() {
  const [dateFilter, setDateFilter] = useState('today');
  const [platformFilter, setPlatformFilter] = useState('all');

  const analyticsCards = [
    {
      title: 'Total Reach',
      value: '2.4M',
      change: '+12.3%',
      trend: 'up',
      icon: TrendingUp,
      color: 'blue',
      period: 'vs last week'
    },
    {
      title: 'Engagement Rate',
      value: '8.7%',
      change: '+2.1%',
      trend: 'up',
      icon: Heart,
      color: 'green',
      period: 'vs last week'
    },
    {
      title: 'Total Followers',
      value: '456K',
      change: '+5.2K',
      trend: 'up',
      icon: Users,
      color: 'purple',
      period: 'this month'
    },
    {
      title: 'Content Performance',
      value: '94.2',
      change: '+3.7%',
      trend: 'up',
      icon: FileText,
      color: 'orange',
      period: 'avg across all posts'
    },
    {
      title: 'Scheduled Posts',
      value: '48',
      change: '+8',
      trend: 'up',
      icon: Clock,
      color: 'indigo',
      period: 'this week'
    },
    {
      title: 'Automation Success',
      value: '98.5%',
      change: '+0.8%',
      trend: 'up',
      icon: Target,
      color: 'red',
      period: 'success rate'
    },
    {
      title: 'ROI Generated',
      value: '$127K',
      change: '+15.2K',
      trend: 'up',
      icon: DollarSign,
      color: 'emerald',
      period: 'quarterly'
    },
    {
      title: 'Trend Impact',
      value: '3.2x',
      change: '+0.8x',
      trend: 'up',
      icon: TrendingIcon,
      color: 'cyan',
      period: 'engagement multiplier'
    }
  ];

  const topPerformingPosts = [
    { platform: 'Instagram', content: 'How to start your morning meditation routine effectively', engagement: '12.5K', reach: '245K', posts: 3 },
    { platform: 'TikTok', content: 'Quick tutorial: Setting up automated social media posting', engagement: '8.2K', reach: '189K', posts: 5 },
    { platform: 'LinkedIn', content: 'The future of AI in content creation explained', engagement: '5.8K', reach: '156K', posts: 2 },
  ];

  const activeAutomations = [
    { name: 'Daily Morning Posts', platforms: ['Instagram', 'LinkedIn'], status: 'running', success: 98.5 },
    { name: 'Trend Response Bot', platforms: ['TikTok', 'Twitter'], status: 'running', success: 95.2 },
    { name: 'Weekly Digest', platforms: ['Facebook', 'Instagram'], status: 'paused', success: 92.8 },
  ];

  return (
    <div className='space-y-8'>
      <div className='flex justify-between items-center'>
        <div>
          <h1 className='text-3xl font-bold'>Analytics Dashboard</h1>
          <p className='text-gray-400'>Comprehensive insights into your social media performance</p>
        </div>
        <div className='flex gap-3'>
          <div className='relative'>
            <CalendarIcon className='absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500' />
            <select
              value={dateFilter}
              onChange={(e) => setDateFilter(e.target.value)}
              className='pl-10 pr-4 py-2 bg-[#121822] border border-[#1A2230] rounded-lg text-white focus:outline-none focus:border-purple-500'
            >
              <option value='today'>Today</option>
              <option value='week'>This Week</option>
              <option value='month'>This Month</option>
              <option value='quarter'>This Quarter</option>
            </select>
          </div>
          <div className='relative'>
            <Monitor className='absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500' />
            <select
              value={platformFilter}
              onChange={(e) => setPlatformFilter(e.target.value)}
              className='pl-10 pr-4 py-2 bg-[#121822] border border-[#1A2230] rounded-lg text-white focus:outline-none focus:border-purple-500'
            >
              <option value='all'>All Platforms</option>
              <option value='instagram'>Instagram</option>
              <option value='facebook'>Facebook</option>
              <option value='twitter'>Twitter/X</option>
              <option value='linkedin'>LinkedIn</option>
              <option value='tiktok'>TikTok</option>
            </select>
          </div>
          <Button variant='outline' size='sm'>
            <Filter className='w-4 h-4 mr-2' /> Filter
          </Button>
        </div>
      </div>

      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6'>
        {analyticsCards.map((card, index) => (
          <Card key={index} variant='interactive' className='hover:border-purple-500/50 transition-all'>
            <CardContent className='p-6'>
              <div className='flex items-start justify-between mb-4'>
                <div className={`p-3 rounded-lg bg-${card.color}-500/20`}>{
                  <card.icon className={`w-5 h-5 text-${card.color}-400`} />
                }</div>
                <div className={`flex items-center gap-1 text-sm font-medium ${card.trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>{
                  card.trend === 'up' ? '↗' : '↘'}{
                  card.change}
                </div>
              </div>
              <h3 className='text-sm font-medium text-gray-400 mb-1'>{card.title}</h3>
              <p className='text-2xl font-bold'>{card.value}</p>
              <p className='text-xs text-gray-500 mt-1'>{card.period}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className='grid grid-cols-1 lg:grid-cols-3 gap-6'>
        <div className='lg:col-span-2'>
          <Card>
            <CardHeader>
              <CardTitle>Top Performing Content</CardTitle>
            </CardHeader>
            <CardContent>
              <div className='space-y-4'>
                {topPerformingPosts.map((post, index) => (
                  <div key={index} className='flex items-center justify-between p-4 bg-[#1A2230] rounded-lg hover:bg-purple-500/10 cursor-pointer transition-colors'>
                    <div className='flex items-center gap-4'>
                      <div className='w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center'>{
                        <Smartphone className='w-5 h-5 text-white' />
                      }</div>
                      <div>
                        <p className='font-medium'>{post.content}</p>
                        <p className='text-sm text-gray-400'>{post.platform}</p>
                      </div>
                    </div>
                    <div className='flex items-center gap-8'>
                      <div className='text-center'>
                        <p className='text-xs text-gray-500'>Engagement</p>
                        <p className='text-sm font-medium'>{post.engagement}</p>
                      </div>
                      <div className='text-center'>
                        <p className='text-xs text-gray-500'>Reach</p>
                        <p className='text-sm font-medium'>{post.reach}</p>
                      </div>
                      <div className='text-center'>
                        <p className='text-xs text-gray-500'>Posts</p>
                        <p className='text-sm font-medium'>{post.posts}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div>
          <Card>
            <CardHeader>
              <CardTitle>Active Automations</CardTitle>
            </CardHeader>
            <CardContent>
              <div className='space-y-4'>
                {activeAutomations.map((auto, index) => (
                  <div key={index} className='p-4 bg-[#1A2230] rounded-lg'>
                    <div className='flex items-center justify-between mb-3'>
                      <h3 className='font-medium'>{auto.name}</h3>
                      <div className={`px-2 py-0.5 rounded-full text-xs font-medium ${auto.status === 'running' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'}`}>{auto.status}</div>
                    </div>
                    <div className='flex items-center gap-2 mb-3'>{
                      auto.platforms.map((platform) => (
                        <div key={platform} className='w-6 h-6 bg-gray-600 rounded-full flex items-center justify-center text-xs'>{
                          platform.charAt(0).toUpperCase()
                        }}</div>
                      ))}
                    </div>
                    <div className='flex items-center justify-between'>
                      <span className='text-sm text-gray-400'>Success Rate</span>
                      <span className={`font-medium ${auto.success >= 95 ? 'text-green-400' : auto.success >= 90 ? 'text-yellow-400' : 'text-red-400'}`}>{auto.success}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className='mt-6'>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className='space-y-3'>
              <Button variant='primary' size='sm' className='w-full justify-start'>
                <Plus className='w-4 h-4 mr-2' /> Create New Campaign
              </Button>
              <Button variant='outline' size='sm' className='w-full justify-start'>
                <TrendingIcon className='w-4 h-4 mr-2' /> Analyze Trends
              </Button>
              <Button variant='outline' size='sm' className='w-full justify-start'>
                <BarChart2 className='w-4 h-4 mr-2' /> View Reports
              </Button>
              <Button variant='outline' size='sm' className='w-full justify-start'>
                <Users className='w-4 h-4 mr-2' /> Manage Accounts
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
