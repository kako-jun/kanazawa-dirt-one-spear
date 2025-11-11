#!/bin/bash
echo "現在のファイル数:"
for year in 2015 2016 2017 2018 2019 2020 2021 2022; do
    deba=$(find data/html/$year -name "*_deba.html" 2>/dev/null | wc -l)
    result=$(find data/html/$year -name "*_result.html" 2>/dev/null | wc -l)
    printf "%s年: 出馬表 %4d  結果 %4d\n" "$year" "$deba" "$result"
done
