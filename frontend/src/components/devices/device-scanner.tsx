'use client'

import { useState } from 'react'
import { api } from '@/lib/api-client'
import type { DeviceInfo } from '@/lib/types'

export default function DeviceScanner() {
  const [scanning, setScanning] = useState(false)
  const [devices, setDevices] = useState<DeviceInfo[]>([])
  const [error, setError] = useState<string | null>(null)
  const [connecting, setConnecting] = useState<string | null>(null)

  const handleScan = async () => {
    setScanning(true)
    setError(null)
    setDevices([])

    try {
      const foundDevices = await api.devices.scanDevices()
      setDevices(foundDevices)

      if (foundDevices.length === 0) {
        setError(
          'No ADB devices found. Please check USB connection and enable USB debugging.'
        )
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to scan devices')
    } finally {
      setScanning(false)
    }
  }

  const handleConnect = async (deviceId: string) => {
    setConnecting(deviceId)
    setError(null)

    try {
      const profile = await api.devices.connectDevice(deviceId)
      alert(
        `디바이스 연결 성공!\n\nProfile: ${profile.profile_id}\nModel: ${profile.model}\n\n디바이스 목록 페이지가 새로고침됩니다.`
      )
      // Refresh the page to show updated device list
      window.location.reload()
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to connect device')
    } finally {
      setConnecting(null)
    }
  }

  return (
    <div className="space-y-6">
      {/* Scan Button */}
      <div>
        <button
          onClick={handleScan}
          disabled={scanning}
          className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors shadow-md hover:shadow-lg"
        >
          {scanning ? (
            <span className="flex items-center gap-2">
              <svg
                className="animate-spin h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Scanning...
            </span>
          ) : (
            '🔍 디바이스 스캔'
          )}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 font-medium">⚠️ Error</p>
          <p className="text-red-700 text-sm mt-1">{error}</p>
        </div>
      )}

      {/* Scanned Devices */}
      {devices.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Found {devices.length} device(s)
          </h3>

          <div className="grid gap-4">
            {devices.map((device) => (
              <div
                key={device.device_id}
                className="p-6 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all"
              >
                <div className="flex justify-between items-start">
                  <div className="space-y-2 flex-1">
                    <h4 className="text-lg font-semibold text-gray-900">
                      {device.model}
                    </h4>
                    <div className="grid grid-cols-2 gap-x-8 gap-y-1 text-sm">
                      <div className="text-gray-600">
                        <span className="font-medium">Manufacturer:</span>{' '}
                        {device.manufacturer}
                      </div>
                      <div className="text-gray-600">
                        <span className="font-medium">Android:</span>{' '}
                        {device.android_version}
                      </div>
                      <div className="text-gray-600">
                        <span className="font-medium">Resolution:</span>{' '}
                        {device.width} × {device.height}
                      </div>
                      <div className="text-gray-600">
                        <span className="font-medium">DPI:</span> {device.dpi}
                      </div>
                      <div className="text-gray-600 col-span-2">
                        <span className="font-medium">Serial:</span>{' '}
                        <code className="bg-gray-100 px-2 py-1 rounded text-xs">
                          {device.device_id}
                        </code>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => handleConnect(device.device_id)}
                    disabled={connecting === device.device_id}
                    className="ml-4 px-6 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 disabled:bg-green-300 disabled:cursor-not-allowed transition-colors shadow hover:shadow-md"
                  >
                    {connecting === device.device_id ? (
                      <span className="flex items-center gap-2">
                        <svg
                          className="animate-spin h-4 w-4"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          />
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          />
                        </svg>
                        Connecting...
                      </span>
                    ) : (
                      '✅ Connect'
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
