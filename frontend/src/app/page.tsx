"use client";

import { useState, useEffect } from 'react';
import QuestionForm from '@/components/QuestionForm';
import ResponseDisplay from '@/components/ResponseDisplay';
import QueryHistory from '@/components/QueryHistory';
import Header from '@/components/Header';
import { QueryHistoryItem } from '@/types';

export default function Home() {
  const [currentResponse, setCurrentResponse] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [queryHistory, setQueryHistory] = useState<QueryHistoryItem[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  const handleQuestionSubmit = async (question: string, context?: string) => {
    setIsLoading(true);
    setCurrentResponse(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question, context }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to get response');
      }
      
      const data = await response.json();
      setCurrentResponse(data);
      
      // Refresh history
      fetchQueryHistory();
    } catch (error) {
      console.error('Error:', error);
      setCurrentResponse({
        error: true,
        message: 'Failed to get response. Please try again.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const fetchQueryHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/history?limit=20');
      if (response.ok) {
        const data = await response.json();
        setQueryHistory(data);
      }
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  useEffect(() => {
    fetchQueryHistory();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Q&A Section */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-200 dark:border-slate-700">
              <h2 className="text-2xl font-bold text-slate-800 dark:text-white mb-6">
                Ask Your Question
              </h2>
              <QuestionForm onSubmit={handleQuestionSubmit} isLoading={isLoading} />
            </div>
            
            <ResponseDisplay response={currentResponse} isLoading={isLoading} />
          </div>
          
          {/* Sidebar */}
          <div className="space-y-6">
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-200 dark:border-slate-700">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800 dark:text-white">
                  Query History
                </h3>
                <button
                  onClick={() => setShowHistory(!showHistory)}
                  className="text-blue-600 hover:text-blue-700 dark:text-blue-400 text-sm font-medium"
                >
                  {showHistory ? 'Hide' : 'Show'}
                </button>
              </div>
              
              {showHistory && (
                <QueryHistory 
                  queries={queryHistory} 
                  onQuerySelect={(query: QueryHistoryItem) => setCurrentResponse(query)}
                />
              )}
            </div>
            
            {/* Stats Card */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-200 dark:border-slate-700">
              <h3 className="text-lg font-semibold text-slate-800 dark:text-white mb-4">
                Statistics
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-slate-600 dark:text-slate-400">Total Queries</span>
                  <span className="font-semibold text-slate-800 dark:text-white">
                    {queryHistory.length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600 dark:text-slate-400">Status</span>
                  <span className="text-green-600 dark:text-green-400 font-semibold">
                    Online
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
