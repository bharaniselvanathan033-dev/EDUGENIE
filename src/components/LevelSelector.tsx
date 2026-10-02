import type { Level } from '@/lib/knowledgeEngine';

const LEVELS: { id: Level; label: string; description: string }[] = [
  { id: 'beginner', label: 'Beginner', description: 'New to the topic' },
  { id: 'intermediate', label: 'Intermediate', description: 'Some background' },
  { id: 'advanced', label: 'Advanced', description: 'Looking to go deep' },
];

export function LevelSelector({
  level,
  onChange,
}: {
  level: Level;
  onChange: (l: Level) => void;
}) {
  return (
    <div>
      <label className="block text-xs font-semibold text-slate-300 mb-2">Learning Level</label>
      <div className="grid grid-cols-3 gap-2">
        {LEVELS.map((l) => {
          const isActive = level === l.id;
          return (
            <button
              key={l.id}
              onClick={() => onChange(l.id)}
              className={`p-3 rounded-lg border text-center transition-all ${
                isActive
                  ? 'border-cyan-400 bg-cyan-400/[0.10] text-white'
                  : 'border-white/10 bg-white/[0.025] text-slate-400 hover:border-white/20 hover:bg-white/[0.04]'
              }`}
            >
              <p className="font-semibold text-sm">{l.label}</p>
              <p className="text-[11px] mt-0.5 opacity-80">{l.description}</p>
            </button>
          );
        })}
      </div>
    </div>
  );
}
