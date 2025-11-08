import { Suspense } from 'react'
import DeviceList from '@/components/devices/device-list'
import DeviceScanner from '@/components/devices/device-scanner'

export const metadata = {
  title: '디바이스 관리 | CareOn Admin',
  description: 'Android 디바이스 검색 및 프로필 관리',
}

export default function DevicesPage() {
  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">디바이스 관리</h1>
          <p className="mt-2 text-gray-600">
            ADB 연결 디바이스 검색 및 프로필 설정
          </p>
        </div>
      </div>

      {/* Device Scanner Section */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          🔍 디바이스 스캔
        </h2>
        <p className="text-gray-600 mb-6">
          USB로 연결된 Android 디바이스를 검색합니다
        </p>
        <Suspense fallback={<div className="text-gray-500">Loading scanner...</div>}>
          <DeviceScanner />
        </Suspense>
      </div>

      {/* Device List Section */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          📱 등록된 디바이스 프로필
        </h2>
        <Suspense fallback={<div className="text-gray-500">Loading devices...</div>}>
          <DeviceList />
        </Suspense>
      </div>
    </div>
  )
}
