import GlassCard from "@/components/GlassCard";

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">
          About <span className="text-accent-gold">ZenithSpectra</span>
        </h1>
      </header>

      <div className="space-y-6">
        <GlassCard hover={false} tilt={false} padding="lg">
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">What is ZenithSpectra?</h2>
            <p className="text-text-secondary leading-relaxed">
              ZenithSpectra is an AI-powered science intelligence platform that tracks live
              developments in space exploration, quantum computing, theoretical physics, and
              frontier research. It aggregates content from trusted scientific sources, scores
              credibility, identifies trends, and provides multi-level explanations.
            </p>
          </div>
        </GlassCard>

        <GlassCard hover={false} tilt={false} padding="lg">
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">How It Works</h2>
            <div className="space-y-3 text-sm text-text-secondary leading-relaxed">
              <p>
                <span className="text-text-primary font-medium">Ingestion:</span>{" "}
                RSS feeds from publications like NASA, ESA, Nature, Science, and arXiv
                are polled on a schedule. New articles are parsed, cleaned, and classified
                by category.
              </p>
              <p>
                <span className="text-text-primary font-medium">Credibility Scoring:</span>{" "}
                Each article receives a credibility score based on the source baseline,
                presence of primary data, scientific hedging language, and hype detection.
              </p>
              <p>
                <span className="text-text-primary font-medium">Trend Detection:</span>{" "}
                Keywords are extracted from titles and tracked over rolling time windows.
                Velocity — the rate of mention acceleration — identifies emerging topics.
              </p>
              <p>
                <span className="text-text-primary font-medium">AI Explanations:</span>{" "}
                Articles can be explained at beginner, intermediate, and technical levels
                using LLM-generated summaries. You can also ask follow-up questions.
              </p>
            </div>
          </div>
        </GlassCard>

        <GlassCard hover={false} tilt={false} padding="lg">
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">Technology</h2>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-text-muted mb-1">Frontend</p>
                <p className="text-text-secondary">Next.js, TypeScript, Tailwind CSS</p>
              </div>
              <div>
                <p className="text-text-muted mb-1">Backend</p>
                <p className="text-text-secondary">FastAPI, SQLAlchemy, PostgreSQL</p>
              </div>
              <div>
                <p className="text-text-muted mb-1">AI</p>
                <p className="text-text-secondary">Ollama / Groq LLM Providers</p>
              </div>
              <div>
                <p className="text-text-muted mb-1">Data</p>
                <p className="text-text-secondary">RSS Ingestion, Full-Text Search</p>
              </div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
