import React from 'react';
import { usePathname } from 'next/navigation';
import {
  Layout,
  Users,
  FileText,
  Calendar,
  TrendingUp,
  BarChart2,
  Cpu,
  Bot,
  Search,
  Settings,
  HelpCircle,
  X,
} from 'lucide-react';

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
  badge?: string;
  badgeColor?: 'blue' | 'green' | 'yellow' | 'red' | 'purple';
}

interface LeftSidebarProps {
  open: boolean;
  onClose: () => void;
}

const navItems: NavItem[] = [
  { label: 'Dashboard', href: '/dashboard', icon: <Layout className='w-5 h-5' /> },
  { label: 'Workspace', href: '/workspace', icon: <Users className='w-5 h-5' /> },
  { label: 'Content Studio', href: '/content-studio', icon: <FileText className='w-5 h-5' /> },
  { label: 'Publishing', href: '/publishing', icon: <Calendar className='w-5 h-5' />, badge: '12', badgeColor: 'blue' },
  { label: 'Automation', href: '/automation', icon: <Cpu className='w-5 h-5' />, badge: '3', badgeColor: 'red' },
  { label: 'Research Center', href: '/research', icon: <Search className='w-5 h-5' /> },
  { label: 'Trend Intelligence', href: '/trends', icon: <TrendingUp className='w-5 h-5' />, badge: 'Live', badgeColor: 'green' },
  { label: 'Accounts', href: '/accounts', icon: <Users className='w-5 h-5' /> },
  { label: 'Analytics', href: '/analytics', icon: <BarChart2 className='w-5 h-5' /> },
  { label: 'AI Center', href: '/ai-center', icon: <Bot className='w-5 h-5' /> },
  { label: 'Team', href: '/team', icon: <Users className='w-5 h-5' /> },
  { label: 'Settings', href: '/settings', icon: <Settings className='w-5 h-5' /> },
];

export default function LeftSidebar({ open, onClose }: LeftSidebarProps) {
  const pathname = usePathname();

  return (
    <aside
      className={`fixed left-0 top-16 h-[calc(100vh-64px)] w-64 bg-[#121822] border-r border-[#1A2230] transform transition-transform duration-300 ease-in-out z-40 ${open ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'} lg:static lg:translate-x-0`}
    >
      <div className='h-full overflow-y-auto p-4'>
        <div className='space-y-1'>
          {navItems.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(item.href + '/');

            return (
              <a
                key={item.href}
                href={item.href}
                className={`flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 group ${isActive ? 'bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-white border border-purple-500/30' : 'text-gray-400 hover:text-white hover:bg-[#1A2230]'}`}
              >
                <div className='flex items-center gap-3'>
                  <div className={`${isActive ? 'text-purple-400' : 'text-gray-500 group-hover:text-gray-300'}`}>{item.icon}</div>
                  <span className='whitespace-nowrap'>{item.label}</span>
                </div>

                {item.badge && (
                  <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${item.badgeColor === 'blue' ? 'bg-blue-500/20 text-blue-400' : item.badgeColor === 'green' ? 'bg-green-500/20 text-green-400' : item.badgeColor === 'red' ? 'bg-red-500/20 text-red-400' : item.badgeColor === 'yellow' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-purple-500/20 text-purple-400'}`}>{
                    item.badge}
                  </span>
                )}
              </a>
            );
          })}
        </div>

        <div className='mt-8 pt-4 border-t border-[#1A2230]'>
          <div className='px-3 mb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider'>Workspace</div>
          <div className='flex items-center gap-3 px-3 py-2 rounded-lg bg-[#0B0F14] border border-purple-500/30'>
            <div className='w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center'>
              <span className='text-white font-semibold text-sm'>SF</span>
            </div>
            <div>
              <div className='text-sm font-medium text-white'>Social Farm AI</div>
              <div className='text-xs text-gray-500'>Enterprise Plan</div>
            </div>
          </div>
        </div>

        <div className='mt-auto pt-4'>
          <button className='w-full flex items-center gap-3 px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-[#1A2230] transition-colors'>
            <HelpCircle className='w-5 h-5' /> <span>Help & Support</span>
          </button>
        </div>
      </div>

      {/* Mobile close button */}
      <button
        onClick={onClose}
        className='absolute -right-12 top-4 bg-[#0B0F14] border border-[#1A2230] rounded-r-lg p-2 text-gray-400 hover:text-white lg:hidden'
      >
        <X className='w-4 h-4' />
      </button>
    </aside>
  );
}
