import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ModalContextType {
  isOpen: boolean;
  title?: string;
  content?: ReactNode;
  onClose: () => void;
  onOpen: (title?: string, content?: ReactNode) => void;
}

const ModalContext = createContext<ModalContextType | undefined>(undefined);

export function ModalProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState<string>();
  const [content, setContent] = useState<ReactNode>();

  const onOpen = (title?: string, content?: ReactNode) => {
    setTitle(title);
    setContent(content);
    setIsOpen(true);
  };

  const onClose = () => {
    setIsOpen(false);
    setTitle(undefined);
    setContent(undefined);
  };

  return (
    <ModalContext.Provider value={{ isOpen, title, content, onClose, onOpen }}>
      {children}
      <ModalContainer />
    </ModalContext.Provider>
  );
}

export function useModal() {
  const context = useContext(ModalContext);
  if (!context) {
    throw new Error('useModal must be used within a ModalProvider');
  }
  return context;
}

export function ModalContainer() {
  const { isOpen, title, content, onClose } = useModal();

  if (!isOpen) return null;

  return (
    <div className='fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm'>
      <div
        className='w-full max-w-2xl bg-[#121822] border border-[#1A2230] rounded-xl shadow-xl animate-scale-in'
        onClick={(e) => e.stopPropagation()}
      >
        {title && (
          <div className='flex items-center justify-between p-6 border-b border-[#1A2230]'>
            <h2 className='text-xl font-semibold'>{title}</h2>
            <button onClick={onClose} className='p-1 rounded-lg text-gray-400 hover:text-white hover:bg-[#1A2230]'>
              <X className='w-5 h-5' />
            </button>
          </div>
        )}
        <div className='p-6'>{content}</div>
      </div>
    </div>
  );
}
