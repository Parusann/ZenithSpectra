import Link from "next/link";
import { api } from "@/lib/api";
import ContentItemCard from "@/components/ContentItemCard";
import TrendChip from "@/components/TrendChip";
import CategoryChip from "@/components/CategoryChip";
import { PageTransition, ScrollReveal, StaggerContainer, StaggerItem } from "@/components/MotionWrapper";
import HeroSection from "@/components/HeroSection";

export const revalidate = 120;

export default async function Home() {
  let items, trends, categories;

  try {
    [items, trends, categories] = await Promise.all([
      api.getItems({ limit: "12", sort: "ingested_at" }),
      api.getTrends({ limit: "8" }),
      api.getCategories(),
    ]);
  } catch {
    return <HomeFallback />;
  }

  const featured = items.items[0] ?? null;
  const feedItems = items.items.slice(featured ? 1 : 0);

  return (
    <PageTransition className="min-h-screen">
      <HeroSection />

      {/* Section separator */}
      <div className="section-divider max-w-5xl mx-auto mb-12" />

      {/* Trending Bar */}
      {trends.length > 0 && (
        <ScrollReveal>
          <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto mb-12">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-1.5 h-1.5 rounded-full bg-accent-gold animate-pulse-glow" />
              <h2 className="text-xs font-semibold text-accent-gold uppercase tracking-[0.2em]">
                Trending Now
              </h2>
              <div className="flex-1 section-divider" />
            </div>
            <div className="flex flex-wrap gap-2">
              {trends.map((t) => (
                <TrendChip key={t.id} name={t.name} velocity={t.velocity} />
              ))}
            </div>
          </section>
        </ScrollReveal>
      )}

      {/* Categories */}
      {categories.length > 0 && (
        <ScrollReveal>
          <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto mb-12">
            <div className="flex items-center gap-3 mb-5">
              <h2 className="text-xs font-semibold text-text-muted uppercase tracking-[0.2em]">
                Categories
              </h2>
              <div className="flex-1 section-divider" />
            </div>
            <div className="flex flex-wrap gap-2">
              {categories.map((c) => (
                <CategoryChip key={c.slug} slug={c.slug} name={c.name} />
              ))}
            </div>
          </section>
        </ScrollReveal>
      )}

      {/* Featured */}
      {featured && (
        <ScrollReveal>
          <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto mb-12">
            <div className="flex items-center gap-3 mb-5">
              <h2 className="text-xs font-semibold text-text-muted uppercase tracking-[0.2em]">
                Featured
              </h2>
              <div className="flex-1 section-divider" />
            </div>
            <ContentItemCard item={featured} />
          </section>
        </ScrollReveal>
      )}

      {/* Live Feed */}
      <section id="feed" className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto pb-24">
        <div className="flex items-center gap-3 mb-6">
          <h2 className="text-xs font-semibold text-text-muted uppercase tracking-[0.2em]">
            Latest
          </h2>
          <div className="flex-1 section-divider" />
          <Link href="/search" className="text-xs text-accent-gold hover:text-accent-gold-bright transition-colors">
            View all
          </Link>
        </div>
        <StaggerContainer className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
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
  return <HeroSection />;
}
