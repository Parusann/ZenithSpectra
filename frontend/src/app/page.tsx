import Link from "next/link";
import { api } from "@/lib/api";
import ContentItemCard from "@/components/ContentItemCard";
import TrendChip from "@/components/TrendChip";
import CategoryChip from "@/components/CategoryChip";
import GlassCard from "@/components/GlassCard";
import { PageTransition, ScrollReveal, StaggerContainer, StaggerItem } from "@/components/MotionWrapper";

export const revalidate = 120; // ISR: refresh every 2 minutes

export default async function Home() {
  let items, trends, categories;

  try {
    [items, trends, categories] = await Promise.all([
      api.getItems({ limit: "12", sort: "ingested_at" }),
      api.getTrends({ limit: "8" }),
      api.getCategories(),
    ]);
  } catch {
    // API not available — show fallback
    return <HomeFallback />;
  }

  const featured = items.items[0] ?? null;
  const feedItems = items.items.slice(featured ? 1 : 0);

  return (
    <PageTransition className="min-h-screen">
      {/* Hero */}
      <section className="relative flex items-center justify-center min-h-[60vh] px-4">
        <div className="absolute inset-0 bg-gradient-to-b from-accent-gold/5 via-transparent to-transparent pointer-events-none" />
        <div className="relative text-center max-w-3xl mx-auto space-y-6">
          <h1 className="text-5xl sm:text-6xl font-bold tracking-tight">
            See the full picture.
            <br />
            <span className="text-accent-gold">Trust the source.</span>
          </h1>
          <p className="text-lg text-text-secondary max-w-xl mx-auto">
            AI-powered science intelligence tracking live developments in space
            exploration, quantum physics, and frontier research.
          </p>
          <div className="flex items-center justify-center gap-3 pt-2">
            <Link
              href="#feed"
              className="px-6 py-2.5 bg-accent-gold/15 border border-accent-gold/40 text-accent-gold rounded-xl text-sm font-medium hover:bg-accent-gold/25 transition-colors"
            >
              Explore Feed
            </Link>
            <Link
              href="/trends"
              className="px-6 py-2.5 bg-white/5 border border-border-glass text-text-secondary rounded-xl text-sm font-medium hover:border-border-active hover:text-text-primary transition-colors"
            >
              View Trends
            </Link>
          </div>
        </div>
      </section>

      {/* Trending Bar */}
      {trends.length > 0 && (
        <ScrollReveal><section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto mb-12">
          <div className="flex items-center gap-3 mb-4">
            <h2 className="text-sm font-semibold text-text-muted uppercase tracking-wider">
              Trending Now
            </h2>
            <div className="flex-1 h-px bg-border-glass" />
          </div>
          <div className="flex flex-wrap gap-2">
            {trends.map((t) => (
              <TrendChip key={t.id} name={t.name} velocity={t.velocity} />
            ))}
          </div>
        </section></ScrollReveal>
      )}

      {/* Categories */}
      {categories.length > 0 && (
        <ScrollReveal><section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto mb-12">
          <div className="flex items-center gap-3 mb-4">
            <h2 className="text-sm font-semibold text-text-muted uppercase tracking-wider">
              Categories
            </h2>
            <div className="flex-1 h-px bg-border-glass" />
          </div>
          <div className="flex flex-wrap gap-2">
            {categories.map((c) => (
              <CategoryChip key={c.slug} slug={c.slug} name={c.name} />
            ))}
          </div>
        </section></ScrollReveal>
      )}

      {/* Featured */}
      {featured && (
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto mb-12">
          <div className="flex items-center gap-3 mb-4">
            <h2 className="text-sm font-semibold text-text-muted uppercase tracking-wider">
              Featured
            </h2>
            <div className="flex-1 h-px bg-border-glass" />
          </div>
          <ContentItemCard item={featured} />
        </section>
      )}

      {/* Live Feed */}
      <section id="feed" className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto pb-20">
        <div className="flex items-center gap-3 mb-6">
          <h2 className="text-sm font-semibold text-text-muted uppercase tracking-wider">
            Latest
          </h2>
          <div className="flex-1 h-px bg-border-glass" />
          <Link
            href="/search"
            className="text-xs text-accent-gold hover:underline"
          >
            View all
          </Link>
        </div>
        <StaggerContainer className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {feedItems.map((item) => (
            <StaggerItem key={item.id}>
              <ContentItemCard item={item} />
            </StaggerItem>
          ))}
        </StaggerContainer>
      </section>
    </PageTransition>
  );
}

function HomeFallback() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)]">
      <GlassCard hover={false} tilt={false} padding="lg">
        <div className="text-center max-w-md space-y-4">
          <h1 className="text-4xl font-semibold">ZenithSpectra</h1>
          <p className="text-text-secondary text-lg font-light">
            See the full picture. Trust the source.
          </p>
          <p className="text-text-muted text-sm font-mono">
            Connect the backend API to see live content.
          </p>
        </div>
      </GlassCard>
    </div>
  );
}
