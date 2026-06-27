import React from 'react';
import { Settings2, PanelLeft, PanelRight, Home, Menu, X, Save } from 'lucide-react';
import { Button } from './ui/Button';
import { Avatar } from './ui/Avatar';

interface AppShellProps {
  children: React.ReactNode;
}

export default function AppShell({ children }: AppShellProps) {
  const [sidebarOpen, setSidebarOpen] = React.useState(true);
  const [rightPanelOpen, setRightPanelOpen] = React.useState(true);

  return (
    <div className='min-h-screen bg-[#0B0F14] text-white overflow-hidden'>
      {/* Top Navigation */}
      <TopNavigation
        onSidebarToggle={() => setSidebarOpen(!sidebarOpen)}
        onRightPanelToggle={() => setRightPanelOpen(!rightPanelOpen)}
      />

      <div className='flex h-[calc(100vh-65px)] pt-16'>
        {/* Left Sidebar */}
        <LeftSidebar
          open={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />

        {/* Main Content */}
        <main
          className={`flex-1 overflow-auto transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-16'} ${rightPanelOpen ? 'mr-80' : 'mr-16'}`}
        >
          <div className='max-w-[1600px] mx-auto p-8'>{children}</div>
        </main>

        {/* Right Panel - AI Assistant */}
        <RightPanel
          open={rightPanelOpen}
          onClose={() => setRightPanelOpen(false)}
        />
      </div>

      {/* Notification Toast Container */}
      <ToastContainer />

      {/* Modal Container */}
      <ModalContainer />
    </div>
  );
}
