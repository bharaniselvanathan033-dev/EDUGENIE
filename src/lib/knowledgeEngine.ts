export type Level = 'beginner' | 'intermediate' | 'advanced';
export type Mode = 'qa' | 'explain' | 'quiz' | 'summary' | 'learning_path';

export interface QuizQuestion {
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
}

export interface QuizResult {
  questions: QuizQuestion[];
}

export interface ExplainResult {
  title: string;
  overview: string;
  keyPoints: string[];
  analogy: string;
  deeperDetail: string;
}

export interface SummaryResult {
  title: string;
  mainIdea: string;
  keyPoints: string[];
  takeaways: string[];
}

export interface LearningPathResult {
  title: string;
  steps: { name: string; description: string; resources: string[] }[];
}

export interface QAResult {
  answer: string;
}

export type EngineResult =
  | { type: 'qa'; data: QAResult }
  | { type: 'explain'; data: ExplainResult }
  | { type: 'quiz'; data: QuizResult }
  | { type: 'summary'; data: SummaryResult }
  | { type: 'learning_path'; data: LearningPathResult };

const levelLabels: Record<Level, string> = {
  beginner: 'Beginner',
  intermediate: 'Intermediate',
  advanced: 'Advanced',
};

function cleanTopic(topic: string): string {
  return topic.trim().replace(/\s+/g, ' ');
}

function titleCase(s: string): string {
  return s.replace(/\b\w/g, (c) => c.toUpperCase());
}

/* ------------------------------------------------------------------ */
/* Sentence utilities                                                  */
/* ------------------------------------------------------------------ */

function splitSentences(text: string): string[] {
  return text
    .split(/(?<=[.!?])\s+/)
    .map((s) => s.trim())
    .filter((s) => s.length > 10);
}

function extractKeywords(topic: string, notes: string): string[] {
  const stopWords = new Set([
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'can', 'to', 'of', 'in', 'on', 'at',
    'by', 'for', 'with', 'about', 'as', 'into', 'like', 'through', 'after',
    'over', 'between', 'out', 'against', 'during', 'without', 'before',
    'under', 'around', 'among', 'and', 'or', 'but', 'not', 'no', 'so', 'if',
    'than', 'that', 'this', 'these', 'those', 'it', 'its', 'they', 'them',
    'their', 'we', 'you', 'your', 'he', 'she', 'his', 'her', 'what', 'which',
    'who', 'whom', 'whose', 'when', 'where', 'why', 'how', 'all', 'each',
    'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'only',
    'own', 'same', 'very', 'just', 'because', 'also', 'there', 'here',
  ]);

  const combined = `${topic} ${notes}`;
  const words = combined
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter((w) => w.length > 3 && !stopWords.has(w));

  const freq: Record<string, number> = {};
  for (const w of words) freq[w] = (freq[w] || 0) + 1;

  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([w]) => w);
}

/* ------------------------------------------------------------------ */
/* EXPLAIN                                                             */
/* ------------------------------------------------------------------ */

function generateExplanation(topic: string, level: Level): ExplainResult {
  const t = titleCase(cleanTopic(topic));
  const kw = extractKeywords(topic, '');

  const overviewIntro: Record<Level, string> = {
    beginner: `${t} is a concept worth understanding because it appears in many real-world situations. At its core, ${t} refers to the ideas and principles that define how this subject works.`,
    intermediate: `${t} encompasses a set of principles and mechanisms that work together within a broader framework. Understanding ${t} requires examining its components, how they interact, and the context in which they operate.`,
    advanced: `${t} is a multifaceted domain that integrates theoretical foundations with practical applications. A rigorous treatment of ${t} involves analyzing its underlying mechanisms, edge cases, and the broader implications within its field.`,
  };

  const keyPoints: string[] = [];
  const basePoints = [
    `${t} has a clear definition that distinguishes it from related concepts.`,
    `The main components of ${t} work together to produce its characteristic behavior.`,
    `Understanding ${t} requires knowing both the "what" and the "why" behind it.`,
    `${t} connects to other ideas in its field, forming a broader knowledge network.`,
  ];

  if (kw.length > 0) {
    keyPoints.push(`Central to ${t} are concepts like ${kw.slice(0, 3).join(', ')}${kw.length > 3 ? ', and ' + kw[3] : ''}.`);
  }
  keyPoints.push(...basePoints.slice(0, level === 'beginner' ? 3 : 4));

  if (level !== 'beginner') {
    keyPoints.push(`${t} often involves trade-offs — simplifying one aspect may complicate another.`);
  }
  if (level === 'advanced') {
    keyPoints.push(`Advanced study of ${t} examines edge cases, limitations, and open research questions.`);
  }

  const analogies = [
    `Think of ${t} like a recipe: you have ingredients (the components), steps (the process), and a final dish (the outcome). Changing any part changes the result.`,
    `Imagine ${t} as a team sport: each player has a role, and success depends on how well they coordinate rather than any single player's effort.`,
    `${t} is like building with blocks — each piece supports the others, and removing one can destabilize the whole structure.`,
  ];

  const deeperDetail: Record<Level, string> = {
    beginner: `To get started with ${t}, focus on the basic definition and one or two simple examples. Once you can explain ${t} in your own words, you have a solid foundation. Try relating it to something you already know — this makes the concept "stick."`,
    intermediate: `Going deeper into ${t}, consider how its components interact dynamically. Ask yourself: what happens when one element changes? What are the feedback loops? ${t} is best understood by tracing cause-and-effect relationships and identifying the conditions under which the system behaves differently.`,
    advanced: `At an advanced level, ${t} demands critical examination of assumptions, boundary conditions, and the validity of models used to describe it. Consider competing interpretations, the evidence supporting each, and the domains where standard treatments of ${t} break down. Engage with primary literature and attempt to synthesize across sub-fields.`,
  };

  return {
    title: t,
    overview: overviewIntro[level],
    keyPoints,
    analogy: analogies[Math.floor(Math.random() * analogies.length)],
    deeperDetail: deeperDetail[level],
  };
}

/* ------------------------------------------------------------------ */
/* QUIZ                                                                */
/* ------------------------------------------------------------------ */

function shuffleArray<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function generateQuiz(topic: string, level: Level): QuizResult {
  const t = titleCase(cleanTopic(topic));
  const kw = extractKeywords(topic, '');

  type Template = { q: string; correct: string; wrong: string[]; explain: string };
  const templates: Template[] = [];
  const questions: QuizQuestion[] = [];

  const questionTemplates: Template[] = [
    {
      q: `Which best describes the core idea of ${t}?`,
      correct: `It is a concept built on key principles that work together to define how the subject operates.`,
      wrong: [
        `It is a random collection of unrelated facts.`,
        `It only applies to one very specific and narrow situation.`,
        `It is a historical event that no longer matters.`,
      ],
      explain: `${t} is defined by its underlying principles and their interactions, not by isolated facts.`,
    },
    {
      q: `Why is it important to understand the "why" behind ${t}, not just the "what"?`,
      correct: `Because knowing the reasons helps you apply ${t} to new situations you haven't seen before.`,
      wrong: [
        `Because the "what" is always wrong.`,
        `Because the "why" is only needed for exams.`,
        `Because understanding the "what" is impossible.`,
      ],
      explain: `Transferable understanding — knowing why something works — lets you adapt knowledge to novel contexts.`,
    },
    {
      q: `What is a good way to build a solid understanding of ${t}?`,
      correct: `Relate it to something you already know and explain it in your own words.`,
      wrong: [
        `Memorize a single sentence and never think about it again.`,
        `Ignore all examples and only read definitions.`,
        `Avoid connecting it to other topics in the field.`,
      ],
      explain: `Connecting new concepts to existing knowledge and articulating them yourself strengthens retention.`,
    },
    {
      q: level !== 'beginner'
        ? `What does an intermediate or advanced understanding of ${t} require?`
        : `What helps you go beyond the basics of ${t}?`,
      correct: level === 'beginner'
        ? `Looking at more examples and asking how changing one part affects the whole.`
        : `Examining how components interact dynamically and tracing cause-and-effect relationships.`,
      wrong: [
        `Only repeating the beginner definition louder.`,
        `Memorizing more vocabulary without understanding.`,
        `Avoiding any analysis of how parts connect.`,
      ],
      explain: `Deeper understanding comes from analyzing relationships, interactions, and the effects of change.`,
    },
    {
      q: `Which statement about ${t} is most accurate?`,
      correct: `${t} connects to other ideas in its field, forming a broader knowledge network.`,
      wrong: [
        `${t} exists completely isolated from every other concept.`,
        `${t} has no practical relevance whatsoever.`,
        `${t} can only be understood by experts with decades of training.`,
      ],
      explain: `No concept stands alone — ${t} fits within a web of related ideas, which is why connections matter.`,
    },
  ];

  if (kw.length >= 2) {
    templates.push({
      q: `Which of these is most closely associated with ${t}?`,
      correct: kw[0],
      wrong: shuffleArray([kw[1], 'unrelated concept', 'random observation']).slice(0, 3),
      explain: `${kw[0]} appeared frequently in the topic text, indicating it is closely associated with ${t}.`,
    });
  }

  const selected = shuffleArray([...questionTemplates, ...templates]).slice(0, level === 'beginner' ? 5 : 6);

  for (const tmpl of selected) {
    const allOptions = shuffleArray([tmpl.correct, ...tmpl.wrong]);
    questions.push({
      question: tmpl.q,
      options: allOptions,
      correctIndex: allOptions.indexOf(tmpl.correct),
      explanation: tmpl.explain,
    });
  }

  return { questions };
}

/* ------------------------------------------------------------------ */
/* SUMMARY                                                             */
/* ------------------------------------------------------------------ */

function generateSummary(notes: string, level: Level): SummaryResult {
  const sentences = splitSentences(notes);
  const kw = extractKeywords('', notes);
  const title = kw[0] ? titleCase(kw[0]) : 'Your Notes';

  if (sentences.length === 0) {
    return {
      title,
      mainIdea: 'No readable sentences were found in the provided notes. Please paste longer, more detailed notes.',
      keyPoints: [],
      takeaways: ['Add more content to your notes for a meaningful summary.'],
    };
  }

  // Score sentences by keyword frequency and position
  const kwSet = new Set(kw);
  const scored = sentences.map((s, i) => {
    const words = s.toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/);
    let score = 0;
    for (const w of words) if (kwSet.has(w)) score += 2;
    // Boost early and late sentences
    if (i < 2) score += 1;
    if (i === sentences.length - 1) score += 1;
    // Boost longer sentences (more information)
    if (words.length > 12) score += 1;
    return { sentence: s, score, index: i };
  });

  const topCount = level === 'beginner' ? 3 : level === 'intermediate' ? 5 : 7;
  const top = [...scored]
    .sort((a, b) => b.score - a.score)
    .slice(0, Math.min(topCount, sentences.length))
    .sort((a, b) => a.index - b.index);

  const keyPoints = top.map((t) => t.sentence);

  const mainIdea = sentences[0];

  const takeaways = [
    `The notes center on ${kw.slice(0, 3).join(', ') || 'the main topic'}.`,
    level !== 'beginner'
      ? `There are ${sentences.length} sentences covering ${kw.length} key themes.`
      : `Focus on the main idea and the top ${keyPoints.length} points to start.`,
    `Review the key points below and try to restate the main idea in your own words.`,
  ];

  return {
    title,
    mainIdea,
    keyPoints,
    takeaways,
  };
}

/* ------------------------------------------------------------------ */
/* LEARNING PATH                                                       */
/* ------------------------------------------------------------------ */

function generateLearningPath(topic: string, level: Level): LearningPathResult {
  const t = titleCase(cleanTopic(topic));
  const kw = extractKeywords(topic, '');

  const stepCount = level === 'beginner' ? 4 : level === 'intermediate' ? 5 : 6;

  const stepTemplates = [
    {
      name: `Foundations of ${t}`,
      description: `Start by understanding the basic definition, purpose, and scope of ${t}. Learn the key terms and why this subject matters.`,
      resources: [
        `Search YouTube for "${t} for beginners"`,
        `Read the Wikipedia article on ${t}`,
        `Find a simple blog post introducing ${t}`,
      ],
    },
    {
      name: `Core Concepts`,
      description: `Dive into the central principles of ${t}. Focus on${kw[0] ? ` topics like ${kw.slice(0, 3).join(', ')}` : ' the main building blocks'} and how they relate.`,
      resources: [
        `Look for a free online course covering ${t}`,
        `Watch tutorial videos on each core concept`,
        `Take notes and write definitions in your own words`,
      ],
    },
    {
      name: `Hands-On Practice`,
      description: `Apply what you've learned through exercises or small projects. Practice solidifies understanding better than passive reading.`,
      resources: [
        `Find practice problems or exercises about ${t}`,
        `Build a small project using ${t}`,
        `Join a free forum or community to ask questions`,
      ],
    },
    {
      name: `Connecting Ideas`,
      description: `Map how ${t} relates to other subjects in its field. Understanding connections deepens mastery and aids recall.`,
      resources: [
        `Read about fields adjacent to ${t}`,
        `Create a mind map linking ${t} to related topics`,
        `Write a short essay explaining the connections`,
      ],
    },
    {
      name: `Intermediate Deepening`,
      description: `Go beyond the basics by exploring how the components of ${t} interact dynamically and what trade-offs exist.`,
      resources: [
        `Read an intermediate-level textbook chapter on ${t}`,
        `Study case studies or real-world applications`,
        `Compare different approaches within ${t}`,
      ],
    },
    {
      name: `Advanced Mastery`,
      description: `Tackle edge cases, open questions, and the latest developments in ${t}. Engage with primary sources and research.`,
      resources: [
        `Search Google Scholar for recent papers on ${t}`,
        `Read advanced documentation or specification papers`,
        `Attempt to contribute to an open-source project related to ${t}`,
      ],
    },
  ];

  const steps = stepTemplates.slice(0, stepCount);

  return {
    title: `Learning Path: ${t} (${levelLabels[level]})`,
    steps,
  };
}

/* ------------------------------------------------------------------ */
/* MAIN ENTRY                                                          */
/* ------------------------------------------------------------------ */

/* ------------------------------------------------------------------ */
/* QUESTION & ANSWER (offline fallback)                               */
/* ------------------------------------------------------------------ */

function generateQA(question: string, level: Level): QAResult {
  const q = cleanTopic(question);
  const kw = extractKeywords(q, '');
  const lower = q.toLowerCase();

  // Pattern-based answers for common question types
  const whatMatch = lower.match(/^what (is|are|was|were) (.+)/);
  const whyMatch = lower.match(/^why (is|are|does|do|did|can|should) (.+)/);
  const howMatch = lower.match(/^how (do|does|did|can|could|to) (.+)/);

  let answer = '';

  if (whatMatch) {
    const subject = whatMatch[2].replace(/[?.]+$/, '');
    const t = titleCase(subject);
    answer =
      level === 'beginner'
        ? `${t} is a concept that can be understood by looking at what it does and why it matters. In simple terms, ${t} refers to the set of ideas and principles that define this subject. ` +
          `The key thing to remember is that ${t} has practical applications — it shows up in real situations. ` +
          `Think of it like a tool: once you know what it's for and how to use it, you can apply it to new problems.`
        : level === 'intermediate'
          ? `${t} is best understood by examining its core components and how they interact. ` +
            `At the intermediate level, the important thing is not just what ${t} is, but how its parts work together. ` +
            `Consider the conditions under which ${t} behaves differently, and what factors influence it. ` +
            `This systems-level view lets you predict how ${t} will behave in new situations.`
          : `${t} is a multifaceted concept that requires careful analysis of its assumptions, mechanisms, and boundary conditions. ` +
            `At an advanced level, you should critically examine the models used to describe ${t}, the evidence supporting them, and the domains where they break down. ` +
            `Consider competing interpretations and the trade-offs inherent in different approaches to ${t}.`;
  } else if (whyMatch) {
    const subject = whyMatch[2].replace(/[?.]+$/, '');
    answer =
      `This happens because of cause-and-effect relationships within the subject. ` +
      `In the case of "${subject}," the underlying reasons connect to how the components interact and what conditions are present. ` +
      (level !== 'beginner'
        ? `At a deeper level, this involves feedback loops and the interplay between multiple factors — changing one element can ripple through the whole system.`
        : `A simple way to think about it: when the right conditions are met, the result naturally follows. It's like pushing a ball downhill — gravity does the rest.`);
  } else if (howMatch) {
    const subject = howMatch[2].replace(/[?.]+$/, '');
    answer =
      `To work with "${subject}," you need to understand the steps involved and the principles behind them. ` +
      `Start by identifying the key components and what each one does. Then, follow the process step by step, paying attention to how each part connects to the next. ` +
      (level === 'beginner'
        ? `Don't worry about getting everything perfect at first — practice and repetition will make it natural.`
        : `At this level, you should also consider edge cases and what happens when the standard process doesn't apply.`);
  } else {
    // Generic answer
    answer =
      level === 'beginner'
        ? `Great question! Let me break this down simply. "${q}" is something that can be understood by looking at the key ideas involved. ` +
          `The most important thing is to focus on the main concept and how it connects to what you already know. ` +
          (kw.length > 0
            ? `The words that come up most in your question — ${kw.slice(0, 3).join(', ')} — are good starting points for deeper study.`
            : `Try rephrasing your question or breaking it into smaller parts for a more specific answer.`)
        : level === 'intermediate'
          ? `This is a good question that touches on several connected ideas. "${q}" can be approached by examining the underlying principles and how they interact. ` +
            `At the intermediate level, the key is to understand not just the surface answer but the mechanisms behind it. ` +
            (kw.length > 0
              ? `Consider how concepts like ${kw.slice(0, 3).join(', ')} relate to each other and to your question.`
              : `Look for the cause-and-effect relationships that drive the answer.`)
          : `This question requires a nuanced answer that considers multiple perspectives. "${q}" sits at the intersection of several ideas, each with its own assumptions and limitations. ` +
            `At an advanced level, critically evaluate the frameworks used to answer this, the quality of evidence, and where standard explanations might fail. ` +
            `Synthesize across sub-fields and be aware of open questions.`;
  }

  return { answer };
}

/* ------------------------------------------------------------------ */
/* MAIN ENTRY                                                          */
/* ------------------------------------------------------------------ */

export function generateResult(mode: Mode, input: string, level: Level): EngineResult {
  const topic = cleanTopic(input);

  if (!topic) {
    throw new Error('Please enter a topic or paste your notes before submitting.');
  }

  switch (mode) {
    case 'qa':
      return { type: 'qa', data: generateQA(topic, level) };
    case 'explain':
      return { type: 'explain', data: generateExplanation(topic, level) };
    case 'quiz':
      return { type: 'quiz', data: generateQuiz(topic, level) };
    case 'summary':
      return { type: 'summary', data: generateSummary(topic, level) };
    case 'learning_path':
      return { type: 'learning_path', data: generateLearningPath(topic, level) };
    default:
      throw new Error('Unknown mode.');
  }
}
