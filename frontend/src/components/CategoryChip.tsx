import Link from "next/link";

const CATEGORY_COLORS: Record<string, string> = {
  space: "border-blue-500/30 text-blue-400",
  quantum: "border-purple-500/30 text-purple-400",
  theoretical: "border-cyan-500/30 text-cyan-400",
  frontier: "border-accent-gold/30 text-accent-gold",
};

interface CategoryChipProps {
  slug: string;
  name?: string;
  linked?: boolean;
  className?: string;
}

export default function CategoryChip({ slug, name, linked = true, className = "" }: CategoryChipProps) {
  const display = name ?? slug.charAt(0).toUpperCase() + slug.slice(1);
  const colors = CATEGORY_COLORS[slug] ?? "border-border-glass text-text-secondary";

  const chip = (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full border text-xs font-medium ${colors} ${className}`}>
      {display}
    </span>
  );

  if (!linked) return chip;

  return (
    <Link href={`/category/${slug}`} className="hover:opacity-80 transition-opacity">
      {chip}
    </Link>
  );
}
