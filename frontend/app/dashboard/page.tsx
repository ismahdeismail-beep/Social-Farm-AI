'use client';
import React from 'react';
import { useState } from 'react';
import { Calendar, Clock, CheckCircle, TrendingUp, Users, FileText, Hash, Target, BarChart2 } from 'lucide-react';

export default function DashboardPage() {
  const [date, setDate] = useState(new Date());

  const stats = [
    { label: 'Connected Accounts', value: '12', change: '+2', color: 'blue', icon: Users },
    { label: 'Scheduled Posts', value: '48', change: '+6', color: 'purple', icon: FileText },
    { label: 'Published Today', value: '8', change: '+3', color: 'green', icon: CheckCircle },
    { label: 'AI Tasks', value: '15', change: '+4', color: 'yellow', icon: FileText },
    { label: 'Active Automations', value: '5', change: '0', color: 'red', icon: Target },
    { label: 'Trending Topics', value: '24', change: '+8', color: 'indigo', icon: TrendingUp },
    { label: 'Engagement Score', value: '87%', change: '+5%', color: 'pink', icon: BarChart2 },
    { label: 'Followers Growth', value: '+1.2K', change: '+12%', color: 'teal', icon: Users },
  ];

  const getColorClass = (color: string) => {
    const colors: Record<string, string> = {
      blue: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
      purple: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
      green: 'bg-green-500/20 text-green-400 border-green-500/30',
      yellow: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
      red: 'bg-red-500/20 text-red-400 border-red-500/30',
      indigo: 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30',
      pink: 'bg-pink-500/20 text-pink-400 border-pink-500/30',
      teal: 'bg-teal-500/20 text-teal-400 border-teal-500/30',
    };
    return colors[color];
  };

  return (
    <div className='space-y-8'>
      {/* Welcome Section */}
      <div>
        <h1 className='text-3xl font-bold mb-2'>Dashboard</h1>
        <p className='text-gray-400'>Your social media intelligence hub</p>
      </div>

      {/* Overview Cards */}
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6'>
        {stats.map((stat, index) => (
          <div key={index} className='bg-[#121822] rounded-xl border border-[#1A2230] p-6 hover:shadow-lg transition-shadow'>
            <div className='flex items-start justify-between mb-4'>
              <div className={`p-3 rounded-lg ${getColorClass(stat.color)}`}>{
                React.createElement(stat.icon, { className: 'w-5 h-5' })
              }</div>
              <span className={`text-sm font-medium ${stat.change.startsWith('+') ? 'text-green-400' : 'text-red-400'}`}>{
                stat.change}
              </span>
            </div>
            <h3 className='text-sm font-medium text-gray-400 mb-1'>{stat.label}</h3>
            <p className='text-2xl font-bold'>{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className='grid grid-cols-1 lg:grid-cols-3 gap-8'>
        {/* Calendar Section */}
        <div className='lg:col-span-1'>
          <div className='bg-[#121822] rounded-xl border border-[#1A2230] p-6'>
            <div className='flex items-center justify-between mb-4'>
              <h2 className='text-lg font-semibold'>Publishing Calendar</h2>
              <Calendar className='w-5 h-5 text-purple-400' />
            </div>

            <div className='space-y-3'>
              {Array.from({ length: 7 }).map((_, i) => (
                <div key={i} className='flex items-center justify-between p-3 bg-[#1A2230] rounded-lg hover:bg-purple-500/10 cursor-pointer transition-colors'>
                  <div className='flex items-center gap-3'>
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center font-semibold ${i === 3 ? 'bg-purple-500 text-white' : 'bg-[#0B0F14] text-gray-400'}`}>{i + 1}</div>
                    <div>
                      <p className={`text-sm font-medium ${i === 3 ? 'text-purple-400' : 'text-gray-300'}`}>{['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i]}</p>
                      <p className='text-xs text-gray-500'>{i === 3 ? '3 posts' : i === 1 ? '1 post' : '0 posts'}</p>
                    </div>
                  </div>
                  {i === 3 && (
                    <div className='flex gap-1'>
                      <div className='w-16 h-2 bg-blue-500 rounded-full' />
                      <div className='w-8 h-2 bg-purple-500 rounded-full' />
                      <div className='w-8 h-2 bg-green-500 rounded-full' />
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className='mt-6 pt-4 border-t border-[#1A2230]'>
              <button className='w-full py-2 bg-gradient-to-r from-purple-500/20 to-blue-500/20 hover:from-purple-500/30 hover:to-blue-500/30 rounded-lg text-sm font-medium transition-colors'>
                View Full Calendar
              </button>
            </div>
          </div>
        </div>

        {/* AI Suggestions Section */}
        <div className='lg:col-span-2'>
          <div className='bg-[#121822] rounded-xl border border-[#1A2230] p-6'>
            <div className='flex items-center justify-between mb-4'>
              <h2 className='text-lg font-semibold'>AI Suggestions</h2>
              <Clock className='w-5 h-5 text-blue-400' />
            </div>

            <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
              <div className='bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-lg p-4 border border-purple-500/20 hover:border-purple-500/40 cursor-pointer transition-all'>
                <div className='flex items-start gap-3'>
                  <div className='w-8 h-8 bg-purple-500/20 rounded-lg flex items-center justify-center'>{
                    React.createElement(TrendingUp, { className: 'w-4 h-4 text-purple-400' })
                  }</div>
                  <div>
                    <h3 className='font-medium mb-1'>Trending Topics</h3>
                    <p className='text-xs text-gray-400 mb-2'>6 new trending topics detected</p>
                    <div className='flex flex-wrap gap-1'>
                      {['Productivity', 'Wellness', 'AI Tools', 'Sustainability'].map((tag) => (
                        <span key={tag} className='px-2 py-0.5 bg-purple-500/20 text-purple-400 rounded-full text-xs'>{
                          tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              <div className='bg-gradient-to-r from-blue-500/10 to-teal-500/10 rounded-lg p-4 border border-blue-500/20 hover:border-blue-500/40 cursor-pointer transition-all'>
                <div className='flex items-start gap-3'>
                  <div className='w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center'>{
                    React.createElement(Clock, { className: 'w-4 h-4 text-blue-400' })
                  }</div>
                  <div>
                    <h3 className='font-medium mb-1'>Best Posting Time</h3>
                    <p className='text-xs text-gray-400 mb-2'>Tomorrow at 2:00 PM EST</p>
                    <div className='flex items-center gap-1'>
                      <Hash className='w-3 h-3 text-blue-400' />
                      <span className='text-xs text-blue-400'>#AI #Productivity</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className='bg-gradient-to-r from-green-500/10 to-emerald-500/10 rounded-lg p-4 border border-green-500/20 hover:border-green-500/40 cursor-pointer transition-all'>
                <div className='flex items-start gap-3'>
                  <div className='w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center'>{
                    React.createElement(Hash, { className: 'w-4 h-4 text-green-400' })
                  }</div>
                  <div>
                    <h3 className='font-medium mb-1'>Recommended Hashtags</h3>
                    <p className='text-xs text-gray-400 mb-2'>8 relevant hashtags for your niche</p>
                    <div className='flex flex-wrap gap-1'>
                      {['#AI', '#Tech', '#Innovation', '#Future'].map((tag) => (
                        <span key={tag} className='px-2 py-0.5 bg-green-500/20 text-green-400 rounded-full text-xs'>{
                          tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              <div className='bg-gradient-to-r from-orange-500/10 to-red-500/10 rounded-lg p-4 border border-orange-500/20 hover:border-orange-500/40 cursor-pointer transition-all'>
                <div className='flex items-start gap-3'>
                  <div className='w-8 h-8 bg-orange-500/20 rounded-lg flex items-center justify-center'>{
                    React.createElement(Target, { className: 'w-4 h-4 text-orange-400' })
                  }</div>
                  <div>
                    <h3 className='font-medium mb-1'>Content Ideas</h3>
                    <p className='text-xs text-gray-400 mb-2'>5 new content ideas suggested</p>
                    <div className="text-xs text-orange-400 font-medium">Click for details →</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Activity Section */}
          <div className='mt-8 bg-[#121822] rounded-xl border border-[#1A2230] p-6'>
            <h2 className='text-lg font-semibold mb-4'>Recent Activity</h2>

            <div className='space-y-4'>
              {Array.from({ length: 8 }).map((_, i) => (
                <div key={i} className='flex items-start gap-4'>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${i < 4 ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'}`}>{i < 4 ? '✓' : '📤'}</div>
                  <div className='flex-1'>
                    <p className='text-sm'><span className='font-medium'>{
                      ['Post scheduled', 'Content generated', 'AI analysis complete', 'Trend identified'][i % 4]
                    }}</span> for {['Instagram', 'TikTok', 'LinkedIn', 'Twitter'][i % 4]}</p>
                    <p className='text-xs text-gray-500 mt-0.5'>{
                      i === 0 ? '5 minutes ago' : i === 1 ? '15 minutes ago' : i === 2 ? '1 hour ago' : '2 hours ago'
                    }</p>
                  </div>
                  <div className={`px-2 py-1 rounded text-xs ${i % 2 === 0 ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'}`}>{i % 2 === 0 ? 'Success' : 'Scheduled'}</div>
                </div>
              ))}
            </div>

            <div className='mt-6 pt-4 border-t border-[#1A2230]'>
              <button className='w-full py-2 text-center text-sm text-purple-400 hover:text-purple-300 transition-colors'>
                View Full Activity Log
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
