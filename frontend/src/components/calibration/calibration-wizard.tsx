'use client'

import { useState, useEffect, useRef, use } from 'react'
import { api } from '@/lib/api-client'
import type {
  DeviceProfile,
  CalibrationSession,
  CalibrationResult,
} from '@/lib/types'
import { cn } from '@/lib/utils'

interface CalibrationWizardProps {
  searchParams: Promise<{ profile?: string; device?: string }>
}

export default function CalibrationWizard({
  searchParams,
}: CalibrationWizardProps) {
  const params = use(searchParams)

  // State
  const [profiles, setProfiles] = useState<DeviceProfile[]>([])
  const [selectedProfile, setSelectedProfile] = useState<string | null>(
    params.profile || null
  )
  const [session, setSession] = useState<CalibrationSession | null>(null)
  const [screenshot, setScreenshot] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [wsConnected, setWsConnected] = useState(false)

  // WebSocket
  const wsRef = useRef<WebSocket | null>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  // Load profiles on mount
  useEffect(() => {
    loadProfiles()
  }, [])

  // Connect WebSocket when session starts
  useEffect(() => {
    if (session && !session.completed && selectedProfile) {
      connectWebSocket()
    }

    return () => {
      disconnectWebSocket()
    }
  }, [session, selectedProfile])

  const loadProfiles = async () => {
    try {
      const response = await api.devices.listProfiles()
      setProfiles(response.devices)

      // Auto-select if only one profile
      if (response.devices.length === 1 && !selectedProfile) {
        setSelectedProfile(response.devices[0].profile_id)
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load profiles')
    }
  }

  const connectWebSocket = () => {
    if (!selectedProfile) return

    const profile = profiles.find((p) => p.profile_id === selectedProfile)
    if (!profile || profile.device_ids.length === 0) return

    const deviceId = profile.device_ids[0]
    const wsUrl = api.calibration.getWebSocketUrl(deviceId)

    try {
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        console.log('WebSocket connected')
        setWsConnected(true)
      }

      ws.onmessage = (event) => {
        const message = JSON.parse(event.data)

        if (message.type === 'screenshot') {
          setScreenshot(message.screenshot)
        } else if (message.type === 'error') {
          setError(message.message)
        }
      }

      ws.onerror = (err) => {
        console.error('WebSocket error:', err)
        setError('WebSocket connection failed')
        setWsConnected(false)
      }

      ws.onclose = () => {
        console.log('WebSocket disconnected')
        setWsConnected(false)
      }

      wsRef.current = ws
    } catch (err) {
      console.error('Failed to connect WebSocket:', err)
      setError('Failed to connect to device screen')
    }
  }

  const disconnectWebSocket = () => {
    if (wsRef.current) {
      wsRef.current.send(JSON.stringify({ type: 'stop' }))
      wsRef.current.close()
      wsRef.current = null
      setWsConnected(false)
    }
  }

  const handleStartCalibration = async () => {
    if (!selectedProfile) {
      setError('Please select a device profile')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const newSession = await api.calibration.startSession(selectedProfile)
      setSession(newSession)
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : 'Failed to start calibration'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleCanvasClick = async (
    event: React.MouseEvent<HTMLCanvasElement>
  ) => {
    console.log('Canvas clicked!')
    console.log('Session:', session)
    console.log('Canvas ref:', canvasRef.current)

    if (!session || session.completed || !canvasRef.current) {
      console.warn('Click ignored - session or canvas not ready')
      return
    }

    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()

    // Calculate click position relative to canvas
    const scaleX = canvas.width / rect.width
    const scaleY = canvas.height / rect.height
    const x = Math.round((event.clientX - rect.left) * scaleX)
    const y = Math.round((event.clientY - rect.top) * scaleY)

    console.log(`✅ Clicked at: (${x}, ${y})`)

    // Submit coordinate to backend
    setLoading(true)
    setError(null)

    try {
      const result: CalibrationResult = {
        session_id: session.session_id,
        element_type: session.element_type,
        x,
        y,
        calibrated_by: 'admin',
        timestamp: new Date().toISOString(),
      }

      const nextSession = await api.calibration.submitCoordinate(
        session.session_id,
        result
      )

      setSession(nextSession)

      // Show visual feedback
      drawClickMarker(x, y)
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : 'Failed to submit coordinate'
      )
    } finally {
      setLoading(false)
    }
  }

  const drawClickMarker = (x: number, y: number) => {
    if (!canvasRef.current) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Draw green circle at clicked position
    ctx.strokeStyle = '#10B981'
    ctx.lineWidth = 3
    ctx.beginPath()
    ctx.arc(x, y, 20, 0, 2 * Math.PI)
    ctx.stroke()

    // Draw crosshair
    ctx.beginPath()
    ctx.moveTo(x - 30, y)
    ctx.lineTo(x + 30, y)
    ctx.moveTo(x, y - 30)
    ctx.lineTo(x, y + 30)
    ctx.stroke()

    // Fade out after 2 seconds
    setTimeout(() => {
      if (screenshot && canvasRef.current) {
        const img = new Image()
        img.onload = () => {
          const ctx = canvasRef.current?.getContext('2d')
          if (ctx) {
            ctx.clearRect(0, 0, canvas.width, canvas.height)
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
          }
        }
        img.src = `data:image/png;base64,${screenshot}`
      }
    }, 2000)
  }

  // Draw screenshot on canvas
  useEffect(() => {
    if (screenshot && canvasRef.current) {
      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')
      if (!ctx) return

      const img = new Image()
      img.onload = () => {
        // Set canvas size to image size
        canvas.width = img.width
        canvas.height = img.height

        // Draw image
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx.drawImage(img, 0, 0)
      }
      img.src = `data:image/png;base64,${screenshot}`
    }
  }, [screenshot])

  const handleCancelCalibration = async () => {
    if (!session) return

    try {
      await api.calibration.cancelSession(session.session_id)
      setSession(null)
      disconnectWebSocket()
    } catch (err) {
      console.error('Failed to cancel session:', err)
    }
  }

  return (
    <div className="space-y-6">
      {/* Device Selection */}
      {!session && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            1. 디바이스 선택
          </h2>

          {profiles.length === 0 ? (
            <p className="text-gray-500">
              No device profiles found. Please scan and connect a device first.
            </p>
          ) : (
            <div className="space-y-3">
              {profiles.map((profile) => (
                <label
                  key={profile.profile_id}
                  className={cn(
                    'flex items-center p-4 border rounded-lg cursor-pointer transition-all',
                    selectedProfile === profile.profile_id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  )}
                >
                  <input
                    type="radio"
                    name="profile"
                    value={profile.profile_id}
                    checked={selectedProfile === profile.profile_id}
                    onChange={(e) => setSelectedProfile(e.target.value)}
                    className="mr-4 h-4 w-4 text-blue-600"
                  />
                  <div className="flex-1">
                    <p className="font-semibold text-gray-900">
                      {profile.model}
                    </p>
                    <p className="text-sm text-gray-600">
                      {profile.resolution.width} × {profile.resolution.height} •{' '}
                      {profile.device_ids.length} device(s)
                    </p>
                  </div>
                  {profile.calibrated && (
                    <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
                      ✅ Calibrated
                    </span>
                  )}
                </label>
              ))}
            </div>
          )}

          {selectedProfile && (
            <div className="mt-6">
              <button
                onClick={handleStartCalibration}
                disabled={loading}
                className="w-full px-6 py-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 disabled:bg-purple-300 disabled:cursor-not-allowed transition-colors shadow-md hover:shadow-lg"
              >
                {loading ? 'Starting...' : '🚀 캘리브레이션 시작'}
              </button>
            </div>
          )}
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 font-medium">⚠️ Error</p>
          <p className="text-red-700 text-sm mt-1">{error}</p>
        </div>
      )}

      {/* Calibration Session */}
      {session && (
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Left: Device Screen */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900">
                📱 Device Screen
              </h2>
              <div className="flex items-center gap-2">
                <div
                  className={cn(
                    'w-3 h-3 rounded-full',
                    wsConnected ? 'bg-green-500' : 'bg-red-500'
                  )}
                />
                <span className="text-sm text-gray-600">
                  {wsConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            </div>

            {/* Canvas for device screen */}
            <div className="relative bg-gray-900 rounded-lg overflow-hidden shadow-xl">
              {screenshot ? (
                <canvas
                  ref={canvasRef}
                  onClick={handleCanvasClick}
                  className="w-full h-auto cursor-crosshair"
                  style={{ maxHeight: '70vh' }}
                />
              ) : (
                <div className="flex items-center justify-center h-96 text-gray-400">
                  {wsConnected
                    ? 'Waiting for screenshot...'
                    : 'Connecting to device...'}
                </div>
              )}

              {loading && (
                <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                  <div className="text-white text-lg">Processing...</div>
                </div>
              )}
            </div>

            <p className="mt-4 text-sm text-gray-500 text-center">
              💡 Tip: Click on the UI element shown in the instructions
            </p>
          </div>

          {/* Right: Instructions & Progress */}
          <div className="space-y-6">
            {/* Progress */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                📊 Progress
              </h3>

              <div className="mb-4">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">
                    Step {session.current_step + 1} of {session.total_steps}
                  </span>
                  <span className="font-semibold text-blue-600">
                    {Math.round(
                      ((session.current_step + 1) / session.total_steps) * 100
                    )}
                    %
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-500"
                    style={{
                      width: `${((session.current_step + 1) / session.total_steps) * 100}%`,
                    }}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <p className="text-xs text-gray-500">Current Element:</p>
                <p className="font-semibold text-gray-900">
                  {session.element_name}
                </p>
              </div>
            </div>

            {/* Instructions */}
            <div className="bg-purple-50 rounded-lg border border-purple-200 p-6">
              <h3 className="text-lg font-semibold text-purple-900 mb-3">
                📝 Instructions
              </h3>
              <p className="text-purple-800 leading-relaxed">
                {session.instructions}
              </p>
            </div>

            {/* Actions */}
            <div className="space-y-3">
              <button
                onClick={handleCancelCalibration}
                className="w-full px-4 py-2 bg-gray-600 text-white font-medium rounded-lg hover:bg-gray-700 transition-colors"
              >
                ❌ Cancel Calibration
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Completion Message */}
      {session?.completed && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-8 text-center">
          <div className="text-6xl mb-4">🎉</div>
          <h2 className="text-2xl font-bold text-green-900 mb-2">
            Calibration Complete!
          </h2>
          <p className="text-green-800 mb-6">
            모든 UI 요소 좌표 설정이 완료되었습니다.
            <br />
            이제 자동 포스팅을 실행할 수 있습니다.
          </p>
          <button
            onClick={() => {
              setSession(null)
              setScreenshot(null)
              disconnectWebSocket()
            }}
            className="px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors shadow-md"
          >
            ✅ Done
          </button>
        </div>
      )}
    </div>
  )
}
