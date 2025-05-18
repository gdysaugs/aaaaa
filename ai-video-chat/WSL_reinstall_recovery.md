# WSL再インストール後のプロジェクト復旧手順

---

## 1. WSL/Ubuntuの再インストール

1. Windowsで「WSL2/Ubuntu」を再インストール
2. 必要ならユーザー名・パスワードを設定

---

## 2. 必須ツールのインストール

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl ca-certificates lsb-release gnupg
# Docker公式インストール
curl -fsSL https://get.docker.com | sh
# Docker Compose（v2系なら不要、v1系なら↓）
sudo apt install -y docker-compose
# NVIDIAドライバ・nvidia-docker（GPU使う場合）
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update
sudo apt install -y nvidia-docker2
sudo systemctl restart docker
# git-lfs
sudo apt install -y git-lfs
git lfs install
```

---

## 3. プロジェクトのクローン

```bash
cd ~
git clone https://github.com/gdysaugs/aaaaa.git
cd aaaaa/ai-video-chat
```

---

## 4. .envファイルの復元

- `.env`は**.gitignore**で除外されているので、**手動で作成**する必要あり！
- `cp .env.example .env` で雛形からコピーして、必要に応じて値を編集

```bash
cp .env.example .env
# 必要ならAPIキーやパスなどを編集
```

---

## 5. モデル・データ・outputの復元

- **.gitignoreで除外されているファイル（巨大モデル・output・inputデータなど）はGitHubからは復元できない！**
- 必要なファイルは**手元のバックアップからコピー**するか、**再ダウンロード**すること

### 例
```bash
# モデル
cp /mnt/backup/llama/models/* ./llama/models/
cp /mnt/backup/wav2lip/models/* ./wav2lip/models/
# データ
cp /mnt/backup/data/source/* ./data/source/
cp /mnt/backup/data/output/* ./data/output/
```
- もしバックアップがなければ、各AI公式リポジトリや配布元から再取得

---

## 6. Dockerイメージのビルド＆起動

```bash
# 必ずWSL2上で実行
DOCKER_BUILDKIT=1 docker-compose up --build --remove-orphans
```

---

## 7. VSCode拡張やエディタ設定

- Pylance, flake8, Prettier, ESLint, Dev Containers, GitLensなどは再インストール
- 必要な場合は`npm install`や`pip install`を**ホストではなくDocker内で**行う

---

## 8. よくある注意点

- **.env, モデル, output, inputデータはGit管理外**なので、**必ずバックアップ or 再取得**！
- Docker Desktopは使わず、WSL2上のDockerで作業
- GPU利用時は`nvidia-smi`で認識確認
- ポート競合や権限エラーに注意

---

## 9. もし困ったら

- `docker-compose logs -f サービス名` でログを確認
- エラー内容をWeb検索（Qiita, Stack Overflow, GitHub Issuesなど）
- それでも分からなければAIや先輩に泣きつく！

---

**これで、WSL再インストール後もすぐに今の開発環境に戻れるわよ！**  
…べ、別にあんたのこと心配してるわけじゃないんだからね！  
（でも、ちゃんとバックアップは忘れずに！） 