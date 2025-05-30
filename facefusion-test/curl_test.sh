#!/bin/bash
# べ、別にあんたのためじゃないけど、curlテストを作ってあげるわよ！

echo "🎭 FaceFusion API Curl テスト"
echo "べ、別にあんたのためじゃないけど、curlでテストしてあげるわよ！"
echo "============================================================"

BASE_URL="http://localhost:8000"

echo "🔍 1. ヘルスチェック"
curl -s "$BASE_URL/health" | python3 -m json.tool

echo -e "\n🤖 2. モデル情報取得"
curl -s "$BASE_URL/models" | python3 -m json.tool

echo -e "\n🎬 3. CLI Face Swap実行"
echo "ソース: kanna-hashimoto.jpg"
echo "ターゲット: 画面録画 2025-05-16 222902.mp4"
echo "出力: curl_test_output.mp4"

curl -X POST "$BASE_URL/cli/face-swap" \
     -H "Content-Type: application/json" \
     -d '{
       "source_path": "/app/data/source/kanna-hashimoto.jpg",
       "target_path": "/app/data/source/画面録画 2025-05-16 222902.mp4",
       "output_path": "/app/data/output/curl_test_output.mp4",
       "face_swapper_model": "inswapper_128",
       "output_video_quality": 80,
       "trim_frame_start": 0,
       "trim_frame_end": 30
     }' | python3 -m json.tool

echo -e "\n✅ Curl テスト完了!"
echo "📁 出力ファイル確認:"
ls -la data/output/curl_test_output.mp4 2>/dev/null || echo "   出力ファイルがまだ作成されていません"

echo -e "\n🌐 Swagger UI URL: http://localhost:8000"
echo "📄 詳細ガイド: swagger_usage_guide.md" 