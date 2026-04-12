"use client";

import GlassCard from "@/components/GlassCard";

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] px-4">
      <GlassCard hover={false} tilt={false} padding="lg">
        <div className="text-center max-w-md space-y-4">
          <h2 className="text-2xl font-bold text-text-primary">
            Something went wrong
          </h2>
          <p className="text-sm text-text-secondary">
            {error.message || "An unexpected error occurred while loading this page."}
          </p>
          <button
            onClick={reset}
            className="px-5 py-2.5 bg-accent-gold/15 border border-accent-gold/40 text-accent-gold rounded-xl text-sm font-medium hover:bg-accent-gold/25 transition-colors"
          >
            Try again
          </button>
        </div>
      </GlassCard>
    </div>
  );
}
