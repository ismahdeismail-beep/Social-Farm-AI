export default function LoadingSkeleton() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-4 bg-gray-700 rounded w-1/4" />
      <div className="h-4 bg-gray-700 rounded w-1/2" />
      <div className="h-32 bg-gray-700 rounded" />
      <div className="grid grid-cols-3 gap-4">
        <div className="h-20 bg-gray-700 rounded" />
        <div className="h-20 bg-gray-700 rounded" />
        <div className="h-20 bg-gray-700 rounded" />
      </div>
    </div>
  )
}
