# マルチステージビルド - Node.js 18
FROM node:18-alpine AS builder

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonをコピー
COPY package.json ./

# 依存関係をインストール
RUN npm install

# ソースコードをコピー
COPY . .

# プロダクション用ビルド
RUN npm run build

# プロダクション用のNginxステージ
FROM nginx:alpine AS production

# カスタムNginx設定をコピー
COPY nginx.conf /etc/nginx/nginx.conf

# ビルドされた静的ファイルをNginxのドキュメントルートにコピー
COPY --from=builder /app/dist /usr/share/nginx/html

# ポート80を公開
EXPOSE 80

# Nginxを起動
CMD ["nginx", "-g", "daemon off;"] 