#!/bin/bash
# 欠損している結果データを追加スクレイピング

cd "$(dirname "$0")"

echo "========================================"
echo "欠損結果データの追加スクレイピング"
echo "開始時刻: $(date)"
echo "========================================"

# 2015-2022年の結果データを取得
for year in 2022 2021 2020 2019 2018 2017 2016 2015; do
    echo ""
    echo "========================================"
    echo "${year}年 結果データ取得"
    echo "開始時刻: $(date)"
    echo "========================================"

    uv run python3 scrape_from_yaml.py "data/${year}_schedule.yaml" --results

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ ${year}年 完了"
        echo "終了時刻: $(date)"
    else
        echo ""
        echo "❌ ${year}年 エラー発生"
        echo "終了時刻: $(date)"
    fi
done

# 2023年と2024年の部分的欠損を修正
echo ""
echo "========================================"
echo "2023-2024年 部分欠損の修正"
echo "========================================"

for year in 2024 2023; do
    echo "${year}年 再実行..."
    uv run python3 scrape_from_yaml.py "data/${year}_schedule.yaml" --results
done

echo ""
echo "========================================"
echo "全スクレイピング完了"
echo "終了時刻: $(date)"
echo "========================================"

# 統計表示
echo ""
echo "収集統計:"
for year in 2025 2024 2023 2022 2021 2020 2019 2018 2017 2016 2015; do
    deba=$(find data/html/$year -name "*_deba.html" 2>/dev/null | wc -l)
    result=$(find data/html/$year -name "*_result.html" 2>/dev/null | wc -l)
    printf "%s年: 出馬表 %4d  結果 %4d\n" "$year" "$deba" "$result"
done

echo ""
du -sh data/html
du -sh kanazawa_dirt_one_spear.db
