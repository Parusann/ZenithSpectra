import { notFound } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import type { ContentItemDetail } from "@/lib/api";
import { PageTransition } from "@/components/MotionWrapper";
import GlassCard from "@/components/GlassCard";
import CredibilityBadge from "@/components/CredibilityBadge";
import ScientificStatusLabel from "@/components/ScientificStatusLabel";
import CategoryChip from "@/components/CategoryChip";
import ExplanationTabs from "@/components/ExplanationTabs";
import AskQuestion from "@/components/AskQuestion";

export const revalidate = 300;

interface Props {
  params: Promise<{ id: string }>;
}

export default async function ItemDetailPage({ params }: Props) {
  const { id } = await params;

  let item: ContentItemDetail;
  try {
    item = await api.getItem(id);
  } catch {
    notFound();
  }

  const publishedDate = item.published_at
    ? new Date(item.published_at).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      })
    : null;

  return (
    <PageTransition className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-xs text-text-muted mb-6">
        <Link href="/" className="hover:text-text-secondary transition-colors">
          Feed
        </Link>
        <span>/</span>
        <Link
          href={`/category/${item.category}`}
          className="hover:text-text-secondary transition-colors"
        >
          {item.category.charAt(0).toUpperCase() + item.category.slice(1)}
        </Link>
        <span>/</span>
        <span className="text-text-secondary truncate max-w-[200px]">
          {item.title}
        </span>
      </nav>

      {/* Header */}
      <header className="mb-8 space-y-4">
        <div className="flex items-center gap-2 flex-wrap">
          <CategoryChip slug={item.category} />
          <ScientificStatusLabel status={item.scientific_status} />
        </div>

        <h1 className="text-3xl sm:text-4xl font-bold leading-tight">
          {item.title}
        </h1>

        <div className="flex items-center gap-4 text-sm text-text-muted flex-wrap">
          {item.source && <span>{item.source.name}</span>}
          {item.author && (
            <>
              <span className="opacity-40">•</span>
              <span>{item.author}</span>
            </>
          )}
          {publishedDate && (
            <>
              <span className="opacity-40">•</span>
              <span>{publishedDate}</span>
            </>
          )}
          <CredibilityBadge score={item.credibility_score} />
        </div>
      </header>

      {/* Summary */}
      {(item.summary_quick || item.summary_expanded) && (
        <GlassCard hover={false} tilt={false} padding="lg" className="mb-8">
          <div className="space-y-3">
            <h2 className="text-sm font-semibold text-text-muted uppercase tracking-wider">
              Summary
            </h2>
            {item.summary_quick && (
              <p className="text-text-primary leading-relaxed">
                {item.summary_quick}
              </p>
            )}
            {item.summary_expanded && (
              <p className="text-sm text-text-secondary leading-relaxed">
                {item.summary_expanded}
              </p>
            )}
          </div>
        </GlassCard>
      )}

      {/* Credibility */}
      {item.credibility_explanation && (
        <GlassCard hover={false} tilt={false} padding="lg" className="mb-8">
          <div className="space-y-3">
            <h2 className="text-sm font-semibold text-text-muted uppercase tracking-wider">
              Credibility Analysis
            </h2>
            <p className="text-sm text-text-secondary leading-relaxed">
              {item.credibility_explanation}
            </p>
          </div>
        </GlassCard>
      )}

      {/* Explanations */}
      {(item.explanation_beginner || item.explanation_intermediate || item.explanation_technical) && (
        <GlassCard hover={false} tilt={false} padding="lg" className="mb-8">
          <h2 className="text-sm font-semibold text-text-muted uppercase tracking-wider mb-4">
            Explanations
          </h2>
          <ExplanationTabs
            beginner={item.explanation_beginner}
            intermediate={item.explanation_intermediate}
            technical={item.explanation_technical}
          />
        </GlassCard>
      )}

      {/* Tags */}
      {item.tags && item.tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-8">
          {item.tags.map((tag) => (
            <span
              key={tag}
              className="px-2.5 py-1 bg-white/5 border border-border-glass rounded-full text-xs text-text-muted"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* Ask a Question */}
      <GlassCard hover={false} tilt={false} padding="lg" className="mb-8">
        <h2 className="text-sm font-semibold text-text-muted uppercase tracking-wider mb-4">
          Ask a Question
        </h2>
        <AskQuestion itemId={item.id} />
      </GlassCard>

      {/* Source link */}
      <div className="flex items-center gap-4">
        <a
          href={item.original_url}
          target="_blank"
          rel="noopener noreferrer"
          className="px-5 py-2.5 bg-accent-gold/15 border border-accent-gold/40 text-accent-gold rounded-xl text-sm font-medium hover:bg-accent-gold/25 transition-colors"
        >
          Read Original Source
        </a>
        <Link
          href="/"
          className="px-5 py-2.5 bg-white/5 border border-border-glass text-text-secondary rounded-xl text-sm font-medium hover:border-border-active transition-colors"
        >
          Back to Feed
        </Link>
      </div>
    </PageTransition>
  );
}
