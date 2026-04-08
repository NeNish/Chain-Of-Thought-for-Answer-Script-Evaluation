import { NextResponse } from 'next/server';

function clampScore(value) {
  return Math.max(0, Math.min(100, Math.round(value)));
}

function scoreAnswer(answerText) {
  const words = answerText.trim().split(/\s+/).filter(Boolean);
  const lower = answerText.toLowerCase();
  const sentenceCount = Math.max((answerText.match(/[.!?]/g) || []).length, 1);

  const rubricKeywords = [
    'because',
    'therefore',
    'however',
    'evidence',
    'example',
    'assumption',
    'conclusion',
    'step',
    'analysis',
    'trade-off'
  ];

  const subjectSignals = [
    'model',
    'algorithm',
    'system',
    'data',
    'mechanism',
    'evaluate',
    'accuracy',
    'metric',
    'reasoning'
  ];

  const rubricHits = rubricKeywords.reduce(
    (sum, keyword) => sum + (lower.includes(keyword) ? 1 : 0),
    0
  );
  const subjectHits = subjectSignals.reduce(
    (sum, keyword) => sum + (lower.includes(keyword) ? 1 : 0),
    0
  );

  const avgSentenceLength = words.length / sentenceCount;
  const clarity = clampScore(45 + avgSentenceLength * 2 + rubricHits * 3);
  const coherence = clampScore(40 + rubricHits * 5 + Math.min(sentenceCount, 12));
  const rubricAlignment = clampScore(30 + rubricHits * 7 + (words.length > 180 ? 10 : 0));
  const conceptualAccuracy = clampScore(35 + subjectHits * 7 + (words.length > 120 ? 8 : 0));
  const reasoningDepth = clampScore(25 + rubricHits * 6 + (words.length > 220 ? 20 : words.length / 12));
  const actionability = clampScore(30 + (lower.includes('recommend') ? 15 : 0) + rubricHits * 4);

  const overall = clampScore(
    (clarity + coherence + rubricAlignment + conceptualAccuracy + reasoningDepth + actionability) / 6
  );

  const strengths = [
    clarity >= 70 ? 'Clear sentence construction and readable flow.' : null,
    coherence >= 70 ? 'Logical progression between ideas.' : null,
    rubricAlignment >= 70 ? 'Good alignment with rubric cues and evidence framing.' : null,
    conceptualAccuracy >= 70 ? 'Strong use of domain-relevant concepts.' : null,
    reasoningDepth >= 70 ? 'Reasoning shows depth and multi-step thinking.' : null,
    actionability >= 70 ? 'Contains practical, actionable suggestions.' : null
  ].filter(Boolean);

  const improvements = [
    clarity < 70 ? 'Use shorter, clearer sentences with concrete terminology.' : null,
    coherence < 70 ? 'Strengthen transitions between claims and supporting points.' : null,
    rubricAlignment < 70 ? 'Explicitly include evidence, assumptions, and conclusions.' : null,
    conceptualAccuracy < 70 ? 'Add more precise subject-specific terminology and checks.' : null,
    reasoningDepth < 70 ? 'Expand causal links and intermediate reasoning steps.' : null,
    actionability < 70 ? 'Add specific recommendations and next-step guidance.' : null
  ].filter(Boolean);

  const feedback =
    overall >= 80
      ? 'High-quality answer with strong rubric alignment and reasoning structure.'
      : overall >= 60
        ? 'Solid baseline answer; refining evidence use and depth can improve score further.'
        : 'Needs more structure, rubric cues, and conceptual depth for stronger performance.';

  return {
    overall,
    clarity,
    coherence,
    rubricAlignment,
    conceptualAccuracy,
    reasoningDepth,
    actionability,
    strengths,
    improvements,
    feedback
  };
}

export async function POST(request) {
  try {
    const { answerText } = await request.json();

    if (!answerText || typeof answerText !== 'string') {
      return NextResponse.json(
        { message: 'Invalid payload. answerText is required.' },
        { status: 400 }
      );
    }

    const metrics = scoreAnswer(answerText);
    return NextResponse.json(metrics);
  } catch {
    return NextResponse.json(
      { message: 'Unexpected error while evaluating answer script.' },
      { status: 500 }
    );
  }
}
