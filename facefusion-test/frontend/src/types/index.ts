// API関連の型定義
export interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
  error?: string;
}

// ヘルスチェック
export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  version: string;
  facefusion_available: boolean;
  gpu_available: boolean;
  cuda_version?: string;
  memory_usage?: {
    total: number;
    available: number;
    percent: number;
  };
}

// システム情報
export interface SystemInfo {
  cpu_count: number;
  memory_total: number;
  memory_available: number;
  gpu_available: boolean;
  cuda_version?: string;
  python_version: string;
  facefusion_version: string;
}

// モデル情報
export interface ModelsInfo {
  available_models: string[];
  default_model: string;
  model_details: Record<string, string>;
}

// ファイルアップロード
export interface FileUploadResponse {
  success: boolean;
  filename: string;
  file_path: string;
  file_size: number;
  media_type: 'image' | 'video';
  message: string;
}

// Face Swap結果
export interface FaceSwapResponse {
  success: boolean;
  message: string;
  output_filename: string;
  file_size: number;
  media_type: 'image' | 'video';
  processing_time: number;
  model_used?: string;
  quality?: number;
}

// CLI Face Swapリクエスト
export interface CLIFaceSwapRequest {
  source_path: string;
  target_path: string;
  output_path: string;
  face_swapper_model?: string;
  output_video_quality?: number;
  output_image_quality?: number;
  trim_frame_start?: number;
  trim_frame_end?: number;
}

// フロントエンド用の型
export interface UploadedFile {
  file: File;
  preview: string;
  type: 'image' | 'video';
  size: number;
}

export interface ProcessingStatus {
  isProcessing: boolean;
  progress?: number;
  message?: string;
  error?: string;
}

export interface AppSettings {
  model: string;
  quality: number;
  maxFrames: number;
  trimStart: number;
  trimEnd?: number;
}

// UI状態
export type TabType = 'upload' | 'process' | 'result';

export interface AppState {
  activeTab: TabType;
  sourceFile: UploadedFile | null;
  targetFile: UploadedFile | null;
  resultFile: string | null;
  settings: AppSettings;
  processing: ProcessingStatus;
} 