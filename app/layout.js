import './globals.css';

export const metadata = {
  title: 'Mechanistic Interpretability of Chain-of-Thought',
  description: 'Rubric-aligned circuits for automated answer script evaluation'
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
