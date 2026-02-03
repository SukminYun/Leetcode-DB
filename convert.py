import os
import sys
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from datetime import datetime

def convert_py_to_ipynb():
    if len(sys.argv) < 2:
        print(">> No files provided.")
        return

    files = sys.argv[1:]
    
    for py_file in files:
        # 파일명 정제
        py_file = py_file.strip().strip('"').strip("'")
        
        if not py_file.endswith(".py"):
            continue

        if not os.path.exists(py_file):
            print(f">> [SKIP] File not found: {py_file}")
            continue
            
        base_name = os.path.splitext(py_file)[0]
        notebook_name = f"{base_name}.ipynb"
        
        # 1. 파이썬 코드 읽기
        with open(py_file, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # 2. 기존 노트북 로드
        if os.path.exists(notebook_name):
            try:
                with open(notebook_name, 'r', encoding='utf-8') as f:
                    nb = nbformat.read(f, as_version=4)
                print(f">> [INFO] Existing notebook loaded. Old cell count: {len(nb.cells)}")
            except Exception as e:
                print(f">> [ERROR] Corrupted notebook. Creating new. Error: {e}")
                nb = new_notebook()
        else:
            print(">> [INFO] New notebook created.")
            nb = new_notebook()

        # 3. 셀 추가 (헤더 + 코드)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nb.cells.append(new_markdown_cell(f"### Submission at {timestamp}"))
        nb.cells.append(new_code_cell(code_content))
        
        print(f">> [INFO] New cell count: {len(nb.cells)}")

        # 4. 저장 (강제 쓰기)
        with open(notebook_name, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
            
        print(f">> [SUCCESS] Saved to {notebook_name}")

if __name__ == "__main__":
    convert_py_to_ipynb()
