#!/bin/bash
# 欠損resultファイルをリスト化

echo "欠損resultファイルをリスト化中..."
> missing_results.txt

for year in 2015 2016 2017 2018 2019 2020 2021 2022; do
    year_dir="data/html/$year"
    
    if [ ! -d "$year_dir" ]; then
        echo "$year: ディレクトリなし"
        continue
    fi
    
    # deba HTMLがあるのにresult HTMLがない場合をリスト化
    find "$year_dir" -name "*_deba.html" | while read deba_file; do
        result_file="${deba_file/_deba.html/_result.html}"
        
        if [ ! -f "$result_file" ]; then
            # URLを生成
            date=$(echo "$deba_file" | grep -oP '\d{8}')
            race=$(echo "$deba_file" | grep -oP 'race_\K\d+' | sed 's/^0*//')
            formatted_date="${date:0:4}-${date:4:2}-${date:6:2}"
            
            url="https://www2.keiba.go.jp/KeibaWeb/TodayRaceInfo/RaceMarkTable?k_raceDate=${formatted_date}&k_raceNo=${race}&k_babaCode=23"
            
            echo -e "${result_file}\t${url}" >> missing_results.txt
        fi
    done
done

count=$(wc -l < missing_results.txt)
echo "欠損ファイル数: $count"
echo "リストを missing_results.txt に保存しました"

# 年別統計
echo ""
echo "年別欠損数:"
for year in 2015 2016 2017 2018 2019 2020 2021 2022; do
    year_count=$(grep -c "html/$year/" missing_results.txt 2>/dev/null || echo 0)
    if [ $year_count -gt 0 ]; then
        echo "  $year: $year_count"
    fi
done
