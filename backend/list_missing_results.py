#!/usr/bin/env python3
"""
欠損しているresult HTMLファイルのURLをリスト化
"""
import yaml
from pathlib import Path

def main():
    missing_urls = []
    
    for year in range(2015, 2023):  # 2015-2022
        schedule_file = Path(f"data/{year}_schedule.yaml")
        if not schedule_file.exists():
            continue
            
        with open(schedule_file) as f:
            schedule = yaml.safe_load(f)
        
        for date_key, races in schedule.items():
            date_str = date_key.replace('-', '')  # 2022-04-03 → 20220403
            
            for race in races:
                race_num = race['race_number']
                result_file = Path(f"data/html/{year}/{date_str}/race_{race_num:02d}_result.html")
                
                if not result_file.exists():
                    # URLを生成
                    url = f"https://www2.keiba.go.jp/KeibaWeb/TodayRaceInfo/DebaTable?k_raceDate={date_key}&k_raceNo={race_num}&k_babaCode=23"
                    missing_urls.append({
                        'year': year,
                        'date': date_str,
                        'race': race_num,
                        'file': str(result_file),
                        'url': url.replace('DebaTable', 'RaceMarkTable')  # result用URL
                    })
    
    print(f"欠損ファイル数: {len(missing_urls)}")
    
    # URLリストをファイルに保存
    with open('missing_results.txt', 'w') as f:
        for item in missing_urls:
            f.write(f"{item['file']}\t{item['url']}\n")
    
    print(f"リストを missing_results.txt に保存しました")
    
    # 年別統計
    from collections import Counter
    year_counts = Counter(item['year'] for item in missing_urls)
    print("\n年別欠損数:")
    for year in sorted(year_counts.keys()):
        print(f"  {year}: {year_counts[year]}")

if __name__ == '__main__':
    main()
