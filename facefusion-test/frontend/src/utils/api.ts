import {
  HealthResponse,
  SystemInfo,
  ModelsInfo,
  FileUploadResponse,
  FaceSwapResponse,
  CLIFaceSwapRequest,
} from '../types';

const API_BASE_URL = '/api';

// APIクライアントクラス
class FaceFusionAPI {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // ヘルスチェック
  async healthCheck(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health');
  }

  // システム情報取得
  async getSystemInfo(): Promise<SystemInfo> {
    return this.request<SystemInfo>('/system/info');
  }

  // モデル情報取得
  async getModels(): Promise<ModelsInfo> {
    return this.request<ModelsInfo>('/models');
  }

  // ファイルアップロード
  async uploadFile(file: File): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // 動画Face Swap (アップロード形式)
  async faceSwapVideo(
    sourceFile: File,
    targetFile: File,
    options: {
      model?: string;
      quality?: number;
      maxFrames?: number;
      trimStart?: number;
      trimEnd?: number;
    } = {}
  ): Promise<FaceSwapResponse> {
    const formData = new FormData();
    formData.append('source_file', sourceFile);
    formData.append('target_file', targetFile);
    formData.append('model', options.model || 'inswapper_128');
    formData.append('quality', String(options.quality || 80));
    formData.append('max_frames', String(options.maxFrames || 50));
    
    if (options.trimStart !== undefined) {
      formData.append('trim_start', String(options.trimStart));
    }
    
    if (options.trimEnd !== undefined) {
      formData.append('trim_end', String(options.trimEnd));
    }

    const response = await fetch(`${API_BASE_URL}/face-swap/video`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Face Swap Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // 画像Face Swap (アップロード形式)
  async faceSwapImage(
    sourceFile: File,
    targetFile: File,
    options: {
      model?: string;
      quality?: number;
      pixelBoost?: string;
    } = {}
  ): Promise<FaceSwapResponse> {
    const formData = new FormData();
    formData.append('source_file', sourceFile);
    formData.append('target_file', targetFile);
    formData.append('model', options.model || 'inswapper_128');
    formData.append('quality', String(options.quality || 90));
    formData.append('pixel_boost', options.pixelBoost || '128x128');

    const response = await fetch(`${API_BASE_URL}/face-swap/image`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Face Swap Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // CLI形式Face Swap
  async cliFaceSwap(request: CLIFaceSwapRequest): Promise<any> {
    return this.request('/cli/face-swap', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // ファイルダウンロードURL取得
  getDownloadUrl(filename: string): string {
    return `${API_BASE_URL}/download/${filename}`;
  }
}

// ユーティリティ関数
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B';
  
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
};

export const formatTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  
  if (minutes > 0) {
    return `${minutes}分${remainingSeconds}秒`;
  }
  return `${remainingSeconds}秒`;
};

export const isImageFile = (file: File): boolean => {
  return file.type.startsWith('image/');
};

export const isVideoFile = (file: File): boolean => {
  return file.type.startsWith('video/');
};

export const getFileType = (file: File): 'image' | 'video' | 'unknown' => {
  if (isImageFile(file)) return 'image';
  if (isVideoFile(file)) return 'video';
  return 'unknown';
};

export const createFilePreview = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => resolve(e.target?.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};

// APIクライアントのインスタンスをエクスポート
export const api = new FaceFusionAPI(); 