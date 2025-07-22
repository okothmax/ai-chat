export interface QueryHistoryItem {
  id: number;
  question: string;
  answer: string;
  llm_provider: string;
  model_used: string;
  response_time?: number;
  tokens_used?: number;
  created_at: string;
}

export interface QuestionResponse {
  question: string;
  answer: string;
  llm_provider: string;
  model_used: string;
  response_time: number;
  tokens_used?: number;
  timestamp: string;
  error?: boolean;
  message?: string;
}

export interface LLMProvider {
  name: string;
  model: string;
  status: string;
}
