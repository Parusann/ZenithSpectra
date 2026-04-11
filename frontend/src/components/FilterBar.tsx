"use client";

interface FilterOption {
  value: string;
  label: string;
}

interface FilterBarProps {
  categories: FilterOption[];
  activeCategory: string;
  onCategoryChange: (value: string) => void;
  sortOptions?: FilterOption[];
  activeSort?: string;
  onSortChange?: (value: string) => void;
  className?: string;
}

export default function FilterBar({
  categories,
  activeCategory,
  onCategoryChange,
  sortOptions,
  activeSort,
  onSortChange,
  className = "",
}: FilterBarProps) {
  return (
    <div className={`flex items-center gap-4 flex-wrap ${className}`}>
      {/* Category pills */}
      <div className="flex items-center gap-1.5 flex-wrap">
        {categories.map((cat) => (
          <button
            key={cat.value}
            onClick={() => onCategoryChange(cat.value)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
              activeCategory === cat.value
                ? "bg-accent-gold/20 text-accent-gold border border-accent-gold/40"
                : "bg-white/5 text-text-secondary border border-border-glass hover:border-border-active"
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Sort dropdown */}
      {sortOptions && onSortChange && (
        <select
          value={activeSort}
          onChange={(e) => onSortChange(e.target.value)}
          className="bg-white/5 border border-border-glass rounded-lg px-3 py-1.5 text-xs text-text-secondary focus:outline-none focus:border-accent-gold/40 transition-colors"
        >
          {sortOptions.map((opt) => (
            <option key={opt.value} value={opt.value} className="bg-bg-secondary text-text-primary">
              {opt.label}
            </option>
          ))}
        </select>
      )}
    </div>
  );
}
