FROM node:18-alpine AS builder

WORKDIR /app

# 依存関係インストール
COPY ./frontend/package.json ./frontend/package-lock.json* ./
RUN npm ci

# ソースコードコピー
COPY ./frontend /app/

# ビルド
RUN npm run build

# 実行ステージ
FROM nginx:alpine

# ビルド成果物をnginxにコピー
COPY --from=builder /app/dist /usr/share/nginx/html

# nginx設定
COPY ./frontend/nginx.conf /etc/nginx/conf.d/default.conf

# ポート公開
EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"] 