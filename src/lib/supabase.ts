import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

export type SessionMode = 'qa' | 'explain' | 'quiz' | 'summary' | 'learning_path';

export type StudySession = {
  id: string;
  mode: SessionMode;
  level: 'beginner' | 'intermediate' | 'advanced';
  topic: string;
  result: string;
  created_at: string;
};
