#!/usr/bin/env python3
"""
Parse jockey master data from HTML and output to YAML.

This script extracts jockey master information from the official jockey list page,
including license numbers, birth dates, furigana, and gender.
"""

import re
import yaml
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime


def parse_jockey_html(html_path: Path) -> list[dict]:
    """
    Parse jockey master data from HTML.

    Args:
        html_path: Path to jockeys_kanazawa.html

    Returns:
        List of jockey dictionaries
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    jockeys = []

    # Find all jockey list items for Kanazawa (data-belong="kana")
    items = soup.find_all('li', class_='guideList__item', attrs={'data-belong': 'kana'})

    print(f"Found {len(items)} Kanazawa jockeys")

    skipped_items = []

    for item in items:
        try:
            # Extract data attributes
            birth_date_str = item.get('data-birth')  # YYYYMMDD format
            gender = item.get('data-sex')  # 'male' or 'female'

            # Extract link and license number
            link = item.find('a', class_='guideList__link')
            if not link:
                skipped_items.append(('no link', item.get_text(strip=True)[:50]))
                continue

            href = link.get('href', '')
            license_match = re.search(r'k_riderLicenseNo=(\d+)', href)
            if not license_match:
                skipped_items.append(('no license', item.get_text(strip=True)[:50]))
                continue

            license_no = license_match.group(1)

            # Extract name and furigana
            name_elem = item.find('p', class_='guideList__name')
            furigana_elem = item.find('p', class_='guideList__firigana')

            if not name_elem:
                skipped_items.append(('no name', item.get_text(strip=True)[:50]))
                continue

            name = name_elem.get_text(strip=True)
            furigana = furigana_elem.get_text(strip=True) if furigana_elem else None

            # Parse birth date (YYYYMMDD -> YYYY-MM-DD)
            birth_date = None
            if birth_date_str and len(birth_date_str) == 8:
                try:
                    year = birth_date_str[0:4]
                    month = birth_date_str[4:6]
                    day = birth_date_str[6:8]
                    birth_date = f"{year}-{month}-{day}"
                    # Validate date
                    datetime.strptime(birth_date, '%Y-%m-%d')
                except ValueError:
                    print(f"Warning: Invalid birth date for {name}: {birth_date_str}")
                    birth_date = None

            jockey_data = {
                'license_no': license_no,
                'name': name,
                'furigana': furigana,
                'birth_date': birth_date,
                'gender': gender,
                'belonging': 'kana',  # 金沢所属
            }

            jockeys.append(jockey_data)

        except Exception as e:
            print(f"Error parsing jockey item: {e}")
            skipped_items.append(('exception', str(e)[:50]))
            continue

    # Print skipped items for debugging
    if skipped_items:
        print(f"\nSkipped {len(skipped_items)} items:")
        for reason, text in skipped_items:
            print(f"  {reason}: {text}")

    return jockeys


def main():
    """Main execution."""
    # Paths
    backend_dir = Path(__file__).parent
    html_path = backend_dir / 'data' / 'reference_data' / 'html' / 'guide' / 'jockeys_kanazawa.html'
    output_dir = backend_dir / 'data' / 'reference_data' / 'yaml' / 'master'
    output_path = output_dir / 'jockeys_kanazawa.yaml'

    # Validate input
    if not html_path.exists():
        print(f"Error: HTML file not found: {html_path}")
        return

    print(f"Parsing jockey master data from: {html_path}")

    # Parse HTML
    jockeys = parse_jockey_html(html_path)

    print(f"Parsed {len(jockeys)} jockeys")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write YAML
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump({
            'metadata': {
                'source': 'https://www.keiba.go.jp/guide/jockey/?belong=kana',
                'parsed_at': datetime.now().isoformat(),
                'total_jockeys': len(jockeys),
            },
            'jockeys': jockeys,
        }, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print(f"✅ Jockey master data written to: {output_path}")

    # Print sample
    if jockeys:
        print("\nSample jockey data:")
        for jockey in jockeys[:3]:
            print(f"  - {jockey['name']} ({jockey['furigana']}) - Born: {jockey['birth_date']} - License: {jockey['license_no']}")


if __name__ == '__main__':
    main()
