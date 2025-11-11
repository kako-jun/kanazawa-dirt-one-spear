#!/bin/bash
# 2024年と2023年を順次スクレイピング

cd "$(dirname "$0")"

echo "========================================"
echo "2024年 スクレイピング開始"
echo "開始時刻: $(date)"
echo "========================================"

uv run python3 scrape_from_yaml.py data/2024_schedule.yaml --results

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 2024年 完了"
    echo "終了時刻: $(date)"
    echo ""
else
    echo ""
    echo "❌ 2024年 エラー発生"
    echo "終了時刻: $(date)"
    echo ""
    exit 1
fi

echo "========================================"
echo "2023年 スクレイピング開始"
echo "開始時刻: $(date)"
echo "========================================"

uv run python3 scrape_from_yaml.py data/2023_schedule.yaml --results

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 2023年 完了"
    echo "終了時刻: $(date)"
    echo ""
else
    echo ""
    echo "❌ 2023年 エラー発生"
    echo "終了時刻: $(date)"
    echo ""
    exit 1
fi

echo "========================================"
echo "全スクレイピング完了"
echo "終了時刻: $(date)"
echo "========================================"

# 統計表示
echo ""
echo "収集統計:"
find data/html/2024 -name "*_deba.html" 2>/dev/null | wc -l | xargs echo "2024年 出馬表HTML数:"
find data/html/2024 -name "*_result.html" 2>/dev/null | wc -l | xargs echo "2024年 結果HTML数:"
find data/html/2023 -name "*_deba.html" 2>/dev/null | wc -l | xargs echo "2023年 出馬表HTML数:"
find data/html/2023 -name "*_result.html" 2>/dev/null | wc -l | xargs echo "2023年 結果HTML数:"
du -sh data/html/2024 2>/dev/null
du -sh data/html/2023 2>/dev/null
du -sh kanazawa_dirt_one_spear.db 2>/dev/null
