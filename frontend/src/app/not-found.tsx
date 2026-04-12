import Link from "next/link";
import GlassCard from "@/components/GlassCard";

export default function NotFound() {
  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] px-4">
      <GlassCard hover={false} tilt={false} padding="lg">
        <div className="text-center max-w-md space-y-4">
          <p className="text-6xl font-bold font-mono text-accent-gold">404</p>
          <h2 className="text-xl font-semibold text-text-primary">
            Page not found
          </h2>
          <p className="text-sm text-text-secondary">
            The page you&apos;re looking for doesn&apos;t exist or has been moved.
          </p>
          <Link
            href="/"
            className="inline-block px-5 py-2.5 bg-accent-gold/15 border border-accent-gold/40 text-accent-gold rounded-xl text-sm font-medium hover:bg-accent-gold/25 transition-colors"
          >
            Back to Feed
          </Link>
        </div>
      </GlassCard>
    </div>
  );
}
