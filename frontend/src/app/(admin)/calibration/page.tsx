import { Suspense } from 'react'
import CalibrationWizard from '@/components/calibration/calibration-wizard'

export const metadata = {
  title: '좌표 캘리브레이션 | CareOn Admin',
  description: '인터랙티브 UI 요소 좌표 설정',
}

export default function CalibrationPage({
  searchParams,
}: {
  searchParams: Promise<{ profile?: string; device?: string }>
}) {
  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          🎯 인터랙티브 캘리브레이션
        </h1>
        <p className="mt-2 text-gray-600">
          디바이스 화면을 클릭하여 UI 요소 좌표를 정확하게 설정합니다
        </p>
      </div>

      {/* Instructions Card */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-blue-900 mb-3">
          📖 사용 방법
        </h2>
        <ol className="space-y-2 text-blue-800">
          <li className="flex items-start">
            <span className="font-bold mr-2">1.</span>
            <span>디바이스를 선택하고 캘리브레이션을 시작합니다</span>
          </li>
          <li className="flex items-start">
            <span className="font-bold mr-2">2.</span>
            <span>
              실시간으로 표시되는 디바이스 화면에서 안내에 따라 UI 요소를 클릭합니다
            </span>
          </li>
          <li className="flex items-start">
            <span className="font-bold mr-2">3.</span>
            <span>
              11개의 UI 요소 좌표를 모두 설정하면 자동 포스팅 준비가 완료됩니다
            </span>
          </li>
        </ol>
      </div>

      {/* Calibration Wizard */}
      <Suspense
        fallback={
          <div className="flex items-center justify-center h-96">
            <div className="text-gray-500">Loading calibration wizard...</div>
          </div>
        }
      >
        <CalibrationWizard searchParams={searchParams} />
      </Suspense>
    </div>
  )
}
