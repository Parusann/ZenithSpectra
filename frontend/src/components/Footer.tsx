import Link from "next/link";

export default function Footer() {
  return (
    <footer className="relative z-10 border-t border-border-glass mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold">
              Zenith<span className="text-accent-gold">Spectra</span>
            </span>
            <span className="text-xs text-text-muted">
              AI-Powered Science Intelligence
            </span>
          </div>
          <nav className="flex items-center gap-4 text-xs text-text-muted">
            <Link href="/" className="hover:text-text-secondary transition-colors">Feed</Link>
            <Link href="/trends" className="hover:text-text-secondary transition-colors">Trends</Link>
            <Link href="/sources" className="hover:text-text-secondary transition-colors">Sources</Link>
            <Link href="/about" className="hover:text-text-secondary transition-colors">About</Link>
          </nav>
        </div>
      </div>
    </footer>
  );
}
