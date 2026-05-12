"""
수업용 크롤링 자료 생성 스크립트
실행: python3 create_materials.py
"""

import json
import os

BASE_DIR = '/Users/haku/크롤링'
NOTEBOOKS_DIR = os.path.join(BASE_DIR, 'notebooks')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

os.makedirs(NOTEBOOKS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)


# ─────────────────────────────────────────────
# 헬퍼 함수
# ─────────────────────────────────────────────

def md(source, cell_id):
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source}

def code(source, cell_id):
    return {"cell_type": "code", "execution_count": None, "id": cell_id,
            "metadata": {}, "outputs": [], "source": source}

def notebook(cells):
    return {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py", "mimetype": "text/x-python",
                "name": "python", "pygments_lexer": "ipython3", "version": "3.12.0"
            }
        },
        "cells": cells
    }

def save_nb(nb, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"  ✅ {path}")

def save_md(text, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"  ✅ {path}")


# ═══════════════════════════════════════════════════════════════
# NOTEBOOK 01 — 환경설정과 첫 크롤링
# ═══════════════════════════════════════════════════════════════

nb01_cells = [

md("""# 🌐 01. 환경설정과 첫 크롤링
## — VS Code + Python으로 시작하기

> **이 노트북에서 배울 것**
> 1. 왜 VS Code를 쓰는가 (Colab 대신)
> 2. 필요한 패키지 설치
> 3. `requests`로 웹페이지 가져오기
> 4. HTTP 상태 코드 이해
> 5. User-Agent 헤더 다루기
> 6. robots.txt 확인하는 습관
""", "nb01-01"),

md("""## 1. 왜 VS Code인가? (Colab과의 차이)

```
구글 Colab의 문제점:
┌─────────────────────────────────────────┐
│  클라우드 서버 IP  ──→  사이트가 차단!  │
│  올리브영, 무신사 등 대부분의 쇼핑몰    │
│  → 403 Forbidden (접근 거부)            │
└─────────────────────────────────────────┘

VS Code (내 컴퓨터)의 장점:
┌─────────────────────────────────────────┐
│  내 집 IP  ──→  일반 사용자처럼 접속!  │
│  → 차단될 확률 훨씬 낮음               │
└─────────────────────────────────────────┘
```

> 💡 **핵심**: 크롤링은 항상 자신의 컴퓨터에서 실행하세요.
""", "nb01-02"),

md("""## 2. 패키지 설치

VS Code의 터미널(`Ctrl + 백틱`)을 열고 아래 명령어를 실행하세요.

```bash
pip install requests beautifulsoup4 pandas
```

설치 후 아래 셀을 실행해서 확인합니다.
""", "nb01-03"),

code("""# 패키지 설치 확인
# ─ 에러 없이 실행되면 설치 성공!

import requests
import bs4          # beautifulsoup4
import pandas as pd

print(f"requests 버전: {requests.__version__}")
print(f"BeautifulSoup 버전: {bs4.__version__}")
print(f"pandas 버전: {pd.__version__}")
print("\\n✅ 모든 패키지 설치 완료!")
""", "nb01-04"),

md("""## 3. HTTP가 뭔가요?

웹 크롤링의 원리를 이해하려면 HTTP를 알아야 해요.

```
[내 컴퓨터]  ─── 요청(Request) ──→  [웹 서버]
             ←── 응답(Response) ───

요청: "이 URL의 페이지를 보여줘!"
응답: "여기 HTML 파일이야!"
```

`requests` 라이브러리는 이 과정을 파이썬 코드로 자동으로 해줍니다.
""", "nb01-05"),

code("""# 첫 번째 크롤링!
# ─ 연습용 사이트 books.toscrape.com

import requests

url = 'http://books.toscrape.com/'
response = requests.get(url)

print(f"상태 코드: {response.status_code}")
print(f"응답 크기: {len(response.text):,} 글자")
print(f"\\n--- HTML 앞부분 미리보기 ---")
print(response.text[:300])
""", "nb01-06"),

md("""## 4. 상태 코드 — 숫자로 읽는 서버의 대답

| 코드 | 의미 | 우리가 해야 할 것 |
|------|------|-----------------|
| **200** | 성공! ✅ | 바로 진행 |
| **403** | 접근 거부 ❌ | User-Agent 헤더 추가 |
| **404** | 페이지 없음 | URL 재확인 |
| **429** | 요청 너무 많음 | `time.sleep()` 추가 |
| **500** | 서버 에러 | 잠시 후 재시도 |

> 💡 크롤링에서 가장 많이 만나는 것: **200** (성공)과 **403** (차단)
""", "nb01-07"),

code("""# 상태 코드 확인 패턴
import requests

def check_status(url):
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        print(f"✅ 성공! ({url})")
    elif response.status_code == 403:
        print(f"❌ 차단됨! User-Agent를 추가해보세요. ({url})")
    elif response.status_code == 404:
        print(f"⚠️  페이지 없음! URL을 확인하세요. ({url})")
    else:
        print(f"상태 코드: {response.status_code} ({url})")

    return response.status_code

check_status('http://books.toscrape.com/')
check_status('http://books.toscrape.com/없는페이지')
""", "nb01-08"),

md("""## 5. User-Agent — 내가 누구인지 서버에 알려주기

서버는 요청을 보낸 게 **사람인지 봇인지** 확인해요.
아무 헤더 없이 보내면 파이썬 봇으로 인식해서 차단할 수 있어요.

```
헤더 없을 때:   User-Agent: python-requests/2.31.0  ← 봇처럼 보임
헤더 추가 후:   User-Agent: Mozilla/5.0 ... Chrome/120  ← 크롬 브라우저처럼 보임
```

> 📋 User-Agent 복사하는 법:
> 1. 크롬 브라우저 열기
> 2. F12 → Console 탭
> 3. `navigator.userAgent` 입력 후 Enter
> 4. 나온 문자열을 복사!
""", "nb01-09"),

code("""# User-Agent 헤더 추가
import requests

# ❌ 헤더 없이 요청 — 일부 사이트에서 차단될 수 있음
response_no_header = requests.get('http://books.toscrape.com/')
print(f"헤더 없음: {response_no_header.status_code}")

# ✅ User-Agent 추가 — 일반 크롬 브라우저처럼 보임
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
response_with_header = requests.get('http://books.toscrape.com/', headers=headers)
print(f"헤더 있음: {response_with_header.status_code}")

# 앞으로 항상 이 headers를 기본으로 사용합니다!
""", "nb01-10"),

md("""## 6. 인코딩 — 한글 깨짐 방지

한국 사이트에서 한글이 깨지는 경우가 있어요.
원인: 서버가 `EUC-KR`로 보냈는데 파이썬이 다른 방식으로 읽는 것.

```python
response.encoding = 'utf-8'     # 대부분의 현대 사이트
response.encoding = 'euc-kr'    # 오래된 한국 사이트
```
""", "nb01-11"),

code("""# 인코딩 처리 비교
import requests

url = 'https://www.saramin.co.kr/zf_user/search/recruit?searchword=파이썬'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

response = requests.get(url, headers=headers, timeout=15)

# 자동 감지된 인코딩 확인
print(f"자동 인코딩: {response.encoding}")

# 명시적으로 utf-8 설정 (한글 깨짐 방지)
response.encoding = 'utf-8'

# 한글이 포함된 텍스트 일부 확인
import re
korean_texts = re.findall('[가-힣]+', response.text[:2000])
print(f"\\n발견된 한글: {korean_texts[:10]}")
""", "nb01-12"),

md("""## 7. robots.txt — 크롤링 전 필수 확인!

모든 사이트에는 `robots.txt` 파일이 있어요.
이것은 "어디까지 크롤링을 허용하는가"를 명시한 규칙서입니다.

```
https://사이트주소.com/robots.txt
```

```
User-agent: *          ← 모든 봇에 적용
Disallow: /private/    ← 이 경로는 수집 금지!
Disallow: /mypage/     ← 이 경로도 금지!
Allow: /products/      ← 이 경로는 허용 ✅
```

> ⚠️ **Disallow된 경로를 크롤링하면 법적 문제가 될 수 있어요!**
""", "nb01-13"),

code("""# robots.txt 확인 함수
import requests

def check_robots(site_url):
    \"\"\"사이트의 robots.txt를 확인하고 출력합니다\"\"\"
    robots_url = site_url.rstrip('/') + '/robots.txt'

    try:
        response = requests.get(robots_url, timeout=10,
                               headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            print(f"=== {site_url} robots.txt ===")
            print(response.text[:800])
        else:
            print(f"robots.txt 없음 (상태 코드: {response.status_code})")
    except Exception as e:
        print(f"오류: {e}")

# 연습용 사이트 확인
check_robots('http://books.toscrape.com')
""", "nb01-14"),

code("""# 사람인 robots.txt 확인
check_robots('https://www.saramin.co.kr')
""", "nb01-15"),

md("""## ✅ 오늘 배운 것 정리

```python
# 크롤링 기본 템플릿 — 앞으로 항상 이 구조 사용!

import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1단계: robots.txt 확인 (습관!)
# 2단계: 페이지 가져오기
response = requests.get('URL', headers=headers, timeout=15)
response.encoding = 'utf-8'  # 한글 깨짐 방지

# 3단계: 상태 코드 확인
if response.status_code == 200:
    print("성공!")
    # 4단계: BeautifulSoup으로 파싱 (다음 노트북에서!)
```

> **다음 노트북**: BeautifulSoup으로 원하는 데이터만 골라내기!
""", "nb01-16"),
]

save_nb(notebook(nb01_cells), os.path.join(NOTEBOOKS_DIR, '01_환경설정과_첫크롤링.ipynb'))


# ═══════════════════════════════════════════════════════════════
# NOTEBOOK 02 — BeautifulSoup 완전정복
# ═══════════════════════════════════════════════════════════════

nb02_cells = [

md("""# 🍜 02. BeautifulSoup 완전정복
## — HTML에서 원하는 데이터만 골라내기

> **이 노트북에서 배울 것**
> 1. HTML 구조 복습
> 2. BeautifulSoup 기본 4가지 함수
> 3. 텍스트 & 속성값 추출
> 4. None 안전 처리 패턴
> 5. 개발자도구로 선택자 찾는 법
> 6. 실전: books.toscrape.com 완전 공략
""", "nb02-01"),

md("""## 1. HTML 구조 복습

웹페이지는 HTML 태그들이 겹겹이 쌓인 구조예요.

```html
<html>
  <body>
    <div class="product-list">          ← 컨테이너 (상자)
      <div class="product-item">        ← 상품 카드 1
        <span class="name">립밤</span>  ← 이름
        <span class="price">12,000원</span>  ← 가격
      </div>
      <div class="product-item">        ← 상품 카드 2
        <span class="name">선크림</span>
        <span class="price">25,000원</span>
      </div>
    </div>
  </body>
</html>
```

**핵심 개념:**
- `태그`: `<div>`, `<span>`, `<p>`, `<a>` 등
- `class`: 태그에 붙은 이름표 (CSS 선택자에 `.` 사용)
- `id`: 유일한 이름표 (CSS 선택자에 `#` 사용)
- `href`, `src`: 태그의 속성값
""", "nb02-02"),

code("""# HTML 문자열로 BeautifulSoup 연습
from bs4 import BeautifulSoup

# 가짜 HTML (연습용)
html = \"\"\"
<html>
<body>
  <div class="product-list">
    <div class="product-item">
      <span class="name">립밤 촉촉이</span>
      <span class="price">12,000원</span>
      <a href="/products/001" class="detail-link">상세보기</a>
    </div>
    <div class="product-item">
      <span class="name">수분 선크림</span>
      <span class="price">25,000원</span>
      <a href="/products/002" class="detail-link">상세보기</a>
    </div>
    <div class="product-item">
      <span class="name">촉촉 에센스</span>
      <span class="price">38,000원</span>
      <a href="/products/003" class="detail-link">상세보기</a>
    </div>
  </div>
</body>
</html>
\"\"\"

soup = BeautifulSoup(html, 'html.parser')
print("파싱 완료!")
print(type(soup))  # BeautifulSoup 객체
""", "nb02-03"),

md("""## 2. 핵심 함수 ① — `find()` : 첫 번째 하나만 찾기

```python
soup.find('태그이름')
soup.find('태그이름', class_='클래스명')
soup.find('태그이름', id='아이디')
```

> ⚠️ `class`는 파이썬 예약어라서 `class_`로 씁니다!
""", "nb02-04"),

code("""# find() 실습 — 첫 번째 요소만 가져옴

# 태그이름으로 찾기
first_div = soup.find('div')
print("첫 번째 div:")
print(first_div)
print()

# 태그 + 클래스로 찾기
first_item = soup.find('div', class_='product-item')
print("첫 번째 product-item:")
print(first_item)
""", "nb02-05"),

md("""## 3. 핵심 함수 ② — `find_all()` : 조건에 맞는 전부 찾기

```python
soup.find_all('태그이름')          # 해당 태그 모두
soup.find_all('태그이름', class_='클래스명')  # 조건 맞는 모두
```

결과: **리스트** (0개 이상의 요소들)
""", "nb02-06"),

code("""# find_all() 실습 — 전부 가져옴

# 모든 product-item 찾기
all_items = soup.find_all('div', class_='product-item')
print(f"총 {len(all_items)}개의 상품 발견")
print()

# 반복문으로 각 상품 처리
for i, item in enumerate(all_items, 1):
    name = item.find('span', class_='name')
    price = item.find('span', class_='price')
    print(f"{i}번 상품: {name.text} — {price.text}")
""", "nb02-07"),

md("""## 4. 핵심 함수 ③ — `select()` : CSS 선택자로 찾기 ⭐

가장 많이 쓰는 방법! 개발자도구의 선택자를 그대로 사용할 수 있어요.

```python
soup.select('div')              # 태그만
soup.select('.product-item')    # 클래스만 (앞에 .)
soup.select('#header')          # ID (앞에 #)
soup.select('div.product-item') # 태그 + 클래스
soup.select('div > span')       # div 바로 아래 span
soup.select('div span')         # div 안의 모든 span
soup.select('a[href]')          # href 속성이 있는 a
soup.select('a[href*="product"]') # href에 "product"가 들어간 a
```

결과: **리스트** (find_all과 같음)
""", "nb02-08"),

code("""# select() 실습

# 클래스로 찾기
items = soup.select('.product-item')
print(f"select('.product-item'): {len(items)}개 발견")

# 태그 + 클래스
names = soup.select('span.name')
print(f"\\nselect('span.name'): {len(names)}개 발견")
for name in names:
    print(f"  - {name.text}")

# 속성 조건
links = soup.select('a[href*="products"]')
print(f"\\nselect('a[href*=products]'): {len(links)}개 발견")
for link in links:
    print(f"  - {link['href']}")
""", "nb02-09"),

md("""## 5. 핵심 함수 ④ — `select_one()` : CSS 선택자로 하나만

`select()`의 결과 중 첫 번째 하나만 가져와요.
`find()`와 같은 역할이지만 CSS 선택자를 쓸 수 있어요.

```python
soup.select_one('.product-item')  # 첫 번째 하나
item.select_one('.name')          # item 안에서 찾기
```
""", "nb02-10"),

code("""# select_one() 실습

# 전체 soup에서 하나
first_item = soup.select_one('.product-item')
print("첫 번째 상품:")
print(first_item)

# 하나를 찾은 뒤 그 안에서 다시 찾기
name = first_item.select_one('.name')
price = first_item.select_one('.price')
print(f"\\n이름: {name.text}")
print(f"가격: {price.text}")
""", "nb02-11"),

md("""## 6. 텍스트 추출 — `.text` vs `.get_text()`

| 방법 | 특징 |
|------|------|
| `.text` | 태그 안 모든 텍스트 (자식 태그 포함) |
| `.get_text()` | `.text`와 동일, 옵션 지정 가능 |
| `.get_text(strip=True)` | 앞뒤 공백 자동 제거 |
| `.text.strip()` | 앞뒤 공백 수동 제거 |

```python
# 두 방법 모두 자주 쓰임
element.text.strip()
element.get_text(strip=True)
```
""", "nb02-12"),

code("""# 텍스트 추출 실습

item = soup.select_one('.product-item')

# 태그 전체 텍스트 (공백 포함)
print("=== .text (원본) ===")
print(repr(item.text))

print("\\n=== .text.strip() ===")
print(item.text.strip())

print("\\n=== .get_text(strip=True) ===")
print(item.get_text(strip=True))

# 개별 요소 텍스트
name_el = item.select_one('.name')
print(f"\\n이름 텍스트: '{name_el.text}'")
print(f"이름 strip: '{name_el.text.strip()}'")
""", "nb02-13"),

md("""## 7. 속성값 추출 — `['속성명']` vs `.get('속성명')`

링크(`href`), 이미지(`src`), 데이터 속성(`data-id`) 등을 가져올 때 사용해요.

```python
element['href']          # 없으면 KeyError 발생
element.get('href')      # 없으면 None 반환 (안전)
element.get('href', '')  # 없으면 '' 반환 (기본값 지정)
```
""", "nb02-14"),

code("""# 속성값 추출 실습

# a 태그의 href 속성 가져오기
link = soup.select_one('a.detail-link')
print(f"태그 전체: {link}")

# 방법 1: 딕셔너리처럼 접근
href1 = link['href']
print(f"\\n['href']: {href1}")

# 방법 2: .get() — 더 안전
href2 = link.get('href')
print(f".get('href'): {href2}")

# 모든 링크의 href 가져오기
all_links = soup.select('a[href]')
print("\\n--- 모든 링크 ---")
for a in all_links:
    print(f"  텍스트: {a.text.strip()!r:15}  href: {a.get('href')}")
""", "nb02-15"),

md("""## 8. ⚠️ 가장 중요한 패턴 — None 안전 처리

크롤링에서 가장 많이 나는 에러:
```
AttributeError: 'NoneType' object has no attribute 'text'
```

원인: 요소를 찾지 못하면 `None`이 반환되는데, `None.text`를 호출할 수 없어요.

**해결법 3가지:**
```python
# 방법 1: if else (가장 많이 씀)
name = el.text.strip() if el else None

# 방법 2: try-except
try:
    name = el.text.strip()
except:
    name = None

# 방법 3: and 연산자
name = el and el.text.strip()
```
""", "nb02-16"),

code("""# None 안전 처리 실습

# 존재하지 않는 클래스 선택
missing_el = soup.select_one('.존재하지않는클래스')
print(f"못 찾으면: {missing_el}")  # None

# ❌ 잘못된 방법 — 에러 발생!
try:
    name = missing_el.text  # AttributeError!
except AttributeError as e:
    print(f"\\n에러 발생: {e}")

# ✅ 올바른 방법 — 항상 이렇게!
name = missing_el.text.strip() if missing_el else None
print(f"\\n안전한 방법 결과: {name}")

# 실제 사용 예
for item in soup.select('.product-item'):
    name = item.select_one('.name')
    price = item.select_one('.price')
    rating = item.select_one('.rating')  # 이 클래스는 없음!

    print({
        '이름': name.text.strip() if name else None,
        '가격': price.text.strip() if price else None,
        '평점': rating.text.strip() if rating else '정보없음',  # 기본값 지정
    })
""", "nb02-17"),

md("""## 9. 개발자도구로 선택자 찾는 법

실제 사이트에서 어떤 선택자를 써야 하는지 찾는 방법이에요.

### 방법 1: Copy Selector (가장 빠름)
```
1. 크롬에서 원하는 요소 위에 마우스 올리기
2. 우클릭 → "검사" (Inspect)
3. 파란색으로 강조된 태그에서 우클릭
4. Copy → Copy selector
```

### 방법 2: 직접 읽기 (이해하기 좋음)
```html
<ul class="book-list">          → soup.select('ul.book-list')
  <li class="book-item">        → soup.select('li.book-item')
    <a href="/book/1">          → soup.select('li.book-item a')
      <h3>책 제목</h3>          → soup.select('li.book-item h3')
    </a>
  </li>
</ul>
```

### 방법 3: Elements 탭 검색 (Ctrl+F)
```
F12 → Elements 탭 → Ctrl+F → 클래스명 검색
```
""", "nb02-18"),

md("""## 10. 실전 실습 — books.toscrape.com 완전 공략

이제 배운 것을 실제 사이트에 적용해봅시다!

**books.toscrape.com HTML 구조:**
```html
<article class="product_pod">
  <p class="star-rating Three">   ← 평점 (class에 숫자 단어)
  <h3>
    <a href="..." title="책 제목">  ← 제목은 title 속성에!
  </h3>
  <p class="price_color">£51.77</p>  ← 가격
</article>
```
""", "nb02-19"),

code("""# 실전: books.toscrape.com 1페이지 수집
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://books.toscrape.com/'
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
print(f"상태 코드: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')
""", "nb02-20"),

code("""# 페이지 구조 탐색
# (개발자도구 없이도 파악할 수 있어요)

# 1. 책 컨테이너 확인
books = soup.select('article.product_pod')
print(f"총 {len(books)}권 발견")
print()

# 2. 첫 번째 책의 HTML 구조 확인
first_book = books[0]
print("=== 첫 번째 책 HTML ===")
print(first_book.prettify()[:600])
""", "nb02-21"),

code("""# 데이터 추출

rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
rows = []

for book in books:
    # 제목: h3 > a 태그의 title 속성
    title_el = book.select_one('h3 a')
    title = title_el['title'] if title_el else None
    # ↑ title은 태그 안 텍스트가 아니라 속성에 있어요!

    # 가격: p.price_color의 텍스트
    price_el = book.select_one('p.price_color')
    price = price_el.text.strip() if price_el else None

    # 평점: p.star-rating의 두 번째 class가 숫자 단어
    # class 예: ['star-rating', 'Three']
    rating_el = book.select_one('p.star-rating')
    if rating_el:
        rating_word = rating_el['class'][1]  # 'Three'
        rating = rating_map.get(rating_word, 0)
    else:
        rating = None

    # 링크
    link_el = book.select_one('h3 a')
    link = 'http://books.toscrape.com/catalogue/' + link_el['href'] if link_el else None

    rows.append({
        '제목': title,
        '가격': price,
        '평점': rating,
        '링크': link,
    })

df = pd.DataFrame(rows)
print(df[['제목', '가격', '평점']].to_string(index=False))
""", "nb02-22"),

code("""# 여러 페이지 수집 (3페이지)
import time

all_books = []

for page in range(1, 4):
    url = f'http://books.toscrape.com/catalogue/page-{page}.html'
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.select('article.product_pod')

    for book in books:
        title_el = book.select_one('h3 a')
        price_el = book.select_one('p.price_color')
        rating_el = book.select_one('p.star-rating')

        all_books.append({
            '제목': title_el['title'] if title_el else None,
            '가격': price_el.text.strip() if price_el else None,
            '평점': rating_map.get(
                rating_el['class'][1] if rating_el else '', 0
            ),
            '페이지': page,
        })

    print(f"  {page}페이지 완료 ({len(books)}권)")
    time.sleep(1)  # ← 항상 1초 쉬기!

df_all = pd.DataFrame(all_books)
print(f"\\n총 {len(df_all)}권 수집!")
df_all.head(5)
""", "nb02-23"),

code("""# 연습문제 1: 5점짜리 책만 필터링

five_star = df_all[df_all['평점'] == 5]
print(f"5점 책 총 {len(five_star)}권:")
print(five_star[['제목', '가격']].to_string(index=False))
""", "nb02-24"),

code("""# 연습문제 2: 평점별 평균 가격 (문자열 → 숫자 변환 필요)

df_all['가격_숫자'] = (df_all['가격']
    .str.replace('£', '')
    .str.strip()
    .pipe(pd.to_numeric, errors='coerce')
)

print("=== 평점별 평균 가격 ===")
result = df_all.groupby('평점')['가격_숫자'].agg(['mean', 'count'])
result.columns = ['평균가격(£)', '책수']
result['평균가격(£)'] = result['평균가격(£)'].round(2)
print(result.to_string())
""", "nb02-25"),

md("""## ✅ 오늘 배운 것 정리

| 함수 | 언제 쓰나 | 반환 |
|------|----------|------|
| `find('태그')` | 첫 번째 하나 | 요소 or None |
| `find_all('태그')` | 전부 | 리스트 |
| `select('선택자')` | CSS로 전부 | 리스트 |
| `select_one('선택자')` | CSS로 하나 | 요소 or None |
| `el.text.strip()` | 텍스트 추출 | 문자열 |
| `el['속성']` | 속성값 | 문자열 |
| `el.get('속성')` | 속성값 (안전) | 문자열 or None |

**핵심 패턴:**
```python
element = soup.select_one('선택자')
value = element.text.strip() if element else None  # 항상!
```

> **다음 노트북**: 사람인 채용공고 실전 크롤링!
""", "nb02-26"),
]

save_nb(notebook(nb02_cells), os.path.join(NOTEBOOKS_DIR, '02_BeautifulSoup_완전정복.ipynb'))


# ═══════════════════════════════════════════════════════════════
# NOTEBOOK 03 — 실전 정적 사이트 크롤링
# ═══════════════════════════════════════════════════════════════

nb03_cells = [

md("""# 💼 03. 실전 — 정적 사이트 크롤링
## — 사람인 채용공고 완전 공략

> **이 노트북에서 배울 것**
> 1. robots.txt 확인 자동화
> 2. 사람인 채용공고 수집 (1페이지 → 여러 페이지)
> 3. 여러 키워드 한번에 수집
> 4. 데이터 정제 (문자열 → 숫자)
> 5. CSV 저장 & 간단한 분석

> ⚠️ **VS Code 로컬 환경 필수!** Colab에서는 IP 차단으로 안 됩니다.
""", "nb03-01"),

md("""## 1. 사람인 robots.txt 확인

크롤링 전 항상 첫 번째로 하는 것!
""", "nb03-02"),

code("""import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 표준 헤더 — 매번 이걸 복사해서 시작
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# robots.txt 확인
r = requests.get('https://www.saramin.co.kr/robots.txt',
                 headers=HEADERS, timeout=10)
print(r.text[:600])
""", "nb03-03"),

md("""## 2. 사람인 페이지 구조 파악

**개발자도구로 확인한 HTML 구조:**
```html
<div class="item_recruit">          ← 채용공고 하나
  <strong class="corp_name">
    <a>회사명</a>
  </strong>
  <h2 class="job_tit">
    <a>공고 제목</a>
  </h2>
  <div class="job_condition">
    <span>지역</span>
    <span>경력</span>
    <span>학력</span>
    <span>고용형태</span>
  </div>
  <div class="job_date">
    <span class="date">마감일</span>
  </div>
</div>
```
""", "nb03-04"),

code("""# 사람인 1페이지 수집

keyword = '데이터분석'
url = f'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}'

response = requests.get(url, headers=HEADERS, timeout=15)
response.encoding = 'utf-8'
print(f"상태 코드: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')

# 채용공고 카드 찾기
jobs = soup.select('div.item_recruit')
print(f"발견된 공고: {len(jobs)}건")
""", "nb03-05"),

code("""# 첫 번째 공고 구조 확인
if jobs:
    first_job = jobs[0]
    print("=== 첫 번째 공고 HTML ===")
    print(first_job.prettify()[:800])
""", "nb03-06"),

code("""# 전체 데이터 추출

rows = []

for job in jobs:
    # 회사명
    company_el = job.select_one('strong.corp_name a')
    company = company_el.text.strip() if company_el else None

    # 공고 제목
    title_el = job.select_one('h2.job_tit a')
    title = title_el.text.strip() if title_el else None

    # 조건들 (지역, 경력, 학력, 고용형태)
    conditions = job.select('div.job_condition span')
    cond_texts = [c.text.strip() for c in conditions]

    # 마감일
    deadline_el = job.select_one('div.job_date span.date')
    deadline = deadline_el.text.strip() if deadline_el else None

    rows.append({
        '회사명': company,
        '공고제목': title,
        '지역': cond_texts[0] if len(cond_texts) > 0 else None,
        '경력': cond_texts[1] if len(cond_texts) > 1 else None,
        '학력': cond_texts[2] if len(cond_texts) > 2 else None,
        '고용형태': cond_texts[3] if len(cond_texts) > 3 else None,
        '마감일': deadline,
    })

df = pd.DataFrame(rows)
print(f"수집 완료: {len(df)}건")
df[['회사명', '공고제목', '지역', '경력']].head(10)
""", "nb03-07"),

md("""## 3. 여러 페이지 수집 (페이지네이션)

사람인 URL 패턴:
```
1페이지: ?searchword=키워드&recruitPage=1
2페이지: ?searchword=키워드&recruitPage=2
3페이지: ?searchword=키워드&recruitPage=3
```

→ URL의 숫자만 바꾸면 됩니다!
""", "nb03-08"),

code("""# 여러 페이지 수집

def crawl_saramin(keyword, max_page=3):
    \"\"\"사람인에서 키워드 검색 결과를 max_page 페이지까지 수집\"\"\"
    all_jobs = []

    for page in range(1, max_page + 1):
        url = (f'https://www.saramin.co.kr/zf_user/search/recruit'
               f'?searchType=search&searchword={keyword}&recruitPage={page}')

        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"  {page}페이지 오류: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.select('div.item_recruit')

        for job in jobs:
            company_el = job.select_one('strong.corp_name a')
            title_el = job.select_one('h2.job_tit a')
            conditions = job.select('div.job_condition span')
            cond_texts = [c.text.strip() for c in conditions]
            deadline_el = job.select_one('div.job_date span.date')

            all_jobs.append({
                '키워드': keyword,
                '페이지': page,
                '회사명': company_el.text.strip() if company_el else None,
                '공고제목': title_el.text.strip() if title_el else None,
                '지역': cond_texts[0] if len(cond_texts) > 0 else None,
                '경력': cond_texts[1] if len(cond_texts) > 1 else None,
                '학력': cond_texts[2] if len(cond_texts) > 2 else None,
                '마감일': deadline_el.text.strip() if deadline_el else None,
            })

        print(f"  {page}페이지 완료: {len(jobs)}건")
        time.sleep(1)  # 서버 부담 줄이기!

    return pd.DataFrame(all_jobs)


# 실행
print("=== 데이터분석 채용공고 수집 ===")
df_data = crawl_saramin('데이터분석', max_page=3)
print(f"\\n총 {len(df_data)}건 수집 완료!")
""", "nb03-09"),

code("""# 여러 키워드 한번에 수집

keywords = ['데이터분석', '파이썬', 'SQL']
frames = []

for kw in keywords:
    print(f"\\n[{kw}] 수집 중...")
    df_kw = crawl_saramin(kw, max_page=2)
    frames.append(df_kw)
    time.sleep(2)  # 키워드 사이 2초 대기

df_all = pd.concat(frames, ignore_index=True)
print(f"\\n전체 수집: {len(df_all)}건")
print(df_all.groupby('키워드').size().rename('공고수'))
""", "nb03-10"),

md("""## 4. 데이터 분석 & 정제

수집한 데이터를 바로 분석해봅시다!
""", "nb03-11"),

code("""# 지역별 공고 수
print("=== 지역별 공고 수 (상위 10) ===")
print(df_all['지역'].value_counts().head(10).to_string())

print("\\n=== 경력 조건별 공고 수 ===")
print(df_all['경력'].value_counts().head(10).to_string())
""", "nb03-12"),

code("""# 서울 강남구 공고만 필터링
gangnam = df_all[df_all['지역'].str.contains('강남', na=False)]
print(f"강남 지역 공고: {len(gangnam)}건")
print(gangnam[['키워드', '회사명', '공고제목', '경력']].head(10).to_string(index=False))
""", "nb03-13"),

code("""# 경력무관 or 신입 공고만 필터링
entry = df_all[
    df_all['경력'].isin(['경력무관', '신입', '신입·경력'])
]
print(f"신입/경력무관 공고: {len(entry)}건")
print(entry[['키워드', '회사명', '공고제목', '지역']].head(10).to_string(index=False))
""", "nb03-14"),

code("""# CSV 저장

save_path = r'사람인_채용공고.csv'
# 윈도우에서는 r 문자열 또는 / 사용 권장

df_all.to_csv(save_path, index=False, encoding='utf-8-sig')
# utf-8-sig: 엑셀에서 열었을 때 한글 안 깨지게!

print(f"저장 완료: {save_path}")
print(f"파일 크기: {len(df_all)}행 × {len(df_all.columns)}열")
print(f"컬럼: {list(df_all.columns)}")
""", "nb03-15"),

md("""## 5. 취업 포트폴리오 아이디어

이 데이터로 만들 수 있는 분석:

```
📊 Tableau / Power BI 시각화:
├── 지역 히트맵: 어느 지역에 공고가 많나?
├── 키워드별 경력 요구사항 비교
├── 마감일 타임라인
└── 회사별 채용 규모

🐍 Python 추가 분석:
├── 공고 제목에서 기술 스택 추출 (Python, SQL, R 등)
├── 경력 연차 분포
└── 월별 채용 트렌드
```
""", "nb03-16"),

code("""# 보너스: 공고 제목에서 기술 스택 추출

tech_keywords = ['Python', 'SQL', 'R', 'Tableau', 'Excel',
                 '머신러닝', '딥러닝', 'AI', 'AWS', 'Spark']

for tech in tech_keywords:
    count = df_all['공고제목'].str.contains(tech, case=False, na=False).sum()
    if count > 0:
        print(f"  {tech:15}: {count}건")
""", "nb03-17"),

md("""## ✅ 오늘 배운 것 정리

```python
# 완성된 크롤링 템플릿

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

# 1. robots.txt 확인
# 2. 페이지 가져오기
# 3. BeautifulSoup 파싱
# 4. 데이터 추출 (select + if else None)
# 5. time.sleep(1) — 항상!
# 6. CSV 저장 (encoding='utf-8-sig')
```

> **다음 노트북**: JavaScript 렌더링 사이트는 Selenium으로!
""", "nb03-18"),
]

save_nb(notebook(nb03_cells), os.path.join(NOTEBOOKS_DIR, '03_실전_정적사이트크롤링.ipynb'))


# ═══════════════════════════════════════════════════════════════
# NOTEBOOK 04 — Selenium 동적 사이트 크롤링
# ═══════════════════════════════════════════════════════════════

nb04_cells = [

md("""# 🤖 04. Selenium — 동적 사이트 크롤링
## — JavaScript 렌더링 사이트 완전 공략

> **이 노트북에서 배울 것**
> 1. 왜 Selenium이 필요한가
> 2. Windows에서 설치 & 세팅
> 3. 브라우저 제어 기본기
> 4. 요소 찾기 & 클릭 & 입력
> 5. 대기 전략 (Explicit Wait)
> 6. 실전: JS 렌더링 사이트 크롤링
> 7. 실전: 무한스크롤 크롤링
> 8. 실전: 사람인 버튼 클릭으로 페이지 이동
""", "nb04-01"),

md("""## 1. 왜 Selenium이 필요한가?

BeautifulSoup으로 안 되는 경우:

```
케이스 1: JavaScript 렌더링
─────────────────────────────────
requests로 가져온 HTML:          실제 브라우저에서 보이는 화면:
<div id="product-list">          <div id="product-list">
  <!-- 데이터 없음 -->              <div class="item">아이폰 15</div>
</div>                             <div class="item">갤럭시 S24</div>
                                 </div>

→ JS가 실행되면서 데이터를 채워넣음! requests는 JS 실행 못함.

케이스 2: 무한 스크롤
─────────────────────────────────
처음엔 20개 → 스크롤하면 20개 더 → 계속...
→ 스크롤 동작을 Selenium으로 제어해야 함!

케이스 3: 로그인 / 버튼 클릭 필요
─────────────────────────────────
→ Selenium으로 실제 버튼 클릭 가능!
```

**결론:**
- 화면에 보이는데 BeautifulSoup으로 못 가져온다 → **Selenium 사용!**
""", "nb04-02"),

md("""## 2. 설치 방법 (Windows + VS Code)

**터미널에서 실행:**
```bash
pip install selenium webdriver-manager
```

**Chrome 브라우저 확인:**
- 크롬이 설치되어 있어야 합니다
- 버전 확인: 크롬 우상단 메뉴(⋮) → 도움말 → Chrome 정보

**`webdriver-manager`를 쓰는 이유:**
```
기존 방식: ChromeDriver를 직접 다운로드해서 경로 설정 (번거로움)
webdriver-manager: 자동으로 맞는 버전 다운로드! 설정 필요 없음 ✅
```
""", "nb04-03"),

code("""# 설치 확인

import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'pip', 'show', 'selenium', 'webdriver-manager'],
                       capture_output=True, text=True)
for line in result.stdout.split('\\n'):
    if line.startswith('Name') or line.startswith('Version'):
        print(line)

print("\\n패키지 확인 완료!")
""", "nb04-04"),

code("""# Selenium import & 브라우저 열기

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

print("import 완료!")
print("아래 셀을 실행하면 Chrome이 자동으로 열립니다.")
""", "nb04-05"),

code("""# Chrome 브라우저 열기

# Chrome 옵션 설정
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 창 안 열기 (배포용)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1280,900')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0')

# 드라이버 자동 설치 및 실행
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

print("✅ Chrome이 열렸습니다!")
print(f"Chrome 버전: {driver.capabilities['browserVersion']}")
""", "nb04-06"),

md("""## 3. 기본 브라우저 제어

```python
# URL 이동
driver.get('https://www.google.com')

# 현재 URL 확인
driver.current_url

# 페이지 제목 확인
driver.title

# 뒤로 가기 / 앞으로 가기
driver.back()
driver.forward()

# 새로고침
driver.refresh()

# 종료 (항상 마지막에!)
driver.quit()
```
""", "nb04-07"),

code("""# 기본 내비게이션

# 페이지 이동
driver.get('http://quotes.toscrape.com/')
time.sleep(2)

print(f"제목: {driver.title}")
print(f"URL: {driver.current_url}")

# 페이지 소스 (HTML) 가져오기
page_source = driver.page_source
print(f"\\n소스 크기: {len(page_source):,} 글자")
print("소스 미리보기:")
print(page_source[:300])
""", "nb04-08"),

md("""## 4. 요소 찾기 — `find_element` vs `find_elements`

| 함수 | 반환 | 없을 때 |
|------|------|---------|
| `find_element(By.X, '선택자')` | 요소 하나 | 에러 발생! |
| `find_elements(By.X, '선택자')` | 요소 리스트 | 빈 리스트 [] |

**By 종류:**
```python
By.CSS_SELECTOR   # CSS 선택자 (가장 많이 씀)
By.XPATH          # XPath
By.ID             # id 속성
By.CLASS_NAME     # class명 (공백 없는 단일 클래스만)
By.TAG_NAME       # 태그 이름
By.LINK_TEXT      # 링크 텍스트 전체 일치
By.PARTIAL_LINK_TEXT  # 링크 텍스트 부분 일치
```

> 💡 **By.CSS_SELECTOR 하나만 잘 써도 대부분 해결됩니다!**
""", "nb04-09"),

code("""# 요소 찾기 실습
# 현재 quotes.toscrape.com에 있어야 함!

# ─── find_element: 하나만 (첫 번째)
first_quote = driver.find_element(By.CSS_SELECTOR, '.quote')
print("첫 번째 명언 요소:")
print(first_quote.text[:100])

# ─── find_elements: 전부
all_quotes = driver.find_elements(By.CSS_SELECTOR, '.quote')
print(f"\\n총 명언 수: {len(all_quotes)}개")

# ─── 요소 안에서 다시 찾기 (중첩 선택)
for i, quote in enumerate(all_quotes[:3], 1):
    text = quote.find_element(By.CSS_SELECTOR, '.text').text
    author = quote.find_element(By.CSS_SELECTOR, '.author').text
    print(f"\\n{i}. {author}: {text[:50]}...")
""", "nb04-10"),

md("""## 5. 텍스트 가져오기 & 속성값 가져오기

```python
element.text                    # 화면에 보이는 텍스트
element.get_attribute('href')   # 속성값
element.get_attribute('class')  # class 속성
element.get_attribute('innerHTML')  # 내부 HTML
element.get_attribute('value')  # input 박스의 값
```
""", "nb04-11"),

code("""# 텍스트와 속성값 가져오기

first_quote = driver.find_element(By.CSS_SELECTOR, '.quote')

# 텍스트
text_el = first_quote.find_element(By.CSS_SELECTOR, '.text')
print(f".text:            {text_el.text[:60]}")

# a 태그의 href
author_link = first_quote.find_element(By.CSS_SELECTOR, 'a')
print(f"href 속성:        {author_link.get_attribute('href')}")

# 클래스 확인
span_el = first_quote.find_element(By.CSS_SELECTOR, '.text')
print(f"class 속성:       {span_el.get_attribute('class')}")

# 태그들 가져오기
tags = first_quote.find_elements(By.CSS_SELECTOR, '.tag')
tag_texts = [t.text for t in tags]
print(f"태그들:           {tag_texts}")
""", "nb04-12"),

md("""## 6. 클릭 & 입력 & 키보드

```python
# 클릭
element.click()

# 텍스트 입력 (input, textarea)
element.send_keys('입력할 텍스트')

# 기존 내용 지우고 입력
element.clear()
element.send_keys('새 텍스트')

# 키보드 특수키
from selenium.webdriver.common.keys import Keys
element.send_keys(Keys.ENTER)     # 엔터
element.send_keys(Keys.TAB)       # 탭
element.send_keys(Keys.ESCAPE)    # ESC
element.send_keys(Keys.CONTROL, 'a')  # Ctrl+A
```
""", "nb04-13"),

code("""# 클릭 실습: '다음 페이지' 버튼 클릭

from selenium.webdriver.common.keys import Keys

# 현재 URL 확인
print(f"현재: {driver.current_url}")

# '다음' 버튼 찾기
next_btn = driver.find_element(By.CSS_SELECTOR, 'li.next a')
print(f"다음 버튼 href: {next_btn.get_attribute('href')}")

# 클릭!
next_btn.click()
time.sleep(2)

print(f"이동 후: {driver.current_url}")
print(f"제목: {driver.title}")
""", "nb04-14"),

md("""## 7. ⭐ Explicit Wait — 가장 중요한 개념!

JS 사이트에서 가장 많이 나는 에러:
```
NoSuchElementException: 요소를 찾지 못했습니다
```

원인: 페이지가 완전히 로드되기 전에 요소를 찾으려 해서!

**해결: Explicit Wait (명시적 대기)**
```python
wait = WebDriverWait(driver, 10)  # 최대 10초 대기
# 조건이 만족될 때까지 대기 (최대 10초)
element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.quote'))
)
```

**자주 쓰는 조건:**
```python
EC.presence_of_element_located(...)      # 요소가 DOM에 존재할 때
EC.visibility_of_element_located(...)    # 요소가 화면에 보일 때
EC.element_to_be_clickable(...)          # 요소를 클릭할 수 있을 때
EC.text_to_be_present_in_element(...)   # 요소에 특정 텍스트가 있을 때
```
""", "nb04-15"),

code("""# Explicit Wait 실습

# 페이지 이동
driver.get('http://quotes.toscrape.com/')

# 대기 객체 생성 (최대 10초)
wait = WebDriverWait(driver, 10)

# 요소가 나타날 때까지 대기
quotes = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.quote'))
)

print(f"✅ 대기 완료! {len(quotes)}개 명언 발견")

# 더 이상 time.sleep()에 의존하지 않아도 됨
# (하지만 빠른 반복 요청 방지를 위해 time.sleep(1) 은 여전히 권장)
""", "nb04-16"),

md("""## 8. 실전 ①: JS 렌더링 사이트 크롤링

`http://quotes.toscrape.com/js/` — JavaScript로 데이터를 렌더링하는 버전

BeautifulSoup으로는 빈 리스트가 나오지만, Selenium으로는 가져올 수 있어요!
""", "nb04-17"),

code("""# ❌ BeautifulSoup으로는 못 가져옴 (비교용)
import requests
from bs4 import BeautifulSoup

response = requests.get('http://quotes.toscrape.com/js/')
soup = BeautifulSoup(response.text, 'html.parser')
quotes_bs = soup.select('.quote')
print(f"BeautifulSoup: {len(quotes_bs)}개 발견 (JS 렌더링이라 0개!)")
""", "nb04-18"),

code("""# ✅ Selenium으로 JS 렌더링 사이트 크롤링

driver.get('http://quotes.toscrape.com/js/')

# JS 실행 완료까지 대기
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.quote')))

quotes_el = driver.find_elements(By.CSS_SELECTOR, '.quote')
print(f"Selenium: {len(quotes_el)}개 발견 ✅")

# 데이터 추출
rows = []
for q in quotes_el:
    text = q.find_element(By.CSS_SELECTOR, '.text').text
    author = q.find_element(By.CSS_SELECTOR, '.author').text
    tags_el = q.find_elements(By.CSS_SELECTOR, '.tag')
    tags = ', '.join(t.text for t in tags_el)

    rows.append({'명언': text, '저자': author, '태그': tags})

import pandas as pd
df = pd.DataFrame(rows)
print(df[['저자', '명언']].to_string(index=False))
""", "nb04-19"),

code("""# 여러 페이지 수집 (버튼 클릭 방식)

driver.get('http://quotes.toscrape.com/js/')

all_quotes = []
page = 1

while page <= 5:  # 최대 5페이지
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.quote')))

    quotes_el = driver.find_elements(By.CSS_SELECTOR, '.quote')

    for q in quotes_el:
        text = q.find_element(By.CSS_SELECTOR, '.text').text
        author = q.find_element(By.CSS_SELECTOR, '.author').text
        all_quotes.append({'페이지': page, '명언': text, '저자': author})

    print(f"  {page}페이지: {len(quotes_el)}개 수집")

    # 다음 페이지 버튼 확인
    next_btns = driver.find_elements(By.CSS_SELECTOR, 'li.next a')
    if not next_btns:
        print("  마지막 페이지!")
        break

    next_btns[0].click()
    page += 1
    time.sleep(1)

df_quotes = pd.DataFrame(all_quotes)
print(f"\\n총 {len(df_quotes)}개 명언 수집!")
print(df_quotes.groupby('저자').size().sort_values(ascending=False).head(5))
""", "nb04-20"),

md("""## 9. 실전 ②: 무한스크롤 크롤링

무한스크롤: 페이지 끝까지 내리면 새 데이터가 자동으로 로드!

**전략:**
```
1. 스크롤을 맨 아래로 내린다
2. 새 데이터가 로드될 때까지 기다린다
3. 데이터를 수집한다
4. 새 데이터가 없으면 중단한다
```
""", "nb04-21"),

code("""# 무한스크롤 크롤링: quotes.toscrape.com/scroll

driver.get('http://quotes.toscrape.com/scroll')
time.sleep(2)

all_quotes = []
last_count = 0
scroll_count = 0
max_scrolls = 10  # 최대 10번만 스크롤

while scroll_count < max_scrolls:
    # 현재 페이지의 모든 명언 수집
    quotes_el = driver.find_elements(By.CSS_SELECTOR, '.quote')
    current_count = len(quotes_el)

    if current_count == last_count:
        print(f"더 이상 새 데이터 없음. 종료!")
        break

    # 새로 추가된 것만 저장
    for q in quotes_el[last_count:]:
        text = q.find_element(By.CSS_SELECTOR, '.text').text
        author = q.find_element(By.CSS_SELECTOR, '.author').text
        all_quotes.append({'명언': text, '저자': author})

    print(f"  스크롤 {scroll_count + 1}: 누적 {current_count}개 (새 {current_count - last_count}개)")
    last_count = current_count
    scroll_count += 1

    # 맨 아래로 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 데이터 로드 대기

df_scroll = pd.DataFrame(all_quotes)
print(f"\\n총 {len(df_scroll)}개 명언 수집!")
df_scroll.head(5)
""", "nb04-22"),

md("""## 10. 실전 ③: 사람인 Selenium 버전

BeautifulSoup으로도 되지만, Selenium 버전은 이런 경우에 유리해요:
- 버튼 클릭으로 필터 적용 후 수집
- 팝업 닫기
- 로그인 후 수집

여기서는 "경력무관" 필터 클릭 후 수집하는 예제를 해봅니다.
""", "nb04-23"),

code("""# 사람인 Selenium — 검색 + 필터링

driver.get('https://www.saramin.co.kr/zf_user/search/recruit?searchword=데이터분석')
time.sleep(2)

# 팝업이 뜨면 닫기
try:
    close_btns = driver.find_elements(By.CSS_SELECTOR, '.btn-close, .close-btn, #layerRecmd .close')
    for btn in close_btns:
        if btn.is_displayed():
            btn.click()
            time.sleep(0.5)
except:
    pass

# 채용공고 수집
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.item_recruit')))

jobs_el = driver.find_elements(By.CSS_SELECTOR, 'div.item_recruit')
print(f"발견된 공고: {len(jobs_el)}개")

rows = []
for job in jobs_el:
    try:
        company = job.find_element(By.CSS_SELECTOR, 'strong.corp_name').text.strip()
        title = job.find_element(By.CSS_SELECTOR, 'h2.job_tit').text.strip()

        conditions = job.find_elements(By.CSS_SELECTOR, 'div.job_condition span')
        conds = [c.text.strip() for c in conditions]

        rows.append({
            '회사명': company,
            '공고제목': title,
            '지역': conds[0] if conds else None,
            '경력': conds[1] if len(conds) > 1 else None,
        })
    except Exception as e:
        continue

df_saramin = pd.DataFrame(rows)
print(df_saramin[['회사명', '공고제목', '경력']].head(10).to_string(index=False))
""", "nb04-24"),

md("""## 11. JavaScript 직접 실행

Selenium으로 JS를 직접 실행할 수 있어요.

```python
# 스크롤 관련
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 맨 아래
driver.execute_script("window.scrollTo(0, 0);")  # 맨 위
driver.execute_script("window.scrollBy(0, 500);")  # 500px 아래로

# 요소 스크롤
driver.execute_script("arguments[0].scrollIntoView();", element)

# 숨겨진 요소 클릭
driver.execute_script("arguments[0].click();", element)

# 값 가져오기
height = driver.execute_script("return document.body.scrollHeight")
```
""", "nb04-25"),

code("""# JS 실행 실습

driver.get('http://quotes.toscrape.com/')
time.sleep(2)

# 페이지 높이 가져오기
height = driver.execute_script("return document.body.scrollHeight")
print(f"페이지 높이: {height}px")

# 스크롤 위치 가져오기
scroll_pos = driver.execute_script("return window.pageYOffset")
print(f"현재 스크롤 위치: {scroll_pos}px")

# 500px 아래로 스크롤
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(1)

new_pos = driver.execute_script("return window.pageYOffset")
print(f"스크롤 후 위치: {new_pos}px")
""", "nb04-26"),

code("""# 브라우저 종료 — 항상 마지막에!

driver.quit()
print("브라우저 종료 완료!")
""", "nb04-27"),

md("""## ✅ 오늘 배운 것 정리

```python
# Selenium 크롤링 기본 템플릿

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, pandas as pd

# 1. 브라우저 열기
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 2. 페이지 이동
    driver.get('URL')

    # 3. 로드 대기
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item')))

    # 4. 데이터 수집
    items = driver.find_elements(By.CSS_SELECTOR, '.item')
    rows = []
    for item in items:
        text = item.find_element(By.CSS_SELECTOR, '.title').text
        rows.append({'제목': text})
        time.sleep(0.3)

    # 5. 저장
    df = pd.DataFrame(rows)
    df.to_csv('결과.csv', index=False, encoding='utf-8-sig')

finally:
    driver.quit()  # 항상 종료!
```

### BeautifulSoup vs Selenium 언제 쓰나?

| 상황 | 도구 |
|------|------|
| HTML이 서버에서 완성되어 옴 | BeautifulSoup ✅ (빠름) |
| JS로 데이터를 채워넣음 | Selenium |
| 무한스크롤 | Selenium |
| 버튼 클릭 / 로그인 필요 | Selenium |
| 대량 데이터 (수천 페이지) | BeautifulSoup (속도 이점) |
""", "nb04-28"),
]

save_nb(notebook(nb04_cells), os.path.join(NOTEBOOKS_DIR, '04_Selenium_동적사이트크롤링.ipynb'))


# ═══════════════════════════════════════════════════════════════
# MARKDOWN 01 — 환경설정 가이드 (Windows)
# ═══════════════════════════════════════════════════════════════

md01 = """# 🛠️ 환경설정 가이드 — Windows + VS Code

> 크롤링 수업을 시작하기 전에 이 가이드를 따라 환경을 세팅하세요.
> 한 번만 하면 됩니다!

---

## 1단계: Python 설치 확인

**이미 설치된 경우:** 아래로 건너뛰기

**설치 확인 방법:**
```
1. Win + R → cmd 입력 → Enter
2. 터미널에서: python --version
3. Python 3.10 이상이면 OK!
```

**설치가 안 되어 있다면:**
1. https://www.python.org/downloads/ 접속
2. "Download Python 3.x.x" 클릭
3. **⚠️ 중요: "Add Python to PATH" 체크박스 반드시 체크!**
4. Install Now 클릭

---

## 2단계: VS Code 설치

1. https://code.visualstudio.com/ 접속
2. "Download for Windows" 클릭
3. 설치 시 **"PATH에 추가"** 옵션 체크

**VS Code Python 확장 설치:**
1. VS Code 열기
2. 왼쪽 Extensions 아이콘 (Ctrl+Shift+X)
3. "Python" 검색 → Microsoft 만든 것 설치
4. "Jupyter" 검색 → Microsoft 만든 것 설치

---

## 3단계: 패키지 설치

VS Code 터미널 열기: **Ctrl + ` (백틱)**

```bash
# BeautifulSoup 수업용
pip install requests beautifulsoup4 pandas

# Selenium 수업용 (추가)
pip install selenium webdriver-manager
```

설치 확인:
```bash
python -c "import requests, bs4, pandas; print('설치 완료!')"
```

---

## 4단계: 폴더 구조 만들기

```
C:\\크롤링\\
├── notebooks\\      ← .ipynb 파일 저장
├── docs\\           ← 강의 자료
└── data\\           ← 수집한 CSV 파일
```

---

## 5단계: .ipynb 파일 열기

1. VS Code에서 `File → Open Folder` → 크롤링 폴더 선택
2. 탐색기에서 `.ipynb` 파일 클릭
3. 오른쪽 상단 커널 선택 → Python 3 선택
4. 셀 왼쪽 ▶ 버튼 또는 **Shift+Enter**로 실행

---

## 6단계: 크롬 개발자도구 사용법

크롤링에서 가장 중요한 스킬!

```
F12 → Elements 탭

원하는 요소 찾는 법:
① Elements 탭 상단 왼쪽 아이콘(↖) 클릭
② 웹페이지에서 원하는 요소 클릭
③ 자동으로 해당 HTML 코드가 강조됨

선택자 복사:
④ 강조된 태그 위에서 우클릭
⑤ Copy → Copy selector
```

---

## 자주 발생하는 문제

### `pip` 명령어가 안 될 때
```bash
# 대신 사용
python -m pip install 패키지명
```

### `ModuleNotFoundError` 에러
```bash
# 어떤 Python에 설치됐는지 확인
python -c "import sys; print(sys.executable)"
# 나온 경로의 pip로 설치
```

### Selenium에서 Chrome이 안 열릴 때
1. Chrome 브라우저가 설치되어 있는지 확인
2. 관리자 권한으로 VS Code 실행
3. 방화벽/보안 프로그램이 차단하는지 확인

### 한글 CSV가 엑셀에서 깨질 때
```python
df.to_csv('파일.csv', index=False, encoding='utf-8-sig')
# utf-8 이 아니라 utf-8-sig 를 써야 엑셀에서 정상 표시!
```

---

## 수업 진행 순서

```
01_환경설정과_첫크롤링.ipynb
    ↓
02_BeautifulSoup_완전정복.ipynb
    ↓
03_실전_정적사이트크롤링.ipynb
    ↓
04_Selenium_동적사이트크롤링.ipynb
```

각 노트북은 이전 노트북의 내용을 알고 있다고 가정합니다.
"""

save_md(md01, os.path.join(DOCS_DIR, '00_환경설정_윈도우_가이드.md'))


# ═══════════════════════════════════════════════════════════════
# MARKDOWN 02 — BeautifulSoup 강의자료
# ═══════════════════════════════════════════════════════════════

md02 = """# 🍜 BeautifulSoup 강의자료

> **학습 목표**: HTML에서 원하는 데이터를 정확하게 추출할 수 있다.
> **실습 환경**: VS Code + Python (로컬, Colab 아님!)
> **실습 파일**: `02_BeautifulSoup_완전정복.ipynb`

---

## 핵심 개념 한눈에 보기

```
웹페이지 (HTML)
     ↓
requests.get(url)    ← 페이지 가져오기
     ↓
BeautifulSoup(html)  ← HTML을 파이썬이 읽을 수 있는 형태로 변환
     ↓
select() / find()    ← 원하는 요소 찾기
     ↓
.text / ['href']     ← 데이터 추출
     ↓
DataFrame + CSV      ← 저장
```

---

## HTML 구조 이해

```html
<div class="product-card">           ← 태그: div, 클래스: product-card
    <h2 class="name">립밤</h2>       ← 태그: h2, 클래스: name
    <p class="price">12,000원</p>    ← 태그: p, 클래스: price
    <a href="/buy/123">구매하기</a>  ← 태그: a, href 속성
</div>
```

**용어 정리:**
- `<div>`: 여는 태그
- `</div>`: 닫는 태그
- `class="..."`: 스타일/선택자를 위한 이름표 (여러 요소가 같은 클래스 가능)
- `id="..."`: 유일한 식별자 (하나의 요소만 가짐)
- `href`, `src`: 속성 (attribute)

---

## BeautifulSoup 4가지 핵심 함수

### ① `find()` — 첫 번째 하나

```python
soup.find('p')                        # p 태그 첫 번째
soup.find('p', class_='price')        # class='price'인 p 태그
soup.find('div', id='main')           # id='main'인 div 태그
```

### ② `find_all()` — 조건에 맞는 전부

```python
soup.find_all('p')                    # 모든 p 태그 (리스트 반환)
soup.find_all('p', class_='price')    # class='price'인 모든 p
soup.find_all('p', limit=5)           # 최대 5개까지만
```

### ③ `select()` — CSS 선택자로 전부 ⭐ 가장 많이 씀

```python
soup.select('p')                      # 모든 p
soup.select('.price')                 # class="price" 전부
soup.select('#main')                  # id="main"
soup.select('div.product-card')       # div이면서 class="product-card"
soup.select('div > p')                # div 바로 아래 p
soup.select('div p')                  # div 안의 모든 p (중첩 포함)
soup.select('a[href]')                # href 속성 있는 a
soup.select('a[href*="product"]')     # href에 "product" 포함된 a
```

### ④ `select_one()` — CSS 선택자로 하나

```python
soup.select_one('.price')             # class="price" 첫 번째 하나
item.select_one('.name')              # item 안에서 첫 번째
```

---

## 데이터 추출 방법

```python
element = soup.select_one('.name')

# 텍스트 추출
element.text              # 텍스트 (앞뒤 공백 포함)
element.text.strip()      # 앞뒤 공백 제거 ← 이걸 주로 씀
element.get_text()        # text와 동일
element.get_text(strip=True)  # 공백 제거

# 속성값 추출
element['href']           # href 속성 (없으면 KeyError!)
element.get('href')       # href 속성 (없으면 None, 안전)
element.get('href', '')   # 없으면 빈 문자열 반환
```

---

## ⚠️ 절대 잊으면 안 되는 패턴

```python
# 요소를 찾지 못하면 None이 반환됨
# None.text를 호출하면 AttributeError 발생!

# ❌ 위험한 코드
name = soup.select_one('.name').text  # .name이 없으면 에러!

# ✅ 안전한 코드 (항상 이렇게!)
element = soup.select_one('.name')
name = element.text.strip() if element else None
```

---

## CSS 선택자 치트시트

| 선택자 | 설명 | HTML 예시 |
|--------|------|-----------|
| `div` | div 태그 | `<div>` |
| `.price` | class="price" | `<p class="price">` |
| `#header` | id="header" | `<div id="header">` |
| `div.card` | div + class="card" | `<div class="card">` |
| `div > p` | div 바로 아래 p | 직접 자식만 |
| `div p` | div 안의 모든 p | 중첩 포함 |
| `a[href]` | href 있는 a | `<a href="...">` |
| `a[href="/home"]` | href="/home"인 a | 값 일치 |
| `a[href*="product"]` | href에 "product" 포함 | 부분 포함 |
| `a[href^="http"]` | href가 "http"로 시작 | 시작 일치 |

---

## 개발자도구 활용법

### 방법 1: 직접 클릭 (추천)
```
① F12로 개발자도구 열기
② 상단 왼쪽 커서 아이콘 클릭 (또는 Ctrl+Shift+C)
③ 원하는 요소 위에 마우스 올리기 → 파란색 강조됨
④ 클릭! → Elements 탭에서 해당 HTML 코드 강조됨
⑤ 강조된 태그 우클릭 → Copy → Copy selector
```

### 방법 2: Elements 탭 검색
```
① F12 → Elements 탭
② Ctrl+F → 클래스명이나 텍스트 검색
③ 일치하는 요소 확인
```

### 방법 3: 소스 직접 읽기
```python
# HTML 구조 보기
print(soup.prettify()[:2000])

# 특정 요소의 HTML 보기
element = soup.select_one('.product')
print(element.prettify())
```

---

## 에러 해결 가이드

| 에러 | 원인 | 해결 |
|------|------|------|
| `AttributeError: 'NoneType'...` | 요소를 못 찾음 | `if element else None` 패턴 |
| `KeyError: 'href'` | 속성이 없음 | `element.get('href')` 사용 |
| 결과가 빈 리스트 `[]` | 선택자가 틀림 | F12로 선택자 다시 확인 |
| 한글 깨짐 | 인코딩 문제 | `response.encoding = 'utf-8'` |
| `403 Forbidden` | 차단됨 | User-Agent 헤더 추가 |
| 수집 중 멈춤 | 너무 빠른 요청 | `time.sleep(1)` 추가 |

---

## 전체 코드 템플릿

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# ① robots.txt 확인 (항상!)
robots = requests.get('https://사이트.com/robots.txt', headers=HEADERS)
print(robots.text[:500])

# ② 페이지 수집
all_items = []

for page in range(1, 4):
    url = f'https://사이트.com/list?page={page}'
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        print(f"{page}페이지 오류: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('div.item-selector')

    for item in items:
        name_el = item.select_one('.name')
        price_el = item.select_one('.price')

        all_items.append({
            '이름': name_el.text.strip() if name_el else None,
            '가격': price_el.text.strip() if price_el else None,
            '페이지': page,
        })

    print(f"{page}페이지: {len(items)}개 수집")
    time.sleep(1)  # ← 항상!

# ③ 저장
df = pd.DataFrame(all_items)
df.to_csv('결과.csv', index=False, encoding='utf-8-sig')
print(f"저장 완료: {len(df)}행")
```

---

## 연습 문제

### 문제 1 (기초)
`http://books.toscrape.com/`에서 가격이 £20 이하인 책만 수집하세요.

<details>
<summary>힌트</summary>

1. 모든 책을 수집한다
2. 가격 문자열을 float으로 변환한다 (£ 제거 → float())
3. 20.0 이하인 것만 필터링한다
</details>

### 문제 2 (응용)
`http://books.toscrape.com/`에서 50페이지 전체를 수집하고,
카테고리별 평균 가격을 구하세요.
(힌트: 각 책의 상세 페이지 URL에 카테고리 정보가 있습니다)

### 문제 3 (실전)
사람인에서 '파이썬' 키워드로 3페이지를 수집하고,
서울 지역 공고 중 경력무관인 것만 필터링하여 CSV로 저장하세요.
"""

save_md(md02, os.path.join(DOCS_DIR, '01_BeautifulSoup_강의자료.md'))


# ═══════════════════════════════════════════════════════════════
# MARKDOWN 03 — Selenium 강의자료
# ═══════════════════════════════════════════════════════════════

md03 = """# 🤖 Selenium 강의자료

> **학습 목표**: JavaScript로 렌더링되는 동적 사이트를 크롤링할 수 있다.
> **사전 조건**: BeautifulSoup 크롤링 기초, Chrome 브라우저 설치 완료
> **실습 파일**: `04_Selenium_동적사이트크롤링.ipynb`

---

## Selenium이란?

```
Selenium = 파이썬 코드로 브라우저를 자동으로 조작하는 도구

[파이썬 코드]  →  Selenium  →  ChromeDriver  →  Chrome 브라우저
    명령               변환         실행                동작
```

**할 수 있는 것:**
- URL 이동 / 뒤로가기 / 새로고침
- 버튼 클릭
- 텍스트 입력 (검색창, 로그인 등)
- 스크롤
- 스크린샷 찍기
- JS 코드 실행

---

## 설치 (Windows)

```bash
pip install selenium webdriver-manager
```

`webdriver-manager`는 ChromeDriver를 자동으로 설치해줍니다.
Chrome 버전에 맞는 드라이버를 수동으로 찾을 필요가 없어요!

---

## BeautifulSoup vs Selenium 비교

| | BeautifulSoup | Selenium |
|---|---|---|
| **속도** | 빠름 ⚡ | 느림 🐢 |
| **JS 실행** | ❌ 불가 | ✅ 가능 |
| **버튼 클릭** | ❌ 불가 | ✅ 가능 |
| **무한스크롤** | ❌ 불가 | ✅ 가능 |
| **메모리** | 적게 사용 | 많이 사용 |
| **사용 난이도** | 쉬움 | 보통 |

**언제 Selenium을 써야 하나?**
```
✅ Selenium 필요:
- 화면에는 보이는데 requests로 가져오면 비어있음
- 버튼 클릭 후에 데이터가 나타남
- 스크롤해야 데이터가 추가로 로드됨
- 로그인이 필요함

❌ Selenium 불필요 (BeautifulSoup으로 충분):
- 정적 HTML (서버에서 완성된 HTML이 옴)
- 단순 페이지 이동 (URL만 바꾸면 됨)
```

**확인 방법:**
```
1. 크롬에서 페이지 열기
2. Ctrl+U (페이지 소스 보기)
3. 소스에서 원하는 데이터 검색 (Ctrl+F)
4. 데이터가 소스에 없으면 → JS 렌더링 → Selenium 필요!
```

---

## 브라우저 열기 & 기본 설정

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 옵션 설정
options = webdriver.ChromeOptions()
# options.add_argument('--headless')          # 창 없이 실행 (서버용)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1280,900')
options.add_argument('--disable-blink-features=AutomationControlled')  # 봇 감지 회피
options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 브라우저 실행
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
driver.implicitly_wait(3)  # 기본 대기 3초
```

---

## 요소 찾기

### find_element vs find_elements

```python
# 하나만 (없으면 에러!)
element = driver.find_element(By.CSS_SELECTOR, '.quote')

# 전부 (없으면 빈 리스트)
elements = driver.find_elements(By.CSS_SELECTOR, '.quote')

# 요소 안에서 다시 찾기
container = driver.find_element(By.CSS_SELECTOR, '.product')
name = container.find_element(By.CSS_SELECTOR, '.name')
```

### By 종류

```python
By.CSS_SELECTOR    # '.class', '#id', 'div.card' 등 CSS 선택자
By.XPATH           # //div[@class='name'] 등 XPath
By.ID              # 'header' (id="header"인 요소)
By.CLASS_NAME      # 'name' (단일 클래스만, 공백 포함 불가)
By.TAG_NAME        # 'div', 'a', 'span' 등
By.LINK_TEXT       # 링크 텍스트 전체 일치
By.NAME            # name 속성값
```

> 💡 **CSS_SELECTOR 하나만 써도 거의 다 됩니다!**

---

## 데이터 가져오기

```python
element = driver.find_element(By.CSS_SELECTOR, '.name')

# 텍스트
element.text                          # 화면에 보이는 텍스트
element.get_attribute('innerHTML')   # 내부 HTML

# 속성값
element.get_attribute('href')        # href 속성
element.get_attribute('src')         # src 속성
element.get_attribute('class')       # class 속성
element.get_attribute('data-id')     # data-id 속성
element.get_attribute('value')       # input의 value
```

---

## 상호작용

```python
# 클릭
element.click()

# 강제 클릭 (일반 클릭이 안 될 때)
driver.execute_script("arguments[0].click();", element)

# 텍스트 입력
search_box = driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
search_box.clear()
search_box.send_keys('검색어')

# 특수키
from selenium.webdriver.common.keys import Keys
search_box.send_keys(Keys.ENTER)
search_box.send_keys(Keys.TAB)
search_box.send_keys(Keys.ESCAPE)
search_box.send_keys(Keys.CONTROL, 'a')  # 전체선택
```

---

## ⭐ Explicit Wait — 핵심 기술

### 왜 필요한가?
```
페이지 이동 후 즉시 요소를 찾으려 하면:
- JS가 아직 실행 중 → 요소가 아직 없음 → 에러!

해결: "요소가 나타날 때까지 기다리기"
```

### 기본 사용법

```python
wait = WebDriverWait(driver, 10)  # 최대 10초 대기

# 요소가 DOM에 생길 때까지
element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.item'))
)

# 요소가 화면에 보일 때까지
element = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '.popup'))
)

# 클릭 가능할 때까지
button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-load-more'))
)
button.click()
```

### 자주 쓰는 조건들

| 조건 | 설명 |
|------|------|
| `presence_of_element_located` | DOM에 존재할 때 |
| `presence_of_all_elements_located` | 여러 요소가 DOM에 있을 때 |
| `visibility_of_element_located` | 화면에 보일 때 |
| `element_to_be_clickable` | 클릭 가능할 때 |
| `text_to_be_present_in_element` | 텍스트가 있을 때 |
| `url_contains` | URL이 특정 문자 포함할 때 |

---

## 스크롤 제어

```python
# 맨 아래로
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 맨 위로
driver.execute_script("window.scrollTo(0, 0);")

# 500px 아래로
driver.execute_script("window.scrollBy(0, 500);")

# 특정 요소가 보이도록 스크롤
element = driver.find_element(By.CSS_SELECTOR, '.target')
driver.execute_script("arguments[0].scrollIntoView(true);", element)

# 현재 스크롤 위치 확인
y = driver.execute_script("return window.pageYOffset")

# 페이지 전체 높이
height = driver.execute_script("return document.body.scrollHeight")
```

---

## 무한스크롤 패턴

```python
driver.get('https://무한스크롤_사이트.com')
time.sleep(2)

collected = []
last_count = 0

for _ in range(10):  # 최대 10번 스크롤
    items = driver.find_elements(By.CSS_SELECTOR, '.item')
    current_count = len(items)

    if current_count == last_count:
        break  # 더 이상 새 데이터 없음

    # 새로 추가된 것만 처리
    for item in items[last_count:]:
        collected.append({'텍스트': item.text})

    last_count = current_count

    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 로딩 대기

print(f"총 {len(collected)}개 수집")
```

---

## 팝업 & 레이어 처리

```python
# 팝업 닫기 버튼 (여러 가능한 선택자 시도)
close_selectors = ['.popup-close', '.btn-close', '.modal-close', '#layerClose']

for selector in close_selectors:
    try:
        btn = driver.find_element(By.CSS_SELECTOR, selector)
        if btn.is_displayed():
            btn.click()
            time.sleep(0.5)
    except:
        continue

# 알림창 (alert) 처리
try:
    alert = driver.switch_to.alert
    print(f"알림창 내용: {alert.text}")
    alert.accept()   # 확인
    # alert.dismiss() # 취소
except:
    pass  # 알림창 없으면 무시
```

---

## 에러 해결 가이드

| 에러 | 원인 | 해결 |
|------|------|------|
| `NoSuchElementException` | 요소 없음 | 선택자 확인, Wait 추가 |
| `ElementClickInterceptedException` | 다른 요소가 위에 있음 | 팝업 닫기, JS 클릭 |
| `StaleElementReferenceException` | 페이지 새로고침으로 요소 사라짐 | 요소 다시 찾기 |
| `TimeoutException` | Wait 시간 초과 | 대기 시간 늘리기 |
| `WebDriverException` | 브라우저 크래시 | driver.quit() 후 재시작 |
| 창이 안 열림 | ChromeDriver 버전 불일치 | `webdriver-manager` 사용 |

---

## 전체 코드 템플릿

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, pandas as pd

# 브라우저 설정
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
wait = WebDriverWait(driver, 10)

try:
    all_data = []

    driver.get('https://크롤링할_사이트.com')

    # 팝업 처리
    try:
        close_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.popup-close')))
        close_btn.click()
    except:
        pass

    # 데이터 수집
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item')))
    items = driver.find_elements(By.CSS_SELECTOR, '.item')

    for item in items:
        name_el = item.find_elements(By.CSS_SELECTOR, '.name')
        name = name_el[0].text if name_el else None
        all_data.append({'이름': name})
        time.sleep(0.2)

    # 저장
    df = pd.DataFrame(all_data)
    df.to_csv('결과.csv', index=False, encoding='utf-8-sig')
    print(f"완료: {len(df)}행")

finally:
    driver.quit()  # 항상! try-finally로 보장
```

---

## 연습 문제

### 문제 1 (기초)
`http://quotes.toscrape.com/js/`에서 명언, 저자, 태그를 수집하여
DataFrame으로 만들고 CSV로 저장하세요.

### 문제 2 (응용)
`http://quotes.toscrape.com/scroll`에서 무한스크롤로
모든 명언을 수집하세요. (총 몇 개나 나오는지 확인!)

### 문제 3 (실전)
사람인에서 '데이터' 키워드로 검색한 뒤,
Selenium으로 2페이지까지 버튼 클릭으로 이동하며 공고를 수집하세요.
"""

save_md(md03, os.path.join(DOCS_DIR, '02_Selenium_강의자료.md'))


# ═══════════════════════════════════════════════════════════════
# 완료 출력
# ═══════════════════════════════════════════════════════════════

print("\n" + "="*50)
print("✅ 모든 파일 생성 완료!")
print("="*50)
print("\n📁 생성된 파일:")
for root, dirs, files in os.walk(BASE_DIR):
    level = root.replace(BASE_DIR, '').count(os.sep)
    indent = '  ' * level
    folder = os.path.basename(root)
    if folder not in ['__pycache__']:
        if level > 0:
            print(f"{indent}📂 {folder}/")
        for f in sorted(files):
            if not f.endswith('.py') and not f.endswith('.pyc'):
                size = os.path.getsize(os.path.join(root, f))
                print(f"{'  ' * (level+1)}📄 {f} ({size:,} bytes)")
