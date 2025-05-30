import React, { useState, useRef, useCallback } from 'react';
import { Upload, X, Image, Video, FileText } from 'lucide-react';
import { UploadedFile } from '../types';
import { formatFileSize, getFileType, createFilePreview } from '../utils/api';

interface FileUploadProps {
  onFileSelect: (file: UploadedFile) => void;
  acceptedTypes: string[];
  title: string;
  description: string;
  maxSize?: number; // MB
  currentFile?: UploadedFile | null;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  acceptedTypes,
  title,
  description,
  maxSize = 500,
  currentFile,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelection = useCallback(async (file: File) => {
    setIsProcessing(true);
    
    try {
      // ファイルサイズチェック
      const fileSizeMB = file.size / (1024 * 1024);
      if (fileSizeMB > maxSize) {
        alert(`ファイルサイズが${maxSize}MBを超えています`);
        return;
      }

      // ファイルタイプチェック
      const fileType = getFileType(file);
      if (fileType === 'unknown') {
        alert('サポートされていないファイル形式です');
        return;
      }

      // プレビューを作成
      const preview = await createFilePreview(file);

      const uploadedFile: UploadedFile = {
        file,
        preview,
        type: fileType,
        size: file.size,
      };

      onFileSelect(uploadedFile);
    } catch (error) {
      console.error('ファイル処理エラー:', error);
      alert('ファイルの処理中にエラーが発生しました');
    } finally {
      setIsProcessing(false);
    }
  }, [onFileSelect, maxSize]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  }, [handleFileSelection]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      handleFileSelection(files[0]);
    }
  }, [handleFileSelection]);

  const handleRemoveFile = useCallback(() => {
    onFileSelect(null as any);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, [onFileSelect]);

  const handleClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const getFileIcon = (type: 'image' | 'video') => {
    switch (type) {
      case 'image':
        return <Image className="w-8 h-8 text-blue-500" />;
      case 'video':
        return <Video className="w-8 h-8 text-purple-500" />;
      default:
        return <FileText className="w-8 h-8 text-gray-500" />;
    }
  };

  return (
    <div className="w-full">
      {!currentFile ? (
        <div
          className={`upload-area cursor-pointer relative ${
            isDragging ? 'active' : ''
          } ${isProcessing ? 'opacity-50 pointer-events-none' : ''}`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={handleClick}
        >
          <div className="flex flex-col items-center space-y-4">
            <div className={`p-4 rounded-full ${isDragging ? 'bg-blue-100' : 'bg-gray-100'} 
                         transition-colors duration-300`}>
              <Upload className={`w-12 h-12 ${isDragging ? 'text-blue-500' : 'text-gray-400'}`} />
            </div>
            
            <div className="text-center">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {title}
              </h3>
              <p className="text-gray-600 mb-4">
                {isDragging ? 'ファイルをここにドロップ' : description}
              </p>
              
              {isProcessing ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                  <span className="ml-2 text-sm text-gray-600">処理中...</span>
                </div>
              ) : (
                <div className="btn-primary inline-block">
                  ファイルを選択
                </div>
              )}
            </div>
            
            <div className="text-xs text-gray-500 text-center">
              <p>対応形式: {acceptedTypes.join(', ')}</p>
              <p>最大サイズ: {maxSize}MB</p>
            </div>
          </div>

          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            accept={acceptedTypes.join(',')}
            onChange={handleFileInputChange}
          />
        </div>
      ) : (
        <div className="card p-6">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              {currentFile.type === 'image' ? (
                <img
                  src={currentFile.preview}
                  alt="Preview"
                  className="w-20 h-20 object-cover rounded-lg"
                />
              ) : (
                <div className="w-20 h-20 bg-gray-100 rounded-lg flex items-center justify-center">
                  {getFileIcon(currentFile.type)}
                </div>
              )}
            </div>

            <div className="flex-1 min-w-0">
              <h4 className="text-lg font-semibold text-gray-900 truncate">
                {currentFile.file.name}
              </h4>
              <p className="text-sm text-gray-600 mt-1">
                {formatFileSize(currentFile.size)} • {currentFile.type === 'image' ? '画像' : '動画'}
              </p>
              <div className="mt-3">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  ✓ 選択済み
                </span>
              </div>
            </div>

            <button
              onClick={handleRemoveFile}
              className="flex-shrink-0 p-2 text-gray-400 hover:text-red-500 transition-colors duration-200"
              title="ファイルを削除"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload; 