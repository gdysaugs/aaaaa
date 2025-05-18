import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { toast } from 'react-toastify'
import axios from 'axios'

function HomePage() {
  const [videos, setVideos] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        setLoading(true)
        // 事前準備済みの動画一覧を取得
        const response = await axios.get('/api/videos/source')
        setVideos(response.data.videos || [])
      } catch (error) {
        console.error('Failed to fetch videos:', error)
        toast.error('動画一覧の取得に失敗しました')
      } finally {
        setLoading(false)
      }
    }

    fetchVideos()
  }, [])

  return (
    <div className="space-y-8">
      <section className="text-center py-12 bg-primary-50 rounded-lg shadow-inner">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">AI Video Chat</h1>
        <p className="text-xl text-gray-700 mb-8">
          リアルタイムで会話するAI動画キャラクター
        </p>
        <Link to="/prepare" className="btn btn-primary text-lg py-3 px-8">
          素材を準備する
        </Link>
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-4">利用可能な動画</h2>
        {loading ? (
          <div className="text-center py-8">読み込み中...</div>
        ) : videos.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {videos.map((video) => (
              <div key={video.id} className="card">
                <h3 className="text-lg font-semibold mb-2">{video.name}</h3>
                <div className="aspect-video bg-gray-200 mb-3 rounded overflow-hidden">
                  <video
                    src={video.url}
                    className="w-full h-full object-cover"
                    controls
                  />
                </div>
                <Link
                  to={`/prepare?video=${video.name}`}
                  className="btn btn-primary block text-center"
                >
                  この動画を使用
                </Link>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 bg-gray-100 rounded-lg">
            <p>準備済みの動画はありません</p>
            <Link to="/prepare" className="text-primary-600 hover:underline mt-2 inline-block">
              素材を準備する
            </Link>
          </div>
        )}
      </section>
    </div>
  )
}

export default HomePage 