import { useState, useEffect } from 'react';
import { Play, Download, Settings, Monitor, Cpu, HardDrive } from 'lucide-react';
import FileUpload from './components/FileUpload';
import apiService from './services/api';
import { FaceSwapResponse, HealthResponse, ProcessingStatus } from './types/api';

function App() {
  const [sourceFile, setSourceFile] = useState<File | null>(null);
  const [targetFile, setTargetFile] = useState<File | null>(null);
  const [result, setResult] = useState<FaceSwapResponse | null>(null);
  const [processing, setProcessing] = useState<ProcessingStatus>({ isProcessing: false });
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // 設定
  const [settings, setSettings] = useState({
    model: 'inswapper_128',
    quality: 80,
    pixel_boost: '128x128',
    max_frames: 50
  });

  useEffect(() => {
    // 初期ヘルスチェック
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const healthData = await apiService.healthCheck();
      setHealth(healthData);
    } catch (err) {
      console.error('Health check failed:', err);
    }
  };

  const handleFaceSwap = async () => {
    if (!sourceFile || !targetFile) {
      setError('ソース画像とターゲットファイルの両方を選択してください');
      return;
    }

    setError(null);
    setProcessing({ isProcessing: true, stage: '処理開始中...' });

    try {
      const isVideo = targetFile.type.startsWith('video/');
      
      setProcessing({ isProcessing: true, stage: `${isVideo ? '動画' : '画像'}処理中...` });

      const request = {
        source_file: sourceFile,
        target_file: targetFile,
        model: settings.model,
        quality: settings.quality,
        pixel_boost: settings.pixel_boost,
        max_frames: isVideo ? settings.max_frames : undefined
      };

      const response = isVideo 
        ? await apiService.videoSwap(request)
        : await apiService.imageSwap(request);

      setResult(response);
      setProcessing({ isProcessing: false });
    } catch (err: any) {
      setError(err.response?.data?.message || err.message || 'エラーが発生しました');
      setProcessing({ isProcessing: false });
    }
  };

  const handleDownload = async () => {
    if (!result) return;

    try {
      const blob = await apiService.downloadFile(result.output_filename);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = result.output_filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('ダウンロードに失敗しました');
    }
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}分${secs}秒`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🎭 FaceFusion Frontend
          </h1>
          <p className="text-gray-600">
            べ、別にあんたのためじゃないけど、Face Swapができるフロントエンドよ！
          </p>
        </div>

        {/* Health Status */}
        {health && (
          <div className="bg-white rounded-lg shadow-md p-4 mb-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Monitor className="w-6 h-6 text-green-500" />
                <div>
                  <p className="font-semibold text-gray-800">
                    システム状態: <span className="text-green-600">{health.status}</span>
                  </p>
                  <p className="text-sm text-gray-600">
                    GPU: {health.gpu_available ? '利用可能' : '利用不可'} 
                    {health.cuda_version && ` (CUDA ${health.cuda_version})`}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <div className="flex items-center space-x-1">
                  <Cpu className="w-4 h-4" />
                  <span>使用率: {health.memory_usage.percent}%</span>
                </div>
                <div className="flex items-center space-x-1">
                  <HardDrive className="w-4 h-4" />
                  <span>{formatBytes(health.memory_usage.available)} 利用可能</span>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Panel - File Upload */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                📁 ファイル選択
              </h2>
              
              <div className="space-y-4">
                <FileUpload
                  onFileSelect={setSourceFile}
                  onFileRemove={() => setSourceFile(null)}
                  selectedFile={sourceFile}
                  accept="image/*"
                  label="ソース画像 (顔を交換する画像)"
                />

                <FileUpload
                  onFileSelect={setTargetFile}
                  onFileRemove={() => setTargetFile(null)}
                  selectedFile={targetFile}
                  accept="image/*,video/*"
                  label="ターゲットファイル (顔を適用する画像・動画)"
                  maxSize={500 * 1024 * 1024}
                />
              </div>
            </div>

            {/* Settings Panel */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center space-x-2 mb-4">
                <Settings className="w-5 h-5 text-gray-600" />
                <h3 className="text-lg font-semibold text-gray-800">設定</h3>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    モデル
                  </label>
                  <select 
                    value={settings.model}
                    onChange={(e) => setSettings({...settings, model: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="inswapper_128">inswapper_128 (高速・標準品質)</option>
                    <option value="ghost_2_256">ghost_2_256 (最高品質・推奨)</option>
                    <option value="blendswap_256">blendswap_256 (自然な仕上がり)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    品質: {settings.quality}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="100"
                    value={settings.quality}
                    onChange={(e) => setSettings({...settings, quality: parseInt(e.target.value) || 80})}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    最大フレーム数 (動画用)
                  </label>
                  <input
                    type="number"
                    min="10"
                    max="200"
                    value={settings.max_frames}
                    onChange={(e) => setSettings({...settings, max_frames: parseInt(e.target.value) || 50})}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Right Panel - Processing & Results */}
          <div className="space-y-6">
            {/* Processing Button */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <button
                onClick={handleFaceSwap}
                disabled={!sourceFile || !targetFile || processing.isProcessing}
                className={`w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-lg font-semibold transition-colors ${
                  !sourceFile || !targetFile || processing.isProcessing
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:from-blue-600 hover:to-purple-700'
                }`}
              >
                <Play className="w-5 h-5" />
                <span>
                  {processing.isProcessing ? 'Processing...' : 'Face Swap 開始'}
                </span>
              </button>

              {processing.isProcessing && (
                <div className="mt-4">
                  <div className="text-center text-gray-600 mb-2">
                    {processing.stage}
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full animate-pulse" style={{width: '100%'}}></div>
                  </div>
                  <div className="text-center text-xs text-gray-500 mt-2">
                    ⏱️ 動画処理は時間がかかります（数分～数十分）<br/>
                    😤 べ、別に心配してるわけじゃないけど、気長に待ちなさいよ！
                  </div>
                </div>
              )}
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="text-red-800">
                  <strong>エラー:</strong> {error}
                </div>
              </div>
            )}

            {/* Results */}
            {result && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  ✅ 処理完了
                </h3>
                
                <div className="space-y-3 mb-4">
                  <div className="flex justify-between">
                    <span className="text-gray-600">ファイル名:</span>
                    <span className="font-mono text-sm">{result.output_filename}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">ファイルサイズ:</span>
                    <span>{formatBytes(result.output_size)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">処理時間:</span>
                    <span>{formatTime(result.processing_time)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">使用モデル:</span>
                    <span>{result.model_used}</span>
                  </div>
                </div>

                <button
                  onClick={handleDownload}
                  className="w-full flex items-center justify-center space-x-2 py-2 px-4 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                >
                  <Download className="w-4 h-4" />
                  <span>ダウンロード</span>
                </button>

                {/* Preview */}
                <div className="mt-4">
                  <p className="text-sm text-gray-600 mb-2">プレビュー:</p>
                  {result.output_filename.endsWith('.mp4') ? (
                    <video 
                      controls 
                      className="w-full max-h-64 bg-gray-100 rounded-lg"
                      src={apiService.getDownloadUrl(result.output_filename)}
                    />
                  ) : (
                    <img 
                      src={apiService.getDownloadUrl(result.output_filename)}
                      alt="Result" 
                      className="w-full max-h-64 object-contain bg-gray-100 rounded-lg"
                    />
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 