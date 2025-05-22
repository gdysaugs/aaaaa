import { Link } from 'react-router-dom'

function NotFoundPage() {
  return (
    <div className="max-w-xl mx-auto text-center py-16">
      <h1 className="text-6xl font-bold text-gray-900">404</h1>
      <p className="text-2xl text-gray-600 mt-4 mb-8">ページが見つかりませんでした</p>
      <Link to="/" className="btn btn-primary">
        ホームに戻る
      </Link>
    </div>
  )
}

export default NotFoundPage 