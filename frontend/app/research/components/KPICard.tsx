interface KPICardProps {
  title: string
  value: string | number
  change?: string
  icon?: string
}

export default function KPICard({ title, value, change, icon }: KPICardProps) {
  return (
    <div className="bg-gray-800 rounded-lg p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="text-gray-400 text-sm">{title}</span>
        {icon && <span className="text-xl">{icon}</span>}
      </div>
      <div className="text-2xl font-bold">{value}</div>
      {change && (
        <div className={`text-xs mt-1 ${change.startsWith('+') ? 'text-green-400' : 'text-red-400'}`}>
          {change}
        </div>
      )}
    </div>
  )
}
