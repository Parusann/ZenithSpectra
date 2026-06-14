const STATUS_CONFIG: Record<string, { label: string; color: string; bg: string }> = {
  established: { label: "Established", color: "text-success", bg: "bg-success/10" },
  supported: { label: "Supported", color: "text-success", bg: "bg-success/10" },
  active_research: { label: "Active Research", color: "text-accent-gold", bg: "bg-accent-gold-soft" },
  speculative: { label: "Speculative", color: "text-warning", bg: "bg-warning/10" },
  highly_speculative: { label: "Highly Speculative", color: "text-warning", bg: "bg-warning/10" },
  media_hype: { label: "Media Hype", color: "text-text-muted", bg: "bg-white/5" },
};

interface ScientificStatusLabelProps {
  status: string | null;
  className?: string;
}

export default function ScientificStatusLabel({ status, className = "" }: ScientificStatusLabelProps) {
  if (!status) return null;

  const config = STATUS_CONFIG[status.toLowerCase()] ?? {
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
