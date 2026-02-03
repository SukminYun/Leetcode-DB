import os
import sys
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from datetime import datetime

def convert_py_to_ipynb():
    if len(sys.argv) < 2:
        print(">> No files provided to convert.")
        return

    # 인자로 받은 파일 목록 처리
    files = sys.argv[1:]
    
    for py_file in files:
        # 1. 파일명 앞뒤 공백 및 따옴표 제거 (핵심 수정 사항)
        py_file = py_file.strip().strip('"').strip("'")
        
        # .py 파일이 아니면 스킵
        if not py_file.endswith(".py"):
            continue

        print(f">> Processing: [{py_file}]")

        # 2. 파일이 실제로 존재하는지 확인 (안전장치)
        if not os.path.exists(py_file):
            print(f">> [SKIP] File not found on disk: {py_file} (Maybe deleted or renamed?)")
            continue
            
        base_name = os.path.splitext(py_file)[0]
        notebook_name = f"{base_name}.ipynb"
        
        # .py 파일 내용 읽기
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
        except Exception as e:
            print(f">> [ERROR] Could not read file {py_file}: {e}")
            continue
        
        # 노트북 로드 또는 생성
        if os.path.exists(notebook_name):
            print(f">> [FOUND] Appending to existing notebook: {notebook_name}")
            try:
                with open(notebook_name, 'r', encoding='utf-8') as f:
                    nb = nbformat.read(f, as_version=4)
            except Exception as e:
                print(f">> [ERROR] Corrupted notebook, creating new one: {e}")
                nb = new_notebook()
        else:
            print(f">> [NEW] Creating new notebook: {notebook_name}")
            nb = new_notebook()

        # 타임스탬프 헤더 추가
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_cell = new_markdown_cell(f"### Submission at {timestamp}")
        nb.cells.append(header_cell)

        # 코드 셀 추가
        code_cell = new_code_cell(code_content)
        nb.cells.append(code_cell)
        
        # 노트북 저장
        try:
            with open(notebook_name, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            print(f">> [SUCCESS] Saved notebook: {notebook_name}")
        except Exception as e:
            print(f">> [ERROR] Failed to save notebook: {e}")

if __name__ == "__main__":
    convert_py_to_ipynb()
