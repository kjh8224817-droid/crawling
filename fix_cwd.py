import sys, json, pathlib
sys.stdout.reconfigure(encoding='utf-8')

nb_path = r'c:/Users/hyup/Desktop/크롤링/notebooks/03_실전_다양한사이트크롤링.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# New first code cell: set CWD to project root
cwd_cell = {
    "cell_type": "code",
    "execution_count": None,
    "id": "div-00-setup",
    "metadata": {},
    "outputs": [],
    "source": (
        "import os, pathlib\n"
        "\n"
        "# 노트북 위치 기준으로 프로젝트 루트(크롤링/)를 CWD로 설정\n"
        "# → 어디서 Jupyter를 실행해도 data/ 경로가 항상 맞게 됨\n"
        "project_root = pathlib.Path(__file__).parent if '__file__' in dir() else pathlib.Path.cwd()\n"
        "# VS Code / Jupyter 모두 대응\n"
        "if project_root.name == 'notebooks':\n"
        "    project_root = project_root.parent\n"
        "os.chdir(project_root)\n"
        "print(f'작업 디렉토리: {os.getcwd()}')\n"
        "print(f'data 폴더 확인: {list(pathlib.Path(\"data\").glob(\"*.html\"))}')\n"
    )
}

# Insert as the very first code cell (after the two markdown cells)
# Find index of div-03 (first code cell)
insert_idx = next(i for i, c in enumerate(nb['cells']) if c.get('id') == 'div-03')
nb['cells'].insert(insert_idx, cwd_cell)

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Done. Total cells:', len(nb['cells']))
