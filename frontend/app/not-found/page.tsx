import React from 'react';

export default function NotFoundPage() {
  return (
    <div className='min-h-screen bg-[#0B0F14] text-white flex flex-col items-center justify-center px-4'>
      <div className='text-center max-w-md'>
        <div className='w-20 h-20 bg-[#121822] rounded-full flex items-center justify-center mx-auto mb-6 border border-purple-500/30'>
          <span className='text-4xl'>🤖</span>
        </div>
        
        <h1 className='text-4xl font-bold mb-4'>Page Not Found</h1>
        
        <p className='text-gray-400 mb-8'>The page you're looking for doesn't exist or has been moved.</p>
        
        <div className='space-y-4'>
          <a 
            href='/dashboard' 
            className='block w-full px-6 py-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg font-medium hover:from-purple-600 hover:to-blue-600 transition-colors'
          >
            Go to Dashboard
          </a>
          
          <a 
            href='/accounts' 
            className='block w-full px-6 py-3 bg-[#121822] border border-[#1A2230] rounded-lg font-medium hover:border-purple-500/30 hover:bg-[#1E2230] transition-colors'
          >
            View Connected Accounts
          </a>
        </div>
        
        <div className='mt-8 pt-8 border-t border-[#1A2230]'>
          <p className='text-sm text-gray-500 mb-2'>Need help?</p>
          <div className='flex justify-center gap-4'>
            <a href='/ai-center' className='text-purple-400 hover:text-purple-300 text-sm'>Contact AI Assistant</a>
            <a href='/team' className='text-purple-400 hover:text-purple-300 text-sm'>Visit Support</a>
          </div>
        </div>
      </div>
    </div>
  );
}
