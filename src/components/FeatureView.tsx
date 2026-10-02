import { useState } from 'react';
import { Send, Loader2, Sparkles } from 'lucide-react';
import type { Level, EngineResult } from '@/lib/knowledgeEngine';
import type { ApiMode } from '@/lib/api';
import { generate } from '@/lib/api';
import { supabase } from '@/lib/supabase';
import { LevelSelector } from '@/components/LevelSelector';
import { ResultCard } from '@/components/ResultCard';
import { EmptyState } from '@/components/EmptyState';

interface FeatureViewProps {
  mode: ApiMode;
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  placeholder: string;
  inputLabel: string;
  emptyIcon: React.ReactNode;
  emptyTitle: string;
  emptyDescription: string;
  maxChars?: number;
}

export function FeatureView({
  mode,
  title,
  subtitle,
  icon,
  placeholder,
  inputLabel,
  emptyIcon,
  emptyTitle,
  emptyDescription,
  maxChars = 5000,
}: FeatureViewProps) {
  const [level, setLevel] = useState<Level>('beginner');
  const [input, setInput] = useState('');
  const [result, setResult] = useState<EngineResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [source, setSource] = useState<'gemini' | 'offline' | null>(null);

  const handleGenerate = async () => {
    if (!input.trim()) {
      setError('Please enter a topic or question before submitting.');
      return;
    }
    if (input.length > maxChars) {
      setError(`Please keep your input under ${maxChars} characters.`);
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const { result: res, source: src } = await generate(mode, input.trim(), level);
      setResult(res);
      setSource(src);

      // Save to study history (best-effort)
      try {
        await supabase.from('study_sessions').insert({
          mode,
          level,
          topic: input.trim(),
          result: JSON.stringify(res),
        });
      } catch {
        // Saving is best-effort
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      handleGenerate();
    }
  };

  return (
    <div className="animate-fadeIn">
      {/* Header */}
      <div className="flex items-start gap-4 mb-6">
        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-500/20 to-cyan-400/20 border border-white/10 flex items-center justify-center text-violet-300 shrink-0">
          {icon}
        </div>
        <div>
          <h1 className="font-display font-bold text-2xl text-white tracking-tight">{title}</h1>
          <p className="text-sm text-slate-400 mt-1">{subtitle}</p>
        </div>
      </div>

      {/* Input card */}
      <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-[#181f40]/60 to-[#0d1428]/60 backdrop-blur-sm p-6">
        <div className="mb-5">
          <LevelSelector level={level} onChange={setLevel} />
        </div>

        <div className="mb-5">
          <label className="block text-xs font-semibold text-slate-300 mb-2">{inputLabel}</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            maxLength={maxChars}
            className="w-full bg-[#0d1429] border border-[#303c60] rounded-xl p-4 text-sm text-slate-100 leading-relaxed resize-y min-h-[130px] outline-none transition-all focus:border-violet-400 focus:shadow-[0_0_0_3px_rgba(154,130,255,0.12)] placeholder:text-slate-500"
          />
          <div className="flex items-center justify-between mt-3">
            <span className="text-[11px] text-slate-500">
              {input.length}/{maxChars} characters
            </span>
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="flex items-center gap-2 px-5 py-3 rounded-[10px] bg-gradient-to-r from-violet-500 to-cyan-400 text-[#0a1022] font-semibold text-sm shadow-[0_7px_22px_rgba(98,129,255,0.18)] transition-transform hover:not-disabled:-translate-y-0.5 disabled:opacity-60 disabled:cursor-wait"
            >
              {loading ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
              {loading ? 'Generating...' : 'Generate'}
            </button>
          </div>
        </div>

        {error && (
          <div className="rounded-[10px] p-3.5 text-sm leading-relaxed border border-red-400/35 bg-red-500/[0.08] text-red-200 animate-fadeIn">
            {error}
          </div>
        )}

        {source && !error && (
          <div className="flex items-center gap-2 text-[11px] text-slate-500 mt-3">
            <Sparkles size={12} className={source === 'gemini' ? 'text-cyan-400' : 'text-amber-400'} />
            {source === 'gemini'
              ? 'Powered by Google Gemini'
              : 'Offline mode — backend not connected. Start the Python backend with your Gemini key for AI-powered responses.'}
          </div>
        )}
      </div>

      {/* Result or empty state */}
      {result ? (
        <ResultCard result={result} />
      ) : (
        !loading && (
          <div className="mt-4 rounded-2xl border border-white/5 bg-white/[0.015]">
            <EmptyState icon={emptyIcon} title={emptyTitle} description={emptyDescription} />
          </div>
        )
      )}

      {loading && (
        <div className="mt-4 rounded-[18px] border border-white/10 bg-[#0a1123]/60 p-8 flex flex-col items-center gap-3">
          <Loader2 size={28} className="animate-spin text-violet-400" />
          <p className="text-sm text-slate-400">Generating your {title.toLowerCase()}...</p>
        </div>
      )}
    </div>
  );
}
