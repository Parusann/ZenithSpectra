interface TrendChipProps {
  name: string;
  velocity: number;
  className?: string;
}

export default function TrendChip({ name, velocity, className = "" }: TrendChipProps) {
  const isHot = velocity >= 5;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs font-medium transition-colors ${
        isHot
          ? "border-accent-gold/40 text-accent-gold bg-accent-gold-soft"
          : "border-border-glass text-text-secondary bg-white/5"
      } ${className}`}
    >
      <span>{name}</span>
      <span className="font-mono text-[10px] opacity-70">
        {velocity > 0 ? "+" : ""}
        {velocity.toFixed(1)}
      </span>
    </span>
  );
}
