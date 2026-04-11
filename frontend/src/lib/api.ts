const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export interface Source {
  id: string;
  name: string;
  source_type: string;
  base_url: string | null;
  institution: string | null;
  credibility_baseline: number;
  region: string | null;
  is_active: boolean;
  last_polled_at: string | null;
}

export interface ContentItem {
  id: string;
  title: string;
  original_url: string;
  author: string | null;
  published_at: string | null;
  ingested_at: string;
  category: string;
  tags: string[] | null;
  summary_quick: string | null;
  scientific_status: string | null;
  credibility_score: number | null;
  credibility_explanation: string | null;
  trend_score: number | null;
  source: Source | null;
}

export interface ContentItemDetail extends ContentItem {
  summary_expanded: string | null;
  explanation_beginner: string | null;
  explanation_intermediate: string | null;
  explanation_technical: string | null;
  cleaned_content: string | null;
}

export interface TrendingTopic {
  id: string;
  name: string;
  category: string;
  trend_score: number;
  mention_count_24h: number;
  mention_count_7d: number;
  velocity: number;
  updated_at: string;
}

export interface Category {
  slug: string;
  name: string;
  description: string;
  item_count: number;
}

export interface PaginatedResponse {
  items: ContentItem[];
  total: number;
  limit: number;
  offset: number;
}

export const api = {
  getItems: (params?: Record<string, string>) => {
    const query = params ? `?${new URLSearchParams(params)}` : "";
    return fetchAPI<PaginatedResponse>(`/api/v1/items${query}`);
  },
  getItem: (id: string) => fetchAPI<ContentItemDetail>(`/api/v1/items/${id}`),
  askQuestion: (id: string, question: string) =>
    fetchAPI<{ question: string; answer: string; item_id: string }>(
      `/api/v1/items/${id}/ask`,
      { method: "POST", body: JSON.stringify({ question }) },
    ),
  getCategories: () => fetchAPI<Category[]>("/api/v1/categories"),
  getTrends: (params?: Record<string, string>) => {
    const query = params ? `?${new URLSearchParams(params)}` : "";
    return fetchAPI<TrendingTopic[]>(`/api/v1/trends${query}`);
  },
  getSources: () => fetchAPI<Source[]>("/api/v1/sources"),
  search: (params: Record<string, string>) =>
    fetchAPI<PaginatedResponse>(`/api/v1/search?${new URLSearchParams(params)}`),
};
