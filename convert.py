import os
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from datetime import datetime

def sync_all_problems():
    print(">> [START] Scanning for .py files...")
    
    # 현재 디렉토리의 모든 파일 검색
    for root, dirs, files in os.walk("."):
        if ".git" in root:
            continue
            
        for file in files:
            if file.endswith(".py") and file != "convert.py":
                py_path = os.path.join(root, file)
                ipynb_path = os.path.splitext(py_path)[0] + ".ipynb"
                
                update_notebook(py_path, ipynb_path)

def update_notebook(py_path, ipynb_path):
    # 1. 파이썬 코드 읽기
    try:
        with open(py_path, 'r', encoding='utf-8') as f:
            py_content = f.read().strip()
    except Exception as e:
        print(f">> [ERROR] Cannot read {py_path}: {e}")
        return

    # 2. 기존 노트북 불러오기 (실패 시 복구 시도)
    nb = None
    if os.path.exists(ipynb_path):
        try:
            with open(ipynb_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            print(f">> [LOAD] Loaded existing notebook: {ipynb_path} (Cells: {len(nb.cells)})")
        except Exception as e:
            print(f">> [WARNING] Corrupted notebook found ({e}). Creating a NEW one.")
            nb = new_notebook()
    else:
        print(f">> [NEW] No notebook found. Creating: {ipynb_path}")
        nb = new_notebook()

    # 3. 내용 추가 (중복 체크 없이 무조건 추가)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 헤더(시간) 추가
    nb.cells.append(new_markdown_cell(f"### Submission at {timestamp}"))
    
    # 코드 추가
    nb.cells.append(new_code_cell(py_content))

    # 4. 저장
    try:
        with open(ipynb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f">> [SUCCESS] Appended new solution. Total cells: {len(nb.cells)}")
    except Exception as e:
        print(f">> [FATAL] Failed to save notebook: {e}")

if __name__ == "__main__":
    sync_all_problems()
