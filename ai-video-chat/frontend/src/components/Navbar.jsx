import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="bg-primary-700 text-white shadow-md">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Link to="/" className="text-xl font-bold">AI Video Chat</Link>
        </div>
        <div>
          <ul className="flex space-x-6">
            <li>
              <Link to="/" className="hover:text-primary-200 transition-colors">
                ホーム
              </Link>
            </li>
            <li>
              <Link to="/prepare" className="hover:text-primary-200 transition-colors">
                素材準備
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  )
}

export default Navbar 