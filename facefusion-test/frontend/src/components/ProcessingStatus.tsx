import React from 'react';
import { Loader2, XCircle, Zap } from 'lucide-react';
import { ProcessingStatus as StatusType } from '../types';
import { formatTime } from '../utils/api';

interface ProcessingStatusProps {
  status: StatusType;
  processingTime?: number;
}

const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ 
  status, 
  processingTime 
}) => {
  const loadingMessages = [
    "🎭 魔法をかけています...",
    "🔥 GPUが全力で計算中...",
    "✨ 顔を美しく変換中...",
    "🚀 AIが画像を分析中...",
    "⚡ 高品質な結果を生成中...",
    "🎨 アートのような仕上がりを作成中...",
    "🌟 もうすぐ完成です..."
  ];

  const getRandomMessage = () => {
    return loadingMessages[Math.floor(Math.random() * loadingMessages.length)];
  };

  if (!status.isProcessing && !status.error) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="card max-w-md w-full mx-4">
        <div className="p-8 text-center">
          {status.isProcessing ? (
            <div className="space-y-6">
              {/* アニメーションアイコン */}
              <div className="flex justify-center">
                <div className="relative">
                  <Loader2 className="w-16 h-16 text-blue-500 animate-spin" />
                  <Zap className="w-8 h-8 text-yellow-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-pulse" />
                </div>
              </div>

              {/* メッセージ */}
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  処理中...
                </h3>
                <p className="text-gray-600 mb-4">
                  {status.message || getRandomMessage()}
                </p>
                
                {processingTime && (
                  <p className="text-sm text-gray-500">
                    処理時間: {formatTime(processingTime)}
                  </p>
                )}
              </div>

              {/* プログレスバー */}
              {status.progress !== undefined ? (
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-300"
                    style={{ width: `${status.progress}%` }}
                  />
                  <p className="text-sm text-gray-600 mt-2">{status.progress}%</p>
                </div>
              ) : (
                <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-blue-500 to-purple-600 animate-pulse" />
                </div>
              )}

              {/* 注意事項 */}
              <div className="text-xs text-gray-500 bg-gray-50 p-3 rounded-lg">
                <p>💡 高品質な結果のため、通常1-3分程度かかります</p>
                <p>🔄 ページを閉じずにお待ちください</p>
              </div>
            </div>
          ) : status.error ? (
            <div className="space-y-6">
              {/* エラーアイコン */}
              <div className="flex justify-center">
                <XCircle className="w-16 h-16 text-red-500" />
              </div>

              {/* エラーメッセージ */}
              <div>
                <h3 className="text-xl font-semibold text-red-600 mb-2">
                  エラーが発生しました
                </h3>
                <p className="text-gray-600 mb-4">
                  {status.error}
                </p>
              </div>

              {/* 再試行ボタン */}
              <button 
                onClick={() => window.location.reload()}
                className="btn-primary"
              >
                ページを再読み込み
              </button>

              {/* トラブルシューティング */}
              <div className="text-xs text-gray-500 bg-red-50 p-3 rounded-lg text-left">
                <p className="font-semibold mb-2">トラブルシューティング:</p>
                <ul className="space-y-1">
                  <li>• ファイルサイズが500MB以下か確認</li>
                  <li>• 対応形式(JPG, PNG, MP4)か確認</li>
                  <li>• インターネット接続を確認</li>
                  <li>• しばらく時間をおいてから再試行</li>
                </ul>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default ProcessingStatus; 