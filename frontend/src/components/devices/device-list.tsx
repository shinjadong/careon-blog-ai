'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api-client'
import type { DeviceProfile } from '@/lib/types'
import {
  formatTimestamp,
  formatResolution,
  formatConfidence,
  getConfidenceColor,
  cn,
} from '@/lib/utils'
import Link from 'next/link'

export default function DeviceList() {
  const [profiles, setProfiles] = useState<DeviceProfile[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadProfiles()
  }, [])

  const loadProfiles = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await api.devices.listProfiles()
      setProfiles(response.devices)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load profiles')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-32">
        <div className="text-gray-500">Loading profiles...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-800 font-medium">⚠️ Error</p>
        <p className="text-red-700 text-sm mt-1">{error}</p>
      </div>
    )
  }

  if (profiles.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No device profiles found</p>
        <p className="text-gray-400 text-sm mt-2">
          Scan and connect a device to create a profile
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-600">
        Total: <span className="font-semibold">{profiles.length}</span> profile(s)
      </p>

      <div className="grid gap-4">
        {profiles.map((profile) => (
          <div
            key={profile.profile_id}
            className="p-6 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all"
          >
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-bold text-gray-900">
                  {profile.model}
                </h3>
                <p className="text-sm text-gray-500 mt-1">
                  {profile.manufacturer} • Android {profile.android_version}
                </p>
              </div>

              {/* Calibration Status Badge */}
              <div
                className={cn(
                  'px-4 py-2 rounded-full text-sm font-semibold',
                  profile.calibrated
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                )}
              >
                {profile.calibrated ? '✅ Calibrated' : '⚠️ Not Calibrated'}
              </div>
            </div>

            {/* Device Specs Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 pb-4 border-b border-gray-200">
              <div>
                <p className="text-xs text-gray-500 mb-1">Resolution</p>
                <p className="font-medium text-gray-900">
                  {formatResolution(profile.resolution.width, profile.resolution.height)}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-500 mb-1">DPI</p>
                <p className="font-medium text-gray-900">{profile.dpi}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 mb-1">Connected Devices</p>
                <p className="font-medium text-gray-900">
                  {profile.device_ids.length}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-500 mb-1">Coordinates</p>
                <p className="font-medium text-gray-900">
                  {profile.coordinate_count || 0}
                </p>
              </div>
            </div>

            {/* Calibration Confidence */}
            <div className="flex items-center gap-4 mb-4">
              <div className="flex-1">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs text-gray-500">
                    Calibration Confidence
                  </span>
                  <span
                    className={cn(
                      'text-sm font-semibold',
                      getConfidenceColor(profile.calibration_confidence)
                    )}
                  >
                    {formatConfidence(profile.calibration_confidence)}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{
                      width: `${profile.calibration_confidence * 100}%`,
                    }}
                  />
                </div>
              </div>
            </div>

            {/* Metadata */}
            <div className="grid grid-cols-2 gap-4 text-xs text-gray-600 mb-4">
              <div>
                <span className="font-medium">Created:</span>{' '}
                {formatTimestamp(profile.created_at)}
              </div>
              <div>
                <span className="font-medium">Last Used:</span>{' '}
                {formatTimestamp(profile.last_used_at)}
              </div>
            </div>

            {/* Notes */}
            {profile.notes && (
              <div className="p-3 bg-gray-50 rounded border border-gray-200 mb-4">
                <p className="text-sm text-gray-700">{profile.notes}</p>
              </div>
            )}

            {/* Device IDs */}
            <div className="mb-4">
              <p className="text-xs text-gray-500 mb-2">Device IDs:</p>
              <div className="flex flex-wrap gap-2">
                {profile.device_ids.map((deviceId) => (
                  <code
                    key={deviceId}
                    className="px-2 py-1 bg-gray-100 rounded text-xs text-gray-700"
                  >
                    {deviceId}
                  </code>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              {!profile.calibrated && (
                <Link
                  href={`/calibration?profile=${profile.profile_id}`}
                  className="px-4 py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 transition-colors text-sm shadow hover:shadow-md"
                >
                  🎯 Start Calibration
                </Link>
              )}

              <Link
                href={`/devices/${profile.profile_id}`}
                className="px-4 py-2 bg-gray-600 text-white font-medium rounded-lg hover:bg-gray-700 transition-colors text-sm shadow hover:shadow-md"
              >
                📊 View Details
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
