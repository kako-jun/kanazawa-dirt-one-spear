#!/bin/bash
# 2025年から2015年まで順次スクレイピング
# 完全自動実行スクリプト

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/scrape_all_${TIMESTAMP}.log"

echo "========================================" | tee -a "$LOG_FILE"
echo "全年度スクレイピング開始" | tee -a "$LOG_FILE"
echo "開始時刻: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 2025年から2015年まで順次実行
for year in 2025 2024 2023 2022 2021 2020 2019 2018 2017 2016 2015
do
    echo "========================================" | tee -a "$LOG_FILE"
    echo "${year}年のスクレイピング開始" | tee -a "$LOG_FILE"
    echo "開始時刻: $(date)" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"

    # スクレイピング実行
    uv run python3 scrape_from_yaml.py "data/${year}_schedule.yaml" --results 2>&1 | tee -a "$LOG_FILE"

    EXIT_CODE=${PIPESTATUS[0]}

    if [ $EXIT_CODE -eq 0 ]; then
        echo "" | tee -a "$LOG_FILE"
        echo "✅ ${year}年 完了" | tee -a "$LOG_FILE"
        echo "終了時刻: $(date)" | tee -a "$LOG_FILE"
        echo "" | tee -a "$LOG_FILE"
    else
        echo "" | tee -a "$LOG_FILE"
        echo "❌ ${year}年 エラー発生 (exit code: $EXIT_CODE)" | tee -a "$LOG_FILE"
        echo "終了時刻: $(date)" | tee -a "$LOG_FILE"
        echo "" | tee -a "$LOG_FILE"
        # エラーでも継続
    fi

    # 年度間の小休止（5秒）
    if [ $year -ne 2015 ]; then
        echo "次の年度まで5秒待機..." | tee -a "$LOG_FILE"
        sleep 5
    fi
done

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "全年度スクレイピング完了" | tee -a "$LOG_FILE"
echo "終了時刻: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "ログファイル: $LOG_FILE" | tee -a "$LOG_FILE"

# 統計表示
echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "収集統計" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
find data/html -name "*_deba.html" | wc -l | xargs echo "出馬表HTML数:" | tee -a "$LOG_FILE"
find data/html -name "*_result.html" | wc -l | xargs echo "結果HTML数:" | tee -a "$LOG_FILE"
du -sh data/html | tee -a "$LOG_FILE"
du -sh kanazawa_dirt_one_spear.db 2>/dev/null | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
