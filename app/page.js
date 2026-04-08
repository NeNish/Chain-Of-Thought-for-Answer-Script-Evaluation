'use client';

import { useMemo, useState } from 'react';

const initialMetrics = {
  overall: 0,
  clarity: 0,
  coherence: 0,
  rubricAlignment: 0,
  conceptualAccuracy: 0,
  reasoningDepth: 0,
  actionability: 0,
  strengths: [],
  improvements: [],
  feedback: ''
};

export default function Home() {
  const [answerText, setAnswerText] = useState('');
  const [studentName, setStudentName] = useState('');
  const [subject, setSubject] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [metrics, setMetrics] = useState(initialMetrics);

  const hasResults = useMemo(() => metrics.overall > 0, [metrics.overall]);

  const handleUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const validMimeTypes = ['text/plain', 'application/pdf'];
    if (!validMimeTypes.includes(file.type) && !file.name.endsWith('.txt')) {
      setError('Please upload a .txt or .pdf file. For PDFs, plain text extraction quality may vary.');
      return;
    }

    const content = await file.text();
    setAnswerText(content);
    setError('');
  };

  const evaluateAnswer = async (event) => {
    event.preventDefault();

    if (!answerText.trim()) {
      setError('Please upload or paste an answer script before evaluating.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answerText, studentName, subject })
      });

      if (!response.ok) {
        throw new Error('Evaluation failed. Please try again.');
      }

      const data = await response.json();
      setMetrics(data);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page">
      <section className="hero card">
        <h1>Mechanistic Interpretability of Chain-of-Thought</h1>
        <p className="subtitle">Rubric-Aligned Circuits for Automated Answer Script Evaluation</p>
        <p>
          Upload an answer script and get rubric-based evaluation metrics for clarity, coherence,
          conceptual accuracy, reasoning depth, and actionability.
        </p>
      </section>

      <section className="grid">
        <form className="card" onSubmit={evaluateAnswer}>
          <h2>Upload & Evaluate</h2>

          <label>
            Student Name
            <input
              value={studentName}
              onChange={(e) => setStudentName(e.target.value)}
              placeholder="e.g. Ada Lovelace"
            />
          </label>

          <label>
            Subject
            <input
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="e.g. AI, Physics, History"
            />
          </label>

          <label>
            Upload Answer Sheet (.txt / .pdf)
            <input type="file" accept=".txt,.pdf,text/plain,application/pdf" onChange={handleUpload} />
          </label>

          <label>
            Or Paste Answer Text
            <textarea
              rows={10}
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
              placeholder="Paste the student's answer here"
            />
          </label>

          {error ? <p className="error">{error}</p> : null}

          <button type="submit" disabled={loading}>
            {loading ? 'Evaluating...' : 'Evaluate Answer'}
          </button>
        </form>

        <aside className="card">
          <h2>Evaluation Dashboard</h2>

          {hasResults ? (
            <>
              <Metric label="Overall" value={metrics.overall} />
              <Metric label="Clarity" value={metrics.clarity} />
              <Metric label="Coherence" value={metrics.coherence} />
              <Metric label="Rubric Alignment" value={metrics.rubricAlignment} />
              <Metric label="Conceptual Accuracy" value={metrics.conceptualAccuracy} />
              <Metric label="Reasoning Depth" value={metrics.reasoningDepth} />
              <Metric label="Actionability" value={metrics.actionability} />

              <h3>Strengths</h3>
              <ul>
                {metrics.strengths.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>

              <h3>Areas to Improve</h3>
              <ul>
                {metrics.improvements.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>

              <h3>Feedback Summary</h3>
              <p>{metrics.feedback}</p>
            </>
          ) : (
            <p>Run an evaluation to see rubric-aligned metrics here.</p>
          )}
        </aside>
      </section>
    </main>
  );
}

function Metric({ label, value }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}/100</strong>
    </div>
  );
}
