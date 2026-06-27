import React from 'react';
import { Avatar } from '../ui/Avatar';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import { Bell, Search, Plus, Command, X, Settings, User, LogOut, MessageSquare } from 'lucide-react';

interface TopNavigationProps {
  onSidebarToggle: () => void;
  onRightPanelToggle: () => void;
}

export default function TopNavigation({
  onSidebarToggle,
  onRightPanelToggle,
}: TopNavigationProps) {
  const [searchValue, setSearchValue] = React.useState('');
  const [notifications, setNotifications] = React.useState(5);

  return (
    <header className='fixed top-0 left-0 right-0 z-50 h-16 bg-[#0B0F14]/80 backdrop-blur-md border-b border-[#1A2230]'>
      <div className='flex items-center justify-between h-full px-6'>
        {/* Left Section */}
        <div className='flex items-center gap-4'>
          <Button variant='ghost' size='sm' onClick={onSidebarToggle} className='text-gray-400 hover:text-white'>
            <Menu className='w-5 h-5' />
          </Button>

          <div className='hidden lg:block'>
            <h1 className='text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent'>
              Social Farm AI OS
            </h1>
            <p className='text-xs text-gray-500'>Enterprise Social Media Management</p>
          </div>
        </div>

        {/* Center - Global Search */}
        <div className='flex-1 max-w-2xl mx-8'>
          <div className='relative'>
            <Search className='absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500' />
            <Input
              placeholder='Search posts, topics, accounts, analytics...'
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              className='pl-10 pr-10 bg-[#121822] border-[#1A2230] text-white placeholder-gray-500 focus:border-purple-500/50'
            />
            {searchValue && (
              <button
                onClick={() => setSearchValue('')}
                className='absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-white'
              >
                <X className='w-4 h-4' />
              </button>
            )}
            <button className='absolute right-12 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-purple-400'>
              <Command className='w-4 h-4' />
            </button>
          </div>
        </div>

        {/* Right Section */}
        <div className='flex items-center gap-4'>
          <Button variant='ghost' size='sm' className='text-gray-400 hover:text-white relative'>
            <Plus className='w-5 h-5' />
          </Button>

          <Button variant='ghost' size='sm' className='text-gray-400 hover:text-white relative'>
            <Bell className='w-5 h-5' />
            {notifications > 0 && (
              <span className='absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-xs flex items-center justify-center'>
                {notifications}
              </span>
            )}
          </Button>

          <Button variant='ghost' size='sm' onClick={onRightPanelToggle} className='text-gray-400 hover:text-white'>
            <MessageSquare className='w-5 h-5' />
          </Button>

          <div className='relative group'>
            <button className='flex items-center gap-2 p-1 rounded-lg hover:bg-[#1A2230] transition-colors'>
              <Avatar fallback='JD' size='sm' />
              <span className='hidden md:block text-sm font-medium'>John Doe</span>
            </button>

            <div className='absolute right-0 mt-2 w-48 bg-[#121822] border border-[#1A2230] rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50'>
              <div className='p-2'>
                <button className='w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-[#1A2230] hover:text-white rounded'>
                  <User className='w-4 h-4 inline mr-2' /> Profile
                </button>
                <button className='w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-[#1A2230] hover:text-white rounded'>
                  <Settings className='w-4 h-4 inline mr-2' /> Settings
                </button>
                <hr className='border-[#1A2230] my-2' />
                <button className='w-full text-left px-3 py-2 text-sm text-red-400 hover:bg-[#1A2230] rounded'>
                  <LogOut className='w-4 h-4 inline mr-2' /> Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
