import { api } from "@/lib/api";
import GlassCard from "@/components/GlassCard";
import CredibilityBadge from "@/components/CredibilityBadge";
import { PageTransition, StaggerContainer, StaggerItem } from "@/components/MotionWrapper";

export const revalidate = 300;

export default async function SourcesPage() {
  let sources: Awaited<ReturnType<typeof api.getSources>>;
  try {
    sources = await api.getSources();
  } catch {
    sources = [];
  }

  return (
    <PageTransition className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Sources</h1>
        <p className="text-text-secondary">
          Trusted science publications and institutions we monitor, ranked by credibility.
        </p>
      </header>

      {sources.length > 0 ? (
        <StaggerContainer className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {sources.map((s) => (
            <StaggerItem key={s.id}><GlassCard hover tilt padding="md">
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-base font-semibold">{s.name}</h3>
                    {s.institution && (
                      <p className="text-xs text-text-muted mt-0.5">
                        {s.institution}
                      </p>
                    )}
                  </div>
                  <CredibilityBadge score={s.credibility_baseline} />
                </div>
                <div className="flex items-center gap-3 text-xs text-text-muted">
                  <span className="capitalize">{s.source_type.replace(/_/g, " ")}</span>
                  {s.region && (
                    <>
                      <span className="opacity-40">•</span>
                      <span>{s.region}</span>
                    </>
                  )}
                  <span className={`ml-auto ${s.is_active ? "text-success" : "text-danger"}`}>
                    {s.is_active ? "Active" : "Inactive"}
                  </span>
                </div>
              </div>
            </GlassCard></StaggerItem>
          ))}
        </StaggerContainer>
      ) : (
        <p className="text-text-muted text-sm">No sources configured yet.</p>
      )}
    </PageTransition>
  );
}
