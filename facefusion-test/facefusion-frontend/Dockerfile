# べ、別にあんたのためじゃないけど、フロントエンド用Dockerfileを作ってあげるわよ！
# FaceFusion Frontend Dockerfile

# ステージ1: ビルド環境
FROM node:18.17.0-alpine AS builder

WORKDIR /app

# 依存関係ファイルコピー
COPY package*.json ./

# 依存関係インストール
RUN npm install

# ソースコードコピー
COPY . .

# ビルド実行
RUN npm run build

# ステージ2: プロダクション環境
FROM nginx:alpine

# カスタムnginx設定
COPY nginx.conf /etc/nginx/nginx.conf

# ビルド成果物をnginxに配置
COPY --from=builder /app/dist /usr/share/nginx/html

# ポート公開
EXPOSE 3000

# nginx起動
CMD ["nginx", "-g", "daemon off;"] 