import { notFound } from "next/navigation";
import { api } from "@/lib/api";
import ContentItemCard from "@/components/ContentItemCard";

export const revalidate = 120;

const CATEGORY_META: Record<string, { name: string; description: string }> = {
  space: {
    name: "Space Exploration",
    description: "Missions, launches, planetary science, and the search for life beyond Earth.",
  },
  quantum: {
    name: "Quantum Computing & Physics",
    description: "Quantum hardware, algorithms, error correction, and fundamental quantum mechanics.",
  },
  theoretical: {
    name: "Theoretical Physics",
    description: "String theory, cosmology, dark matter, dark energy, and fundamental forces.",
  },
  frontier: {
    name: "Frontier Science",
    description: "Breakthrough discoveries, interdisciplinary research, and emerging scientific fields.",
  },
};

interface Props {
  params: Promise<{ slug: string }>;
}

export default async function CategoryPage({ params }: Props) {
  const { slug } = await params;
  const meta = CATEGORY_META[slug];
  if (!meta) notFound();

  let data;
  try {
    data = await api.getItems({ category: slug, limit: "24", sort: "ingested_at" });
  } catch {
    data = { items: [], total: 0 };
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{meta.name}</h1>
        <p className="text-text-secondary">{meta.description}</p>
        <p className="text-xs text-text-muted mt-2 font-mono">
          {data.total} article{data.total !== 1 ? "s" : ""}
        </p>
      </header>

      {data.items.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {data.items.map((item) => (
            <ContentItemCard key={item.id} item={item} />
          ))}
        </div>
      ) : (
        <p className="text-text-muted text-sm">
          No articles in this category yet.
        </p>
      )}
    </div>
  );
}
