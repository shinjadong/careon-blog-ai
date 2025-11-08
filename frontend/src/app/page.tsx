import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-8">
      <div className="max-w-4xl w-full bg-white rounded-2xl shadow-xl p-12">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            CareOn Blog Automation
          </h1>
          <p className="text-xl text-gray-600">
            프로덕션급 모바일 블로그 자동화 시스템
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <Link
            href="/devices"
            className="group block p-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
          >
            <div className="text-white">
              <h2 className="text-3xl font-bold mb-3">📱 디바이스 관리</h2>
              <p className="text-blue-100 text-lg">
                ADB 연결, 디바이스 검색, 프로필 관리
              </p>
            </div>
          </Link>

          <Link
            href="/calibration"
            className="group block p-8 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl hover:from-purple-600 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
          >
            <div className="text-white">
              <h2 className="text-3xl font-bold mb-3">🎯 좌표 캘리브레이션</h2>
              <p className="text-purple-100 text-lg">
                인터랙티브 UI 요소 좌표 설정
              </p>
            </div>
          </Link>
        </div>

        <div className="mt-12 p-6 bg-gray-50 rounded-xl border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            🚀 시작하기
          </h3>
          <ol className="space-y-2 text-gray-700">
            <li className="flex items-start">
              <span className="font-bold mr-2">1.</span>
              <span>Android 디바이스 USB 연결 및 디버깅 모드 활성화</span>
            </li>
            <li className="flex items-start">
              <span className="font-bold mr-2">2.</span>
              <span>디바이스 관리에서 연결된 기기 스캔</span>
            </li>
            <li className="flex items-start">
              <span className="font-bold mr-2">3.</span>
              <span>캘리브레이션으로 UI 좌표 설정 (11단계)</span>
            </li>
            <li className="flex items-start">
              <span className="font-bold mr-2">4.</span>
              <span>자동화 실행 준비 완료!</span>
            </li>
          </ol>
        </div>
      </div>
    </div>
  )
}
