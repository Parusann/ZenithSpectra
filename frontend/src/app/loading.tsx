import { Skeleton, FeedSkeleton } from "@/components/Skeleton";

export default function HomeLoading() {
  return (
    <div className="min-h-screen">
      {/* Hero skeleton */}
      <section className="flex items-center justify-center min-h-[60vh] px-4">
        <div className="text-center max-w-3xl mx-auto space-y-6">
          <Skeleton className="h-14 w-96 mx-auto" />
          <Skeleton className="h-14 w-72 mx-auto" />
          <Skeleton className="h-6 w-80 mx-auto" />
          <div className="flex justify-center gap-3 pt-2">
            <Skeleton className="h-10 w-32 rounded-xl" />
            <Skeleton className="h-10 w-32 rounded-xl" />
          </div>
        </div>
      </section>

      {/* Trending skeleton */}
      <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto mb-12">
        <Skeleton className="h-4 w-32 mb-4" />
        <div className="flex gap-2">
          {Array.from({ length: 5 }, (_, i) => (
            <Skeleton key={i} className="h-8 w-24 rounded-full" />
          ))}
        </div>
      </section>

      {/* Feed skeleton */}
      <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto pb-20">
        <Skeleton className="h-4 w-20 mb-6" />
        <FeedSkeleton count={6} />
      </section>
    </div>
  );
}
