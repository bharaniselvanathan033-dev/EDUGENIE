import { useState, useEffect, useCallback } from 'react';
import {
  GraduationCap,
  LayoutDashboard,
  MessageCircleQuestion,
  BookOpen,
  Brain,
  FileText,
  Route,
  History,
  Menu,
  X,
} from 'lucide-react';
import type { EngineResult } from '@/lib/knowledgeEngine';
import type { StudySession } from '@/lib/supabase';
import { supabase } from '@/lib/supabase';
import { checkBackendHealth } from '@/lib/api';
import { Dashboard } from '@/components/Dashboard';
import { FeatureView } from '@/components/FeatureView';
import { ResultCard } from '@/components/ResultCard';
import { HistoryDrawer } from '@/components/HistoryDrawer';

type View = 'dashboard' | 'qa' | 'explain' | 'quiz' | 'summary' | 'learning_path';

const NAV_ITEMS: { view: View; label: string; icon: typeof BookOpen }[] = [
  { view: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { view: 'qa', label: 'Ask a Question', icon: MessageCircleQuestion },
  { view: 'explain', label: 'Explain a Concept', icon: BookOpen },
  { view: 'quiz', label: 'Generate a Quiz', icon: Brain },
  { view: 'summary', label: 'Summarize Notes', icon: FileText },
  { view: 'learning_path', label: 'Learning Path', icon: Route },
];

export default function App() {
  const [view, setView] = useState<View>('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [history, setHistory] = useState<StudySession[]>([]);
  const [historyLoaded, setHistoryLoaded] = useState(false);
  const [geminiOnline, setGeminiOnline] = useState(false);
  const [loadedResult, setLoadedResult] = useState<EngineResult | null>(null);

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth().then(({ online, geminiConfigured }) => {
      setGeminiOnline(online && geminiConfigured);
    });
  }, []);

  const loadHistory = useCallback(async () => {
    if (historyLoaded) {
      setShowHistory(true);
      return;
    }
    const { data } = await supabase
      .from('study_sessions')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(30);

    setHistory((data as StudySession[]) ?? []);
    setHistoryLoaded(true);
    setShowHistory(true);
  }, [historyLoaded]);

  const deleteHistoryItem = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    await supabase.from('study_sessions').delete().eq('id', id);
    setHistory((prev) => prev.filter((h) => h.id !== id));
  };

  const loadFromHistory = (session: StudySession) => {
    try {
      const parsed = JSON.parse(session.result) as EngineResult;
      setLoadedResult(parsed);
      setView(session.mode as View);
      setShowHistory(false);
    } catch {
      // ignore parse errors
    }
  };

  const handleNavigate = (v: View) => {
    setView(v);
    setSidebarOpen(false);
    setLoadedResult(null);
  };

  const featureViewConfig: Record<
    Exclude<View, 'dashboard'>,
    {
      title: string;
      subtitle: string;
      icon: React.ReactNode;
      placeholder: string;
      inputLabel: string;
      emptyIcon: React.ReactNode;
      emptyTitle: string;
      emptyDescription: string;
    }
  > = {
    qa: {
      title: 'Ask a Question',
      subtitle: 'Get an AI-powered answer to any study question.',
      icon: <MessageCircleQuestion size={24} />,
      placeholder: 'Type your question here, e.g. "What is photosynthesis?" or "Why is the sky blue?"',
      inputLabel: 'Your Question',
      emptyIcon: <MessageCircleQuestion size={28} />,
      emptyTitle: 'No answer yet',
      emptyDescription: 'Ask a question above and EduGenie will give you a clear, structured answer.',
    },
    explain: {
      title: 'Explain a Concept',
      subtitle: 'Get a clear, structured explanation of any topic.',
      icon: <BookOpen size={24} />,
      placeholder: 'e.g. Photosynthesis, Recursion, Supply and Demand...',
      inputLabel: 'Concept to Explain',
      emptyIcon: <BookOpen size={28} />,
      emptyTitle: 'Nothing explained yet',
      emptyDescription: 'Enter a concept above and EduGenie will break it down for you.',
    },
    quiz: {
      title: 'Generate a Quiz',
      subtitle: 'Test your understanding with auto-generated questions.',
      icon: <Brain size={24} />,
      placeholder: "e.g. World War II, Newton's Laws, The Water Cycle...",
      inputLabel: 'Quiz Topic',
      emptyIcon: <Brain size={28} />,
      emptyTitle: 'No quiz generated yet',
      emptyDescription: 'Enter a topic above and EduGenie will create a quiz for you.',
    },
    summary: {
      title: 'Summarize Notes',
      subtitle: 'Paste your notes and get a concise summary.',
      icon: <FileText size={24} />,
      placeholder: 'Paste your lecture notes, textbook passage, or article here...',
      inputLabel: 'Notes to Summarize',
      emptyIcon: <FileText size={28} />,
      emptyTitle: 'Nothing summarized yet',
      emptyDescription: 'Paste your notes above and EduGenie will summarize them for you.',
    },
    learning_path: {
      title: 'Build a Learning Path',
      subtitle: 'Get a step-by-step study plan for any subject.',
      icon: <Route size={24} />,
      placeholder: 'e.g. Machine Learning, Spanish, Organic Chemistry...',
      inputLabel: 'Subject to Learn',
      emptyIcon: <Route size={28} />,
      emptyTitle: 'No learning path yet',
      emptyDescription: 'Enter a subject above and EduGenie will build a study path for you.',
    },
  };

  const currentView = view as View;
  const isFeatureView = currentView !== 'dashboard';

  return (
    <div className="min-h-screen bg-[#090e1d] text-slate-100 font-sans flex">
      {/* Background glows */}
      <div className="fixed top-[20%] -left-48 w-[340px] h-[340px] rounded-full bg-[#6655ff] blur-[110px] opacity-[0.12] pointer-events-none -z-10" />
      <div className="fixed top-[55%] -right-48 w-[340px] h-[340px] rounded-full bg-[#23cbdc] blur-[110px] opacity-[0.10] pointer-events-none -z-10" />

      {/* Sidebar — desktop */}
      <aside className="hidden lg:flex flex-col w-64 shrink-0 border-r border-white/[0.07] bg-[#0c1122]/80 backdrop-blur-sm min-h-screen sticky top-0 h-screen">
        <SidebarContent view={currentView} onNavigate={handleNavigate} onHistory={loadHistory} />
      </aside>

      {/* Sidebar — mobile drawer */}
      {sidebarOpen && (
        <div className="lg:hidden fixed inset-0 z-50">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setSidebarOpen(false)} />
          <aside className="relative w-64 h-full bg-[#0c1122] border-r border-white/10 animate-slideIn">
            <button
              onClick={() => setSidebarOpen(false)}
              className="absolute top-4 right-4 p-2 rounded-lg hover:bg-white/5"
            >
              <X size={18} className="text-slate-400" />
            </button>
            <SidebarContent view={currentView} onNavigate={handleNavigate} onHistory={loadHistory} />
          </aside>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 min-w-0 flex flex-col">
        {/* Top bar — mobile */}
        <header className="lg:hidden flex items-center gap-3 px-4 h-16 border-b border-white/[0.07] bg-[#0c1122]/80 backdrop-blur-sm sticky top-0 z-40">
          <button onClick={() => setSidebarOpen(true)} className="p-2 rounded-lg hover:bg-white/5">
            <Menu size={20} className="text-slate-300" />
          </button>
          <div className="flex items-center gap-2">
            <span className="inline-grid place-items-center w-7 h-7 rounded-lg bg-gradient-to-br from-violet-500 to-cyan-400 text-[#10152a]">
              <GraduationCap size={16} strokeWidth={2.5} />
            </span>
            <span className="font-display font-bold text-lg tracking-tight">EduGenie</span>
          </div>
        </header>

        {/* Content area */}
        <main className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto px-5 sm:px-8 py-8 lg:py-12">
            {currentView === 'dashboard' && (
              <Dashboard onNavigate={(m) => handleNavigate(m as View)} geminiOnline={geminiOnline} />
            )}

            {isFeatureView && (
              <>
                <FeatureView
                  key={currentView}
                  mode={currentView}
                  title={featureViewConfig[currentView].title}
                  subtitle={featureViewConfig[currentView].subtitle}
                  icon={featureViewConfig[currentView].icon}
                  placeholder={featureViewConfig[currentView].placeholder}
                  inputLabel={featureViewConfig[currentView].inputLabel}
                  emptyIcon={featureViewConfig[currentView].emptyIcon}
                  emptyTitle={featureViewConfig[currentView].emptyTitle}
                  emptyDescription={featureViewConfig[currentView].emptyDescription}
                />
                {loadedResult && <ResultCard result={loadedResult} />}
              </>
            )}
          </div>

          <footer className="text-center py-6 text-[11px] text-slate-600 border-t border-white/[0.04]">
            EduGenie — Google Gemini Powered Learning Assistant. Free &amp; open for learners everywhere.
          </footer>
        </main>
      </div>

      {/* History drawer */}
      {showHistory && (
        <HistoryDrawer
          history={history}
          onClose={() => setShowHistory(false)}
          onLoad={loadFromHistory}
          onDelete={deleteHistoryItem}
        />
      )}
    </div>
  );
}

function SidebarContent({
  view,
  onNavigate,
  onHistory,
}: {
  view: View;
  onNavigate: (v: View) => void;
  onHistory: () => void;
}) {
  return (
    <div className="flex flex-col h-full">
      {/* Brand */}
      <div className="flex items-center gap-2.5 px-5 h-16 border-b border-white/[0.07]">
        <span className="inline-grid place-items-center w-8 h-8 rounded-[10px] bg-gradient-to-br from-violet-500 to-cyan-400 text-[#10152a]">
          <GraduationCap size={18} strokeWidth={2.5} />
        </span>
        <span className="font-display font-bold text-xl tracking-tight">EduGenie</span>
      </div>

      {/* Nav items */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <p className="px-3 text-[10px] font-bold text-slate-600 uppercase tracking-wider mb-2">Menu</p>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = view === item.view;
          return (
            <button
              key={item.view}
              onClick={() => onNavigate(item.view)}
              className={`flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-gradient-to-r from-violet-500/20 to-cyan-400/10 text-white border border-violet-400/20'
                  : 'text-slate-400 hover:text-white hover:bg-white/[0.04] border border-transparent'
              }`}
            >
              <Icon size={18} className={isActive ? 'text-violet-300' : ''} />
              {item.label}
            </button>
          );
        })}
      </nav>

      {/* History button */}
      <div className="px-3 py-4 border-t border-white/[0.07]">
        <button
          onClick={onHistory}
          className="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-white/[0.04] transition-all"
        >
          <History size={18} />
          Study History
        </button>
        <p className="px-3 mt-3 text-[10px] text-slate-600 leading-relaxed">
          Powered by Google Gemini
        </p>
      </div>
    </div>
  );
}
