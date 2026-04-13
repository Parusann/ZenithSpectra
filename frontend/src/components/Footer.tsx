import Link from "next/link";

export default function Footer() {
  return (
    <footer className="relative z-10 mt-auto">
      <div className="section-divider" />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex flex-col items-center sm:items-start gap-1">
            <span className="text-sm font-bold tracking-tight">
              Zenith<span className="text-gradient-gold">Spectra</span>
            </span>
            <span className="text-xs text-text-muted">
              AI-Powered Science Intelligence
            </span>
          </div>
          <nav className="flex items-center gap-5 text-xs text-text-muted">
            <Link href="/" className="hover:text-text-primary transition-colors">Feed</Link>
            <Link href="/trends" className="hover:text-text-primary transition-colors">Trends</Link>
            <Link href="/sources" className="hover:text-text-primary transition-colors">Sources</Link>
            <Link href="/about" className="hover:text-text-primary transition-colors">About</Link>
          </nav>
        </div>
      </div>
    </footer>
  );
}
