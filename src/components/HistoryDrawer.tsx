import { X, History, Trash2 } from 'lucide-react';
import type { StudySession } from '@/lib/supabase';

const modeLabels: Record<string, string> = {
  qa: 'Q&A',
  explain: 'Explain',
  quiz: 'Quiz',
  summary: 'Summary',
  learning_path: 'Learning Path',
};

const modeColors: Record<string, string> = {
  qa: 'text-cyan-400',
  explain: 'text-violet-400',
  quiz: 'text-pink-400',
  summary: 'text-cyan-400',
  learning_path: 'text-violet-400',
};

const levelColors: Record<string, string> = {
  beginner: 'text-green-400',
  intermediate: 'text-cyan-400',
  advanced: 'text-violet-400',
};

export function HistoryDrawer({
  history,
  onClose,
  onLoad,
  onDelete,
}: {
  history: StudySession[];
  onClose: () => void;
  onLoad: (session: StudySession) => void;
  onDelete: (id: string, e: React.MouseEvent) => void;
}) {
  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-md h-full bg-[#0d1429] border-l border-white/10 overflow-y-auto animate-slideIn">
        <div className="sticky top-0 flex items-center justify-between p-5 border-b border-white/10 bg-[#0d1429] z-10">
          <h3 className="font-display font-semibold text-lg flex items-center gap-2">
            <History size={20} className="text-violet-400" />
            Study History
          </h3>
          <button onClick={onClose} className="p-2 rounded-lg hover:bg-white/5 transition-colors">
            <X size={18} className="text-slate-400" />
          </button>
        </div>
        <div className="p-4">
          {history.length === 0 ? (
            <p className="text-slate-500 text-sm text-center py-12">
              No saved sessions yet. Generate something and it will appear here.
            </p>
          ) : (
            <div className="space-y-2">
              {history.map((session) => (
                <div
                  key={session.id}
                  onClick={() => onLoad(session)}
                  className="group p-4 rounded-xl border border-white/10 bg-white/[0.025] hover:border-violet-400/40 hover:bg-white/[0.04] cursor-pointer transition-all"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className={`text-xs font-semibold ${modeColors[session.mode] || 'text-slate-400'}`}>
                      {modeLabels[session.mode] || session.mode}
                    </span>
                    <span className={`text-[11px] font-medium ${levelColors[session.level] || 'text-slate-400'}`}>
                      {session.level}
                    </span>
                  </div>
                  <p className="text-sm text-slate-300 line-clamp-2 leading-relaxed">{session.topic}</p>
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-[11px] text-slate-500">
                      {new Date(session.created_at).toLocaleDateString(undefined, {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                    <button
                      onClick={(e) => onDelete(session.id, e)}
                      className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-red-500/10 transition-all"
                    >
                      <Trash2 size={14} className="text-red-400" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
