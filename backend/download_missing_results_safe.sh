#!/bin/bash
# エラーチェック付き直列ダウンロード

DELAY=3  # リクエスト間隔（秒） - NARScraperと同じ間隔

total=$(wc -l < missing_results.txt)
success=0
error=0
current=0

echo "========================================"
echo "欠損resultファイルダウンロード（直列・エラーチェック付き）"
echo "総数: $total"
echo "間隔: ${DELAY}秒"
echo "開始: $(date)"
echo "========================================"

while IFS=$'\t' read -r filepath url; do
    ((current++))

    # ディレクトリ作成
    mkdir -p "$(dirname "$filepath")"

    # ダウンロード（User-Agentヘッダー付き）
    curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -o "$filepath" "$url"
    sleep "$DELAY"
    
    # HTMLエラーチェック（タイトルに「エラー」が含まれていないか）
    if [ -f "$filepath" ] && [ -s "$filepath" ]; then
        if grep -q "<title>エラー" "$filepath" 2>/dev/null; then
            echo "❌ エラーHTML: $filepath"
            rm -f "$filepath"
            ((error++))
        else
            ((success++))
        fi
    else
        echo "❌ ダウンロード失敗: $filepath"
        ((error++))
    fi
    
    # 進捗表示（100件ごと）
    if [ $((current % 100)) -eq 0 ]; then
        echo "進捗: $current/$total (成功: $success, エラー: $error)"
    fi
done < missing_results.txt

echo ""
echo "========================================"
echo "ダウンロード完了"
echo "成功: $success"
echo "エラー: $error"
echo "終了: $(date)"
echo "========================================"

# 結果確認
echo ""
echo "最終統計:"
for year in 2015 2016 2017 2018 2019 2020 2021 2022; do
    deba=$(find data/html/$year -name "*_deba.html" 2>/dev/null | wc -l)
    result=$(find data/html/$year -name "*_result.html" 2>/dev/null | wc -l)
    printf "%s年: 出馬表 %4d  結果 %4d\n" "$year" "$deba" "$result"
done
