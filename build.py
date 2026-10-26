"""items.json -> index.html (허브 페이지). 새 항목은 items.json 맨 뒤에 추가하고 이 파일을 실행한다.
화면에는 최신 번호가 맨 위. hidden=true 인 항목(비공개로 내린 영상)은 빼고, 번호는 다시 쓰지 않는다."""
import html
import json
from pathlib import Path

HERE = Path(__file__).parent
DISCLOSURE = "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."

items = [i for i in json.loads((HERE / "items.json").read_text(encoding="utf-8")) if not i.get("hidden")]
items.sort(key=lambda i: i["no"], reverse=True)
e = html.escape


def card(i):
    soldout = i.get("soldout")
    price = "품절" if soldout else f"{i['price']:,}원"
    return f"""    <li class="item" id="{i['no']}">
      <img src="{e(i['img'])}" alt="{e(i['short'])}" width="96" height="96" loading="lazy">
      <div class="body">
        <p class="no">#{i['no']}</p>
        <h2>{e(i['name'])}</h2>
        <p class="price">{price} <span>· {e(i['checked'])} 확인</span></p>
        <a class="buy" href="{e(i['link'])}" rel="sponsored noopener" target="_blank">쿠팡에서 보기</a>
        <span class="tag">파트너스 링크</span>
      </div>
    </li>"""


page = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>템슐랭 상품 모음</title>
<meta name="description" content="템슐랭 쇼츠에 나온 상품을 영상 번호로 찾는 곳">
<style>
:root{{--bg:#f6f5f2;--card:#fff;--ink:#1d1d1f;--sub:#6b6b70;--line:#e3e1dc;--accent:#d9480f;--accent-ink:#fff;--note:#fff4e6}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151515;--card:#1f1f21;--ink:#f2f2f2;--sub:#a3a3a8;--line:#2e2e31;--accent:#ff7a3d;--accent-ink:#151515;--note:#2a2118}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}}
main{{max-width:560px;margin:0 auto;padding:20px 16px 48px}}
h1{{font-size:22px;margin:4px 0 2px}}
.lead{{color:var(--sub);margin:0 0 14px;font-size:14px}}
.notice{{background:var(--note);border:1px solid var(--line);border-radius:10px;padding:10px 12px;font-size:13px;margin:0 0 18px}}
ul{{list-style:none;margin:0;padding:0;display:grid;gap:12px}}
.item{{display:flex;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;scroll-margin-top:16px}}
.item:target{{outline:2px solid var(--accent)}}
.item img{{width:96px;height:96px;border-radius:10px;object-fit:cover;flex:none;background:var(--line)}}
.body{{min-width:0}}
.no{{margin:0;font-weight:800;color:var(--accent);font-size:15px}}
h2{{font-size:15px;margin:2px 0 4px;line-height:1.35}}
.price{{margin:0 0 8px;font-weight:700}}
.price span{{font-weight:400;color:var(--sub);font-size:13px}}
.buy{{display:inline-block;background:var(--accent);color:var(--accent-ink);text-decoration:none;font-weight:700;padding:8px 14px;border-radius:999px;font-size:14px}}
.tag{{display:inline-block;margin-left:6px;color:var(--sub);font-size:12px}}
footer{{margin-top:28px;color:var(--sub);font-size:13px}}
footer a{{color:inherit}}
</style>
</head>
<body>
<main>
  <h1>템슐랭 상품 모음</h1>
  <p class="lead">쇼츠 화면의 #번호로 찾으세요. 가격은 확인한 날 기준이며 바뀔 수 있어요.</p>
  <p class="notice">{DISCLOSURE}</p>
  <ul>
{chr(10).join(card(i) for i in items)}
  </ul>
  <footer>유튜브 <a href="https://www.youtube.com/@temchelin_shop" rel="noopener">템슐랭</a></footer>
</main>
</body>
</html>
"""
(HERE / "index.html").write_text(page, encoding="utf-8")
print("built", len(items), "items")
