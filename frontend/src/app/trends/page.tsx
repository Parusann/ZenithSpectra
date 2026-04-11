import { api } from "@/lib/api";
import GlassCard from "@/components/GlassCard";

export const revalidate = 120;

export default async function TrendsPage() {
  let trends: Awaited<ReturnType<typeof api.getTrends>>;
  try {
    trends = await api.getTrends({ limit: "30" });
  } catch {
    trends = [];
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Trending Topics</h1>
        <p className="text-text-secondary">
          Topics gaining momentum across science publications, ranked by velocity.
        </p>
      </header>

      {trends.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {trends.map((t, i) => (
            <GlassCard key={t.id} hover tilt padding="md">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-mono text-text-muted">
                      #{i + 1}
                    </span>
                    <span className="text-xs text-text-muted capitalize">
                      {t.category}
                    </span>
                  </div>
                  <h3 className="text-base font-semibold truncate">
                    {t.name}
                  </h3>
                  <div className="flex items-center gap-3 mt-2 text-xs text-text-muted">
                    <span>{t.mention_count_24h} mentions (24h)</span>
                    <span>{t.mention_count_7d} mentions (7d)</span>
                  </div>
                </div>
                <div className="text-right shrink-0">
                  <span
                    className={`text-lg font-mono font-bold ${
                      t.velocity >= 5 ? "text-accent-gold" : "text-text-secondary"
                    }`}
                  >
                    {t.velocity > 0 ? "+" : ""}
                    {t.velocity.toFixed(1)}
                  </span>
                  <p className="text-[10px] text-text-muted">velocity</p>
                </div>
              </div>
            </GlassCard>
          ))}
        </div>
      ) : (
        <p className="text-text-muted text-sm">
          No trending topics available yet. Data populates after ingestion runs.
        </p>
      )}
    </div>
  );
}
