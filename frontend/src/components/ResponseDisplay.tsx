import React from 'react';
import { QuestionResponse } from '@/types';

interface ResponseDisplayProps {
  response: QuestionResponse | null;
  isLoading: boolean;
}

const ResponseDisplay: React.FC<ResponseDisplayProps> = ({ response, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-200 dark:border-slate-700">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <svg className="w-4 h-4 text-white animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white">
            AI is thinking...
          </h3>
        </div>
        
        <div className="space-y-3">
          <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded animate-pulse"></div>
          <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded animate-pulse w-5/6"></div>
          <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded animate-pulse w-4/6"></div>
        </div>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-200 dark:border-slate-700">
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-slate-800 dark:text-white mb-2">
            Ready to Help!
          </h3>
          <p className="text-slate-600 dark:text-slate-400">
            Ask me any question and I'll provide you with a comprehensive answer.
          </p>
        </div>
      </div>
    );
  }

  if (response.error) {
    return (
      <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6 border border-red-200 dark:border-red-800">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-8 h-8 bg-red-500 rounded-lg flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-red-600 dark:text-red-400">
            Error
          </h3>
        </div>
        <p className="text-slate-700 dark:text-slate-300">
          {response.message || 'An error occurred while processing your request.'}
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-200 dark:border-slate-700">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-blue-600 rounded-lg flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-slate-800 dark:text-white">
            AI Response
          </h3>
        </div>
        
        <div className="flex items-center space-x-4 text-sm text-slate-500 dark:text-slate-400">
          <span className="flex items-center space-x-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{response.response_time?.toFixed(2)}s</span>
          </span>
          {response.tokens_used && (
            <span className="flex items-center space-x-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              <span>{response.tokens_used} tokens</span>
            </span>
          )}
        </div>
      </div>

      <div className="mb-4 p-4 bg-slate-50 dark:bg-slate-700 rounded-xl">
        <h4 className="font-medium text-slate-800 dark:text-white mb-2">Question:</h4>
        <p className="text-slate-700 dark:text-slate-300">{response.question}</p>
      </div>

      <div className="prose prose-slate dark:prose-invert max-w-none">
        <div className="whitespace-pre-wrap text-slate-700 dark:text-slate-300 leading-relaxed">
          {response.answer}
        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
        <div className="flex items-center space-x-2">
          <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-md font-medium">
            {response.llm_provider}
          </span>
          <span>{response.model_used}</span>
        </div>
        <div>
          {new Date(response.timestamp).toLocaleString()}
        </div>
      </div>
    </div>
  );
};

export default ResponseDisplay;
