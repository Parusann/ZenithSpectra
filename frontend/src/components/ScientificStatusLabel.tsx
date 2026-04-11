const STATUS_CONFIG: Record<string, { label: string; color: string; bg: string }> = {
  peer_reviewed: { label: "Peer Reviewed", color: "text-success", bg: "bg-success/10" },
  preprint: { label: "Preprint", color: "text-warning", bg: "bg-warning/10" },
  press_release: { label: "Press Release", color: "text-accent-gold", bg: "bg-accent-gold-soft" },
  news_coverage: { label: "News Coverage", color: "text-text-secondary", bg: "bg-white/5" },
  editorial: { label: "Editorial", color: "text-text-muted", bg: "bg-white/5" },
};

interface ScientificStatusLabelProps {
  status: string | null;
  className?: string;
}

export default function ScientificStatusLabel({ status, className = "" }: ScientificStatusLabelProps) {
  if (!status) return null;

  const config = STATUS_CONFIG[status] ?? {
    label: status.replace(/_/g, " "),
    color: "text-text-muted",
    bg: "bg-white/5",
  };

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${config.color} ${config.bg} ${className}`}>
      {config.label}
    </span>
  );
}
