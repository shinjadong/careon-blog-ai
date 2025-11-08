/**
 * API Client for CareOn Blog Automation Backend
 * Type-safe REST API wrapper
 */

import type {
  DeviceInfo,
  DeviceProfile,
  DeviceListResponse,
  DeviceProfileUpdate,
  CoordinateConfig,
  CoordinateListResponse,
  CoordinateCreate,
  CoordinateUpdate,
  CalibrationSession,
  CalibrationResult,
  CalibrationGuide,
  ScreenshotResponse,
} from './types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public details?: unknown
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new ApiError(
        response.status,
        errorData.detail || response.statusText,
        errorData
      )
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return undefined as T
    }

    return response.json()
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError(0, 'Network error', error)
  }
}

// Device Management API

export const deviceApi = {
  /**
   * Scan for connected ADB devices
   */
  async scanDevices(): Promise<DeviceInfo[]> {
    return fetchApi<DeviceInfo[]>('/api/v1/devices/scan')
  },

  /**
   * Connect to specific device and get/create profile
   */
  async connectDevice(deviceId: string): Promise<DeviceProfile> {
    return fetchApi<DeviceProfile>(`/api/v1/devices/connect/${deviceId}`, {
      method: 'POST',
    })
  },

  /**
   * List all device profiles
   */
  async listProfiles(skip = 0, limit = 100): Promise<DeviceListResponse> {
    return fetchApi<DeviceListResponse>(
      `/api/v1/devices/profiles?skip=${skip}&limit=${limit}`
    )
  },

  /**
   * Get specific device profile
   */
  async getProfile(profileId: string): Promise<DeviceProfile> {
    return fetchApi<DeviceProfile>(`/api/v1/devices/profiles/${profileId}`)
  },

  /**
   * Update device profile
   */
  async updateProfile(
    profileId: string,
    data: DeviceProfileUpdate
  ): Promise<DeviceProfile> {
    return fetchApi<DeviceProfile>(`/api/v1/devices/profiles/${profileId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
  },

  /**
   * Delete device profile
   */
  async deleteProfile(profileId: string): Promise<void> {
    return fetchApi<void>(`/api/v1/devices/profiles/${profileId}`, {
      method: 'DELETE',
    })
  },

  /**
   * Get real-time screenshot from device
   */
  async getScreenshot(deviceId: string): Promise<ScreenshotResponse> {
    return fetchApi<ScreenshotResponse>(`/api/v1/devices/${deviceId}/screenshot`)
  },
}

// Coordinate Management API

export const coordinateApi = {
  /**
   * Get all coordinates for a profile
   */
  async getCoordinates(profileId: string): Promise<CoordinateListResponse> {
    return fetchApi<CoordinateListResponse>(
      `/api/v1/devices/profiles/${profileId}/coordinates`
    )
  },

  /**
   * Create new coordinate configuration
   */
  async createCoordinate(data: CoordinateCreate): Promise<CoordinateConfig> {
    return fetchApi<CoordinateConfig>('/api/v1/devices/coordinates', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  /**
   * Update coordinate configuration
   */
  async updateCoordinate(
    coordId: number,
    data: CoordinateUpdate
  ): Promise<CoordinateConfig> {
    return fetchApi<CoordinateConfig>(
      `/api/v1/devices/coordinates/${coordId}`,
      {
        method: 'PATCH',
        body: JSON.stringify(data),
      }
    )
  },

  /**
   * Delete coordinate configuration
   */
  async deleteCoordinate(coordId: number): Promise<void> {
    return fetchApi<void>(`/api/v1/devices/coordinates/${coordId}`, {
      method: 'DELETE',
    })
  },
}

// Calibration API

export const calibrationApi = {
  /**
   * Start new calibration session
   */
  async startSession(
    profileId: string,
    calibratedBy = 'admin'
  ): Promise<CalibrationSession> {
    return fetchApi<CalibrationSession>(
      `/api/v1/calibration/sessions?profile_id=${profileId}&calibrated_by=${calibratedBy}`,
      {
        method: 'POST',
      }
    )
  },

  /**
   * Get calibration session status
   */
  async getSession(sessionId: string): Promise<CalibrationSession> {
    return fetchApi<CalibrationSession>(
      `/api/v1/calibration/sessions/${sessionId}`
    )
  },

  /**
   * Submit calibration coordinate for current step
   */
  async submitCoordinate(
    sessionId: string,
    result: CalibrationResult
  ): Promise<CalibrationSession> {
    return fetchApi<CalibrationSession>(
      `/api/v1/calibration/sessions/${sessionId}/submit`,
      {
        method: 'POST',
        body: JSON.stringify(result),
      }
    )
  },

  /**
   * Cancel calibration session
   */
  async cancelSession(sessionId: string): Promise<void> {
    return fetchApi<void>(`/api/v1/calibration/sessions/${sessionId}`, {
      method: 'DELETE',
    })
  },

  /**
   * Get calibration workflow guide
   */
  async getGuide(): Promise<CalibrationGuide[]> {
    return fetchApi<CalibrationGuide[]>('/api/v1/calibration/guide')
  },

  /**
   * Get WebSocket URL for device screen streaming
   */
  getWebSocketUrl(deviceId: string): string {
    const wsProtocol = API_BASE_URL.startsWith('https') ? 'wss' : 'ws'
    const wsHost = API_BASE_URL.replace(/^https?:\/\//, '')
    return `${wsProtocol}://${wsHost}/api/v1/calibration/ws/${deviceId}`
  },
}

// Export all
export const api = {
  devices: deviceApi,
  coordinates: coordinateApi,
  calibration: calibrationApi,
}

export default api
