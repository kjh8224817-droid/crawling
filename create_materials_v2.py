"""
수업 자료 v2 — 헷갈리는 개념 완전정복 + 다양한 실전 사이트
생성 파일:
  notebooks/02_헷갈리는개념_완전정복.ipynb  (el.name 등)
  notebooks/03_실전_다양한사이트.ipynb      (쇼핑몰/중고/채용 다양)
  data/mock_used_market.html               (연습용 중고거래 HTML)
  data/mock_shopping.html                  (연습용 쇼핑몰 HTML)
  docs/01_BeautifulSoup_강의자료_수강생용.md (학생 전용 상세 자료)
"""

import json, os

BASE  = '/Users/haku/크롤링'
NB    = os.path.join(BASE, 'notebooks')
DOCS  = os.path.join(BASE, 'docs')
DATA  = os.path.join(BASE, 'data')

for d in [NB, DOCS, DATA]:
    os.makedirs(d, exist_ok=True)

# ── 헬퍼 ──────────────────────────────────────────────────────
def md(src, cid):
    return {"cell_type":"markdown","id":cid,"metadata":{},"source":src}

def code(src, cid):
    return {"cell_type":"code","execution_count":None,"id":cid,
            "metadata":{},"outputs":[],"source":src}

def nb(cells):
    return {
        "nbformat":4,"nbformat_minor":5,
        "metadata":{
            "kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
            "language_info":{
                "codemirror_mode":{"name":"ipython","version":3},
                "file_extension":".py","mimetype":"text/x-python",
                "name":"python","pygments_lexer":"ipython3","version":"3.12.0"
            }
        },
        "cells":cells
    }

def save_nb(notebook, path):
    with open(path,'w',encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)
    print(f"  ✅ {path}")

def save_text(text, path):
    with open(path,'w',encoding='utf-8') as f:
        f.write(text)
    print(f"  ✅ {path}")


# ══════════════════════════════════════════════════════════════
#  연습용 HTML 파일
# ══════════════════════════════════════════════════════════════

MOCK_USED_MARKET = """<!DOCTYPE html>
<html lang="ko">
<head><meta charset="UTF-8"><title>중고나라 - 인기 중고 거래</title></head>
<body>
<header>
  <h1 class="site-title">중고나라</h1>
  <nav><a href="/login">로그인</a> <a href="/sell">판매하기</a></nav>
</header>

<main>
  <h2 class="section-title">오늘의 인기 매물</h2>

  <ul class="article-list">

    <li class="article-item" data-id="1001" data-category="디지털">
      <a href="/articles/1001" class="article-link">
        <div class="thumbnail">
          <img src="/img/iphone.jpg" alt="아이폰 15 프로">
        </div>
        <div class="content">
          <h3 class="title">아이폰 15 프로 256GB 자급제 (미개봉)</h3>
          <p class="price">1,200,000원</p>
          <div class="meta">
            <span class="location">서울 강남구</span>
            <span class="time-ago">10분 전</span>
          </div>
          <div class="badges">
            <span class="badge status-sale">판매중</span>
          </div>
          <span class="like-count">23</span>
        </div>
      </a>
    </li>

    <li class="article-item" data-id="1002" data-category="패션">
      <a href="/articles/1002" class="article-link">
        <div class="thumbnail">
          <img src="/img/jacket.jpg" alt="나이키 자켓">
        </div>
        <div class="content">
          <h3 class="title">나이키 윈드브레이커 자켓 M 사이즈</h3>
          <p class="price">45,000원</p>
          <div class="meta">
            <span class="location">경기 성남시</span>
            <span class="time-ago">1시간 전</span>
          </div>
          <div class="badges">
            <span class="badge status-sale">판매중</span>
            <span class="badge nego">가격제안</span>
          </div>
          <span class="like-count">8</span>
        </div>
      </a>
    </li>

    <li class="article-item" data-id="1003" data-category="디지털">
      <a href="/articles/1003" class="article-link">
        <div class="thumbnail">
          <img src="/img/macbook.jpg" alt="맥북 에어">
        </div>
        <div class="content">
          <h3 class="title">맥북 에어 M2 15인치 스페이스그레이</h3>
          <p class="price">1,550,000원</p>
          <div class="meta">
            <span class="location">서울 마포구</span>
            <span class="time-ago">3시간 전</span>
          </div>
          <div class="badges">
            <span class="badge status-reserved">예약중</span>
          </div>
          <span class="like-count">51</span>
        </div>
      </a>
    </li>

    <li class="article-item" data-id="1004" data-category="가구">
      <a href="/articles/1004" class="article-link">
        <div class="thumbnail">
          <img src="/img/desk.jpg" alt="게이밍 의자">
        </div>
        <div class="content">
          <h3 class="title">시디즈 T50 게이밍 의자 블랙</h3>
          <p class="price">180,000원</p>
          <div class="meta">
            <span class="location">인천 부평구</span>
            <span class="time-ago">5시간 전</span>
          </div>
          <div class="badges">
            <span class="badge status-sale">판매중</span>
            <span class="badge nego">가격제안</span>
          </div>
          <span class="like-count">15</span>
        </div>
      </a>
    </li>

    <li class="article-item" data-id="1005" data-category="패션">
      <a href="/articles/1005" class="article-link">
        <div class="thumbnail">
          <img src="/img/bag.jpg" alt="구찌 가방">
        </div>
        <div class="content">
          <h3 class="title">구찌 GG 마몬트 숄더백 정품</h3>
          <p class="price">890,000원</p>
          <div class="meta">
            <span class="location">서울 청담동</span>
            <span class="time-ago">어제</span>
          </div>
          <div class="badges">
            <span class="badge status-sold">판매완료</span>
          </div>
          <span class="like-count">102</span>
        </div>
      </a>
    </li>

    <li class="article-item" data-id="1006" data-category="디지털">
      <a href="/articles/1006" class="article-link">
        <div class="thumbnail">
          <img src="/img/airpods.jpg" alt="에어팟 프로">
        </div>
        <div class="content">
          <h3 class="title">에어팟 프로 2세대 USB-C 박스포함</h3>
          <p class="price">220,000원</p>
          <div class="meta">
            <span class="location">서울 송파구</span>
            <span class="time-ago">2일 전</span>
          </div>
          <div class="badges">
            <span class="badge status-sale">판매중</span>
          </div>
          <span class="like-count">37</span>
        </div>
      </a>
    </li>

  </ul>
</main>
</body>
</html>"""


MOCK_SHOPPING = """<!DOCTYPE html>
<html lang="ko">
<head><meta charset="UTF-8"><title>뷰티마켓 - 인기 화장품</title></head>
<body>
<header>
  <h1 class="logo">뷰티마켓</h1>
</header>

<section class="product-section">
  <h2 class="section-title">🏆 이번주 베스트</h2>

  <ol class="product-list">

    <li class="product-card" data-rank="1" data-product-id="P001">
      <div class="rank-badge">1</div>
      <div class="brand">라네즈</div>
      <h3 class="product-name">네오 쿠션 파운데이션 21호 아이보리</h3>
      <div class="price-area">
        <span class="original-price">38,000원</span>
        <span class="sale-price">27,000원</span>
        <span class="discount-rate">29%</span>
      </div>
      <div class="rating-area">
        <span class="stars">★★★★☆</span>
        <span class="review-count">(리뷰 1,204개)</span>
      </div>
      <div class="tags">
        <span class="tag">촉촉</span>
        <span class="tag">지속력</span>
        <span class="tag">커버력</span>
      </div>
      <a href="/products/P001" class="buy-link">구매하기</a>
    </li>

    <li class="product-card" data-rank="2" data-product-id="P002">
      <div class="rank-badge">2</div>
      <div class="brand">이니스프리</div>
      <h3 class="product-name">수분크림 그린티 씨드 세럼 80ml</h3>
      <div class="price-area">
        <span class="original-price">25,000원</span>
        <span class="sale-price">19,900원</span>
        <span class="discount-rate">20%</span>
      </div>
      <div class="rating-area">
        <span class="stars">★★★★★</span>
        <span class="review-count">(리뷰 3,891개)</span>
      </div>
      <div class="tags">
        <span class="tag">수분</span>
        <span class="tag">그린티</span>
      </div>
      <a href="/products/P002" class="buy-link">구매하기</a>
    </li>

    <li class="product-card" data-rank="3" data-product-id="P003">
      <div class="rank-badge">3</div>
      <div class="brand">설화수</div>
      <h3 class="product-name">자음 생크림 50ml 리미티드 에디션</h3>
      <div class="price-area">
        <span class="original-price">120,000원</span>
        <span class="sale-price">96,000원</span>
        <span class="discount-rate">20%</span>
      </div>
      <div class="rating-area">
        <span class="stars">★★★★★</span>
        <span class="review-count">(리뷰 572개)</span>
      </div>
      <div class="tags">
        <span class="tag">안티에이징</span>
        <span class="tag">보습</span>
        <span class="tag">한방</span>
      </div>
      <a href="/products/P003" class="buy-link">구매하기</a>
    </li>

    <li class="product-card" data-rank="4" data-product-id="P004">
      <div class="rank-badge">4</div>
      <div class="brand">에스쁘아</div>
      <h3 class="product-name">프로 테일러 비이 파운데이션 SPF34</h3>
      <div class="price-area">
        <span class="original-price">42,000원</span>
        <span class="sale-price">42,000원</span>
        <span class="discount-rate">0%</span>
      </div>
      <div class="rating-area">
        <span class="stars">★★★★☆</span>
        <span class="review-count">(리뷰 887개)</span>
      </div>
      <div class="tags">
        <span class="tag">세미무광</span>
        <span class="tag">지성피부</span>
      </div>
      <a href="/products/P004" class="buy-link">구매하기</a>
    </li>

    <li class="product-card" data-rank="5" data-product-id="P005">
      <div class="rank-badge">5</div>
      <div class="brand">클리오</div>
      <h3 class="product-name">킬 커버 더 뉴 파운웨어 쿠션 기획세트</h3>
      <div class="price-area">
        <span class="original-price">32,000원</span>
        <span class="sale-price">25,600원</span>
        <span class="discount-rate">20%</span>
      </div>
      <div class="rating-area">
        <span class="stars">★★★★★</span>
        <span class="review-count">(리뷰 5,023개)</span>
      </div>
      <div class="tags">
        <span class="tag">쿠션</span>
        <span class="tag">기획세트</span>
        <span class="tag">리필포함</span>
      </div>
      <a href="/products/P005" class="buy-link">구매하기</a>
    </li>

  </ol>
</section>
</body>
</html>"""

save_text(MOCK_USED_MARKET, os.path.join(DATA, 'mock_used_market.html'))
save_text(MOCK_SHOPPING,    os.path.join(DATA, 'mock_shopping.html'))


# ══════════════════════════════════════════════════════════════
#  NOTEBOOK: 헷갈리는 개념 완전정복
# ══════════════════════════════════════════════════════════════

nb_conf_cells = [

md("""# 🔍 헷갈리는 BeautifulSoup 개념 완전정복

> 이 노트북은 **자주 혼동되는 개념들**만 모아서 집중적으로 연습합니다.
> 한 셀씩 직접 실행하면서 결과를 눈으로 확인하세요!

---

## 📋 이 노트북에서 다루는 것들

| 번호 | 주제 | 왜 헷갈리나? |
|------|------|------------|
| 1 | `el.name` vs `.select('.name')` | 둘 다 'name'이 들어가 있어서 |
| 2 | `.text` vs `.string` vs `.get_text()` | 비슷해 보이는데 다름 |
| 3 | `find()` vs `select_one()` | 같은 결과처럼 보이는데 다름 |
| 4 | `['class']` vs `.get('class')` vs `.select('.클래스')` | 'class'가 세 곳에 등장 |
| 5 | `['href']` vs `.get('href')` | 왜 두 가지가 있나? |
| 6 | `find_all()` vs `select()` | 같아 보이는데 차이가 있음 |
| 7 | 부모/자식/형제 태그 탐색 | 개념 자체가 낯섦 |
""", "conf-01"),

# ─────────────────────────────────────────
md("""---
## 1️⃣ `el.name` vs `.select('.name')`
### "둘 다 name인데 전혀 달라요!"

많은 분들이 이렇게 헷갈립니다:
```python
soup.select('.name')   # ← 이게 el.name이랑 같은 건가요?
el.name                # ← 이게 class="name"을 가져오는 건가요?
```

**정답: 완전히 다른 것입니다!**

```
soup.select('.name')
  → CSS 선택자로 "class가 name인 요소들"을 찾는 것
  → .name은 선택자 문자열 안에 있는 것

el.name
  → BeautifulSoup 태그 객체의 속성
  → "이 태그의 이름(종류)이 뭐냐?"를 묻는 것
  → 결과: 'div', 'span', 'p', 'a' 등
```
""", "conf-02"),

code("""from bs4 import BeautifulSoup

html = \"\"\"
<html>
<body>
  <div class="product-card">
    <span class="name">라네즈 수분크림</span>
    <p class="price">38,000원</p>
    <a href="/products/1" class="buy-link">구매</a>
  </div>
</body>
</html>
\"\"\"

soup = BeautifulSoup(html, 'html.parser')

# ─── el.name: 태그의 종류를 확인하는 것 ───────────────────────

div_el = soup.find('div')
span_el = soup.find('span')
a_el = soup.find('a')

print("=== el.name: 태그 이름(종류) 확인 ===")
print(f"div 태그의 .name:  '{div_el.name}'")   # 'div'
print(f"span 태그의 .name: '{span_el.name}'")  # 'span'
print(f"a 태그의 .name:    '{a_el.name}'")     # 'a'
print()

# ─── select('.name'): class='name'인 요소를 찾는 것 ──────────

found = soup.select('.name')  # class="name"인 요소 찾기
print("=== select('.name'): class가 name인 요소 찾기 ===")
print(f"찾은 요소: {found}")
print(f"찾은 요소 수: {len(found)}")
print(f"그 요소의 텍스트: '{found[0].text}'")
print()

# ─── 조합해서 쓰면? ──────────────────────────────────────────

name_el = soup.select_one('.name')  # class='name'인 요소 하나
print("=== 조합 사용 ===")
print(f"select_one('.name')로 찾은 요소의 .name: '{name_el.name}'")
# → class='name'인 span 태그를 찾았고, 그 태그의 이름은 'span'
""", "conf-03"),

md("""### 정리

```python
el.name              # 태그의 종류: 'div', 'span', 'p', 'a' 등
                     # ↑ el은 BeautifulSoup 태그 객체

soup.select('.name') # class="name"인 요소들 찾기
                     # ↑ .name은 CSS 선택자 문자열의 일부
```

> 💡 **외우는 법**: `el.name`은 "이 태그, 너 뭐야?" 라고 물어보는 것.
> `select('.name')`은 "class가 name인 얘 어딨어?" 라고 찾는 것.

### 언제 `el.name`을 실제로 쓰나요?

```python
# 여러 종류의 태그가 섞여있을 때, 어떤 태그인지 확인할 때 씀
for el in soup.find_all(['h1', 'h2', 'h3']):
    print(f"태그: {el.name}, 텍스트: {el.text.strip()}")
```
""", "conf-04"),

code("""# el.name 실제 활용 예시: 태그 종류 확인하기

html2 = \"\"\"
<article class="post">
  <h1>크롤링 완전 정복</h1>
  <h2>BeautifulSoup 편</h2>
  <h3>핵심 개념 1</h3>
  <p>본문 내용입니다.</p>
  <h3>핵심 개념 2</h3>
  <p>두 번째 본문입니다.</p>
</article>
\"\"\"

soup2 = BeautifulSoup(html2, 'html.parser')

print("=== el.name으로 태그 종류 구분하기 ===")
for el in soup2.find_all(['h1', 'h2', 'h3', 'p']):
    level = el.name          # 'h1', 'h2', 'h3', 'p' 중 하나
    text  = el.text.strip()
    print(f"[{level}] {text}")
""", "conf-05"),

# ─────────────────────────────────────────
md("""---
## 2️⃣ `.text` vs `.string` vs `.get_text()`
### "텍스트 뽑는 방법이 왜 세 가지나 있나요?"

세 가지 모두 텍스트를 가져오지만, **동작이 다른 상황이 있습니다.**
""", "conf-06"),

code("""from bs4 import BeautifulSoup

# 케이스 1: 태그 안에 텍스트만 있는 경우
html_simple = '<span class="price">38,000원</span>'
soup_s = BeautifulSoup(html_simple, 'html.parser')
el = soup_s.find('span')

print("=== 케이스 1: 단순한 경우 (세 가지 모두 같음) ===")
print(f".text:       '{el.text}'")
print(f".string:     '{el.string}'")
print(f".get_text(): '{el.get_text()}'")
""", "conf-07"),

code("""# 케이스 2: 태그 안에 다른 태그가 있는 경우
html_nested = \"\"\"
<div class="product">
  <span class="brand">라네즈</span>
  <span class="name">수분크림</span>
  <p class="price">38,000원</p>
</div>
\"\"\"

soup_n = BeautifulSoup(html_nested, 'html.parser')
div_el = soup_n.find('div')

print("=== 케이스 2: 자식 태그가 있는 경우 ===")

# .text — 모든 자식 태그의 텍스트를 합쳐서 반환
print(f".text:         '{div_el.text}'")
# → '\\n  라네즈\\n  수분크림\\n  38,000원\\n'

# .string — 자식이 하나뿐일 때만 동작, 여러 자식이면 None!
print(f".string:       '{div_el.string}'")
# → None (자식이 여러 개라서!)

# .get_text() — .text와 같지만 옵션 지정 가능
print(f".get_text():   '{div_el.get_text()}'")
print(f".get_text(strip=True):  '{div_el.get_text(strip=True)}'")
# strip=True: 각 조각의 앞뒤 공백 제거
print(f".get_text(separator=', '): '{div_el.get_text(separator=', ', strip=True)}'")
# separator: 조각 사이 구분자 지정
""", "conf-08"),

code("""# 케이스 3: 실제 크롤링에서 어떻게 쓰나?

html_product = \"\"\"
<li class="product-item">
  <strong class="brand">이니스프리</strong>
  <span class="name">  그린티 씨드 세럼  </span>
  <p class="price">
    <del class="original">25,000원</del>
    <strong class="sale">19,900원</strong>
  </p>
</li>
\"\"\"

soup_p = BeautifulSoup(html_product, 'html.parser')

# ✅ 실전에서 주로 쓰는 방법: 특정 요소 하나를 골라서 .text.strip()
brand = soup_p.select_one('.brand').text.strip()
name  = soup_p.select_one('.name').text.strip()
sale  = soup_p.select_one('.sale').text.strip()

print(f"브랜드: {brand}")
print(f"상품명: {name}")
print(f"할인가: {sale}")

# ⚠️ 전체 div의 .text는 불필요한 텍스트가 섞여서 보통 안 씀
item = soup_p.find('li')
print(f"\\nli 전체 .text: '{item.text}'")
print(f"li 전체 .get_text(strip=True, separator=' | '): '{item.get_text(strip=True, separator=' | ')}'")
""", "conf-09"),

md("""### 정리

| 방법 | 언제 씀 | 자식 태그 있을 때 |
|------|---------|----------------|
| `.text` | 가장 많이 씀 | 전체 텍스트 합쳐서 반환 |
| `.string` | 잘 안 씀 | 자식이 여러 개면 `None` |
| `.get_text(strip=True)` | 공백 정리할 때 | 옵션 지정 가능 |

**결론: 대부분 `.text.strip()` 하나면 충분합니다!**
""", "conf-10"),

# ─────────────────────────────────────────
md("""---
## 3️⃣ `find()` vs `select_one()` — 거의 같지만 차이가 있어요
""", "conf-11"),

code("""from bs4 import BeautifulSoup

html = \"\"\"
<ul class="list">
  <li class="item active">첫 번째</li>
  <li class="item">두 번째</li>
  <li class="item">세 번째</li>
</ul>
\"\"\"

soup = BeautifulSoup(html, 'html.parser')

# ─── 같은 결과 ──────────────────────────────────────────────

a1 = soup.find('li', class_='item')
a2 = soup.select_one('li.item')
print("=== 같은 결과인 경우 ===")
print(f"find():        '{a1.text}'")
print(f"select_one():  '{a2.text}'")
# 둘 다 '첫 번째'
print()

# ─── 차이: select_one()이 더 표현력이 풍부 ─────────────────

# find()로는 복합 조건이 어색함
# select_one()은 CSS 선택자 그대로 사용 가능
active = soup.select_one('li.item.active')  # item이면서 active인 것
print("=== select_one()의 강점 ===")
print(f"li.item.active: '{active.text}'")   # '첫 번째'

# find()도 가능하지만 문법이 다름
active2 = soup.find('li', class_=['item', 'active'])
# ↑ 이건 item 또는 active, 의도와 다를 수 있어서 주의!
print()

# ─── 둘 다 못 찾으면 None ─────────────────────────────────

not_found_1 = soup.find('div', class_='nothing')
not_found_2 = soup.select_one('div.nothing')
print("=== 못 찾으면 ===")
print(f"find() 결과:        {not_found_1}")  # None
print(f"select_one() 결과:  {not_found_2}")  # None
""", "conf-12"),

md("""### 정리

```python
# 기능상 거의 동일, 실전에서는 select_one()을 더 많이 씀
soup.find('div', class_='name')   →  soup.select_one('div.name')
soup.find('a', id='main')         →  soup.select_one('a#main')

# select_one()이 더 직관적인 경우 (복합 클래스)
soup.select_one('li.item.active')   # item이면서 active
soup.select_one('div > p.price')    # div 바로 아래 p.price
soup.select_one('a[href*="product"]')  # href에 product 포함
```

> 💡 **권장**: 개발자도구에서 Copy selector 하면 CSS 형식으로 나와요.
> 그걸 그대로 `select_one()`에 쓰면 됩니다. `find()`보다 편해요!
""", "conf-13"),

# ─────────────────────────────────────────
md("""---
## 4️⃣ class 관련 3가지 헷갈리는 것

```python
el['class']            # ① HTML 속성 'class'의 값 가져오기
el.get('class')        # ② 위와 같지만 없어도 에러 안 남
soup.select('.name')   # ③ class='name'인 요소 찾기 (탐색!)
```

완전히 다른 용도입니다!
""", "conf-14"),

code("""from bs4 import BeautifulSoup

html = \"\"\"
<div class="product-card featured new-arrival">
  <span class="name">에어팟 프로 2세대</span>
</div>
<div class="product-card">
  <span class="name">아이폰 15</span>
</div>
\"\"\"

soup = BeautifulSoup(html, 'html.parser')

# ① el['class'] — 그 요소의 class 속성값 (리스트로 반환!)
first_div = soup.find('div')
print("=== ① el['class'] — class 속성값 가져오기 ===")
print(f"first_div['class']: {first_div['class']}")
# → ['product-card', 'featured', 'new-arrival']
# ↑ class가 여러 개면 리스트로 반환된다는 점 주의!
print()

# ② el.get('class') — ①과 같지만 없어도 에러 안 남 (안전)
print("=== ② el.get('class') — 안전하게 가져오기 ===")
print(f"first_div.get('class'):  {first_div.get('class')}")
# → ['product-card', 'featured', 'new-arrival']

# 없는 속성이면?
no_id = first_div['id']    if 'id' in first_div.attrs else '없음(KeyError 방지)'
safe  = first_div.get('id', '없음')
print(f"없는 속성 ['id']:       '{no_id}'")
print(f"없는 속성 .get('id'):   '{safe}'")
print()

# ③ soup.select('.product-card') — class='product-card'인 요소 탐색
print("=== ③ select('.product-card') — 해당 클래스 요소 찾기 ===")
cards = soup.select('.product-card')
print(f"찾은 div 수: {len(cards)}")
for card in cards:
    classes = card.get('class')
    name    = card.select_one('.name').text
    print(f"  클래스목록: {classes} / 상품명: {name}")
""", "conf-15"),

md("""### 정리

```
el['class']            → 이 요소의 class 속성을 가져와라 (값 조회)
el.get('class')        → 위와 같지만 없어도 None 반환 (안전)
soup.select('.name')   → class="name"인 요소를 찾아라 (탐색)
```

**class는 여러 개일 수 있어서 리스트로 반환됩니다!**
```python
# <div class="card featured hot">
el['class']   # → ['card', 'featured', 'hot']
el['class'][0]  # → 'card' (첫 번째 클래스)

# 특정 클래스가 있는지 확인
if 'featured' in el.get('class', []):
    print("이 상품은 추천 상품!")
```
""", "conf-16"),

# ─────────────────────────────────────────
md("""---
## 5️⃣ `el['href']` vs `el.get('href')`
### "왜 두 가지 방법이 있나요?"
""", "conf-17"),

code("""from bs4 import BeautifulSoup

html = \"\"\"
<ul>
  <li><a href="/products/1">상품 상세 링크</a></li>
  <li><a>href 없는 링크</a></li>
  <li><a href="https://example.com" target="_blank">외부 링크</a></li>
</ul>
\"\"\"

soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all('a')

print("=== 모든 a 태그의 href 확인 ===")
print()

for i, link in enumerate(links, 1):
    print(f"--- {i}번째 a 태그: {link} ---")

    # ❌ el['href'] — href 없으면 KeyError 에러 발생!
    try:
        href1 = link['href']
        print(f"  ['href']:      '{href1}'")
    except KeyError:
        print(f"  ['href']:      ❌ KeyError 에러! href 속성이 없어요.")

    # ✅ el.get('href') — href 없으면 None 반환 (안전)
    href2 = link.get('href')
    print(f"  .get('href'):  {href2}")

    # ✅ el.get('href', '') — 없으면 기본값 반환
    href3 = link.get('href', '링크없음')
    print(f"  .get('href', '링크없음'): '{href3}'")
    print()
""", "conf-18"),

code("""# 실전에서는 이렇게 써요

from bs4 import BeautifulSoup

html = \"\"\"
<div class="product-list">
  <a href="/products/101" class="product-link">아이폰 15</a>
  <a class="product-link">링크없는상품</a>
  <a href="/products/103" class="product-link">맥북 에어</a>
</div>
\"\"\"

soup = BeautifulSoup(html, 'html.parser')
BASE_URL = 'https://www.shopping.co.kr'

print("=== 실전 href 수집 패턴 ===")
for link in soup.select('a.product-link'):
    name = link.text.strip()
    href = link.get('href')  # 없으면 None

    if href:
        full_url = BASE_URL + href  # 상대경로 → 절대경로
    else:
        full_url = None

    print(f"상품명: {name:10}  링크: {full_url}")
""", "conf-19"),

# ─────────────────────────────────────────
md("""---
## 6️⃣ `find_all()` vs `select()` — 비슷하지만 다릅니다
""", "conf-20"),

code("""from bs4 import BeautifulSoup

html = \"\"\"
<ul class="job-list">
  <li class="job-item urgent">
    <a href="/job/1">데이터 분석가 채용</a>
    <span class="company">네이버</span>
    <span class="deadline urgent">내일 마감</span>
  </li>
  <li class="job-item">
    <a href="/job/2">파이썬 개발자</a>
    <span class="company">카카오</span>
    <span class="deadline">2024-12-31</span>
  </li>
  <li class="job-item">
    <a href="/job/3">ML 엔지니어</a>
    <span class="company">라인</span>
    <span class="deadline">채용시마감</span>
  </li>
</ul>
\"\"\"

soup = BeautifulSoup(html, 'html.parser')

print("=== find_all() 사용 ===")
# 태그이름 + class 조합
items1 = soup.find_all('li', class_='job-item')
print(f"find_all('li', class_='job-item'): {len(items1)}개")

print()
print("=== select() 사용 ===")
# CSS 선택자
items2 = soup.select('li.job-item')
print(f"select('li.job-item'): {len(items2)}개")

print()
print("=== 결과가 같음? ===")
print(f"첫 번째 요소 같음: {items1[0] == items2[0]}")  # True

print()
print("=== select()가 더 강력한 경우 ===")
# li 바로 아래 a만 (find_all은 이게 어색)
direct_links = soup.select('li.job-item > a')
print(f"li 바로 아래 a: {len(direct_links)}개")
for a in direct_links:
    print(f"  {a.text} → {a.get('href')}")

print()
# 특정 속성 포함
urgent = soup.select('li.job-item.urgent')
print(f"urgent 클래스 동시에 가진 li: {len(urgent)}개")
for u in urgent:
    print(f"  {u.select_one('a').text}")
""", "conf-21"),

md("""### 정리

| | `find_all()` | `select()` |
|---|---|---|
| 기본 사용 | `find_all('li', class_='item')` | `select('li.item')` |
| 여러 클래스 동시 조건 | 복잡 | `select('li.item.active')` |
| 자식 관계 지정 | 어려움 | `select('div > p')` |
| 속성 조건 | `attrs={'data-id': '1'}` | `select('[data-id="1"]')` |
| 결과 | 리스트 | 리스트 |

**결론: `select()`가 더 유연합니다. CSS 선택자를 그대로 쓸 수 있어서요.**
""", "conf-22"),

# ─────────────────────────────────────────
md("""---
## 7️⃣ 부모/자식/형제 태그 탐색

트리 구조를 이해하면 더 정확하게 원하는 요소를 찾을 수 있어요.

```html
<div class="card">          ← div의 자식: h3, p
  <h3>제목</h3>            ← h3의 부모: div, 형제: p
  <p>내용</p>              ← p의 부모: div, 형제: h3
</div>
```
""", "conf-23"),

code("""from bs4 import BeautifulSoup

html = \"\"\"
<section class="products">
  <div class="card">
    <h3 class="title">맥북 에어 M2</h3>
    <p class="price">1,550,000원</p>
    <p class="stock">재고: 3개</p>
    <a href="/buy/1" class="buy-btn">구매</a>
  </div>
  <div class="card">
    <h3 class="title">아이패드 프로</h3>
    <p class="price">1,200,000원</p>
    <p class="stock">재고: 0개 (품절)</p>
    <a href="/buy/2" class="buy-btn">구매</a>
  </div>
</section>
\"\"\"

soup = BeautifulSoup(html, 'html.parser')

# 특정 요소 하나 선택
title_el = soup.select_one('h3.title')
print(f"시작점: {title_el}")
print()

# ─── 부모 (parent) ────────────────────────────────────────
parent = title_el.parent
print(f"부모 태그: <{parent.name}> (class: {parent.get('class')})")
print()

# ─── 자식 (children) ──────────────────────────────────────
print("부모의 자식들:")
for child in parent.children:
    # 텍스트 노드(공백 등)도 포함되어 '\n'이 나올 수 있어요
    if child.name:  # 태그인 것만 (텍스트 노드 제외)
        print(f"  <{child.name}> {child.text.strip()}")
print()

# ─── 다음 형제 (next_sibling) ────────────────────────────
# 주의: 공백 텍스트도 형제로 취급됨 → find_next_sibling() 사용 권장
price_sibling = title_el.find_next_sibling('p')
print(f"h3 다음 p 형제: {price_sibling.text}")

# 이전 형제
# prev = price_sibling.find_previous_sibling('h3')
# print(f"p 이전 h3 형제: {prev.text}")
print()

# ─── 실전 활용: 부모 타고 올라가기 ──────────────────────
# buy_btn → 그 div 안의 title 찾기 (형제나 부모 활용)
buy_btn = soup.select('.buy-btn')[1]  # 두 번째 구매 버튼
card_div = buy_btn.parent             # 바로 위 div.card
title_in_same_card = card_div.select_one('.title')
print(f"두 번째 구매 버튼과 같은 카드의 상품명: {title_in_same_card.text}")
""", "conf-24"),

# ─────────────────────────────────────────
md("""---
## 🎯 종합 연습 — 모든 개념 한번에 적용

지금까지 배운 개념을 모두 사용해서 데이터를 수집해봅시다.
""", "conf-25"),

code("""from bs4 import BeautifulSoup
import pandas as pd

# 앞서 만든 mock_shopping.html을 직접 문자열로 파싱

html_shopping = \"\"\"
<ol class="product-list">
  <li class="product-card" data-rank="1" data-product-id="P001">
    <div class="rank-badge">1</div>
    <div class="brand">라네즈</div>
    <h3 class="product-name">네오 쿠션 파운데이션 21호</h3>
    <div class="price-area">
      <span class="original-price">38,000원</span>
      <span class="sale-price">27,000원</span>
      <span class="discount-rate">29%</span>
    </div>
    <div class="rating-area">
      <span class="stars">★★★★☆</span>
      <span class="review-count">(리뷰 1,204개)</span>
    </div>
    <a href="/products/P001" class="buy-link">구매하기</a>
  </li>
  <li class="product-card" data-rank="2" data-product-id="P002">
    <div class="rank-badge">2</div>
    <div class="brand">이니스프리</div>
    <h3 class="product-name">수분크림 그린티 씨드 세럼</h3>
    <div class="price-area">
      <span class="original-price">25,000원</span>
      <span class="sale-price">19,900원</span>
      <span class="discount-rate">20%</span>
    </div>
    <div class="rating-area">
      <span class="stars">★★★★★</span>
      <span class="review-count">(리뷰 3,891개)</span>
    </div>
    <a href="/products/P002" class="buy-link">구매하기</a>
  </li>
  <li class="product-card" data-rank="3" data-product-id="P003">
    <div class="rank-badge">3</div>
    <div class="brand">설화수</div>
    <h3 class="product-name">자음 생크림 50ml 리미티드</h3>
    <div class="price-area">
      <span class="original-price">120,000원</span>
      <span class="sale-price">96,000원</span>
      <span class="discount-rate">20%</span>
    </div>
    <div class="rating-area">
      <span class="stars">★★★★★</span>
      <span class="review-count">(리뷰 572개)</span>
    </div>
    <a href="/products/P003" class="buy-link">구매하기</a>
  </li>
</ol>
\"\"\"

soup = BeautifulSoup(html_shopping, 'html.parser')

# ─── 데이터 추출 ─────────────────────────────────────────

rows = []
cards = soup.select('li.product-card')

for card in cards:
    # data-rank 속성 (el['속성'] 방식)
    rank = card.get('data-rank')
    pid  = card.get('data-product-id')

    # 브랜드 (.brand의 태그 이름은?)
    brand_el = card.select_one('.brand')
    brand    = brand_el.text.strip() if brand_el else None
    print(f"[탐색] brand_el.name = '{brand_el.name}'")  # 태그 이름 확인!

    # 상품명
    name_el = card.select_one('.product-name')
    name    = name_el.text.strip() if name_el else None

    # 가격 (여러 span 중 sale-price만)
    sale_el = card.select_one('.sale-price')
    sale    = sale_el.text.strip() if sale_el else None

    # 할인율
    disc_el = card.select_one('.discount-rate')
    disc    = disc_el.text.strip() if disc_el else '0%'

    # 리뷰수 (괄호와 '리뷰' 제거: '(리뷰 1,204개)' → '1204')
    review_el = card.select_one('.review-count')
    if review_el:
        import re
        nums = re.sub(r'[^0-9]', '', review_el.text)  # 숫자만
        review_cnt = int(nums) if nums else 0
    else:
        review_cnt = 0

    # 링크 (.get('href') — 안전한 방법)
    link_el = card.select_one('.buy-link')
    href    = link_el.get('href') if link_el else None

    rows.append({
        '순위': rank, '상품ID': pid, '브랜드': brand,
        '상품명': name, '할인가': sale, '할인율': disc,
        '리뷰수': review_cnt, '링크': href,
    })

df = pd.DataFrame(rows)
print()
print(df.to_string(index=False))
""", "conf-26"),

md("""## ✅ 이 노트북에서 배운 것 최종 정리

```python
# 헷갈리는 것들 한눈에 보기

el.name                 # 태그 이름: 'div', 'span', 'a' ...
el.text.strip()         # 텍스트 (가장 많이 씀)
el.get_text(strip=True) # 텍스트 (공백 옵션)
el.string               # 자식 하나일 때만, 아니면 None

el['href']              # 속성값 (없으면 KeyError!)
el.get('href')          # 속성값 (없으면 None, 안전)
el.get('href', '기본값') # 속성값 (없으면 기본값)

el['class']             # class 속성 (리스트로 반환!)
el.get('class', [])     # class 속성 (없으면 빈 리스트)

soup.find('태그')        # 하나 (태그/id/class로)
soup.select_one('선택자') # 하나 (CSS 선택자로) ← 주로 이걸 씀
soup.find_all('태그')    # 전부 (리스트)
soup.select('선택자')    # 전부 (CSS 선택자) ← 주로 이걸 씀

el.parent               # 부모 태그
el.find_next_sibling('태그') # 다음 형제 태그
```
""", "conf-27"),
]

save_nb(nb(nb_conf_cells), os.path.join(NB, '02_헷갈리는개념_완전정복.ipynb'))


# ══════════════════════════════════════════════════════════════
#  NOTEBOOK: 실전 다양한 사이트
# ══════════════════════════════════════════════════════════════

nb_diverse_cells = [

md("""# 🛒 실전 — 다양한 사이트 크롤링 연습

> **이 노트북에서 연습할 데이터 유형**
> 1. 🛍️ 쇼핑몰 상품 (로컬 HTML / books.toscrape.com)
> 2. 🔄 중고거래 (로컬 HTML 연습 후 → Selenium으로 실제 당근마켓)
> 3. 💬 텍스트/리뷰 데이터 (quotes.toscrape.com)
> 4. 💼 채용공고 (saramin.co.kr)
> 5. 📊 수집 데이터 합치기 & 저장

> ⚠️ 로컬 HTML 연습용 파일이 `data/` 폴더에 있습니다.
> VS Code에서 폴더를 열 때 `크롤링/` 폴더 자체를 열어야 상대경로가 맞아요!
""", "div-01"),

# ────────────────────────────────────────────────────
md("""---
## Part 1. 🛍️ 쇼핑몰 — 로컬 HTML 파일로 연습

**왜 로컬 파일로?**
- 실제 쇼핑몰(올리브영, 무신사 등)은 봇 차단/JS 렌더링으로 막힘
- 같은 HTML 구조를 `data/mock_shopping.html`로 미리 저장해뒀어요
- 네트워크 없이도 연습 가능!

**HTML 구조 미리보기:**
```html
<ol class="product-list">
  <li class="product-card" data-rank="1" data-product-id="P001">
    <div class="rank-badge">1</div>
    <div class="brand">라네즈</div>
    <h3 class="product-name">네오 쿠션 파운데이션</h3>
    <div class="price-area">
      <span class="original-price">38,000원</span>
      <span class="sale-price">27,000원</span>
      <span class="discount-rate">29%</span>
    </div>
    <div class="rating-area">
      <span class="stars">★★★★☆</span>
      <span class="review-count">(리뷰 1,204개)</span>
    </div>
    <a href="/products/P001" class="buy-link">구매하기</a>
  </li>
  ...
</ol>
```
""", "div-02"),

code("""from bs4 import BeautifulSoup
import pandas as pd
import re
import os

# 로컬 HTML 파일 읽기
# (VS Code에서 '크롤링' 폴더를 열었을 때의 상대경로)
html_path = os.path.join('data', 'mock_shopping.html')

with open(html_path, encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
print(f"파일 로드 완료! HTML 크기: {len(html_content):,} 글자")
print(f"페이지 제목: {soup.find('title').text}")
""", "div-03"),

code("""# 쇼핑몰 데이터 추출

cards = soup.select('li.product-card')
print(f"상품 수: {len(cards)}개")

rows = []
for card in cards:
    # data-* 속성으로 순위와 상품ID 가져오기
    rank = card.get('data-rank')
    pid  = card.get('data-product-id')

    # 브랜드, 상품명
    brand = card.select_one('.brand')
    brand = brand.text.strip() if brand else None

    name  = card.select_one('.product-name')
    name  = name.text.strip() if name else None

    # 가격 (여러 span이 있으니 정확한 클래스로 골라야 함)
    original = card.select_one('.original-price')
    sale     = card.select_one('.sale-price')
    discount = card.select_one('.discount-rate')

    original = original.text.strip() if original else None
    sale     = sale.text.strip() if sale else None
    discount = discount.text.strip() if discount else '0%'

    # 리뷰수 — '(리뷰 1,204개)' 에서 숫자만 추출
    review = card.select_one('.review-count')
    if review:
        review_num = int(re.sub(r'[^0-9]', '', review.text) or 0)
    else:
        review_num = 0

    # 구매 링크
    link = card.select_one('.buy-link')
    href = link.get('href') if link else None

    rows.append({
        '순위': int(rank) if rank else None,
        '상품ID': pid,
        '브랜드': brand,
        '상품명': name,
        '정가': original,
        '할인가': sale,
        '할인율': discount,
        '리뷰수': review_num,
        '링크': href,
    })

df_shop = pd.DataFrame(rows)
print(df_shop.to_string(index=False))
""", "div-04"),

code("""# 가격 문자열 → 숫자로 변환해서 분석

def price_to_int(price_str):
    \"\"\"'27,000원' → 27000\"\"\"
    if not price_str:
        return None
    nums = re.sub(r'[^0-9]', '', price_str)
    return int(nums) if nums else None

df_shop['할인가_숫자'] = df_shop['할인가'].apply(price_to_int)
df_shop['정가_숫자']  = df_shop['정가'].apply(price_to_int)
df_shop['할인금액']   = df_shop['정가_숫자'] - df_shop['할인가_숫자']

print("=== 가격 분석 ===")
print(f"평균 할인가: {df_shop['할인가_숫자'].mean():,.0f}원")
print(f"최고 할인금액: {df_shop['할인금액'].max():,.0f}원")
print()
print(df_shop[['브랜드','상품명','정가_숫자','할인가_숫자','할인금액','리뷰수']].to_string(index=False))
""", "div-05"),

# ────────────────────────────────────────────────────
md("""---
## Part 2. 🔄 중고거래 — 로컬 HTML로 당근마켓 스타일 연습

**실제 당근마켓 / 번개장터는?**
- JavaScript 렌더링 → BeautifulSoup으로 빈 결과 나옴
- Selenium이 필요 (다음 수업에서!)

**지금은:** 실제와 동일한 HTML 구조를 로컬 파일로 연습합니다.

**HTML 구조 미리보기:**
```html
<li class="article-item" data-id="1001" data-category="디지털">
  <a href="/articles/1001" class="article-link">
    <h3 class="title">아이폰 15 프로 256GB</h3>
    <p class="price">1,200,000원</p>
    <span class="location">서울 강남구</span>
    <span class="time-ago">10분 전</span>
    <span class="badge status-sale">판매중</span>
    <span class="like-count">23</span>
  </a>
</li>
```
""", "div-06"),

code("""# 중고거래 HTML 로드

html_path2 = os.path.join('data', 'mock_used_market.html')
with open(html_path2, encoding='utf-8') as f:
    html_used = f.read()

soup2 = BeautifulSoup(html_used, 'html.parser')
print(f"페이지 제목: {soup2.find('title').text}")

articles = soup2.select('li.article-item')
print(f"매물 수: {len(articles)}개")
""", "div-07"),

code("""# 중고거래 데이터 추출

rows_used = []
for article in articles:
    # data-* 속성
    article_id = article.get('data-id')
    category   = article.get('data-category')

    # 제목, 가격
    title_el = article.select_one('.title')
    price_el = article.select_one('.price')

    title = title_el.text.strip() if title_el else None
    price = price_el.text.strip() if price_el else None

    # 지역, 시간
    location_el = article.select_one('.location')
    time_el     = article.select_one('.time-ago')

    location = location_el.text.strip() if location_el else None
    time_ago  = time_el.text.strip()    if time_el     else None

    # 상태 (판매중/예약중/판매완료)
    badge = article.select_one('.badge[class*="status-"]')
    if badge:
        classes = badge.get('class', [])
        # status-sale, status-reserved, status-sold 중 하나
        status_class = [c for c in classes if c.startswith('status-')]
        status_map = {
            'status-sale':     '판매중',
            'status-reserved': '예약중',
            'status-sold':     '판매완료',
        }
        status = status_map.get(status_class[0] if status_class else '', '알수없음')
    else:
        status = None

    # 가격제안 가능 여부
    nego = bool(article.select_one('.badge.nego'))

    # 좋아요 수
    like_el = article.select_one('.like-count')
    like_cnt = int(like_el.text.strip()) if like_el else 0

    # 링크
    link_el = article.select_one('a.article-link')
    href    = link_el.get('href') if link_el else None

    rows_used.append({
        'ID': article_id, '카테고리': category, '제목': title,
        '가격': price, '지역': location, '등록시간': time_ago,
        '상태': status, '가격제안': nego, '좋아요': like_cnt, '링크': href,
    })

df_used = pd.DataFrame(rows_used)
print(df_used[['카테고리','제목','가격','지역','상태','좋아요']].to_string(index=False))
""", "div-08"),

code("""# 중고거래 데이터 분석

print("=== 카테고리별 현황 ===")
print(df_used.groupby('카테고리').agg(
    매물수=('ID', 'count'),
    평균좋아요=('좋아요', 'mean')
).round(1).to_string())

print()
print("=== 판매중인 매물만 ===")
on_sale = df_used[df_used['상태'] == '판매중']
on_sale['가격_숫자'] = on_sale['가격'].apply(price_to_int)
print(on_sale[['카테고리','제목','가격','좋아요']].to_string(index=False))

print()
print(f"=== 가격제안 가능 매물: {df_used['가격제안'].sum()}개 ===")
print(df_used[df_used['가격제안']][['제목','가격']].to_string(index=False))
""", "div-09"),

# ────────────────────────────────────────────────────
md("""---
## Part 3. 💬 텍스트/리뷰 데이터 — quotes.toscrape.com

리뷰, 댓글, 명언 같은 **텍스트 중심 데이터** 수집 연습입니다.
이 사이트는 크롤링 연습용으로 만들어져서 항상 동작합니다!

**HTML 구조:**
```html
<div class="quote">
  <span class="text">"The world as we have created it..."</span>
  <small class="author">Albert Einstein</small>
  <div class="tags">
    <a class="tag">change</a>
    <a class="tag">deep-thoughts</a>
  </div>
</div>
```
""", "div-10"),

code("""import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
}

# 1페이지 수집
url = 'http://quotes.toscrape.com/'
response = requests.get(url, headers=HEADERS)
response.encoding = 'utf-8'
print(f"상태 코드: {response.status_code}")

soup3 = BeautifulSoup(response.text, 'html.parser')
quotes = soup3.select('div.quote')
print(f"명언 수: {len(quotes)}개")
""", "div-11"),

code("""# 명언 데이터 추출

def extract_quotes(soup_obj):
    rows = []
    for q in soup_obj.select('div.quote'):
        # 명언 텍스트 (앞뒤 " " 기호 포함되어 있음)
        text_el  = q.select_one('span.text')
        text     = text_el.text.strip() if text_el else None

        # 저자
        author_el = q.select_one('small.author')
        author    = author_el.text.strip() if author_el else None

        # 저자 상세 링크
        author_link = q.select_one('a')
        author_href = author_link.get('href') if author_link else None

        # 태그들 (여러 개)
        tags = [t.text.strip() for t in q.select('a.tag')]
        tags_str = ', '.join(tags)

        rows.append({
            '명언': text,
            '저자': author,
            '저자링크': author_href,
            '태그': tags_str,
            '태그수': len(tags),
        })
    return rows

all_quotes = extract_quotes(soup3)
df_quotes = pd.DataFrame(all_quotes)
print(df_quotes[['저자','명언','태그']].to_string(index=False))
""", "div-12"),

code("""# 여러 페이지 수집 (자동 다음 페이지 감지)

all_quotes = []
page = 1

while page <= 5:
    url = f'http://quotes.toscrape.com/page/{page}/'
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        break

    soup_p = BeautifulSoup(response.text, 'html.parser')
    page_quotes = extract_quotes(soup_p)

    if not page_quotes:
        print(f"  {page}페이지에 데이터 없음, 종료")
        break

    all_quotes.extend(page_quotes)
    print(f"  {page}페이지: {len(page_quotes)}개 (누적: {len(all_quotes)}개)")

    # 다음 페이지 버튼이 있는지 확인
    next_btn = soup_p.select_one('li.next a')
    if not next_btn:
        print("  마지막 페이지 도달!")
        break

    page += 1
    time.sleep(1)

df_quotes_all = pd.DataFrame(all_quotes)
print(f"\\n총 {len(df_quotes_all)}개 수집!")
""", "div-13"),

code("""# 텍스트 데이터 분석

print("=== 저자별 명언 수 ===")
print(df_quotes_all['저자'].value_counts().head(5).to_string())

print()
print("=== 태그 순위 (전체 태그 중) ===")
all_tags = []
for tags_str in df_quotes_all['태그'].dropna():
    all_tags.extend([t.strip() for t in tags_str.split(',')])

import collections
tag_counter = collections.Counter(all_tags)
for tag, count in tag_counter.most_common(10):
    print(f"  {tag:20}: {count}회")
""", "div-14"),

# ────────────────────────────────────────────────────
md("""---
## Part 4. 💼 채용공고 — 여러 키워드 + 분석

사람인에서 **여러 직무 키워드**를 한번에 수집하고 비교해봅니다.
""", "div-15"),

code("""import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
}

def crawl_saramin_simple(keyword, max_page=2):
    results = []
    for page in range(1, max_page + 1):
        url = (f'https://www.saramin.co.kr/zf_user/search/recruit'
               f'?searchType=search&searchword={keyword}&recruitPage={page}')
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            jobs = soup.select('div.item_recruit')

            for job in jobs:
                co = job.select_one('strong.corp_name a')
                ti = job.select_one('h2.job_tit a')
                conds = [c.text.strip() for c in job.select('div.job_condition span')]

                results.append({
                    '키워드': keyword,
                    '회사명': co.text.strip() if co else None,
                    '공고제목': ti.text.strip() if ti else None,
                    '지역': conds[0] if len(conds) > 0 else None,
                    '경력': conds[1] if len(conds) > 1 else None,
                    '학력': conds[2] if len(conds) > 2 else None,
                })

            print(f"  [{keyword}] {page}p → {len(jobs)}건")
            time.sleep(1)

        except Exception as e:
            print(f"  [{keyword}] {page}p 오류: {e}")
            break

    return results


# 직무 키워드 4종
keywords = ['데이터분석', '파이썬개발', 'UX디자인', '디지털마케팅']
all_jobs = []

for kw in keywords:
    jobs = crawl_saramin_simple(kw, max_page=2)
    all_jobs.extend(jobs)
    time.sleep(2)

df_jobs = pd.DataFrame(all_jobs)
print(f"\\n총 {len(df_jobs)}건 수집 완료!")
""", "div-16"),

code("""# 직무별 비교 분석

print("=== 직무별 공고 수 ===")
print(df_jobs['키워드'].value_counts().to_string())

print()
print("=== 지역별 공고 수 (상위 10) ===")
print(df_jobs['지역'].value_counts().head(10).to_string())

print()
print("=== 직무별 경력 조건 분포 ===")
pivot = df_jobs.groupby(['키워드', '경력']).size().unstack(fill_value=0)
# 경력무관, 신입, 신입·경력만 보기
entry_cols = [c for c in pivot.columns if c in ['경력무관', '신입', '신입·경력']]
if entry_cols:
    print(pivot[entry_cols].to_string())
""", "div-17"),

# ────────────────────────────────────────────────────
md("""---
## Part 5. 📚 books.toscrape.com — 카테고리별 수집

실제 온라인 서점처럼, **카테고리 별로** 데이터를 나눠서 수집합니다.
""", "div-18"),

code("""import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE_URL = 'http://books.toscrape.com'

# 카테고리 목록 가져오기
response = requests.get(BASE_URL, headers=HEADERS)
response.encoding = 'utf-8'
soup_main = BeautifulSoup(response.text, 'html.parser')

# 왼쪽 사이드바의 카테고리 링크들
category_links = soup_main.select('ul.nav-list li ul li a')
categories = []
for link in category_links[:8]:  # 8개만 (시간 절약)
    name = link.text.strip()
    href = link.get('href')
    categories.append({'이름': name, 'href': href})

print(f"발견된 카테고리: {len(category_links)}개 (상위 8개만 수집)")
for c in categories:
    print(f"  - {c['이름']}: {c['href']}")
""", "div-19"),

code("""# 카테고리별 수집

rating_map = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5}
all_books = []

for cat in categories:
    cat_url = BASE_URL + '/' + cat['href']
    resp = requests.get(cat_url, headers=HEADERS)
    resp.encoding = 'utf-8'
    soup_cat = BeautifulSoup(resp.text, 'html.parser')

    books = soup_cat.select('article.product_pod')
    for book in books:
        title_el  = book.select_one('h3 a')
        price_el  = book.select_one('p.price_color')
        rating_el = book.select_one('p.star-rating')

        title  = title_el['title'] if title_el else None
        price  = price_el.text.strip() if price_el else None
        rating = rating_map.get(
            rating_el['class'][1] if rating_el else '', 0
        )

        all_books.append({
            '카테고리': cat['이름'],
            '제목': title,
            '가격': price,
            '평점': rating,
        })

    print(f"  [{cat['이름']}] {len(books)}권")
    time.sleep(0.8)

df_books = pd.DataFrame(all_books)
print(f"\\n총 {len(df_books)}권 수집!")
""", "div-20"),

code("""# 카테고리별 분석

df_books['가격_숫자'] = (df_books['가격']
    .str.replace('£','').str.strip()
    .pipe(pd.to_numeric, errors='coerce'))

print("=== 카테고리별 평균 가격 & 평균 평점 ===")
analysis = df_books.groupby('카테고리').agg(
    책수=('제목','count'),
    평균가격=('가격_숫자','mean'),
    평균평점=('평점','mean')
).round(2).sort_values('평균평점', ascending=False)
print(analysis.to_string())

print()
print("=== 카테고리별 5점 책 수 ===")
five_star = df_books[df_books['평점']==5].groupby('카테고리').size()
print(five_star.sort_values(ascending=False).to_string())
""", "div-21"),

# ────────────────────────────────────────────────────
md("""---
## Part 6. 💾 전체 데이터 합치기 & 저장

지금까지 수집한 데이터를 각각 CSV로 저장합니다.
""", "div-22"),

code("""import os

save_dir = os.path.join('data', 'results')
os.makedirs(save_dir, exist_ok=True)

# 각 데이터 저장
files = {
    '쇼핑몰_베스트.csv': df_shop,
    '중고거래_매물.csv': df_used,
    '명언_수집.csv': df_quotes_all,
    '채용공고_다직무.csv': df_jobs,
    '도서_카테고리별.csv': df_books,
}

for fname, df in files.items():
    path = os.path.join(save_dir, fname)
    df.to_csv(path, index=False, encoding='utf-8-sig')
    print(f"  ✅ {fname}: {len(df)}행 저장")

print(f"\\n모두 {save_dir} 에 저장됐습니다!")
""", "div-23"),

# ────────────────────────────────────────────────────
md("""---
## 🎯 연습문제

### 문제 1 — 중고거래 (기초)
`data/mock_used_market.html`에서
- '서울' 지역 매물만 필터링하세요
- 좋아요 순으로 정렬하세요

### 문제 2 — 쇼핑몰 (응용)
`data/mock_shopping.html`에서
- 할인율이 20% 이상인 상품만 수집하세요
- 리뷰수가 1000개 이상인 상품은 '인기상품' 컬럼을 True로 표시하세요

### 문제 3 — 텍스트 (응용)
`quotes.toscrape.com`에서 전체 페이지를 수집하여
- 'love' 태그가 달린 명언만 모아서 출력하세요
- 가장 많이 인용된 저자 Top 3를 찾으세요

### 문제 4 — 채용공고 (실전)
사람인에서 '머신러닝' 키워드로 2페이지를 수집하고
- 제목에 'Python' 또는 '파이썬'이 들어간 공고만 필터링하세요
- 경력 조건별로 몇 건인지 집계하세요

<details>
<summary>문제 1 정답 보기</summary>

```python
# 서울 지역 필터링 + 좋아요 정렬
seoul = df_used[df_used['지역'].str.startswith('서울', na=False)]
seoul_sorted = seoul.sort_values('좋아요', ascending=False)
print(seoul_sorted[['제목','가격','지역','좋아요']].to_string(index=False))
```
</details>

<details>
<summary>문제 2 정답 보기</summary>

```python
# 할인율 숫자 변환
df_shop['할인율_숫자'] = df_shop['할인율'].str.replace('%','').astype(int)

# 20% 이상 필터
result = df_shop[df_shop['할인율_숫자'] >= 20].copy()

# 인기상품 컬럼 추가
result['인기상품'] = result['리뷰수'] >= 1000
print(result[['브랜드','상품명','할인율','리뷰수','인기상품']].to_string(index=False))
```
</details>
""", "div-24"),
]

save_nb(nb(nb_diverse_cells), os.path.join(NB, '03_실전_다양한사이트크롤링.ipynb'))


# ══════════════════════════════════════════════════════════════
#  MARKDOWN: BeautifulSoup 강의자료 (수강생용 완전판)
# ══════════════════════════════════════════════════════════════

md_student = """# 🍜 BeautifulSoup 완벽 가이드 (수강생용)

> 이 자료는 **처음 크롤링을 배우는 분**을 위해 작성했습니다.
> "왜?" 라는 질문에 모두 답하려고 노력했어요.
> 노트북과 함께 보면서 막히는 부분이 있으면 여기서 찾아보세요!

---

## 📌 목차

1. [HTML이 뭔가요?](#html)
2. [BeautifulSoup은 어떻게 동작하나요?](#bs4)
3. [요소 찾기 4가지 방법](#find)
4. [텍스트 꺼내기](#text)
5. [속성값 꺼내기](#attr)
6. [헷갈리는 것들 완전 정리](#confusing)
7. [에러가 났을 때 해결법](#error)
8. [CSS 선택자 치트시트](#css)
9. [실전 패턴 모음](#pattern)
10. [연습문제](#quiz)

---

<a name="html"></a>
## 1. HTML이 뭔가요?

웹페이지를 "소스 보기"(Ctrl+U)로 열어보면 이런 게 보입니다:

```html
<div class="product-card">
    <h3 class="product-name">립밤 촉촉이</h3>
    <p class="price">12,000원</p>
    <a href="/buy/101" class="buy-btn">구매하기</a>
</div>
```

**HTML 용어 설명:**

```
<div class="product-card">
 ↑    ↑         ↑
 │    태그이름   속성(attribute)
 │              class="product-card" → 이름표 같은 것
 여는 태그

</div>
 ↑
 닫는 태그

<태그이름 속성이름="속성값"> 내용 </태그이름>
```

**자주 나오는 태그들:**

| 태그 | 역할 | 예시 |
|------|------|------|
| `<div>` | 구역 나누기 | 상품 카드 묶음 |
| `<span>` | 인라인 텍스트 | 가격, 태그 |
| `<p>` | 문단 텍스트 | 상품 설명 |
| `<a>` | 링크 | href 속성에 URL |
| `<ul>` / `<li>` | 목록 | 상품 리스트 |
| `<h1>~<h6>` | 제목 | 크기 순서대로 |
| `<img>` | 이미지 | src 속성에 이미지 URL |

**class vs id:**
```
class="product-card"  → 여러 요소가 같은 클래스 가질 수 있음 (반복)
id="header"           → 페이지에서 딱 하나만 있어야 함 (유일)
```

---

<a name="bs4"></a>
## 2. BeautifulSoup은 어떻게 동작하나요?

```
[인터넷]
   ↓  requests.get(url) 로 HTML 받기
[HTML 문자열]
   ↓  BeautifulSoup(html, 'html.parser') 로 파싱
[BeautifulSoup 객체]
   ↓  select(), find() 로 원하는 부분 찾기
[Tag 객체]
   ↓  .text, ['href'] 로 데이터 꺼내기
[데이터]
   ↓  DataFrame으로 정리 + CSV 저장
```

```python
import requests
from bs4 import BeautifulSoup

# 1단계: HTML 받기
response = requests.get('http://example.com',
                        headers={'User-Agent': 'Mozilla/5.0'})
response.encoding = 'utf-8'  # 한글 깨짐 방지

# 2단계: 파싱 (HTML을 파이썬이 이해하는 구조로 변환)
soup = BeautifulSoup(response.text, 'html.parser')
# soup은 이제 HTML을 트리 구조로 가지고 있는 객체

# 3단계: 원하는 데이터 찾기
product = soup.select_one('.product-card')
```

---

<a name="find"></a>
## 3. 요소 찾기 4가지 방법

### ① `soup.find()` — 첫 번째 하나만

```python
soup.find('div')                        # div 태그 첫 번째
soup.find('div', class_='product')      # class="product"인 div 첫 번째
soup.find('a', id='main-link')          # id="main-link"인 a 첫 번째
```

> **왜 `class_`에 언더바가 붙나요?**
> `class`는 파이썬 예약어(클래스 선언할 때 쓰는 단어)라서
> BeautifulSoup에서는 `class_`로 씁니다.

### ② `soup.find_all()` — 전부 다 (리스트 반환)

```python
soup.find_all('li')                     # 모든 li 태그
soup.find_all('li', class_='item')      # class="item"인 모든 li
soup.find_all(['h1','h2','h3'])         # h1, h2, h3 모두
```

### ③ `soup.select_one()` — CSS 선택자로 하나만 ⭐

```python
soup.select_one('.product-name')        # class="product-name" 첫 번째
soup.select_one('#header')              # id="header"
soup.select_one('div.card')             # div이면서 class="card"
soup.select_one('div > p')              # div 바로 아래 p
```

### ④ `soup.select()` — CSS 선택자로 전부 (리스트 반환) ⭐

```python
soup.select('.product-name')            # class="product-name" 전부
soup.select('li.item')                  # li이면서 class="item"
soup.select('a[href]')                  # href 속성 있는 a 전부
soup.select('a[href*="product"]')       # href에 "product" 포함된 a
```

### 비교 정리

| 함수 | 결과 개수 | 선택자 방식 | 주로 쓸 때 |
|------|---------|-----------|----------|
| `find()` | 하나 | 태그/클래스/ID | 가끔 |
| `find_all()` | 전부 | 태그/클래스/ID | 가끔 |
| `select_one()` | 하나 | CSS 선택자 | **자주** |
| `select()` | 전부 | CSS 선택자 | **자주** |

---

<a name="text"></a>
## 4. 텍스트 꺼내기

### `.text` — 가장 많이 씀

```python
element = soup.select_one('.product-name')
print(element.text)         # '  립밤 촉촉이  '  ← 공백 포함될 수 있음
print(element.text.strip()) # '립밤 촉촉이'       ← 앞뒤 공백 제거 ✅
```

### `.text` vs `.string` vs `.get_text()` 차이

```html
<p class="price">38,000원</p>  → 자식 태그 없음
```
→ 셋 다 같은 결과: `'38,000원'`

```html
<div class="info">
  <span class="brand">라네즈</span>
  <span class="name">수분크림</span>
</div>
```
```python
div = soup.select_one('.info')
div.text      # '\n  라네즈\n  수분크림\n'  (전체 합치기)
div.string    # None ← 자식이 여러 개라 None!
div.get_text(strip=True, separator=' | ')  # '라네즈 | 수분크림'
```

**결론:** 대부분 `.text.strip()` 하나면 충분합니다.
세부 컬럼은 개별 요소를 `select_one()`으로 찾아서 각각 `.text.strip()` 하세요.

---

<a name="attr"></a>
## 5. 속성값 꺼내기

```html
<a href="/products/101" class="buy-btn" data-id="101">구매하기</a>
```

```python
a_tag = soup.select_one('a.buy-btn')

# ❌ 위험한 방법 (속성이 없으면 KeyError 에러!)
a_tag['href']     # '/products/101'
a_tag['class']    # ['buy-btn'] ← 리스트로 반환!
a_tag['data-id']  # '101'

# ✅ 안전한 방법 (없으면 None 반환)
a_tag.get('href')          # '/products/101'
a_tag.get('class')         # ['buy-btn']
a_tag.get('존재안함')      # None
a_tag.get('존재안함', '')  # '' (기본값 지정)
```

> **`class`는 왜 리스트로 나오나요?**
> HTML에서 `class="btn primary active"`처럼 여러 클래스가 올 수 있어서
> BeautifulSoup은 항상 리스트로 반환합니다.
> 특정 클래스가 있는지 확인: `'btn' in el.get('class', [])`

---

<a name="confusing"></a>
## 6. 헷갈리는 것들 완전 정리

### 🔴 가장 많이 혼동하는 것: `el.name` vs `select('.name')`

```python
el.name
# → 이 태그가 어떤 태그인지 (div? span? a?)
# → 'div', 'span', 'a', 'li', 'p' 등을 반환

soup.select('.name')
# → class="name"인 요소들을 찾는 것
# → .name 은 CSS 선택자의 일부 (class 이름)
```

```python
# 예시
span_el = soup.select_one('.product-name')  # class="product-name"인 요소 찾기
print(span_el.name)        # → 'span' (그 요소의 태그 종류)
print(span_el.text)        # → '립밤 촉촉이' (그 요소의 텍스트)

# el.name의 실제 활용
for el in soup.find_all(['h1','h2','h3']):
    print(f"[{el.name}] {el.text.strip()}")  # [h1] 제목, [h2] 소제목 ...
```

### 🟡 `find()` vs `select_one()` — 거의 같지만

```python
# 이 두 줄은 같은 결과
soup.find('div', class_='card')
soup.select_one('div.card')

# select_one()이 더 표현력이 좋음
soup.select_one('div.card.featured')      # 두 클래스 동시
soup.select_one('div.card > h3')          # 직접 자식만
soup.select_one('a[href*="product"]')     # 속성 조건
# → find()로는 이런 복합 조건이 어색함
```

### 🟢 `find_all()` vs `select()` — 거의 같지만

```python
# 이 두 줄은 같은 결과 (리스트 반환)
soup.find_all('li', class_='item')
soup.select('li.item')

# select()가 더 CSS 친화적
soup.select('li.item.active')     # 복합 클래스
soup.select('ul > li')            # 직접 자식
```

### 🔵 class 관련 세 가지

```python
el['class']              # 이 요소의 class 속성 값 (리스트)
el.get('class', [])      # 위와 같지만 없어도 안전
soup.select('.클래스명') # class가 '클래스명'인 요소 찾기 (탐색!)
```

```python
# 예시
div = soup.select_one('.card')
div['class']              # ['card'] 또는 ['card', 'featured', ...]
div.get('class', [])      # 동일, 없어도 빈 리스트 반환
'featured' in div.get('class', [])  # True/False: 특정 클래스 있는지 확인

# 찾기용
soup.select('.card')      # class="card"가 있는 요소들 찾기 (전혀 다른 용도!)
```

### 🟤 `['href']` vs `.get('href')`

```python
el['href']       # 있으면 값, 없으면 KeyError 에러!
el.get('href')   # 있으면 값, 없으면 None (안전)

# 실전에서는 항상 .get() 사용 권장
href = link.get('href')
if href:
    full_url = 'https://사이트.com' + href
```

---

<a name="error"></a>
## 7. 에러가 났을 때 해결법

### 에러 1: `AttributeError: 'NoneType' object has no attribute 'text'`

```python
# 원인: 요소를 못 찾아서 None이 반환됐는데 .text를 호출함
name = soup.select_one('.name').text  # ← .name이 없으면 None.text → 에러!

# 해결: 항상 if 체크
name_el = soup.select_one('.name')
name = name_el.text.strip() if name_el else None  # ← 이렇게!
```

### 에러 2: 결과가 빈 리스트 `[]`

```python
items = soup.select('.product-item')
print(items)  # [] ← 왜 비어있지?
```

**원인 체크:**
1. 선택자가 틀렸음 → F12로 실제 클래스 확인
2. JS 렌더링 사이트 → Selenium 필요
3. `response.text` 대신 `response.content` 써봄

```python
# 디버깅 방법
print(response.status_code)    # 200인지?
print(response.text[:500])     # HTML에 원하는 내용이 있는지?
# Ctrl+U 로 본 소스와 response.text 비교!
```

### 에러 3: `403 Forbidden`

```python
# 원인: User-Agent 없어서 봇으로 인식
response = requests.get(url)  # ← User-Agent 없음

# 해결: headers 추가
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)
```

### 에러 4: 한글 깨짐

```python
print(response.text)  # ← 한글이 ??? 로 보임

# 해결
response.encoding = 'utf-8'    # 현대 사이트
response.encoding = 'euc-kr'   # 오래된 한국 사이트
print(response.text)  # ← 이제 한글 정상 출력
```

### 에러 5: `KeyError: 'class'` 또는 `KeyError: 'href'`

```python
el['class']  # 이 요소에 class 속성이 없으면 에러!
el['href']   # 이 요소에 href 속성이 없으면 에러!

# 해결: .get() 사용
el.get('class', [])   # 없으면 빈 리스트
el.get('href')        # 없으면 None
```

---

<a name="css"></a>
## 8. CSS 선택자 치트시트

크롤링에서 가장 중요한 스킬이에요. 이것만 외우면 됩니다!

```
선택자                예시                       의미
─────────────────────────────────────────────────────────
태그                   div                        모든 div
.클래스                .product-name              class="product-name"인 것들
#아이디                #header                    id="header"인 것
태그.클래스            li.item                    li이면서 class="item"
태그#아이디            div#main                   div이면서 id="main"

.클래스1.클래스2       .item.active               두 클래스 모두 가진 것
부모 > 자식            ul > li                    ul 바로 아래 li
조상 후손              div a                      div 안의 모든 a

[속성]                 a[href]                    href 속성이 있는 a
[속성="값"]            a[href="/home"]             href="/home"인 a
[속성*="포함"]         a[href*="product"]         href에 "product" 포함
[속성^="시작"]         a[href^="https"]           href가 https로 시작
[속성$="끝"]           img[src$=".jpg"]           src가 .jpg로 끝나는 img
```

**개발자도구에서 선택자 찾는 법:**
```
1. F12 → Elements 탭
2. Ctrl+Shift+C (또는 상단 커서 아이콘)
3. 원하는 요소 클릭
4. 강조된 태그에서 우클릭 → Copy → Copy selector
5. 복사된 값을 select_one() 안에 넣기
```

---

<a name="pattern"></a>
## 9. 실전 패턴 모음

### 패턴 1: 기본 수집 루프

```python
items = soup.select('li.product-item')  # 반복되는 요소들

rows = []
for item in items:
    name_el  = item.select_one('.name')
    price_el = item.select_one('.price')

    rows.append({
        '이름': name_el.text.strip()  if name_el  else None,
        '가격': price_el.text.strip() if price_el else None,
    })

df = pd.DataFrame(rows)
```

### 패턴 2: 여러 페이지 수집

```python
all_rows = []

for page in range(1, 11):  # 1~10페이지
    url = f'https://사이트.com/list?page={page}'
    response = requests.get(url, headers=headers, timeout=15)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        print(f"{page}페이지 오류, 중단")
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('.item')

    if not items:           # 데이터 없으면 마지막 페이지
        print("마지막 페이지!")
        break

    for item in items:
        all_rows.append({...})

    print(f"{page}페이지 {len(items)}개 수집")
    time.sleep(1)           # ← 절대 빠뜨리지 마세요!
```

### 패턴 3: 상대경로 → 절대경로 변환

```python
# href="/products/101" 처럼 상대경로로 오는 경우
BASE_URL = 'https://www.shopping.co.kr'

link_el = item.select_one('a.detail')
href = link_el.get('href')  # '/products/101'

if href and href.startswith('/'):
    full_url = BASE_URL + href   # 'https://www.shopping.co.kr/products/101'
elif href and href.startswith('http'):
    full_url = href              # 이미 절대경로
else:
    full_url = None
```

### 패턴 4: 가격 문자열 → 숫자 변환

```python
import re

def price_to_int(price_str):
    if not price_str:
        return None
    # '1,200,000원' → '1200000' → 1200000
    nums = re.sub(r'[^0-9]', '', price_str)
    return int(nums) if nums else None

df['가격_숫자'] = df['가격'].apply(price_to_int)
```

### 패턴 5: data-* 속성 활용

```html
<li class="item" data-id="1001" data-category="디지털">
```

```python
item = soup.select_one('li.item')
item_id  = item.get('data-id')       # '1001'
category = item.get('data-category') # '디지털'
```

### 패턴 6: CSV 저장 (한글 깨짐 방지)

```python
df.to_csv('결과.csv', index=False, encoding='utf-8-sig')
# utf-8-sig: 엑셀에서 열 때 한글 안 깨지는 인코딩

# 불러올 때
df = pd.read_csv('결과.csv', encoding='utf-8-sig')
```

---

<a name="quiz"></a>
## 10. 스스로 확인하는 퀴즈

아래 질문에 답할 수 있으면 BeautifulSoup 기초 완성입니다!

**Q1.** `soup.select_one('.price').text`에서 에러가 날 수 있는 이유는?
<details><summary>정답</summary>
`.price` 클래스를 가진 요소가 없으면 `select_one()`이 `None`을 반환하고,
`None.text`를 호출하면 `AttributeError`가 납니다.
항상 `el.text if el else None` 패턴을 써야 합니다.
</details>

**Q2.** `el['class']`와 `soup.select('.class명')`은 어떻게 다른가요?
<details><summary>정답</summary>
`el['class']`는 이미 찾은 요소 `el`의 class 속성값(리스트)을 가져오는 것입니다.
`soup.select('.class명')`은 class가 'class명'인 요소들을 새로 탐색하는 것입니다.
용도가 완전히 다릅니다.
</details>

**Q3.** `el.name`이 반환하는 것은?
<details><summary>정답</summary>
태그의 종류입니다. `div`이면 `'div'`, `span`이면 `'span'`, `a`이면 `'a'`를 반환합니다.
클래스나 ID와는 무관합니다.
</details>

**Q4.** `<a href="/list">` 에서 href 값을 안전하게 가져오는 방법은?
<details><summary>정답</summary>
`link.get('href')`를 사용합니다.
`link['href']`는 href가 없을 때 KeyError가 나지만,
`.get('href')`는 없으면 None을 반환해서 안전합니다.
</details>

**Q5.** 1초 대기(`time.sleep(1)`)를 반드시 넣어야 하는 이유는?
<details><summary>정답</summary>
너무 빠르게 반복 요청을 보내면 서버에 부담을 주고, 사이트 운영자가 우리 IP를
차단(429 Too Many Requests)할 수 있습니다.
크롤링 윤리이자 실용적인 이유 모두에서 필수입니다.
</details>
"""

save_text(md_student, os.path.join(DOCS, '01_BeautifulSoup_강의자료_수강생용.md'))


# ── 완료 ─────────────────────────────────────────────────────

print()
print("="*55)
print("✅ v2 자료 생성 완료!")
print("="*55)
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ['__pycache__','.claude','results']]
    level = root.replace(BASE,'').count(os.sep)
    indent = '  '*level
    folder = os.path.basename(root)
    if level > 0:
        print(f"{indent}📂 {folder}/")
    for fname in sorted(files):
        if fname.endswith(('.py','.pyc')):
            continue
        size = os.path.getsize(os.path.join(root,fname))
        print(f"{'  '*(level+1)}📄 {fname} ({size:,}B)")
