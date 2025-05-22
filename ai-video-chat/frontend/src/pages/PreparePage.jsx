import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { toast } from 'react-toastify'
import axios from 'axios'

function PreparePage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  
  const [loading, setLoading] = useState(false)
  const [preparing, setPreparing] = useState(false)
  const [sourceVideos, setSourceVideos] = useState([])
  const [faces, setFaces] = useState([])
  const [voices, setVoices] = useState([])
  
  const [selectedVideo, setSelectedVideo] = useState('')
  const [selectedFace, setSelectedFace] = useState('')
  const [selectedVoice, setSelectedVoice] = useState('')

  // 素材データの取得
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        
        const [videosRes, facesRes, voicesRes] = await Promise.all([
          axios.get('/api/videos/source'),
          axios.get('/api/faces'),
          axios.get('/api/voices')
        ])
        
        setSourceVideos(videosRes.data.videos || [])
        setFaces(facesRes.data.faces || [])
        setVoices(voicesRes.data.voices || [])
        
        // URLパラメータからの選択値の設定
        const videoParam = searchParams.get('video')
        if (videoParam) {
          setSelectedVideo(videoParam)
        }
      } catch (error) {
        console.error('Failed to fetch materials:', error)
        toast.error('素材データの取得に失敗しました')
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [searchParams])

  // 素材のアップロード処理
  const handleUpload = async (e, type) => {
    const file = e.target.files[0]
    if (!file) return
    
    // ファイル拡張子チェック
    const validExt = {
      video: ['.mp4'],
      face: ['.jpg', '.png'],
      voice: ['.wav']
    }
    
    const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
    if (!validExt[type].includes(ext)) {
      toast.error(`対応していないファイル形式です。${validExt[type].join(', ')}のみ可能です。`)
      return
    }
    
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await axios.post(`/api/upload/${type}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      toast.success('アップロード完了')
      
      // アップロード後にリストを更新
      const refreshRes = type === 'video' 
        ? await axios.get('/api/videos/source')
        : type === 'face'
          ? await axios.get('/api/faces')
          : await axios.get('/api/voices')
      
      if (type === 'video') {
        setSourceVideos(refreshRes.data.videos || [])
        setSelectedVideo(response.data.filename)
      } else if (type === 'face') {
        setFaces(refreshRes.data.faces || [])
        setSelectedFace(response.data.filename)
      } else {
        setVoices(refreshRes.data.voices || [])
        setSelectedVoice(response.data.filename)
      }
    } catch (error) {
      console.error(`Failed to upload ${type}:`, error)
      toast.error(`${type}のアップロードに失敗しました`)
    }
  }

  // 素材準備の実行
  const handlePrepare = async () => {
    if (!selectedVideo || !selectedFace || !selectedVoice) {
      toast.error('すべての素材を選択してください')
      return
    }
    
    try {
      setPreparing(true)
      
      const response = await axios.post('/api/prepare', {
        source_video: selectedVideo,
        target_face: selectedFace,
        voice_sample: selectedVoice
      })
      
      toast.success('素材の準備が完了しました')
      navigate(`/chat/${response.data.video_id}`)
    } catch (error) {
      console.error('Failed to prepare materials:', error)
      toast.error('素材の準備に失敗しました')
    } finally {
      setPreparing(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">読み込み中...</div>
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">素材の準備</h1>
      
      <div className="card mb-8">
        <h2 className="text-xl font-semibold mb-4">1. 動画を選択</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <select 
              className="input mb-4"
              value={selectedVideo}
              onChange={(e) => setSelectedVideo(e.target.value)}
            >
              <option value="">動画を選択...</option>
              {sourceVideos.map(video => (
                <option key={video.id} value={video.name}>{video.name}</option>
              ))}
            </select>
            <div>
              <label className="btn btn-secondary inline-block cursor-pointer">
                <input
                  type="file"
                  accept=".mp4"
                  className="hidden"
                  onChange={(e) => handleUpload(e, 'video')}
                />
                新しい動画をアップロード
              </label>
            </div>
          </div>
          <div>
            {selectedVideo && (
              <div className="aspect-video bg-gray-200 rounded overflow-hidden">
                <video
                  src={`/api/data/source/${selectedVideo}`}
                  className="w-full h-full object-cover"
                  controls
                />
              </div>
            )}
          </div>
        </div>
      </div>
      
      <div className="card mb-8">
        <h2 className="text-xl font-semibold mb-4">2. 顔画像を選択</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <select 
              className="input mb-4"
              value={selectedFace}
              onChange={(e) => setSelectedFace(e.target.value)}
            >
              <option value="">顔画像を選択...</option>
              {faces.map(face => (
                <option key={face.id} value={face.name}>{face.name}</option>
              ))}
            </select>
            <div>
              <label className="btn btn-secondary inline-block cursor-pointer">
                <input
                  type="file"
                  accept=".jpg,.png"
                  className="hidden"
                  onChange={(e) => handleUpload(e, 'face')}
                />
                新しい顔画像をアップロード
              </label>
            </div>
          </div>
          <div>
            {selectedFace && (
              <div className="aspect-square bg-gray-200 rounded overflow-hidden">
                <img
                  src={`/api/data/source/${selectedFace}`}
                  className="w-full h-full object-cover"
                  alt="Selected face"
                />
              </div>
            )}
          </div>
        </div>
      </div>
      
      <div className="card mb-8">
        <h2 className="text-xl font-semibold mb-4">3. 音声サンプルを選択</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <select 
              className="input mb-4"
              value={selectedVoice}
              onChange={(e) => setSelectedVoice(e.target.value)}
            >
              <option value="">音声サンプルを選択...</option>
              {voices.map(voice => (
                <option key={voice.id} value={voice.name}>{voice.name}</option>
              ))}
            </select>
            <div>
              <label className="btn btn-secondary inline-block cursor-pointer">
                <input
                  type="file"
                  accept=".wav"
                  className="hidden"
                  onChange={(e) => handleUpload(e, 'voice')}
                />
                新しい音声サンプルをアップロード
              </label>
            </div>
          </div>
          <div>
            {selectedVoice && (
              <div className="p-4 bg-gray-100 rounded">
                <audio
                  src={`/api/data/source/${selectedVoice}`}
                  className="w-full"
                  controls
                />
              </div>
            )}
          </div>
        </div>
      </div>
      
      <div className="text-center">
        <button
          className="btn btn-primary text-lg py-3 px-8"
          disabled={!selectedVideo || !selectedFace || !selectedVoice || preparing}
          onClick={handlePrepare}
        >
          {preparing ? '処理中...' : 'チャットの準備をする'}
        </button>
      </div>
    </div>
  )
}

export default PreparePage 