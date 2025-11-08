import Link from 'next/link'
import { Suspense } from 'react'

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Admin Navigation */}
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <Link
                href="/"
                className="flex items-center px-4 text-gray-900 font-bold text-xl hover:text-blue-600 transition-colors"
              >
                🤖 CareOn Admin
              </Link>

              <div className="ml-8 flex space-x-4">
                <Link
                  href="/devices"
                  className="inline-flex items-center px-4 py-2 border-b-2 border-transparent text-sm font-medium text-gray-700 hover:text-blue-600 hover:border-blue-600 transition-all"
                >
                  📱 디바이스
                </Link>

                <Link
                  href="/calibration"
                  className="inline-flex items-center px-4 py-2 border-b-2 border-transparent text-sm font-medium text-gray-700 hover:text-purple-600 hover:border-purple-600 transition-all"
                >
                  🎯 캘리브레이션
                </Link>
              </div>
            </div>

            <div className="flex items-center">
              <span className="text-sm text-gray-500">Admin Dashboard</span>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Suspense
          fallback={
            <div className="flex items-center justify-center h-64">
              <div className="text-gray-500">Loading...</div>
            </div>
          }
        >
          {children}
        </Suspense>
      </main>
    </div>
  )
}
