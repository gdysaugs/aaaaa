import React from 'react';
import { Settings, Zap, Video, Scissors } from 'lucide-react';
import { AppSettings } from '../types';

interface SettingsPanelProps {
  settings: AppSettings;
  onSettingsChange: (settings: AppSettings) => void;
  availableModels: string[];
  isVideoMode: boolean;
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({
  settings,
  onSettingsChange,
  availableModels,
  isVideoMode,
}) => {
  const modelDescriptions: Record<string, string> = {
    inswapper_128: '高速・標準品質（推奨）',
    inswapper_128_fp16: '高速・省メモリ',
    ghost_2_256: '最高品質（時間がかかる）',
    blendswap_256: '自然な仕上がり',
    ghost_1_256: '高品質・バランス型',
    ghost_3_256: '最高品質（重い処理）',
    simswap_256: 'リアルタイム向け',
    uniface_256: 'ユニバーサル対応',
  };

  const handleChange = (key: keyof AppSettings, value: any) => {
    onSettingsChange({
      ...settings,
      [key]: value,
    });
  };

  return (
    <div className="card p-6">
      <div className="flex items-center space-x-2 mb-6">
        <Settings className="w-5 h-5 text-gray-600" />
        <h3 className="text-lg font-semibold text-gray-900">処理設定</h3>
      </div>

      <div className="space-y-6">
        {/* AIモデル選択 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Zap className="w-4 h-4 inline mr-1" />
            AIモデル
          </label>
          <select
            value={settings.model}
            onChange={(e) => handleChange('model', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
          >
            {availableModels.map((model) => (
              <option key={model} value={model}>
                {model} - {modelDescriptions[model] || '高品質モデル'}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1">
            💡 初回利用時は「inswapper_128」がおすすめです
          </p>
        </div>

        {/* 品質設定 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            品質: {settings.quality}%
          </label>
          <input
            type="range"
            min="60"
            max="100"
            value={settings.quality}
            onChange={(e) => handleChange('quality', parseInt(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>高速 (60%)</span>
            <span>高品質 (100%)</span>
          </div>
        </div>

        {/* 動画専用設定 */}
        {isVideoMode && (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Video className="w-4 h-4 inline mr-1" />
                最大フレーム数: {settings.maxFrames}
              </label>
              <input
                type="range"
                min="10"
                max="200"
                value={settings.maxFrames}
                onChange={(e) => handleChange('maxFrames', parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>短時間 (10)</span>
                <span>長時間 (200)</span>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                ⚡ フレーム数が多いほど処理時間が長くなります
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Scissors className="w-4 h-4 inline mr-1" />
                  開始フレーム
                </label>
                <input
                  type="number"
                  min="0"
                  max={settings.maxFrames - 1}
                  value={settings.trimStart}
                  onChange={(e) => handleChange('trimStart', parseInt(e.target.value) || 0)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  終了フレーム
                </label>
                <input
                  type="number"
                  min={settings.trimStart + 1}
                  max={settings.maxFrames}
                  value={settings.trimEnd || settings.maxFrames}
                  onChange={(e) => handleChange('trimEnd', parseInt(e.target.value) || undefined)}
                  placeholder="自動"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          </>
        )}

        {/* 処理時間の目安 */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="text-sm font-semibold text-blue-800 mb-2">⏱️ 処理時間の目安</h4>
          <div className="text-xs text-blue-700 space-y-1">
            {isVideoMode ? (
              <>
                <p>• 短い動画(~30フレーム): 1-2分</p>
                <p>• 中程度(~50フレーム): 2-3分</p>
                <p>• 長い動画(100+フレーム): 5-10分</p>
              </>
            ) : (
              <>
                <p>• 画像処理: 30秒-1分</p>
                <p>• 高解像度画像: 1-2分</p>
              </>
            )}
            <p className="font-semibold">💡 GPUを使用して高速処理中！</p>
          </div>
        </div>

        {/* リセットボタン */}
        <button
          onClick={() => onSettingsChange({
            model: 'inswapper_128',
            quality: isVideoMode ? 80 : 90,
            maxFrames: 50,
            trimStart: 0,
            trimEnd: undefined,
          })}
          className="btn-secondary w-full"
        >
          デフォルト設定に戻す
        </button>
      </div>
    </div>
  );
};

export default SettingsPanel; 