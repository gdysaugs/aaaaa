import axios from 'axios'

const API_BASE_URL = '/api'

// APIクライアント
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API関数
export const api = {
  // 素材関連
  getSourceVideos: () => apiClient.get('/videos/source'),
  getFaces: () => apiClient.get('/faces'),
  getVoices: () => apiClient.get('/voices'),
  
  // アップロード
  uploadFile: (fileType, file) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post(`/upload/${fileType}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  
  // 素材準備
  prepareMaterials: (data) => apiClient.post('/prepare', data),
  
  // チャット関連
  sendChatMessage: (data) => apiClient.post('/chat', data),
  checkChatStatus: (requestId) => apiClient.get(`/chat/status/${requestId}`),
}

export default api 