import json
import os
import shutil
from jinja2 import Environment, FileSystemLoader

# 設定
DATA_FILE = 'data.json'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = '.output' 

def load_data(filepath):
    """讀取 JSON 資料"""
    # 錯誤檢查，若無 data.json 則回傳空字典以免報錯
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found, using empty data.")
        return {}
        
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def prepare_output_dir():
    """初始化輸出目錄：清空並重建"""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    print(f"Created directory: {OUTPUT_DIR}")

def copy_static_files():
    """複製靜態資源"""
    # 1. 複製 icon 資料夾
    if os.path.exists('icon'):
        shutil.copytree('icon', os.path.join(OUTPUT_DIR, 'icon'))
        print("Copied: icon/")
    
    # 2. 複製根目錄下的靜態檔案
    files_to_copy = ['CNAME', 'privacy-policy.html', 'profile.jpg']
    
    for filename in files_to_copy:
        if os.path.exists(filename):
            shutil.copy(filename, os.path.join(OUTPUT_DIR, filename))
            print(f"Copied: {filename}")
        else:
            # 因拍完照了但還沒拿到，先給錯誤訊息
            if filename == 'profile.jpg':
                print(f"Info: {filename} not found (skipping).")

def build_site():
    """主建置函式"""
    
    # 步驟 0: 準備乾淨的環境
    prepare_output_dir()
    copy_static_files()

    # 步驟 1: 準備資料
    data = load_data(DATA_FILE)
    
    # 步驟 2: 設定 Jinja2 環境
    # 檢查模板目錄是否存在
    if not os.path.exists(TEMPLATE_DIR):
        print(f"Error: Template directory '{TEMPLATE_DIR}' not found!")
        return

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    
    # 步驟 3: 定義要生成的頁面 (模板檔名 -> 輸出檔名)
    pages = {
        'index_template.html': 'index.html',
        'zh_template.html': 'zh.html'
    }
    
    # 步驟 4: 渲染並寫入檔案
    for template_name, output_name in pages.items():
        try:
            template = env.get_template(template_name)
            rendered_html = template.render(data=data)
            
            output_path = os.path.join(OUTPUT_DIR, output_name)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            
            print(f"Successfully generated: {output_path}")
            
        except Exception as e:
            print(f"Error generating {output_name}: {e}")

if __name__ == "__main__":
    build_site()