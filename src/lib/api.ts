/**
 * EduGenie API Client
 *
 * Talks to the Python FastAPI backend (Gemini-powered) when available.
 * If the backend is unreachable or the Gemini key is not configured,
 * it transparently falls back to the built-in knowledge engine so
 * the app always works.
 */

import { generateResult, type Level, type EngineResult } from '@/lib/knowledgeEngine';

export type ApiMode = 'qa' | 'explain' | 'quiz' | 'summary' | 'learning_path';

const API_BASE = (import.meta.env.VITE_API_BASE_URL as string | undefined) || 'http://localhost:8000';

export interface ApiResponse {
  status: string;
  data: unknown;
}

async function callBackend(endpoint: string, body: Record<string, unknown>): Promise<EngineResult> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    throw new Error(errBody.detail || `Request failed (${res.status})`);
  }

  const json: ApiResponse = await res.json();
  return normalizeBackendResponse(endpoint, json.data, body);
}

/**
 * Convert the raw backend response into the EngineResult discriminated union
 * that the frontend components expect.
 */
function normalizeBackendResponse(
  endpoint: string,
  data: unknown,
  body: Record<string, unknown>
): EngineResult {
  const raw = data as Record<string, unknown>;
  const topic = (body.topic as string) || (body.question as string) || '';

  switch (endpoint) {
    case '/api/qa':
      return { type: 'qa', data: { answer: raw.answer as string } };

    case '/api/explain':
      return {
        type: 'explain',
        data: {
          title: (raw.title as string) || 'Explanation',
          overview: (raw.overview as string) || '',
          keyPoints: Array.isArray(raw.keyPoints) ? (raw.keyPoints as string[]) : [],
          analogy: (raw.analogy as string) || '',
          deeperDetail: (raw.deeperDetail as string) || '',
        },
      };

    case '/api/quiz':
      return {
        type: 'quiz',
        data: {
          questions: Array.isArray(raw.questions)
            ? (raw.questions as Array<Record<string, unknown>>).map((q) => ({
                question: (q.question as string) || '',
                options: Array.isArray(q.options) ? (q.options as string[]) : [],
                correctIndex: typeof q.correctIndex === 'number' ? q.correctIndex : 0,
                explanation: (q.explanation as string) || '',
              }))
            : [],
        },
      };

    case '/api/summarize':
      return {
        type: 'summary',
        data: {
          title: (raw.title as string) || 'Summary',
          mainIdea: (raw.mainIdea as string) || '',
          keyPoints: Array.isArray(raw.keyPoints) ? (raw.keyPoints as string[]) : [],
          takeaways: Array.isArray(raw.takeaways) ? (raw.takeaways as string[]) : [],
        },
      };

    case '/api/learning-path':
      return {
        type: 'learning_path',
        data: {
          title: (raw.title as string) || `Learning Path: ${topic}`,
          steps: Array.isArray(raw.steps)
            ? (raw.steps as Array<Record<string, unknown>>).map((s) => ({
                name: (s.name as string) || '',
                description: (s.description as string) || '',
                resources: Array.isArray(s.resources) ? (s.resources as string[]) : [],
              }))
            : [],
        },
      };

    default:
      throw new Error('Unknown API endpoint.');
  }
}

/**
 * Main entry point. Tries the backend first, falls back to the local engine.
 */
export async function generate(
  mode: ApiMode,
  input: string,
  level: Level
): Promise<{ result: EngineResult; source: 'gemini' | 'offline' }> {
  const endpointMap: Record<ApiMode, string> = {
    qa: '/api/qa',
    explain: '/api/explain',
    quiz: '/api/quiz',
    summary: '/api/summarize',
    learning_path: '/api/learning-path',
  };

  const body =
    mode === 'qa'
      ? { question: input, level }
      : { topic: input, level };

  try {
    const result = await callBackend(endpointMap[mode], body);
    return { result, source: 'gemini' };
  } catch {
    // Backend not available — fall back to the offline knowledge engine
    const result = generateResult(mode === 'qa' ? 'qa' : mode, input, level);
    return { result, source: 'offline' };
  }
}

/**
 * Check if the backend is running and Gemini is configured.
 */
export async function checkBackendHealth(): Promise<{ online: boolean; geminiConfigured: boolean }> {
  try {
    const res = await fetch(`${API_BASE}/api/health`, { method: 'GET' });
    if (!res.ok) return { online: false, geminiConfigured: false };
    const data = await res.json();
    return { online: true, geminiConfigured: data.gemini_configured === true };
  } catch {
    return { online: false, geminiConfigured: false };
  }
}
