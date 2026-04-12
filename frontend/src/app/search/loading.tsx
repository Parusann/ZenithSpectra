import { Skeleton, FeedSkeleton } from "@/components/Skeleton";

export default function SearchLoading() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Skeleton className="h-9 w-32 mb-4" />
      <Skeleton className="h-10 w-full max-w-xl rounded-xl mb-6" />
      <Skeleton className="h-4 w-48 mb-6" />
      <FeedSkeleton count={6} />
    </div>
  );
}
