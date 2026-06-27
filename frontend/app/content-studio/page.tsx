import React from 'react';
import { useState, useEffect } from 'react';
import { FileText, Wand2, Hash, Edit3, Plus, Search, Filter, Grid, List, Save, Copy, Send, Clock, Sparkles, Type, Users, Globe, Archive, Tag, Calendar, BookOpen, Clock3, Layers, Trash2, Download, Upload, FileCheck, History, ChevronRight, Home, FolderOpen, PlusCircle, Filter as FilterIcon, Grid3x3, ListFilter, Star, StarOff, Lock, Unlock, Users2, Building2, Shield, Settings, Bell, Menu, X, Home as HomeIcon, TrendingUp, BarChart2, Target, Hash as HashIcon, Instagram, Youtube, Twitter, Facebook, Linkedin, FileAudio, Video, Image } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/DropdownMenu';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/Dialog';
import { Select, SelectContent, SelectItem, SelectLabel, SelectSeparator, SelectTrigger, SelectValue } from '@/components/ui/Select';
import { Switch } from '@/components/ui/Switch';
import { Label } from '@/components/ui/Label';
import { Textarea } from '@/components/ui/Textarea';
import { Progress } from '@/components/ui/Progress';
import { ScrollArea } from '@/components/ui/ScrollArea';

interface Draft {
  id: string;
  title: string;
  content: string;
  platform: string;
  status: 'draft' | 'scheduled' | 'published' | 'archived';
  lastModified: string;
  createdAt: string;
  tags: string[];
  folder: string;
  isStarred: boolean;
  wordCount: number;
  aiScore: number;
  author: string;
}

interface Folder {
  id: string;
  name: string;
  path: string;
  parentId?: string;
  itemCount: number;
  icon?: string;
}

interface AIWriterProps {
  prompt: string;
  setPrompt: (value: string) => void;
  tone: string;
  setTone: (value: string) => void;
  audience: string;
  setAudience: (value: string) => void;
  platform: string;
  setPlatform: (value: string) => void;
  length: string;
  setLength: (value: string) => void;
  language: string;
  setLanguage: (value: string) => void;
  brandVoice: string;
  setBrandVoice: (value: string) => void;
  generatedContent: string;
  setGeneratedContent: (value: string) => void;
  isGenerating: boolean;
  setIsGenerating: (value: boolean) => void;
}

interface Hook {
  id: string;
  title: string;
  hook: string;
  category: string;
  viralityScore: number;
  aiScore: number;
  brandScore: number;
  trendScore: number;
  isFavorite: boolean;
  isDuplicate: boolean;
  platform: string;
}

interface CaptionProps {
  platform: string;
  hook: string;
  setHook: (value: string) => void;
  cta: string;
  setCta: (value: string) => void;
  emoji: boolean;
  setEmoji: (value: boolean) => void;
  hashtags: string[];
  setHashtags: (value: string[]) => void;
  aiRewrite: () => void;
}

const tones = ['professional', 'casual', 'enthusiastic', 'formal', 'friendly', 'humorous', 'urgent', 'storytelling'];
const audiences = ['general', 'tech-savvy', 'millennials', 'gen-z', 'business', 'creative', 'financial', 'educational'];
const platforms = ['instagram', 'facebook', 'twitter', 'linkedin', 'tiktok', 'youtube', 'threads'];
const lengths = ['short', 'medium', 'long', 'detailed'];
const languages = ['en', 'es', 'fr', 'de', 'pt', 'ja', 'ko', 'zh'];
const brandVoices = ['default', 'aggressive', 'conservative', 'humorous', 'professional', 'casual', 'authoritative', 'playful'];

export default function ContentStudioPage() {
  const [activeTab, setActiveTab] = useState('ai-writer');
  const [folders, setFolders] = useState<Folder[]>([
    { id: '1', name: 'Social Posts', path: '/social-posts', itemCount: 12 },
    { id: '2', name: 'Blog Posts', path: '/blog-posts', itemCount: 8 },
    { id: '3', name: 'Video Scripts', path: '/video-scripts', itemCount: 5 },
    { id: '4', name: 'Campaigns', path: '/campaigns', itemCount: 3 },
  ]);

  return (
    <div className='space-y-6'>
      <div className='flex justify-between items-center'>
        <div>
          <h1 className='text-2xl font-bold'>Content Studio</h1>
          <p className='text-gray-400'>AI-powered content creation workspace</p>
        </div>
        <div className='flex gap-2'> 
          <Button variant='outline' size='sm'>
            <Save className='w-4 h-4 mr-2' /> Save Draft
          </Button>
          <Button variant='primary' size='sm'>
            <Plus className='w-4 h-4 mr-2' /> New Project
          </Button>
        </div>
      </div>

      <div className='grid grid-cols-12 gap-6'>
        <div className='col-span-3'>
          <Card>
            <CardHeader>
              <CardTitle>Tools</CardTitle>
            </CardHeader>
            <CardContent className='p-2'>
              <nav className='space-y-1'>
                <button
                  onClick={() => setActiveTab('ai-writer')}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'ai-writer' ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'text-gray-400 hover:text-white hover:bg-[#1A2230]'}`}
                >
                  <Wand2 className='w-4 h-4' /> AI Writer
                </button>
                <button
                  onClick={() => setActiveTab('hook-generator')}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'hook-generator' ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'text-gray-400 hover:text-white hover:bg-[#1A2230]'}`}
                >
                  <Hash className='w-4 h-4' /> Hook Generator
                </button>
                <button
                  onClick={() => setActiveTab('caption-generator')}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'caption-generator' ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'text-gray-400 hover:text-white hover:bg-[#1A2230]'}`}
                >
                  <FileText className='w-4 h-4' /> Caption Generator
                </button>
                <button
                  onClick={() => setActiveTab('script-writer')}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'script-writer' ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'text-gray-400 hover:text-white hover:bg-[#1A2230]'}`}
                >
                  <Edit3 className='w-4 h-4' /> Script Writer
                </button>
                <button
                  onClick={() => setActiveTab('draft-library')}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'draft-library' ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'text-gray-400 hover:text-white hover:bg-[#1A2230]'}`}
                >
                  <Grid className='w-4 h-4' /> Draft Library
                </button>
              </nav>
            </CardContent>
          </Card>

          <Card className='mt-4'>
            <CardHeader>
              <CardTitle>Folders</CardTitle>
            </CardHeader>
            <CardContent className='p-2'>
              <div className='space-y-1'>
                {folders.map((folder) => (
                  <button
                    key={folder.id}
                    className='w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors text-gray-400 hover:text-white hover:bg-[#1A2230]'
                  >
                    <FolderOpen className='w-4 h-4' /> {folder.name}
                  </button>
                ))}
                <button className='w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors text-gray-400 hover:text-white hover:bg-[#1A2230]'>
                  <PlusCircle className='w-4 h-4' /> New Folder
                </button>
              </div>
            </CardContent>
          </Card>

          <Card className='mt-4'>
            <CardHeader>
              <CardTitle>Quick Stats</CardTitle>
            </CardHeader>
            <CardContent>
              <div className='space-y-3'>
                <div className='flex justify-between'>
                  <span className='text-sm text-gray-500'>Characters Written</span>
                  <span className='font-medium'>12.5K</span>
                </div>
                <div className='flex justify-between'>
                  <span className='text-sm text-gray-500'>Drafts Saved</span>
                  <span className='font-medium'>48</span>
                </div>
                <div className='flex justify-between'>
                  <span className='text-sm text-gray-500'>AI Generations</span>
                  <span className='font-medium'>156</span>
                </div>
                <div className='flex justify-between'>
                  <span className='text-sm text-gray-500'>Published Posts</span>
                  <span className='font-medium'>23</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className='col-span-9'>
          {activeTab === 'ai-writer' && <AIWriterTab />}
          {activeTab === 'hook-generator' && <HookGeneratorTab />}
          {activeTab === 'caption-generator' && <CaptionGeneratorTab />}
          {activeTab === 'script-writer' && <ScriptWriterTab />}
          {activeTab === 'draft-library' && <DraftLibraryTab />}
        </div>
      </div>
    </div>
  );
}

function AIWriterTab() {
  const [prompt, setPrompt] = useState('');
  const [tone, setTone] = useState('professional');
  const [audience, setAudience] = useState('general');
  const [platform, setPlatform] = useState('instagram');
  const [length, setLength] = useState('medium');
  const [language, setLanguage] = useState('en');
  const [brandVoice, setBrandVoice] = useState('default');
  const [generatedContent, setGeneratedContent] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const generateContent = async () => {
    setIsGenerating(true);
    setTimeout(() => {
      setGeneratedContent(`Hey everyone! 👋 Welcome to our latest update where we're exploring the intersection of AI and creative content creation. In this post, we'll dive deep into how artificial intelligence is revolutionizing the way we craft stories, generate ideas, and engage audiences across all social platforms. Whether you're a content creator, marketer, or just curious about the future of digital content, this is something you won't want to miss!

Throughout this journey, we'll cover:
• The evolution of AI-powered writing tools
• Best practices for human-AI collaboration
• Real-world examples of viral content creation
• Tips and tricks to optimize your content strategy

Stay tuned for actionable insights and practical demonstrations that will help you level up your content game. Let's create something amazing together! ✨🎯\n\n#AI #ContentCreation #DigitalMarketing #Innovation #FutureOfWork`);
      setIsGenerating(false);
    }, 2000);
  };

  return (
    <div className='grid grid-cols-12 gap-6'>
      <div className='col-span-4'>
        <Card>
          <CardHeader>
            <CardTitle>Content Settings</CardTitle>
          </CardHeader>
          <CardContent className='space-y-4'>
            <div>
              <label className='block text-sm font-medium text-gray-300 mb-2'>Prompt</label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder='Enter your content prompt...'
                rows={4}
                className='w-full px-3 py-2 bg-[#0B0F14] border border-[#1A2230] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 resize-none'
              />
            </div>

            <div>
              <label className='block text-sm font-medium text-gray-300 mb-2'>Tone</label>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className='w-full px-3 py-2 bg-[#0B0F14] border border-[#1A2230] rounded-lg text-white focus:outline-none focus:border-purple-500'
              >
                {tones.map((t) => (
                  <option key={t} value={t} className='bg-[#0B0F14]'>
                    {t.charAt(0).toUpperCase() + t.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className='block text-sm font-medium text-gray-300 mb-2'>Audience</label>
              <select
                value={audience}
                onChange={(e) => setAudience(e.target.value)}
                className='w-full px-3 py-2 bg-[#0B0F14] border border-[#1A2230] rounded-lg text-white focus:outline-none focus:border-purple-500'
              >
                {audiences.map((a) => (
                  <option key={a} value={a} className='bg-[#0B0F14]'>
                    {a.charAt(0).toUpperCase() + a.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className='block text-sm font-medium text-gray-300 mb-2'>Platform</label>
              <select
                value={platform}
                onChange={(e) => setPlatform(e.target.value)}
                className='w-full px-3 py-2 bg-[#0B0F14] border border-[#1A2230] rounded-lg text-white focus:outline-none focus:border-purple-500'
              >
                {platforms.map((p) => (
                  <option key={p} value={p} className='bg-[#0B0F14]'>
                    {p.charAt(0).toUpperCase() + p.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className='block text-sm font-medium text-gray-300 mb-2'>Length</label>
              <select
                value={length}
                onChange={(e) => setLength(e.target.value)}
                className='w-full px-3 py-2 bg-[#0B0F14] border border-[#1A2230] rounded-lg text-white focus:outline-none focus:border-purple-500'
              >
                {lengths.map((l) => (
                  <option key={l} value={l} className='bg-[#0B0F14]'>
                    {l.charAt(0).toUpperCase() + l.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className='block text-sm font-medium text-gray-300 mb-2'>Language</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className='w-full px-3 py-2 bg-[#0B0F14] border border-[#1A2230] rounded-lg text-white focus:outline-none focus:border-purple-500'
              >
                {languages.map((l) => (
                  <option key={l} value={l} className='bg-[#0B0F14]'>
                    {l.charAt(0).toUpperCase() + l.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className='block text-sm font-medium text-gray-300 mb-2'>Brand Voice</label>
              <select
                value={brandVoice}
                onChange={(e) => setBrandVoice(e.target.value)}
                className='w-full px-3 py-2 bg-[#0B0F14] border border-[#1A2230] rounded-lg text-white focus:outline-none focus:border-purple-500'
              >
                {brandVoices.map((v) => (
                  <option key={v} value={v} className='bg-[#0B0F14]'>
                    {v.charAt(0).toUpperCase() + v.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <Button onClick={generateContent} className='w-full' disabled={isGenerating || !prompt.trim()}>
              {isGenerating ? (
                <>Generating...</>
              ) : (
                <><Sparkles className='w-4 h-4 mr-2' /> Generate Content</>
              )}
            </Button>
          </CardContent>
        </Card>
      </div>

      <div className='col-span-8'>
        <Card>
          <CardHeader>
            <CardTitle>Generated Content</CardTitle>
          </CardHeader>
          <CardContent>
            {generatedContent ? (
              <div className='space-y-4'>
                <div className='flex items-center justify-between mb-2'> 
                  <span className='text-sm text-gray-500'>Last updated: just now</span>
                  <div className='flex gap-2'> 
                    <Button variant='secondary' size='sm'>
                      <Copy className='w-4 h-4 mr-2' /> Copy
                    </Button>
                    <Button variant='secondary' size='sm'>
                      <Save className='w-4 h-4 mr-2' /> Save
                    </Button>
                    <Button variant='secondary' size='sm'>
                      <Download className='w-4 h-4 mr-2' /> Export
                    </Button>
                    <Button variant='primary' size='sm'>
                      <Send className='w-4 h-4 mr-2' /> Publish
                    </Button>
                  </div>
                </div>
                <textarea
                  value={generatedContent}
                  onChange={(e) => setGeneratedContent(e.target.value)}
                  className='w-full px-4 py-3 bg-[#0B0F14] border border-[#1A2230] rounded-lg text-white focus:outline-none focus:border-purple-500 min-h-[400px] resize-none'
                />
              </div>
            ) : (
              <div className='text-center py-20'>
                <div className='w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4'>
                  <Wand2 className='w-8 h-8 text-purple-400' />
                </div>
                <h3 className='text-lg font-medium mb-2'>No content generated yet</h3>
                <p className='text-gray-500'>Fill in the settings and click "Generate Content" to get started</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}