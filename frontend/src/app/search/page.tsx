import { api } from "@/lib/api";
import ContentItemCard from "@/components/ContentItemCard";
import SearchBar from "@/components/SearchBar";

export const revalidate = 0; // always fresh for search

interface Props {
  searchParams: Promise<{ q?: string; category?: string }>;
}

export default async function SearchPage({ searchParams }: Props) {
  const { q, category } = await searchParams;

  let results = null;
  if (q) {
    try {
      const params: Record<string, string> = { q };
      if (category) params.category = category;
      results = await api.search(params);
    } catch {
      results = { items: [], total: 0 };
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-4">Search</h1>
        <SearchBar defaultValue={q ?? ""} className="max-w-xl" />
      </header>

      {q && results && (
        <>
          <p className="text-sm text-text-muted mb-6">
            {results.total} result{results.total !== 1 ? "s" : ""} for{" "}
            <span className="text-text-secondary font-medium">&ldquo;{q}&rdquo;</span>
          </p>

          {results.items.length > 0 ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {results.items.map((item) => (
                <ContentItemCard key={item.id} item={item} />
              ))}
            </div>
          ) : (
            <p className="text-text-muted text-sm">
              No results found. Try a different search term.
            </p>
          )}
        </>
      )}

      {!q && (
        <p className="text-text-muted text-sm">
          Enter a search term to find articles, topics, and sources.
        </p>
      )}
    </div>
  );
}
