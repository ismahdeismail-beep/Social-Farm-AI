import React from 'react';

interface RightPanelProps {
  open: boolean;
  onClose: () => void;
}

export default function RightPanel({ open, onClose }: RightPanelProps) {
  return (
    <aside
      className={`fixed right-0 top-16 h-[calc(100vh-64px)] w-80 bg-[#121822] border-l border-[#1A2230] transform transition-transform duration-300 ease-in-out z-40 ${open ? 'translate-x-0' : 'translate-x-full'}`}
    >
      <div className='p-4 border-b border-[#1A2230] flex items-center justify-between'>
        <h2 className='text-lg font-semibold'>AI Assistant</h2>
        <button
          onClick={onClose}
          className='p-1 text-gray-400 hover:text-white rounded-lg hover:bg-[#1A2230]'
        >
          <X className='w-5 h-5' />
        </button>
      </div>

      <div className='p-4 h-full overflow-y-auto'>
        <div className='bg-gradient-to-r from-purple-500/20 to-blue-500/20 rounded-lg p-4 mb-6'>
          <h3 className='font-semibold mb-2'>Quick Suggestions</h3>
          <div className='space-y-2 text-sm text-gray-300'>
            <p>• "Create an engaging post about weekly productivity tips"</p>
            <p>• "Analyze current trends for content planning"</p>
            <p>• "Schedule posts for tomorrow"</p>
            <p>• "Check automation performance"</p>
          </div>
        </div>

        <div className='mb-6'>
          <h3 className='font-semibold mb-3'>Recent AI Actions</h3>
          <div className='space-y-3'>
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className='flex items-center gap-3 p-3 bg-[#1A2230] rounded-lg'>
                <div className='w-2 h-2 bg-green-500 rounded-full' />
                <div>
                  <p className='text-sm font-medium'>Content generated</p>
                  <p className='text-xs text-gray-500'>2 minutes ago</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className='mb-6'>
          <h3 className='font-semibold mb-3'>Task Queue</h3>
          <div className='space-y-2 text-sm'>
            <div className='p-3 bg-yellow-500/20 border border-yellow-500/30 rounded-lg'>
              <p className='text-yellow-400 font-medium'>Pending Approval</p>
              <p className='text-gray-300'>3 posts awaiting approval</p>
            </div>
            <div className='p-3 bg-blue-500/20 border border-blue-500/30 rounded-lg'>
              <p className='text-blue-400 font-medium'>Scheduled</p>
              <p className='text-gray-300'>8 posts queued for tomorrow</p>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
