import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-4rem)] px-4">
      <div className="glass-panel p-10 text-center max-w-md space-y-5">
        <p className="text-7xl font-bold font-mono text-gradient-gold">404</p>
        <h2 className="text-xl font-semibold text-text-primary">
          Page not found
        </h2>
        <p className="text-sm text-text-secondary">
          The page you&apos;re looking for doesn&apos;t exist or has been moved.
        </p>
        <Link href="/" className="btn-primary inline-flex">
          Back to Feed
        </Link>
      </div>
    </div>
  );
}
