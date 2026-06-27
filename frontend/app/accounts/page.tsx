import React from 'react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { Search, Phone, MessageSquare, Play, Mail, FileText, Image, Video, ExternalLink } from 'lucide-react';

const platforms = [
  {
    title: 'Facebook',
    icon: Phone,
    color: 'bg-blue-500',
    connection: 'Connected',
    health: 'healthy',
    followers: '12,5K',
    postingFreq: 'Daily',
    automationEnabled: true,
  },
  {
    title: 'Instagram',
    icon: MessageSquare,
    color: 'bg-pink-500',
    connection: 'Connected',
    health: 'healthy',
    followers: '45,2K',
    postingFreq: '3x/week',
    automationEnabled: false,
  },
  {
    title: 'TikTok',
    icon: Play,
    color: 'bg-black',
    connection: 'Connected',
    health: 'degraded',
    followers: '78,9K',
    postingFreq: '5x/day',
    automationEnabled: true,
  },
  {
    title: 'Threads',
    icon: MessageSquare,
    color: 'bg-gray-800',
    connection: 'Not Connected',
    health: 'disconnected',
    followers: '0',
    postingFreq: 'N/A',
    automationEnabled: false,
  },
  {
    title: 'LinkedIn',
    icon: Mail,
    color: 'bg-blue-700',
    connection: 'Connected',
    health: 'healthy',
    followers: '8,4K',
    postingFreq: 'Weekly',
    automationEnabled: false,
  },
  {
    title: 'X (Twitter)',
    icon: FileText,
    color: 'bg-gray-900',
    connection: 'Connected',
    health: 'healthy',
    followers: '23,1K',
    postingFreq: '2x/day',
    automationEnabled: true,
  },
  {
    title: 'Pinterest',
    icon: Image,
    color: 'bg-red-500',
    connection: 'Connected',
    health: 'healthy',
    followers: '3,2K',
    postingFreq: 'Bi-weekly',
    automationEnabled: false,
  },
  {
    title: 'YouTube',
    icon: Video,
    color: 'bg-red-600',
    connection: 'Connected',
    health: 'healthy',
    followers: '156K',
    postingFreq: 'Weekly',
    automationEnabled: false,
  },
];

export default function AccountsPage() {
  const [searchQuery, setSearchQuery] = React.useState('');
  const [filterPlatform, setFilterPlatform] = React.useState('all');

  const filteredAccounts = platforms.filter((platform) => {
    const matchesSearch = platform.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterPlatform === 'all' || (filterPlatform === 'connected' ? platform.connection.includes('Connected') : platform.connection === 'Not Connected');
    return matchesSearch && matchesFilter;
  });

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div className='flex flex-col md:flex-row md:items-center md:justify-between gap-4'>
        <div>
          <h1 className='text-2xl font-bold'>Accounts</h1>
          <p className='text-gray-400'>Manage your connected social media accounts</p>
        </div>
        <Button variant='primary'>+ Connect Account</Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className='p-4'>
          <div className='flex flex-col md:flex-row gap-4'>
            <div className='flex-1'>
              <Input
                placeholder='Search platforms...'
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                leftIcon={<Search className='w-4 h-4' />}
              />
            </div>
            <div className='flex gap-2'>
              {['all', 'connected', 'not-connected'].map((filter) => (
                <Button
                  key={filter}
                  variant={filterPlatform === filter ? 'primary' : 'secondary'}
                  size='sm'
                  onClick={() => setFilterPlatform(filter)}
                >
                  {filter === 'all' && 'All Platforms'}
                  {filter === 'connected' && 'Connected'}
                  {filter === 'not-connected' && 'Not Connected'}
                </Button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Accounts Grid */}
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'>
        {filteredAccounts.map((platform, index) => (
          <Card key={index} variant='interactive' className='hover:border-purple-500/50 transition-all'>
            <CardContent className='p-6'>
              <div className='flex items-start justify-between mb-4'>
                <div
                  className={`w-12 h-12 ${platform.color} rounded-lg flex items-center justify-center text-white`}
                >
                  {React.createElement(platform.icon, { className: 'w-6 h-6' })}
                </div>
                <StatusBadge status={platform.health as any} label={platform.connection} />
              </div>

              <h3 className='font-semibold text-lg mb-2'>{platform.title}</h3>

              <div className='space-y-3 mt-4'>
                <div className='flex items-center justify-between'>
                  <span className='text-sm text-gray-500'>Followers</span>
                  <span className='font-medium'>{platform.followers}</span>
                </div>
                <div className='flex items-center justify-between'>
                  <span className='text-sm text-gray-500'>Posting Frequency</span>
                  <span className='font-medium text-sm'>{platform.postingFreq}</span>
                </div>
                <div className='flex items-center justify-between'>
                  <span className='text-sm text-gray-500'>Automation</span>
                  <span className={`text-xs px-2 py-1 rounded-full ${platform.automationEnabled ? 'bg-green-500/20 text-green-400' : 'bg-gray-500/20 text-gray-400'}`}>{platform.automationEnabled ? 'Enabled' : 'Disabled'}</span>
                </div>
              </div>

              <div className='mt-6 pt-4 border-t border-[#1A2230]'>
                <div className='grid grid-cols-2 gap-2'> {/* <a href="#" className="text-sm text-purple-400 hover:text-purple-300 flex items-center gap-1">View Analytics <ExternalLink className="w-3 h-3" /></a> */}
                  <button className='text-sm text-purple-400 hover:text-purple-300 flex items-center gap-1 justify-center'>
                    <ExternalLink className='w-3 h-3' /> Analytics
                  </button>
                  <button className='text-sm text-gray-400 hover:text-white flex items-center gap-1 justify-center'>
                    <FileText className='w-3 h-3' /> Details
                  </button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredAccounts.length === 0 && (
        <Card className='p-12 text-center'>
          <div className='text-gray-500 mb-2'>No accounts found</div>
          <p className='text-gray-400 text-sm'>Try adjusting your search or filters</p>
        </Card>
      )}
    </div>
  );
}
