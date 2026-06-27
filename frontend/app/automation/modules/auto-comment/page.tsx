'use client';
import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Textarea } from '@/components/ui/Textarea';
import { Input } from '@/components/ui/Input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/Select';
import { API_CONFIG } from '@/config/api';

export default function AutoCommentModule() {
  const [comment, setComment] = useState('');
  const [target, setTarget] = useState('');
  const [platform, setPlatform] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const response = await fetch(`${API_CONFIG.baseURL}/api/automation/comments/generate`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ keywords: target, platform, context: comment })
      });
      
      if (response.ok) {
        const data = await response.json();
        setComment(data.content);
        alert('✨ Comment generated successfully!');
      } else {
        throw new Error('Failed to generate comment');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('❌ Failed to generate comment');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>💭 Auto Comment - Smart Comments</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input placeholder="Target (keywords/ID)" value={target} onChange={(e) => setTarget(e.target.value)} />
          <Select onValueChange={setPlatform}>
            <SelectTrigger><SelectValue placeholder="Platform" /></SelectTrigger>
            <SelectContent>
              <SelectItem value="instagram">Instagram</SelectItem>
              <SelectItem value="facebook">Facebook</SelectItem>
              <SelectItem value="tiktok">TikTok</SelectItem>
            </SelectContent>
          </Select>
          <Textarea placeholder="Context" value={comment} onChange={(e) => setComment(e.target.value)} rows={4} />
          <Button onClick={handleGenerate} disabled={isGenerating} className="w-full">
            {isGenerating ? '🤖 Generating...' : '✨ Generate Comment'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
