import { Skeleton, FeedSkeleton } from "@/components/Skeleton";

export default function CategoryLoading() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Skeleton className="h-9 w-64 mb-2" />
      <Skeleton className="h-5 w-96 mb-2" />
      <Skeleton className="h-4 w-20 mb-8" />
      <FeedSkeleton count={6} />
    </div>
  );
}
