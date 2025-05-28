export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface HealthResponse {
  status: string;
  version: string;
  facefusion_available: boolean;
  gpu_available: boolean;
  cuda_version: string;
  memory_usage: {
    total: number;
    available: number;
    percent: number;
  };
}

export interface FaceSwapRequest {
  source_file: File;
  target_file: File;
  model?: string;
  quality?: number;
  pixel_boost?: string;
  trim_start?: number;
  trim_end?: number;
  max_frames?: number;
}

export interface FaceSwapResponse {
  success: boolean;
  message: string;
  output_filename: string;
  output_size: number;
  processing_time: number;
  model_used: string;
  model_details: {
    input_size: string;
    output_quality: number;
    processing_mode: string;
  };
}

export interface UploadResponse {
  success: boolean;
  filename: string;
  original_name: string;
  size: number;
  content_type: string;
  message: string;
}

export interface ProcessingStatus {
  isProcessing: boolean;
  progress?: number;
  stage?: string;
  estimatedTime?: number;
} 