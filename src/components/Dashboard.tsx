import { MessageCircleQuestion, BookOpen, Brain, FileText, Route, ArrowRight } from 'lucide-react';
import type { ApiMode } from '@/lib/api';

interface DashboardProps {
  onNavigate: (mode: ApiMode) => void;
  geminiOnline: boolean;
}

const FEATURES: {
  mode: ApiMode;
  title: string;
  description: string;
  icon: typeof BookOpen;
  gradient: string;
}[] = [
  {
    mode: 'qa',
    title: 'Ask a Question',
    description: 'Get instant AI-powered answers to any study question.',
    icon: MessageCircleQuestion,
    gradient: 'from-cyan-500/20 to-blue-500/20',
  },
  {
    mode: 'explain',
    title: 'Explain a Concept',
    description: 'Break down difficult concepts with simple, structured explanations.',
    icon: BookOpen,
    gradient: 'from-violet-500/20 to-purple-500/20',
  },
  {
    mode: 'quiz',
    title: 'Generate a Quiz',
    description: 'Test your knowledge with auto-generated multiple-choice quizzes.',
    icon: Brain,
    gradient: 'from-pink-500/20 to-rose-500/20',
  },
  {
    mode: 'summary',
    title: 'Summarize Notes',
    description: 'Paste your notes and get a concise summary with key takeaways.',
    icon: FileText,
    gradient: 'from-cyan-500/20 to-teal-500/20',
  },
  {
    mode: 'learning_path',
    title: 'Build a Learning Path',
    description: 'Get a personalized step-by-step study plan for any subject.',
    icon: Route,
    gradient: 'from-violet-500/20 to-indigo-500/20',
  },
];

export function Dashboard({ onNavigate, geminiOnline }: DashboardProps) {
  return (
    <div className="animate-fadeIn">
      {/* Welcome hero */}
      <div className="text-center mb-10">
        <span className="inline-block text-[10px] tracking-[2px] font-bold text-cyan-300 px-3 py-2 border border-cyan-400/25 rounded-full bg-cyan-400/[0.06]">
          AI-POWERED LEARNING
        </span>
        <h1 className="font-display font-bold text-[clamp(34px,6vw,52px)] leading-[1.05] tracking-tight mt-5">
          Welcome to <span className="bg-gradient-to-r from-violet-400 to-cyan-300 bg-clip-text text-transparent">EduGenie</span>
        </h1>
        <p className="max-w-[460px] mx-auto text-slate-400 leading-relaxed text-[15px] mt-3">
          Your Google Gemini-powered learning companion. Ask questions, understand concepts, test yourself, and build study paths — all in one place.
        </p>
        <div className="flex items-center justify-center gap-2 mt-5">
          <span className={`flex items-center gap-2 text-[11px] px-3 py-1.5 rounded-full border ${geminiOnline ? 'border-green-400/30 text-green-300 bg-green-400/[0.06]' : 'border-amber-400/30 text-amber-300 bg-amber-400/[0.06]'}`}>
            <span className={`inline-block w-[7px] h-[7px] rounded-full ${geminiOnline ? 'bg-green-400 shadow-[0_0_8px_#4ade80]' : 'bg-amber-400 shadow-[0_0_8px_#fbbf24]'}`} />
            {geminiOnline ? 'Gemini AI Connected' : 'Offline Mode — Backend Not Running'}
          </span>
        </div>
      </div>

      {/* Feature cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {FEATURES.map((f) => {
          const Icon = f.icon;
          return (
            <button
              key={f.mode}
              onClick={() => onNavigate(f.mode)}
              className={`group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br ${f.gradient} backdrop-blur-sm p-6 text-left transition-all hover:border-white/20 hover:-translate-y-0.5`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="w-11 h-11 rounded-xl border border-white/10 bg-[#0d1429]/60 flex items-center justify-center text-white">
                  <Icon size={22} />
                </div>
                <ArrowRight size={18} className="text-slate-500 group-hover:text-white group-hover:translate-x-1 transition-all" />
              </div>
              <h3 className="font-display font-semibold text-lg text-white mb-1">{f.title}</h3>
              <p className="text-sm text-slate-400 leading-relaxed">{f.description}</p>
            </button>
          );
        })}

        {/* Full-width hint card */}
        <div className="sm:col-span-2 rounded-2xl border border-white/5 bg-white/[0.015] p-5 text-center">
          <p className="text-xs text-slate-500 leading-relaxed">
            EduGenie uses Google Gemini for AI generation. If the backend isn't running, the app automatically falls back to a built-in offline engine so you can keep learning.
          </p>
        </div>
      </div>
    </div>
  );
}
