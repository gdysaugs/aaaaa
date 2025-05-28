import axios, { AxiosInstance } from 'axios';
import { 
  HealthResponse, 
  FaceSwapRequest, 
  FaceSwapResponse, 
  UploadResponse 
} from '../types/api';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: import.meta.env.PROD ? '/api' : 'http://localhost:8000',
      timeout: 1800000, // 30分のタイムアウト（動画処理用）
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // ヘルスチェック
  async healthCheck(): Promise<HealthResponse> {
    const response = await this.api.get<HealthResponse>('/health');
    return response.data;
  }

  // ファイルアップロード
  async uploadFile(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.api.post<UploadResponse>('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // 画像Face Swap
  async imageSwap(request: FaceSwapRequest): Promise<FaceSwapResponse> {
    const formData = new FormData();
    formData.append('source_file', request.source_file);
    formData.append('target_file', request.target_file);
    
    if (request.model) formData.append('model', request.model);
    if (request.quality) formData.append('quality', request.quality.toString());
    if (request.pixel_boost) formData.append('pixel_boost', request.pixel_boost);

    const response = await this.api.post<FaceSwapResponse>('/face-swap/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // 動画Face Swap
  async videoSwap(request: FaceSwapRequest): Promise<FaceSwapResponse> {
    const formData = new FormData();
    formData.append('source_file', request.source_file);
    formData.append('target_file', request.target_file);
    
    if (request.model) formData.append('model', request.model);
    if (request.quality) formData.append('quality', request.quality.toString());
    if (request.pixel_boost) formData.append('pixel_boost', request.pixel_boost);
    if (request.trim_start !== undefined) formData.append('trim_start', request.trim_start.toString());
    if (request.trim_end !== undefined) formData.append('trim_end', request.trim_end.toString());
    if (request.max_frames) formData.append('max_frames', request.max_frames.toString());

    const response = await this.api.post<FaceSwapResponse>('/face-swap/video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // ファイルダウンロード
  async downloadFile(filename: string): Promise<Blob> {
    const response = await this.api.get(`/download/${filename}`, {
      responseType: 'blob',
    });
    return response.data;
  }

  // ファイルダウンロードURL取得
  getDownloadUrl(filename: string): string {
    const baseURL = import.meta.env.PROD ? '/api' : 'http://localhost:8000';
    return `${baseURL}/download/${filename}`;
  }
}

export const apiService = new ApiService();
export default apiService; 