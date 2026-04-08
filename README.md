# Mechanistic Interpretability of Chain-of-Thought: Rubric-Aligned Circuits for Automated Answer Script Evaluation

A full-stack Next.js website for uploading an answer sheet and evaluating it against rubric-aligned metrics.

## Features
- Upload answer scripts (`.txt` and basic `.pdf` text content).
- Paste answer text directly.
- Generate evaluation metrics:
  - Overall score
  - Clarity
  - Coherence
  - Rubric alignment
  - Conceptual accuracy
  - Reasoning depth
  - Actionability
- Displays strengths, improvement areas, and feedback summary.

## Local development
```bash
npm install
npm run dev
```
Then open `http://localhost:3000`.

## Deploy to Vercel
1. Push this repository to GitHub.
2. In Vercel, click **Add New Project** and import your repo.
3. Framework preset: **Next.js** (auto-detected).
4. Build command: `next build` (default).
5. Output: `.next` (default).
6. Click **Deploy**.

### Vercel CLI (optional)
```bash
npm i -g vercel
vercel
vercel --prod
```

## Notes
- PDF extraction here relies on browser `File.text()` and is best-effort.
- For production-grade PDF/DOCX parsing and model-based scoring, add server-side parsers and LLM integration.


## Troubleshooting
- If you see `Cannot find module "tailwindcss"`, this project does **not** require Tailwind. Ensure `postcss.config.mjs` is present with an empty `plugins` object and remove old Tailwind-specific PostCSS configs left from other templates.
