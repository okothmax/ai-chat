import React from 'react';
import { QueryHistoryItem } from '@/types';

interface QueryHistoryProps {
  queries: QueryHistoryItem[];
  onQuerySelect: (query: QueryHistoryItem) => void;
}

const QueryHistory: React.FC<QueryHistoryProps> = ({ queries, onQuerySelect }) => {
  if (queries.length === 0) {
    return (
      <div className="text-center py-8">
        <div className="w-12 h-12 bg-slate-100 dark:bg-slate-700 rounded-xl flex items-center justify-center mx-auto mb-3">
          <svg className="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <p className="text-slate-500 dark:text-slate-400 text-sm">
          No queries yet. Start asking questions!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3 max-h-96 overflow-y-auto">
      {queries.map((query) => (
        <div
          key={query.id}
          onClick={() => onQuerySelect(query)}
          className="p-3 bg-slate-50 dark:bg-slate-700 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-600 cursor-pointer transition-colors border border-slate-200 dark:border-slate-600"
        >
          <div className="flex items-start justify-between mb-2">
            <h4 className="font-medium text-slate-800 dark:text-white text-sm line-clamp-2">
              {query.question.length > 60 
                ? `${query.question.substring(0, 60)}...` 
                : query.question
              }
            </h4>
            <div className="flex items-center space-x-1 text-xs text-slate-500 dark:text-slate-400 ml-2 flex-shrink-0">
              {query.response_time && (
                <span>{query.response_time.toFixed(1)}s</span>
              )}
            </div>
          </div>
          
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded text-xs font-medium">
                {query.llm_provider}
              </span>
              {query.tokens_used && (
                <span>{query.tokens_used} tokens</span>
              )}
            </div>
            <span>
              {new Date(query.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default QueryHistory;
