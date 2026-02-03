import os
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from datetime import datetime

def sync_all_problems():
    # 현재 디렉토리부터 모든 하위 폴더 검색
    print(">> Starting Smart Sync...")
    for root, dirs, files in os.walk("."):
        # .git 폴더나 숨김 폴더는 건너뛰기
        if ".git" in root:
            continue
            
        for file in files:
            # convert.py 자기 자신은 제외하고 .py 파일만 찾음
            if file.endswith(".py") and file != "convert.py":
                py_path = os.path.join(root, file)
                ipynb_path = os.path.splitext(py_path)[0] + ".ipynb"
                
                process_problem(py_path, ipynb_path)

def process_problem(py_path, ipynb_path):
    # 1. 파이썬 소스 코드 읽기
    try:
        with open(py_path, 'r', encoding='utf-8') as f:
            py_content = f.read().strip()
    except Exception as e:
        print(f"Error reading {py_path}: {e}")
        return

    # 2. 노트북 파일 로드 (없으면 생성)
    if os.path.exists(ipynb_path):
        try:
            with open(ipynb_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
        except Exception:
            nb = new_notebook()
    else:
        nb = new_notebook()
        
    # 3. [핵심] 중복 방지 로직
    # 노트북의 가장 마지막 코드 셀 내용을 확인해서, 
    # 지금 넣으려는 파이썬 코드와 똑같으면 저장하지 않고 넘어갑니다.
    if nb.cells:
        last_code_cells = [c for c in nb.cells if c.cell_type == 'code']
        if last_code_cells:
            last_code = last_code_cells[-1].source.strip()
            if last_code == py_content:
                # 이미 최신 코드가 저장되어 있음 -> 건너뜀
                # print(f"Skipping {py_path} (Already up to date)")
                return

    # 4. 새로운 내용이면 추가 (Append)
    print(f">> Updating: {ipynb_path}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nb.cells.append(new_markdown_cell(f"### Submission at {timestamp}"))
    nb.cells.append(new_code_cell(py_content))
    
    # 5. 저장
    with open(ipynb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

if __name__ == "__main__":
    sync_all_problems()
