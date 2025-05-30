import { useState, useEffect } from 'react';
import { Sparkles, Cpu, Zap, Github } from 'lucide-react';
import FileUpload from './components/FileUpload';
import ProcessingStatus from './components/ProcessingStatus';
import SettingsPanel from './components/SettingsPanel';
import ResultDisplay from './components/ResultDisplay';
import { UploadedFile, ProcessingStatus as ProcessingStatusType, AppSettings, FaceSwapResponse } from './types';
import { api } from './utils/api';

function App() {
  // 状態管理
  const [sourceFile, setSourceFile] = useState<UploadedFile | null>(null);
  const [targetFile, setTargetFile] = useState<UploadedFile | null>(null);
  const [result, setResult] = useState<FaceSwapResponse | null>(null);
  const [processing, setProcessing] = useState<ProcessingStatusType>({
    isProcessing: false,
  });
  const [settings, setSettings] = useState<AppSettings>({
    model: 'inswapper_128',
    quality: 80,
    maxFrames: 50,
    trimStart: 0,
    trimEnd: undefined,
  });
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [systemInfo, setSystemInfo] = useState<any>(null);

  // 初期化
  useEffect(() => {
    loadSystemInfo();
    loadModels();
  }, []);

  const loadSystemInfo = async () => {
    try {
      const info = await api.healthCheck();
      setSystemInfo(info);
    } catch (error) {
      console.error('システム情報の取得に失敗:', error);
    }
  };

  const loadModels = async () => {
    try {
      const models = await api.getModels();
      setAvailableModels(models.available_models);
    } catch (error) {
      console.error('モデル情報の取得に失敗:', error);
      setAvailableModels(['inswapper_128']); // フォールバック
    }
  };

  const handleFaceSwap = async () => {
    if (!sourceFile || !targetFile) {
      alert('ソースファイルとターゲットファイルの両方を選択してください');
      return;
    }

    setProcessing({ isProcessing: true, message: '🎭 AI魔法をかけています...' });
    setResult(null);

    try {
      const isVideo = targetFile.type === 'video';
      
      let response: FaceSwapResponse;
      
      if (isVideo) {
        response = await api.faceSwapVideo(sourceFile.file, targetFile.file, {
          model: settings.model,
          quality: settings.quality,
          maxFrames: settings.maxFrames,
          trimStart: settings.trimStart,
          trimEnd: settings.trimEnd,
        });
      } else {
        response = await api.faceSwapImage(sourceFile.file, targetFile.file, {
          model: settings.model,
          quality: settings.quality,
        });
      }

      if (response.success) {
        setResult(response);
        setProcessing({ isProcessing: false });
      } else {
        throw new Error(response.message || 'Face Swap処理に失敗しました');
      }
    } catch (error) {
      console.error('Face Swap処理エラー:', error);
      setProcessing({
        isProcessing: false,
        error: error instanceof Error ? error.message : '処理中にエラーが発生しました',
      });
    }
  };

  const handleNewProcess = () => {
    setSourceFile(null);
    setTargetFile(null);
    setResult(null);
    setProcessing({ isProcessing: false });
  };

  const isVideoMode = targetFile?.type === 'video';
  const canProcess = sourceFile && targetFile && !processing.isProcessing;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <header className="gradient-bg text-white py-6 shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Sparkles className="w-8 h-8" />
              <div>
                <h1 className="text-2xl font-bold">🎭 FaceFusion</h1>
                <p className="text-blue-100 text-sm">AI-Powered Face Swap</p>
              </div>
            </div>
            
            {/* システム状況 */}
            <div className="hidden md:flex items-center space-x-4 text-sm">
              {systemInfo && (
                <>
                  <div className="flex items-center space-x-1">
                    <Cpu className="w-4 h-4" />
                    <span>{systemInfo.gpu_available ? '🟢 GPU' : '🔴 CPU'}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Zap className="w-4 h-4" />
                    <span>CUDA {systemInfo.cuda_version || 'N/A'}</span>
                  </div>
                </>
              )}
              <a
                href="https://github.com/facefusion/facefusion"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-1 hover:text-blue-200 transition-colors"
              >
                <Github className="w-4 h-4" />
                <span>GitHub</span>
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* メインコンテンツ */}
      <main className="container mx-auto px-4 py-8">
        {!result ? (
          <div className="max-w-6xl mx-auto">
            {/* 説明セクション */}
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                AIで顔を簡単に変換
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                ソース画像の顔をターゲット画像・動画に自然に合成します。
                最新のGPU技術で高品質な結果を素早く生成します。
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* ファイルアップロードエリア */}
              <div className="lg:col-span-2 space-y-6">
                {/* ソース画像 */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    1. ソース画像をアップロード
                  </h3>
                  <FileUpload
                    onFileSelect={setSourceFile}
                    acceptedTypes={['.jpg', '.jpeg', '.png']}
                    title="ソース画像を選択"
                    description="変換したい顔の画像をアップロード"
                    maxSize={50}
                    currentFile={sourceFile}
                  />
                </div>

                {/* ターゲットファイル */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    2. ターゲットファイルをアップロード
                  </h3>
                  <FileUpload
                    onFileSelect={setTargetFile}
                    acceptedTypes={['.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi']}
                    title="ターゲットファイルを選択"
                    description="顔を合成する画像または動画をアップロード"
                    maxSize={500}
                    currentFile={targetFile}
                  />
                </div>

                {/* 処理ボタン */}
                {canProcess && (
                  <div className="text-center">
                    <button
                      onClick={handleFaceSwap}
                      className="btn-primary text-lg px-8 py-4"
                      disabled={processing.isProcessing}
                    >
                      🚀 Face Swap実行
                    </button>
                  </div>
                )}
              </div>

              {/* 設定パネル */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  3. 処理設定
                </h3>
                <SettingsPanel
                  settings={settings}
                  onSettingsChange={setSettings}
                  availableModels={availableModels}
                  isVideoMode={isVideoMode}
                />
              </div>
            </div>
          </div>
        ) : (
          /* 結果表示 */
          <div className="max-w-4xl mx-auto">
            <ResultDisplay
              result={result}
              downloadUrl={api.getDownloadUrl(result.output_filename)}
              onNewProcess={handleNewProcess}
            />
          </div>
        )}
      </main>

      {/* フッター */}
      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">
            © 2025 FaceFusion Frontend - べ、別にあんたのためじゃないからね！
          </p>
        </div>
      </footer>

      {/* 処理状況モーダル */}
      <ProcessingStatus status={processing} />
    </div>
  );
}

export default App; 