import csv
import json
import os
import sys

def convert_csv_to_json(csv_file):
    if not os.path.exists(csv_file):
        print(f"錯誤：找不到 CSV 檔案 '{csv_file}'")
        return

    # 取得原始檔名並設定輸出 JSON 檔名 (路徑與原始檔相同)
    base_name = os.path.splitext(csv_file)[0]
    output_file = f"{base_name}.json"

    # --- V3.5+ 專業樣式 ---
    style_string = """<style>.q-table td { vertical-align: middle; } .header-bg { background: #f8f9fa; font-weight: bold; text-align: center; } .category-title { background: #e2e3e5; font-weight: bold; color: #383d41; } .code-font { font-family: 'Cascadia Code', Consolas, monospace; color: #0056b3; font-size: 13px; }</style>"""
    
    rows_html = []
    
    try:
        # 讀取 CSV
        with open(csv_file, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            # 1. 讀取第一列作為標題列 (動態標題)
            headers = next(reader, None)
            if not headers:
                print("錯誤：CSV 檔案為空")
                return
            
            # 根據欄位數量動態生成標題 HTML
            col_count = len(headers)
            header_html = '<table class="q-table w-100 t-left">  <thead>    <tr class="header-bg">'
            for i, h in enumerate(headers):
                # 簡單分配寬度
                width_class = "w-25" if col_count == 4 else "w-33"
                if col_count == 3:
                    width_class = ["w-15", "w-42", "w-42"][i]
                header_html += f'      <td class="{width_class}">{h}</td>'
            header_html += '    </tr>  </thead>  <tbody>'
            
            # 2. 處理資料列
            for row in reader:
                if not row or len(row) == 0: continue
                row = [col.strip() for col in row]
                
                # 判定分類標題 (只有第一欄有字，其餘為空)
                is_category = len(row) == 1 or (len(row) >= 2 and all(not c for c in row[1:]))
                
                if is_category:
                    rows_html.append(f"""    <tr class="category-title"><td colspan="{col_count}">{row[0]}</td></tr>""")
                else:
                    rows_html.append("    <tr>")
                    for i, cell in enumerate(row):
                        # 如果是第二欄 (通常是代碼/語法)，套用 code-font
                        cell_class = ' class="code-font"' if i == 1 else ''
                        # 第一欄加粗 (如果不是分類標題)
                        cell_content = f"<b>{cell}</b>" if i == 0 and cell else cell
                        rows_html.append(f"      <td{cell_class}>{cell_content}</td>")
                    rows_html.append("    </tr>")

        table_footer = "  </tbody></table>"
        
        # 最終輸出
        final_content_array = [
            style_string,
            header_html
        ] + rows_html + [table_footer]

        # 輸出成純 JSON 陣列檔案
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_content_array, f, ensure_ascii=False, indent=4)

        print(f"--- 轉換成功 (動態標題模式) ---")
        print(f"已產出純內容 JSON：{output_file}")

    except Exception as e:
        print(f"錯誤：{e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python convert_csv_to_json.py [您的CSV檔名.csv]")
    else:
        convert_csv_to_json(sys.argv[1])
