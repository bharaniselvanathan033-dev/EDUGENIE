import type { ReactNode } from 'react';

export function EmptyState({
  icon,
  title,
  description,
}: {
  icon: ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-16 px-4">
      <div className="w-16 h-16 rounded-2xl border border-white/10 bg-white/[0.025] flex items-center justify-center mb-4 text-slate-500">
        {icon}
      </div>
      <h3 className="font-display font-semibold text-lg text-slate-300 mb-1.5">{title}</h3>
      <p className="text-sm text-slate-500 max-w-sm leading-relaxed">{description}</p>
    </div>
  );
}
