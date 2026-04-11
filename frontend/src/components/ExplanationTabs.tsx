"use client";

import { useState } from "react";

interface ExplanationTabsProps {
  beginner: string | null;
  intermediate: string | null;
  technical: string | null;
}

const TABS = [
  { key: "beginner", label: "Beginner" },
  { key: "intermediate", label: "Intermediate" },
  { key: "technical", label: "Technical" },
] as const;

type TabKey = (typeof TABS)[number]["key"];

export default function ExplanationTabs({ beginner, intermediate, technical }: ExplanationTabsProps) {
  const content: Record<TabKey, string | null> = { beginner, intermediate, technical };

  const available = TABS.filter((t) => content[t.key]);
  const [active, setActive] = useState<TabKey>(available[0]?.key ?? "beginner");

  if (available.length === 0) return null;

  return (
    <div>
      <div className="flex items-center gap-1 mb-4 border-b border-border-glass">
        {available.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActive(tab.key)}
            className={`px-4 py-2.5 text-sm font-medium transition-colors relative ${
              active === tab.key
                ? "text-accent-gold"
                : "text-text-muted hover:text-text-secondary"
            }`}
          >
            {tab.label}
            {active === tab.key && (
              <span className="absolute bottom-0 inset-x-0 h-0.5 bg-accent-gold rounded-t" />
            )}
          </button>
        ))}
      </div>
      <div className="text-sm text-text-secondary leading-relaxed whitespace-pre-line">
        {content[active] ?? "Explanation not yet available."}
      </div>
    </div>
  );
}
