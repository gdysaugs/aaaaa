import React from 'react';
import { Download, Share2, RefreshCcw } from 'lucide-react';
import { FaceSwapResponse } from '../types';
import { formatTime, formatFileSize } from '../utils/api';

interface ResultDisplayProps {
  result: FaceSwapResponse;
  downloadUrl: string;
  onNewProcess: () => void;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({
  result,
  downloadUrl,
  onNewProcess,
}) => {
  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = result.output_filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: '🎭 FaceFusion - AI Face Swap結果',
          text: 'AI技術で作成した顔変換結果をチェックしてみて！',
          url: window.location.href,
        });
      } catch (error) {
        console.log('シェア機能がキャンセルされました');
      }
    } else {
      navigator.clipboard.writeText(window.location.href);
      alert('URLをクリップボードにコピーしました！');
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
          <span className="text-2xl">🎉</span>
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Face Swap完了！
        </h2>
        <p className="text-gray-600">
          {result.message}
        </p>
      </div>

      <div className="card overflow-hidden">
        <div className="relative group">
          {result.media_type === 'video' ? (
            <video
              src={downloadUrl}
              controls
              className="w-full h-auto max-h-96 object-contain bg-black"
            >
              お使いのブラウザは動画再生に対応していません。
            </video>
          ) : (
            <img
              src={downloadUrl}
              alt="Face Swap結果"
              className="w-full h-auto max-h-96 object-contain bg-gray-100"
            />
          )}
        </div>

        <div className="p-4 bg-gray-50">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-gray-500">ファイルサイズ</span>
              <p className="font-semibold">{formatFileSize(result.file_size)}</p>
            </div>
            <div>
              <span className="text-gray-500">処理時間</span>
              <p className="font-semibold">{formatTime(result.processing_time)}</p>
            </div>
            <div>
              <span className="text-gray-500">使用モデル</span>
              <p className="font-semibold">{result.model_used || 'N/A'}</p>
            </div>
            <div>
              <span className="text-gray-500">品質</span>
              <p className="font-semibold">{result.quality || 'N/A'}%</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          onClick={handleDownload}
          className="btn-primary flex items-center justify-center"
        >
          <Download className="w-4 h-4 mr-2" />
          ダウンロード
        </button>
        
        <button
          onClick={handleShare}
          className="btn-secondary flex items-center justify-center"
        >
          <Share2 className="w-4 h-4 mr-2" />
          シェア
        </button>
        
        <button
          onClick={onNewProcess}
          className="btn-secondary flex items-center justify-center"
        >
          <RefreshCcw className="w-4 h-4 mr-2" />
          新しい変換
        </button>
      </div>
    </div>
  );
};

export default ResultDisplay; 