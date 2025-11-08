/**
 * TypeScript type definitions for CareOn Blog Automation
 * Matches backend Pydantic schemas
 */

export interface DeviceInfo {
  device_id: string
  model: string
  manufacturer: string
  android_version: string
  width: number
  height: number
  dpi: number
}

export interface Resolution {
  width: number
  height: number
}

export interface DeviceProfile {
  profile_id: string
  model: string
  manufacturer: string
  android_version: string
  resolution: Resolution
  dpi: number
  device_ids: string[]
  calibrated: boolean
  calibration_confidence: number
  created_at: string | null
  updated_at: string | null
  last_used_at: string | null
  notes: string | null
  coordinate_count?: number
}

export interface CoordinatePoint {
  x: number
  y: number
}

export interface UsageStats {
  usage_count: number
  success_count: number
  fail_count: number
  success_rate: number
}

export interface CoordinateConfig {
  id: number
  profile_id: string
  element_type: string
  element_name: string
  element_description: string | null
  coordinates: CoordinatePoint
  confidence: number
  validated: boolean
  calibration_method: string
  calibrated_by: string | null
  calibrated_at: string | null
  touch_radius: number
  usage_stats: UsageStats
  created_at: string | null
  updated_at: string | null
  last_used_at: string | null
  notes: string | null
}

export interface CalibrationSession {
  session_id: string
  profile_id: string
  current_step: number
  total_steps: number
  element_type: string
  element_name: string
  instructions: string
  screenshot_url?: string | null
  completed: boolean
}

export interface CalibrationResult {
  session_id: string
  element_type: string
  x: number
  y: number
  calibrated_by: string
  timestamp: string
}

export interface CalibrationGuide {
  step_number: number
  element_type: string
  element_name: string
  instructions: string
  help_text: string | null
  example_image: string | null
}

export interface ScreenshotResponse {
  device_id: string
  screenshot: string // base64 encoded
  format: string
}

export interface WebSocketMessage {
  type: 'connected' | 'screenshot' | 'error' | 'stop'
  device_id?: string
  screenshot?: string
  timestamp?: string
  message?: string
}

// API Response types
export interface DeviceListResponse {
  total: number
  devices: DeviceProfile[]
}

export interface CoordinateListResponse {
  total: number
  coordinates: CoordinateConfig[]
}

// API Request types
export interface DeviceProfileUpdate {
  notes?: string | null
  calibrated?: boolean
  calibration_confidence?: number
}

export interface CoordinateCreate {
  profile_id: string
  element_type: string
  element_name: string
  element_description?: string | null
  x: number
  y: number
  confidence?: number
  validated?: boolean
  calibration_method?: string
  calibrated_by?: string | null
  touch_radius?: number
  notes?: string | null
}

export interface CoordinateUpdate {
  x?: number
  y?: number
  confidence?: number
  validated?: boolean
  calibration_method?: string
  calibrated_by?: string | null
  touch_radius?: number
  notes?: string | null
}
