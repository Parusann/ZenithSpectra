"use client";

interface CredibilityBadgeProps {
  score: number | null;
  className?: string;
}

function getLevel(score: number): { label: string; color: string; bg: string } {
  if (score >= 85) return { label: "High", color: "text-success", bg: "bg-success/15" };
  if (score >= 60) return { label: "Medium", color: "text-warning", bg: "bg-warning/15" };
  return { label: "Low", color: "text-danger", bg: "bg-danger/15" };
}

export default function CredibilityBadge({ score, className = "" }: CredibilityBadgeProps) {
  if (score == null) return null;

  const { label, color, bg } = getLevel(score);

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono font-medium ${color} ${bg} ${className}`}
    >
      <span className="text-[10px]">{score}</span>
      <span className="opacity-70">•</span>
      <span>{label}</span>
    </span>
  );
}
