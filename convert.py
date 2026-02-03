import os
import sys
import glob
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from datetime import datetime

def convert_py_to_ipynb():
    # 현재 디렉토리 및 하위 디렉토리의 모든 .py 파일 검색 (원한다면 특정 폴더로 제한 가능)
    # 실제로는 Git diff를 통해 변경된 파일만 감지하는 것이 좋으나, 
    # 간단한 구현을 위해 여기서는 파일 존재 여부로 판단하거나 GitHub Action에서 변경된 파일 목록을 넘겨받는 방식을 씁니다.
    
    # GitHub Action에서 변경된 파일 목록을 인자로 받는다고 가정
    if len(sys.argv) < 2:
        print("No files to process.")
        return

    files = sys.argv[1:]

    for py_file in files:
        if not py_file.endswith(".py"):
            continue
            
        base_name = os.path.splitext(py_file)[0]
        notebook_name = f"{base_name}.ipynb"
        
        # .py 파일 내용 읽기
        with open(py_file, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # 노트북 로드 또는 생성
        if os.path.exists(notebook_name):
            with open(notebook_name, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
        else:
            nb = new_notebook()

        # 타임스탬프 헤더 추가 (언제 풀었는지 기록)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_cell = new_markdown_cell(f"### Submission at {timestamp}")
        nb.cells.append(header_cell)

        # 코드 셀 추가
        code_cell = new_code_cell(code_content)
        nb.cells.append(code_cell)
        
        # 노트북 저장
        with open(notebook_name, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
            
        print(f"Updated: {notebook_name}")
        
        # (선택사항) 원본 .py 파일 삭제 (중복 방지)
        # os.remove(py_file) 
        # print(f"Removed: {py_file}")

if __name__ == "__main__":
    convert_py_to_ipynb()
