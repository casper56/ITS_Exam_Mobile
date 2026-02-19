import csv
import json
import os
import sys

def convert_csv_to_json(csv_file):
    if not os.path.exists(csv_file):
        print(f"錯誤：找不到 CSV 檔案 '{csv_file}'")
        return

    # 取得原始檔名並設定輸出 JSON 檔名
    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    output_file = f"{base_name}.json"

    # --- 您指定的 V3.5+ 專業樣式與標頭 ---
    style_string = "<style>.q-table td { vertical-align: middle; } .header-bg { background: #f8f9fa; font-weight: bold; text-align: center; } .category-title { background: #e2e3e5; font-weight: bold; color: #383d41; } .code-font { font-family: 'Cascadia Code', Consolas, monospace; color: #0056b3; font-size: 13px; }</style>"
    table_header_string = "<table class=\"q-table w-100 t-center\">  <thead>    <tr class=\"header-bg\">      <td class=\"w-15\">指令 (Command)</td>      <td class=\"w-42\">公式 / 語法結構</td>      <td class=\"w-42\">參數與功能說明</td>    </tr>  </thead>  <tbody>"

    rows_html = []
    
    try:
        # 讀取 CSV
        with open(csv_file, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            # 跳過第一列標題列
            next(reader, None)
            
            for row in reader:
                if not row or len(row) == 0: continue
                row = [col.strip() for col in row]
                
                # 判定分類標題 (只有第一欄有字，其餘為空)
                is_category = len(row) == 1 or (len(row) >= 3 and not row[1] and not row[2])
                
                if is_category:
                    rows_html.append(f"    <tr class=\"category-title\"><td colspan=\"3\">{row[0]}</td></tr>")
                else:
                    cmd = row[0]
                    syntax = row[1] if len(row) > 1 else ""
                    desc = row[2] if len(row) > 2 else ""
                    
                    rows_html.append("    <tr>")
                    rows_html.append(f"      <td><b>{cmd}</b></td>")
                    rows_html.append(f"      <td class=\"code-font\">{syntax}</td>")
                    rows_html.append(f"      <td>{desc}</td>")
                    rows_html.append("    </tr>")

        table_footer = "  </tbody></table>"
        
        # 最終只輸出這段 HTML 陣列，不包含任何題目 Meta 資料
        final_content_array = [
            style_string,
            table_header_string
        ] + rows_html + [table_footer]

        # 輸出成純 JSON 陣列檔案
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_content_array, f, ensure_ascii=False, indent=4)

        print(f"--- 轉換成功 ---")
        print(f"已產出純內容 JSON：{output_file}")
        print(f"您可以直接開啟此檔案，將裡面的陣列內容貼入目標 JSON 的 explanation 欄位中。")

    except Exception as e:
        print(f"錯誤：{e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python convert_csv_to_json.py [您的CSV檔名.csv]")
    else:
        convert_csv_to_json(sys.argv[1])
