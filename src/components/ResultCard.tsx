import { useState } from 'react';
import { Copy, Check } from 'lucide-react';
import type { EngineResult, QuizQuestion } from '@/lib/knowledgeEngine';
import { CircleCheck, CircleX, Lightbulb, Route } from 'lucide-react';

export function ResultCard({ result }: { result: EngineResult }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(resultToText(result));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const titles: Record<string, string> = {
    qa: 'AI Answer',
    explain: 'Explanation',
    quiz: 'Quiz',
    summary: 'Summary',
    learning_path: 'Learning Path',
  };

  return (
    <section className="mt-6 p-6 rounded-[18px] border border-cyan-400/22 bg-[#0a1123]/80 animate-fadeIn">
      <div className="flex items-center justify-between mb-4">
        <div>
          <span className="text-[10px] tracking-[2px] font-bold text-cyan-300">EDUGENIE SAYS</span>
          <h3 className="font-display font-semibold text-[21px] mt-1.5">{titles[result.type]}</h3>
        </div>
        <button
          onClick={handleCopy}
          className="flex items-center gap-2 border border-white/10 rounded-[9px] px-3 py-2 text-[11px] text-slate-300 hover:bg-white/5 transition-colors"
        >
          {copied ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>

      <div className="border-t border-white/5 pt-4">
        {result.type === 'qa' && <QAView data={result.data} />}
        {result.type === 'explain' && <ExplainView data={result.data} />}
        {result.type === 'quiz' && <QuizView data={result.data} />}
        {result.type === 'summary' && <SummaryView data={result.data} />}
        {result.type === 'learning_path' && <LearningPathView data={result.data} />}
      </div>
    </section>
  );
}

function QAView({ data }: { data: { answer: string } }) {
  return <p className="text-slate-300 leading-[1.85] text-sm whitespace-pre-wrap">{data.answer}</p>;
}

function ExplainView({ data }: { data: import('@/lib/knowledgeEngine').ExplainResult }) {
  return (
    <div className="space-y-5">
      <div>
        <h4 className="font-display font-semibold text-lg text-white mb-2">{data.title}</h4>
        <p className="text-slate-300 leading-[1.8] text-sm">{data.overview}</p>
      </div>
      <div>
        <p className="text-xs font-semibold text-cyan-300 uppercase tracking-wider mb-3">Key Points</p>
        <ul className="space-y-2.5">
          {data.keyPoints.map((point, i) => (
            <li key={i} className="flex items-start gap-3 text-sm text-slate-300 leading-relaxed">
              <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-violet-400 shrink-0" />
              {point}
            </li>
          ))}
        </ul>
      </div>
      <div className="p-4 rounded-xl border border-violet-400/20 bg-violet-400/[0.06]">
        <p className="flex items-center gap-2 text-xs font-semibold text-violet-300 uppercase tracking-wider mb-2">
          <Lightbulb size={14} /> Analogy
        </p>
        <p className="text-sm text-slate-300 leading-relaxed">{data.analogy}</p>
      </div>
      <div>
        <p className="text-xs font-semibold text-cyan-300 uppercase tracking-wider mb-2">Going Deeper</p>
        <p className="text-slate-300 leading-[1.8] text-sm">{data.deeperDetail}</p>
      </div>
    </div>
  );
}

function QuizView({ data }: { data: import('@/lib/knowledgeEngine').QuizResult }) {
  return (
    <div className="space-y-1">
      {data.questions.map((q, qi) => (
        <QuizQuestionCard key={qi} question={q} number={qi + 1} />
      ))}
    </div>
  );
}

function QuizQuestionCard({ question, number }: { question: QuizQuestion; number: number }) {
  const [selected, setSelected] = useState<number | null>(null);
  const [checked, setChecked] = useState(false);
  const isCorrect = selected === question.correctIndex;

  return (
    <div className="py-4 border-t border-white/5 first:border-t-0">
      <h4 className="text-[15px] leading-relaxed mb-3 font-medium">
        <span className="text-violet-400 font-semibold">{number}.</span> {question.question}
      </h4>
      <div className="grid gap-2">
        {question.options.map((opt, oi) => {
          const isSelected = selected === oi;
          const isAnswer = oi === question.correctIndex;
          let style = 'border-white/10 bg-white/[0.025] hover:border-white/20';
          if (checked && isAnswer) style = 'border-green-400/50 bg-green-500/[0.12]';
          else if (checked && isSelected && !isAnswer) style = 'border-red-400/50 bg-red-500/[0.12]';
          else if (isSelected) style = 'border-violet-400 bg-violet-400/[0.10]';

          return (
            <label
              key={oi}
              className={`flex items-start gap-3 p-3 rounded-[9px] border cursor-pointer transition-all ${style} ${checked ? 'cursor-default' : ''}`}
            >
              <input
                type="radio"
                name={`q-${number}`}
                checked={isSelected}
                disabled={checked}
                onChange={() => setSelected(oi)}
                className="mt-1 accent-violet-400 shrink-0"
              />
              <span className="text-[13px] leading-relaxed text-slate-300">{opt}</span>
            </label>
          );
        })}
      </div>
      {!checked ? (
        <button
          onClick={() => setChecked(true)}
          disabled={selected === null}
          className="mt-3 px-3.5 py-2 rounded-lg border border-violet-400/50 bg-violet-400/[0.12] text-violet-200 text-sm font-medium hover:bg-violet-400/20 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          Check Answer
        </button>
      ) : (
        <div className="mt-3 flex items-start gap-2">
          {isCorrect ? (
            <CircleCheck size={18} className="text-green-400 shrink-0 mt-0.5" />
          ) : (
            <CircleX size={18} className="text-red-400 shrink-0 mt-0.5" />
          )}
          <div>
            <p className={`text-sm font-medium ${isCorrect ? 'text-green-400' : 'text-red-300'}`}>
              {isCorrect ? 'Correct!' : 'Not quite right.'}
            </p>
            <p className="text-xs text-slate-400 leading-relaxed mt-1">{question.explanation}</p>
            <button
              onClick={() => {
                setSelected(null);
                setChecked(false);
              }}
              className="mt-2 text-xs text-violet-400 hover:underline"
            >
              Try again
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function SummaryView({ data }: { data: import('@/lib/knowledgeEngine').SummaryResult }) {
  return (
    <div className="space-y-5">
      <h4 className="font-display font-semibold text-lg text-white">{data.title}</h4>
      <div>
        <p className="text-xs font-semibold text-cyan-300 uppercase tracking-wider mb-2">Main Idea</p>
        <p className="text-slate-300 leading-[1.8] text-sm">{data.mainIdea}</p>
      </div>
      {data.keyPoints.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-cyan-300 uppercase tracking-wider mb-3">Key Points</p>
          <ul className="space-y-2.5">
            {data.keyPoints.map((point, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-slate-300 leading-relaxed">
                <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0" />
                {point}
              </li>
            ))}
          </ul>
        </div>
      )}
      <div className="p-4 rounded-xl border border-cyan-400/20 bg-cyan-400/[0.06]">
        <p className="flex items-center gap-2 text-xs font-semibold text-cyan-300 uppercase tracking-wider mb-2">
          <Lightbulb size={14} /> Takeaways
        </p>
        <ul className="space-y-2">
          {data.takeaways.map((t, i) => (
            <li key={i} className="text-sm text-slate-300 leading-relaxed flex items-start gap-2">
              <span className="text-cyan-400 mt-0.5">→</span>
              {t}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

function LearningPathView({ data }: { data: import('@/lib/knowledgeEngine').LearningPathResult }) {
  return (
    <div className="space-y-4">
      <h4 className="font-display font-semibold text-lg text-white flex items-center gap-2">
        <Route size={20} className="text-cyan-400" />
        {data.title}
      </h4>
      <div className="space-y-3">
        {data.steps.map((step, i) => (
          <div
            key={i}
            className="flex gap-4 p-4 rounded-xl border border-white/10 bg-white/[0.025] hover:bg-white/[0.04] transition-colors"
          >
            <div className="flex flex-col items-center shrink-0">
              <span className="w-9 h-9 rounded-full bg-gradient-to-br from-violet-500 to-cyan-400 text-[#10152a] font-bold text-sm flex items-center justify-center">
                {i + 1}
              </span>
              {i < data.steps.length - 1 && <span className="w-px flex-1 bg-white/10 mt-1" />}
            </div>
            <div className="flex-1">
              <p className="font-semibold text-sm text-white">{step.name}</p>
              <p className="text-sm text-slate-400 leading-relaxed mt-1">{step.description}</p>
              <div className="mt-3 flex flex-col gap-1.5">
                {step.resources.map((r, ri) => (
                  <span key={ri} className="text-xs text-slate-500 flex items-center gap-2">
                    <span className="w-1 h-1 rounded-full bg-cyan-400" />
                    {r}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function resultToText(result: EngineResult): string {
  switch (result.type) {
    case 'qa':
      return result.data.answer;
    case 'explain': {
      const d = result.data;
      return `${d.title}\n\nOverview: ${d.overview}\n\nKey Points:\n${d.keyPoints.map((p) => `- ${p}`).join('\n')}\n\nAnalogy: ${d.analogy}\n\nGoing Deeper: ${d.deeperDetail}`;
    }
    case 'quiz': {
      const d = result.data;
      return d.questions
        .map(
          (q, i) =>
            `Q${i + 1}: ${q.question}\n${q.options.map((o, oi) => `${oi === q.correctIndex ? '✓' : '○'} ${o}`).join('\n')}\nExplanation: ${q.explanation}`
        )
        .join('\n\n');
    }
    case 'summary': {
      const d = result.data;
      return `${d.title}\n\nMain Idea: ${d.mainIdea}\n\nKey Points:\n${d.keyPoints.map((p) => `- ${p}`).join('\n')}\n\nTakeaways:\n${d.takeaways.map((t) => `- ${t}`).join('\n')}`;
    }
    case 'learning_path': {
      const d = result.data;
      return `${d.title}\n\n${d.steps
        .map(
          (s, i) =>
            `Step ${i + 1}: ${s.name}\n${s.description}\nResources:\n${s.resources.map((r) => `  - ${r}`).join('\n')}`
        )
        .join('\n\n')}`;
    }
  }
}
