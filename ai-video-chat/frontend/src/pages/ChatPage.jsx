import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import axios from 'axios'

function ChatPage() {
  const { videoId } = useParams()
  const navigate = useNavigate()
  
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [videoUrl, setVideoUrl] = useState('')
  const [processingRequestId, setProcessingRequestId] = useState(null)
  const [status, setStatus] = useState(null)
  
  const messagesEndRef = useRef(null)
  const statusCheckInterval = useRef(null)
  
  // 最初のシステムメッセージを設定
  useEffect(() => {
    setMessages([
      {
        role: 'system',
        content: 'あなたはAIビデオキャラクターです。会話を通じてユーザーと対話していきます。',
      },
      {
        role: 'assistant',
        content: 'こんにちは！何でも話しかけてください。',
      }
    ])
    setLoading(false)
  }, [])

  // スクロール処理
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])
  
  // ステータスチェック処理
  useEffect(() => {
    if (processingRequestId) {
      statusCheckInterval.current = setInterval(checkStatus, 2000)
      return () => clearInterval(statusCheckInterval.current)
    }
  }, [processingRequestId])
  
  // ステータスチェック関数
  const checkStatus = async () => {
    try {
      const response = await axios.get(`/api/chat/status/${processingRequestId}`)
      setStatus(response.data)
      
      if (response.data.status === 'completed') {
        // 処理完了
        clearInterval(statusCheckInterval.current)
        setVideoUrl(response.data.video_url)
        setProcessingRequestId(null)
        setSending(false)
      } else if (response.data.status === 'error') {
        // エラー
        clearInterval(statusCheckInterval.current)
        toast.error(`処理中にエラーが発生しました: ${response.data.error}`)
        setProcessingRequestId(null)
        setSending(false)
      } else if (response.data.status === 'llm_response_completed' && response.data.text) {
        // LLMの回答だけ表示
        const updatedMessages = [...messages]
        if (updatedMessages[updatedMessages.length - 1].role === 'assistant') {
          updatedMessages[updatedMessages.length - 1].content = response.data.text
        } else {
          updatedMessages.push({
            role: 'assistant',
            content: response.data.text
          })
        }
        setMessages(updatedMessages)
      }
    } catch (error) {
      console.error('Failed to check status:', error)
    }
  }
  
  // メッセージ送信処理
  const handleSendMessage = async (e) => {
    e.preventDefault()
    
    if (!input.trim() || sending) return
    
    const userMessage = {
      role: 'user',
      content: input,
    }
    
    const updatedMessages = [...messages, userMessage]
    setMessages(updatedMessages)
    setInput('')
    setSending(true)
    
    try {
      // チャットAPIリクエスト
      const response = await axios.post('/api/chat', {
        messages: updatedMessages,
        video_id: videoId
      })
      
      // レスポンスから処理IDを取得してステータスチェック開始
      setProcessingRequestId(response.data.request_id)
      
      // 一時的な回答を追加（後でステータスチェックで更新）
      setMessages([...updatedMessages, {
        role: 'assistant',
        content: '処理中...'
      }])
    } catch (error) {
      console.error('Failed to send message:', error)
      toast.error('メッセージの送信に失敗しました')
      setSending(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">読み込み中...</div>
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-2">AI動画チャット</h1>
        <button 
          className="text-primary-600 hover:underline"
          onClick={() => navigate('/prepare')}
        >
          別の素材で始める
        </button>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 動画エリア */}
        <div className="bg-gray-100 rounded-lg overflow-hidden">
          {videoUrl ? (
            <video 
              src={videoUrl} 
              className="w-full aspect-video object-cover"
              controls
              autoPlay
            />
          ) : (
            <div className="w-full aspect-video flex items-center justify-center">
              <div className="text-gray-500">
                {sending ? '動画生成中...' : '会話を始めると動画が表示されます'}
              </div>
            </div>
          )}
        </div>
        
        {/* チャットエリア */}
        <div className="bg-white rounded-lg shadow-md flex flex-col h-[600px]">
          <div className="flex-grow overflow-y-auto p-4">
            {messages.filter(m => m.role !== 'system').map((message, index) => (
              <div 
                key={index}
                className={`mb-4 ${
                  message.role === 'user' 
                    ? 'text-right' 
                    : 'text-left'
                }`}
              >
                <div
                  className={`inline-block px-4 py-2 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  {message.content}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          
          <div className="p-4 border-t">
            <form onSubmit={handleSendMessage} className="flex">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="メッセージを入力..."
                className="input flex-grow"
                disabled={sending}
              />
              <button
                type="submit"
                className="btn btn-primary ml-2"
                disabled={sending}
              >
                送信
              </button>
            </form>
          </div>
        </div>
      </div>
      
      {status && status.status !== 'completed' && (
        <div className="mt-4 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-semibold mb-2">処理状況:</h3>
          <div className="text-sm text-gray-700">
            {status.status === 'started' && '動画処理を開始しました...'}
            {status.status === 'llm_response_completed' && 'AI応答の生成が完了しました。音声合成中...'}
            {status.status === 'audio_completed' && '音声合成が完了しました。動画処理中...'}
            {status.status === 'face_fusion_completed' && '顔入れ替えが完了しました。口パク合成中...'}
          </div>
        </div>
      )}
    </div>
  )
}

export default ChatPage 