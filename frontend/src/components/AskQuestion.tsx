"use client";

import { useState, useCallback } from "react";
import { api } from "@/lib/api";

interface AskQuestionProps {
  itemId: string;
}

export default function AskQuestion({ itemId }: AskQuestionProps) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      const trimmed = question.trim();
      if (!trimmed || loading) return;

      setLoading(true);
      setError(null);
      setAnswer(null);

      try {
        const res = await api.askQuestion(itemId, trimmed);
        setAnswer(res.answer);
      } catch {
        setError("Failed to get an answer. Please try again.");
      } finally {
        setLoading(false);
      }
    },
    [question, itemId, loading],
  );

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about this article..."
          className="flex-1 px-4 py-2.5 bg-white/5 border border-border-glass rounded-xl text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-gold/40 transition-colors"
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="px-5 py-2.5 bg-accent-gold/15 border border-accent-gold/40 text-accent-gold rounded-xl text-sm font-medium hover:bg-accent-gold/25 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading ? "Asking..." : "Ask"}
        </button>
      </form>

      {answer && (
        <div className="p-4 bg-white/5 border border-border-glass rounded-xl">
          <p className="text-xs text-text-muted mb-2 font-medium">Answer</p>
          <p className="text-sm text-text-secondary leading-relaxed whitespace-pre-line">
            {answer}
          </p>
        </div>
      )}

      {error && (
        <p className="text-sm text-danger">{error}</p>
      )}
    </div>
  );
}
