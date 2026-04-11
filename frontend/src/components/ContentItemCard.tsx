"use client";

import Link from "next/link";
import type { ContentItem } from "@/lib/api";
import GlassCard from "./GlassCard";
import CredibilityBadge from "./CredibilityBadge";
import ScientificStatusLabel from "./ScientificStatusLabel";
import CategoryChip from "./CategoryChip";

interface ContentItemCardProps {
  item: ContentItem;
  className?: string;
}

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export default function ContentItemCard({ item, className = "" }: ContentItemCardProps) {
  return (
    <Link href={`/item/${item.id}`} className={`block ${className}`}>
      <GlassCard hover padding="md">
        <div className="flex flex-col gap-3">
          {/* Top row: category + scientific status */}
          <div className="flex items-center gap-2 flex-wrap">
            <CategoryChip slug={item.category} linked={false} />
            <ScientificStatusLabel status={item.scientific_status} />
          </div>

          {/* Title */}
          <h3 className="text-base font-semibold leading-snug line-clamp-2 text-text-primary">
            {item.title}
          </h3>

          {/* Summary */}
          {item.summary_quick && (
            <p className="text-sm text-text-secondary leading-relaxed line-clamp-2">
              {item.summary_quick}
            </p>
          )}

          {/* Bottom row: source, time, credibility */}
          <div className="flex items-center justify-between gap-2 pt-1">
            <div className="flex items-center gap-2 text-xs text-text-muted min-w-0">
              {item.source && (
                <span className="truncate">{item.source.name}</span>
              )}
              {item.published_at && (
                <>
                  <span className="opacity-40">•</span>
                  <span className="shrink-0">{timeAgo(item.published_at)}</span>
                </>
              )}
            </div>
            <CredibilityBadge score={item.credibility_score} />
          </div>
        </div>
      </GlassCard>
    </Link>
  );
}
