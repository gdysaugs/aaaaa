import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, Image, Video } from 'lucide-react';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  onFileRemove: () => void;
  selectedFile: File | null;
  accept: string;
  label: string;
  maxSize?: number;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  onFileRemove,
  selectedFile,
  accept,
  label,
  maxSize = 500 * 1024 * 1024 // 500MB
}) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const getAcceptObject = (acceptString: string) => {
    if (acceptString === 'image/*') {
      return {
        'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
      };
    } else if (acceptString === 'video/*') {
      return {
        'video/*': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
      };
    } else if (acceptString === 'image/*,video/*') {
      return {
        'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'],
        'video/*': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
      };
    } else {
      const types = acceptString.split(',').map(type => type.trim());
      const acceptObject: Record<string, string[]> = {};
      
      types.forEach(type => {
        if (type === 'image/*') {
          acceptObject['image/*'] = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'];
        } else if (type === 'video/*') {
          acceptObject['video/*'] = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'];
        } else if (type.startsWith('.')) {
          acceptObject[type] = [type];
        }
      });
      
      return acceptObject;
    }
  };

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: getAcceptObject(accept),
    maxSize,
    multiple: false
  });

  const getFileIcon = (file: File) => {
    if (file.type.startsWith('image/')) {
      return <Image className="w-8 h-8 text-blue-500" />;
    } else if (file.type.startsWith('video/')) {
      return <Video className="w-8 h-8 text-purple-500" />;
    }
    return <Upload className="w-8 h-8 text-gray-500" />;
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      
      {selectedFile ? (
        <div className="border-2 border-gray-300 border-dashed rounded-lg p-4 bg-gray-50">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              {getFileIcon(selectedFile)}
              <div>
                <p className="text-sm font-medium text-gray-900">
                  {selectedFile.name}
                </p>
                <p className="text-xs text-gray-500">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>
            <button
              onClick={onFileRemove}
              className="p-1 hover:bg-gray-200 rounded-full transition-colors"
            >
              <X className="w-4 h-4 text-gray-500" />
            </button>
          </div>
        </div>
      ) : (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-blue-400 bg-blue-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
          {isDragActive ? (
            <p className="text-blue-600">ファイルをドロップしてください...</p>
          ) : (
            <div>
              <p className="text-gray-600 mb-1">
                ファイルをドラッグ&ドロップするか、クリックして選択
              </p>
              <p className="text-xs text-gray-500">
                最大サイズ: {formatFileSize(maxSize)}
              </p>
            </div>
          )}
        </div>
      )}

      {fileRejections.length > 0 && (
        <div className="mt-2">
          {fileRejections.map(({ file, errors }) => (
            <div key={file.name} className="text-red-600 text-sm">
              {errors.map(error => (
                <p key={error.code}>{error.message}</p>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FileUpload; 