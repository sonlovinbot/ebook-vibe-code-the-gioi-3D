"""Build a local responsive HTML reader from the editable ebook Markdown files."""
from pathlib import Path
from html import escape
import re
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

ROOT = Path(__file__).parent
CHAPTERS = sorted(ROOT.glob('chuong-[0-9][0-9]-*.md'))
APPENDICES = [ROOT/'phu-luc-a-thuat-ngu.md', ROOT/'phu-luc-b-bo-mau-prompt.md']
OUT = ROOT/'ebook-reader.html'
md = MarkdownIt('commonmark', {'html': False}).enable('table').enable('strikethrough')

def render_file(path):
    raw = path.read_text(encoding='utf-8')
    title = re.search(r'^# (.+)$', raw, re.M).group(1)
    html = md.render(raw)
    soup = BeautifulSoup(html, 'html.parser')
    # Existing Markdown image + following italic caption become one semantic figure.
    for img in list(soup.select('p > img')):
        para = img.parent
        if para.name != 'p' or len(para.contents) != 1:
            continue
        fig = soup.new_tag('figure')
        img.extract(); fig.append(img)
        nxt = para.find_next_sibling()
        if nxt and nxt.name == 'p' and nxt.find('em') and len(nxt.contents) == 1:
            caption = soup.new_tag('figcaption')
            caption.string = re.sub(r'\s+([,.;:!?])', r'\1', nxt.get_text(' ', strip=True))
            fig.append(caption); nxt.decompose()
        para.replace_with(fig)
    # Some source images are linked in prose rather than embedded. Show them below that prose.
    for a in list(soup.select('a[href]')):
        href = a.get('href','')
        if not re.search(r'\.(png|jpe?g|webp)$', href, re.I) or href.startswith('http'):
            continue
        para = a.find_parent('p')
        if not para: continue
        fig = soup.new_tag('figure'); fig['class'] = 'linked-figure'
        im = soup.new_tag('img', src=href, alt=a.get_text(' ',strip=True), loading='lazy')
        fig.append(im)
        caption = soup.new_tag('figcaption'); caption.string = a.get_text(' ',strip=True)
        fig.append(caption)
        para.insert_after(fig)
    # A standalone YouTube link becomes a responsive player with a plain-link fallback.
    for a in list(soup.select('p > a[href]')):
        href = a.get('href', '')
        match = re.fullmatch(r'https?://(?:youtu\.be/|(?:www\.)?youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})(?:[&?].*)?', href)
        para = a.parent
        if not match or para.name != 'p' or len(para.contents) != 1:
            continue
        label = a.get_text(' ', strip=True)
        fig = soup.new_tag('figure')
        fig['class'] = 'video-figure'
        frame = soup.new_tag('div')
        frame['class'] = 'video-frame'
        player = soup.new_tag('iframe')
        player['src'] = f'https://www.youtube-nocookie.com/embed/{match.group(1)}'
        player['title'] = label
        player['loading'] = 'lazy'
        player['allow'] = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'
        player['allowfullscreen'] = ''
        frame.append(player)
        fig.append(frame)
        caption = soup.new_tag('figcaption')
        caption.append(label + ' · ')
        fallback = soup.new_tag('a', href=href)
        fallback.string = 'Mở trên YouTube'
        fallback['target'] = '_blank'
        fallback['rel'] = 'noopener noreferrer'
        caption.append(fallback)
        fig.append(caption)
        para.replace_with(fig)
    for img in soup.select('img'):
        img['loading'] = 'lazy'
        img['decoding'] = 'async'
        img['tabindex'] = '0'
        img['role'] = 'button'
        img['aria-label'] = 'Phóng to hình: ' + img.get('alt', 'minh họa')
    for a in soup.select('a[href]'):
        if a['href'].startswith('http'):
            a['target']='_blank';a['rel']='noopener noreferrer'
    return title, str(soup)

entries=[]
for i,path in enumerate(CHAPTERS,1):
    title,body=render_file(path)
    entries.append((f'chap-{i:02d}',f'{i:02d}',title,body))
for i,path in enumerate(APPENDICES):
    title,body=render_file(path)
    entries.append((f'appendix-{i+1}',f'P{i+1}',title,body))

nav='\n'.join(f'<button class="toc-link" type="button" data-target="{id_}"><span class="toc-num">{num}</span><span>{escape(title.split(" — ",1)[-1])}</span></button>' for id_,num,title,_ in entries)
premium_nav=''.join(f'<button class="toc-link locked" type="button" disabled aria-label="{escape(label)} — Sắp ra mắt"><span class="toc-num">🔒</span><span>{escape(label)}<small>COMING SOON</small></span></button>' for label in [
    'Blender · Hoàn thiện asset 3D',
    'Animation · Chuyển động tự nhiên',
    'Game nhiều màn · AI quái',
    'Database · Đăng nhập · Lưu game',
    'PWA · Chơi offline',
    'Mobile launch · Đưa game lên điện thoại',
    'Game giáo dục · Gamification',
    'Thương mại hóa · Analytics',
    'Landing page GLB tương tác',
])
sections='\n'.join(f'<section class="book-section" id="{id_}" data-title="{escape(title)}"><div class="chapter-kicker">{("CHƯƠNG "+num) if num.isdigit() else "PHỤ LỤC"} <span>·</span> COACHIO ACADEMY</div><div class="prose">{body}</div><div class="chapter-end"><span>Hết {escape(title.split(" — ",1)[0].lower())}</span><button class="next-chapter" type="button">Đọc tiếp <span aria-hidden="true">→</span></button></div></section>' for id_,num,title,body in entries)

TEMPLATE=r'''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Làm chủ Vibe Code 3D · Bản đọc thử</title>
<script>try{if(localStorage.getItem('ebookColorTheme')==='dark')document.documentElement.dataset.theme='dark'}catch{}</script>
<style>
:root{--navy:#1b3a6b;--ink:#263544;--muted:#66747a;--teal:#3c8b87;--orange:#e87722;--line:#dce2e0;--paper:#fffdf9;--bg:#f1f3f0;--font-size:18px;--measure:780px;--image-scale:100%;font-family:Arial,Helvetica,sans-serif;color:var(--ink);background:var(--bg);color-scheme:light}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;min-width:320px;overflow-x:hidden}button,input{font:inherit}button{cursor:pointer}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid var(--orange);outline-offset:3px}a{color:var(--navy);text-underline-offset:3px}.app{min-height:100dvh}
.topbar{height:70px;position:sticky;top:0;z-index:20;background:rgba(255,253,249,.96);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:18px;padding:0 28px;box-shadow:0 2px 16px rgba(28,47,56,.035)}.brand{display:flex;align-items:center;gap:10px;white-space:nowrap;font-size:15px;font-weight:800;letter-spacing:.06em;color:var(--navy)}.brand-icon{width:36px;height:36px;display:grid;place-items:center;border-radius:10px;background:var(--navy);color:#fff;font-size:15px;letter-spacing:0}.top-title{font-size:13px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0;flex:1}.top-actions{display:flex;align-items:center;gap:8px}.ghost{border:1px solid var(--line);background:#fff;border-radius:10px;color:var(--ink);padding:9px 12px;font-size:13px;font-weight:700}.ghost:hover,.toc-link:hover{background:#eef5f2}.menu-btn{display:none}.progress-track{height:3px;background:#e9eeeb;position:absolute;inset:auto 0 0}.progress-fill{height:100%;background:var(--teal);width:0;transition:width .16s}
.layout{display:grid;grid-template-columns:282px minmax(0,1fr) 244px;max-width:1800px;margin:auto}.sidebar{align-self:start;position:sticky;top:70px;height:calc(100dvh - 70px);overflow:auto;background:#f9faf8;border-right:1px solid var(--line);padding:28px 15px}.sidebar-label,.panel-label{font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#81918e;font-weight:800;margin:5px 12px 20px}.toc-link{display:flex;align-items:flex-start;gap:12px;width:100%;border:0;background:transparent;border-radius:10px;text-align:left;padding:10px 11px;color:#46535c;font-size:13px;line-height:1.36}.toc-link.active{background:#e9f2ee;color:var(--navy);font-weight:700}.toc-num{flex:none;font-family:Arial,sans-serif;color:var(--teal);font-weight:800;font-size:12px;padding-top:1px}.sidebar-bottom{border-top:1px solid var(--line);margin:24px 10px 0;padding-top:18px;color:#85918c;font-size:12px;line-height:1.5}.reader-wrap{min-width:0;padding:44px clamp(20px,5vw,74px) 88px}.paper{background:var(--paper);border:1px solid #e5e7e1;border-radius:6px;box-shadow:0 18px 55px rgba(36,48,48,.045);margin:0 auto;max-width:calc(var(--measure) + 104px);min-height:70vh;padding:clamp(28px,5vw,52px)}.book-section{display:none}.book-section.active{display:block}.chapter-kicker{color:var(--teal);font-size:12px;font-weight:800;letter-spacing:.16em;margin:3px 0 24px}.chapter-kicker span{padding:0 7px;color:#b7c3be}.prose{font-size:var(--font-size);line-height:1.72;max-width:var(--measure);margin:auto;overflow-wrap:anywhere}.prose h1{font-size:clamp(32px,calc(var(--font-size)*2.25),48px);line-height:1.13;color:var(--navy);letter-spacing:-.04em;margin:0 0 28px}.prose h2{font-size:calc(var(--font-size)*1.38);line-height:1.22;color:var(--navy);letter-spacing:-.02em;margin:46px 0 15px;padding-top:10px}.prose h3{font-size:calc(var(--font-size)*1.13);color:var(--navy);margin:32px 0 10px}.prose p{margin:0 0 18px}.prose strong{color:#203b4e}.prose ul,.prose ol{padding-left:1.25em;margin:10px 0 24px}.prose li{padding-left:.15em;margin:7px 0}.prose li::marker{color:var(--teal)}.prose blockquote{border-left:4px solid var(--teal);background:#f0f6f3;padding:17px 22px;margin:26px 0;color:#355a5a;border-radius:0 8px 8px 0}.prose blockquote p:last-child{margin-bottom:0}.prose pre{white-space:pre-wrap;overflow-x:auto;padding:18px 20px;background:#f0f3f2;border:1px solid #e3e9e6;border-radius:9px;font-size:calc(var(--font-size)*.75);line-height:1.55;margin:24px 0}.prose code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#edf1ef;padding:.1em .3em;border-radius:4px;font-size:.88em}.prose pre code{background:none;padding:0}.prose table{border-collapse:collapse;width:100%;font-size:calc(var(--font-size)*.82);line-height:1.5;margin:25px 0 31px}.prose th{text-align:left;background:#eaf2ef;color:#214b54}.prose th,.prose td{border:1px solid #d8e1dd;padding:11px 12px;vertical-align:top}.prose tr:nth-child(even) td{background:#fafbf8}.prose figure{margin:34px auto;max-width:var(--image-scale)}.prose figure img{display:block;width:100%;max-height:630px;object-fit:contain;border:1px solid #e2e8e4;background:#f7f8f6;border-radius:9px}.prose figcaption{font-size:calc(var(--font-size)*.75);line-height:1.45;color:var(--muted);margin-top:10px}.prose .linked-figure{max-width:min(var(--image-scale),540px)}.prose .linked-figure img{max-height:620px}.prose hr{border:0;border-top:1px solid var(--line);margin:38px 0}.chapter-end{border-top:1px solid var(--line);margin-top:52px;padding-top:22px;display:flex;align-items:center;justify-content:space-between;gap:18px;font-size:13px;color:#85918c}.next-chapter,.start-btn{border:0;background:var(--navy);color:#fff;border-radius:10px;padding:12px 17px;font-size:14px;font-weight:700}.next-chapter:hover,.start-btn:hover{background:#31588b}
.settings{align-self:start;position:sticky;top:70px;height:calc(100dvh - 70px);padding:30px 22px;border-left:1px solid var(--line);color:var(--muted)}.setting{margin:0 0 26px}.setting-head{display:flex;justify-content:space-between;gap:5px;color:var(--ink);font-size:13px;font-weight:700;margin-bottom:11px}.setting output{color:var(--teal);font-variant-numeric:tabular-nums}.setting input[type=range]{width:100%;accent-color:var(--teal)}.hint{font-size:12px;line-height:1.55;color:#86928e;margin:25px 0}.reset-btn{width:100%;border:1px solid var(--line);background:#fff;border-radius:9px;padding:10px 13px;font-size:12px;font-weight:700;color:var(--navy)}.reset-btn:hover{background:#f3f7f4}.settings-sep{border-top:1px solid var(--line);margin:27px 0}.stat{font-size:12px;line-height:1.6;color:#71817d}.stat strong{display:block;color:var(--navy);font-size:16px;margin-bottom:4px}
.cover{display:none}.cover.active{display:block}.cover-inner{display:grid;grid-template-columns:minmax(0,1fr) minmax(200px,310px);gap:35px;align-items:center;min-height:520px}.cover-tag{color:var(--teal);font-size:13px;font-weight:800;letter-spacing:.17em}.cover h1{font-size:clamp(48px,6vw,86px);letter-spacing:-.075em;line-height:.98;color:var(--navy);margin:22px 0 24px}.cover h1 span{display:block;color:var(--teal)}.cover-sub{font-size:21px;line-height:1.4;color:#405664;max-width:480px}.cover-author{font-size:14px;color:#66747a;margin:30px 0}.cover-photo{max-width:100%;max-height:515px;object-fit:contain;filter:drop-shadow(0 16px 18px rgba(21,32,48,.14))}.cover-notes{display:flex;gap:24px;border-top:1px solid var(--line);padding-top:21px;margin-top:16px;color:#6e807e;font-size:12px}.cover-notes strong{display:block;font-size:20px;color:var(--navy);margin-bottom:4px}
.mobile-toc{display:none}.mobile-toc.open{display:block}.mobile-controls{display:none}.mobile-panel{display:none}
@media(max-width:1250px){.layout{grid-template-columns:250px minmax(0,1fr)}.settings{display:none}.mobile-controls{display:flex;gap:8px}.topbar{padding:0 18px}.reader-wrap{padding:30px 26px 60px}}
@media(max-width:760px){.topbar{height:61px;padding:0 12px;gap:9px}.brand{font-size:12px;gap:7px}.brand-icon{width:32px;height:32px;font-size:12px}.top-title{display:none}.top-actions{margin-left:auto}.top-actions .ghost.print{display:none}.top-actions .ghost{font-size:12px;padding:8px 9px}.menu-btn{display:block}.layout{display:block}.sidebar{display:none}.sidebar.open{display:block;position:fixed;z-index:30;top:61px;left:0;bottom:0;width:min(330px,90vw);height:auto;box-shadow:8px 0 25px rgba(0,0,0,.12)}.reader-wrap{padding:15px 10px 44px}.paper{padding:23px 18px;box-shadow:none;max-width:100%;border-radius:4px}.chapter-kicker{font-size:10px;margin-bottom:17px}.prose{line-height:1.67}.prose h1{font-size:calc(var(--font-size)*1.75)}.prose h2{font-size:calc(var(--font-size)*1.25);margin-top:34px}.prose table{display:block;overflow-x:auto;white-space:normal}.prose th,.prose td{min-width:140px;padding:9px}.cover-inner{display:block;min-height:0}.cover h1{font-size:52px}.cover-sub{font-size:18px}.cover-photo{display:block;max-height:360px;margin:28px auto}.cover-notes{gap:15px}.mobile-panel{display:none;position:fixed;z-index:31;right:10px;top:69px;background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 16px 35px rgba(0,0,0,.14);padding:19px;width:min(310px,calc(100vw - 20px))}.mobile-panel.open{display:block}.mobile-panel .setting{margin-bottom:17px}}
@media print{.topbar,.sidebar,.settings,.chapter-end,.mobile-panel{display:none!important}.layout{display:block}.reader-wrap{padding:0}.paper{border:0;box-shadow:none;padding:0;max-width:none}.book-section{display:block!important;break-before:page}.cover{display:block!important;break-after:page}.prose{max-width:none;font-size:11pt}.prose figure{break-inside:avoid}.prose h2{break-after:avoid}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{scroll-behavior:auto!important;transition:none!important}}
.prose img{cursor:zoom-in}.prose img:focus-visible{outline:3px solid var(--orange);outline-offset:4px}.prose table img{display:block;width:100%;min-width:130px;max-width:180px;aspect-ratio:2/3;object-fit:contain;margin:auto;background:#fff}.prose .video-figure{max-width:100%}.video-frame{position:relative;width:100%;aspect-ratio:16/9;background:#142039;border-radius:10px;overflow:hidden}.video-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}.image-dialog{border:0;border-radius:16px;padding:0;background:#fff;max-width:min(96vw,1560px);max-height:95dvh;box-shadow:0 30px 90px rgba(0,0,0,.34)}.image-dialog::backdrop{background:rgba(6,17,30,.82)}.image-dialog-inner{padding:16px;max-height:95dvh;display:flex;flex-direction:column}.image-dialog-top{display:flex;justify-content:flex-end;margin-bottom:8px}.image-dialog-close{border:0;background:#e8f1ef;border-radius:9px;padding:9px 14px;font-weight:800;color:#17384e}.image-dialog img{display:block;max-width:100%;max-height:calc(95dvh - 115px);object-fit:contain;margin:auto}.image-dialog p{font:14px/1.5 Arial,Helvetica,sans-serif;color:#4f616a;margin:11px 3px 2px}@media print{.image-dialog{display:none!important}}
.layout{grid-template-columns:282px minmax(0,1fr);max-width:1460px}#settingsBtn{display:none}.sidebar .premium-label{margin:28px 12px 10px;padding-top:18px;border-top:1px solid var(--line);font-size:11px;letter-spacing:.12em;font-weight:800;color:#9a7d60}.toc-link.locked{cursor:not-allowed;opacity:.67}.toc-link.locked:hover{background:transparent}.toc-link.locked small{display:block;margin-top:4px;font-size:10px;letter-spacing:.08em;color:#af876a}.free-badge{display:inline-flex;align-items:center;border-radius:999px;background:#eaf2ef;color:#26746f;padding:4px 9px;font-size:10px;font-weight:800;letter-spacing:.08em}@media(max-width:1250px) and (min-width:761px){.layout{grid-template-columns:250px minmax(0,1fr)}}@media(max-width:760px){#settingsBtn{display:inline-flex}}

/* Sidebar course banner */
.bootcamp-banner{display:block;margin:24px 8px 6px;overflow:hidden;border:1px solid #b79b4d;border-radius:12px;background:#101a2c;color:#f6f4fb;text-decoration:none;box-shadow:0 6px 20px rgba(12,22,40,.12)}
.bootcamp-banner img{display:block;width:100%;height:auto}.bootcamp-copy{display:block;padding:15px}.bootcamp-label{display:block;color:#efd271;font-size:10px;font-weight:800;letter-spacing:.08em;line-height:1.5}.bootcamp-copy strong{display:block;color:#fff;font-size:17px;line-height:1.35;margin:8px 0}.bootcamp-sub{display:block;font-size:11px;line-height:1.5;color:#b9c6d9}.bootcamp-cta{display:flex;justify-content:space-between;align-items:center;gap:8px;background:#f5cd47;color:#172136;border-radius:7px;margin-top:14px;padding:10px 11px;font-size:12px;font-weight:800;line-height:1.4}.bootcamp-banner:hover{border-color:#f5cd47;box-shadow:0 8px 24px rgba(12,22,40,.22)}.bootcamp-banner:focus-visible{outline:3px solid #44b9ae;outline-offset:4px}
</style>
<style>
.theme-toggle{display:inline-flex;align-items:center;justify-content:center;gap:7px;min-width:76px}.theme-icon{font-size:17px;line-height:1}.theme-text{font-size:12px}
:root[data-theme="dark"]{--navy:#b9d3ff;--ink:#e2eaf3;--muted:#a8b8c8;--teal:#76dfd1;--orange:#ffb36f;--line:#34465e;--paper:#121f32;--bg:#0b1423;color-scheme:dark}
:root[data-theme="dark"] .topbar{background:#0b1423;box-shadow:0 3px 20px rgba(0,0,0,.23)}
:root[data-theme="dark"] .brand-icon{background:#35547e;color:#fff}
:root[data-theme="dark"] .ghost,:root[data-theme="dark"] .reset-btn{background:#1a2a40;color:var(--ink);border-color:var(--line)}
:root[data-theme="dark"] .ghost:hover,:root[data-theme="dark"] .reset-btn:hover,:root[data-theme="dark"] .toc-link:hover{background:#213a4b}
:root[data-theme="dark"] .progress-track{background:#233449}
:root[data-theme="dark"] .sidebar{background:#0e1b2c;border-color:var(--line)}
:root[data-theme="dark"] .toc-link{color:#c0cfdd}
:root[data-theme="dark"] .toc-link.active{background:#214054;color:#e7f7f8}
:root[data-theme="dark"] .toc-num{color:var(--teal)}
:root[data-theme="dark"] .sidebar-label,:root[data-theme="dark"] .panel-label,:root[data-theme="dark"] .sidebar-bottom{color:#9daec0}
:root[data-theme="dark"] .paper{border-color:#2b3c51;box-shadow:0 22px 55px rgba(0,0,0,.18)}
:root[data-theme="dark"] .prose strong{color:#f4f8fd}
:root[data-theme="dark"] .prose blockquote{background:#1c3740;color:#dcf3ef;border-color:var(--teal)}
:root[data-theme="dark"] .prose pre{background:#0c192b;border-color:var(--line);color:#dce9f5}
:root[data-theme="dark"] .prose code{background:#24364b;color:#dce9f5}
:root[data-theme="dark"] .prose pre code{background:transparent}
:root[data-theme="dark"] .prose th{background:#20384b;color:#ecf8f8}
:root[data-theme="dark"] .prose th,:root[data-theme="dark"] .prose td{border-color:var(--line)}
:root[data-theme="dark"] .prose tr:nth-child(even) td{background:#18283d}
:root[data-theme="dark"] .prose figure img,:root[data-theme="dark"] .prose table img{border-color:var(--line);background:#17263b}
:root[data-theme="dark"] .chapter-end,:root[data-theme="dark"] .cover-notes,:root[data-theme="dark"] .cover-author{color:var(--muted)}
:root[data-theme="dark"] .cover-sub{color:#c4d5e4}
:root[data-theme="dark"] .next-chapter,:root[data-theme="dark"] .start-btn{background:#416ca0;color:#fff}
:root[data-theme="dark"] .next-chapter:hover,:root[data-theme="dark"] .start-btn:hover{background:#527eb5}
:root[data-theme="dark"] .mobile-panel{background:#16263a;border-color:var(--line)}
:root[data-theme="dark"] .image-dialog{background:#14243a;color:var(--ink)}
:root[data-theme="dark"] .image-dialog-close{background:#29485a;color:#e5f7f6}
:root[data-theme="dark"] .image-dialog p{color:var(--muted)}
:root[data-theme="dark"] .toc-link.locked:hover{background:transparent}
:root[data-theme="dark"] .free-badge{background:#244439;color:#a7eee3}
@media(max-width:760px){.theme-toggle{min-width:33px;padding:8px}.theme-text{display:none}}
@media(max-width:420px){.brand>span:last-child{display:none}}
@media print{:root[data-theme="dark"]{--navy:#1b3a6b;--ink:#263544;--muted:#66747a;--teal:#3c8b87;--line:#dce2e0;--paper:#fff;--bg:#fff;color-scheme:light}:root[data-theme="dark"] .paper{background:#fff;border:0;box-shadow:none}:root[data-theme="dark"] .prose strong{color:#203b4e}:root[data-theme="dark"] .prose pre,:root[data-theme="dark"] .prose blockquote,:root[data-theme="dark"] .prose th,:root[data-theme="dark"] .prose tr:nth-child(even) td{background:#f0f3f2;color:#263544}:root[data-theme="dark"] .prose code{background:#edf1ef;color:#263544}:root[data-theme="dark"] .prose figure img{background:#fff}}
</style>
</head>
<body><div class="app">
<header class="topbar"><button id="menuBtn" class="ghost menu-btn" type="button" aria-label="Mở mục lục">☰</button><div class="brand"><span class="brand-icon">3D</span><span>COACHIO · EBOOK</span></div><div class="top-title" id="topTitle">Bản đọc thử</div><div class="top-actions"><button class="ghost" id="coverBtn" type="button">Bìa</button><button class="ghost theme-toggle" id="themeBtn" type="button" aria-pressed="false" aria-label="Bật chế độ tối" title="Chuyển chế độ sáng/tối"><span class="theme-icon" aria-hidden="true">☾</span><span class="theme-text">Tối</span></button><button class="ghost" id="settingsBtn" type="button" aria-label="Điều chỉnh kích thước">Aa</button><button class="ghost print" id="printBtn" type="button">In / PDF</button></div><div class="progress-track"><div class="progress-fill" id="progressFill"></div></div></header>
<div class="layout"><aside class="sidebar" id="sidebar"><div class="sidebar-label">BẢN FREE · 11 CHƯƠNG</div><button class="toc-link" type="button" data-target="cover"><span class="toc-num">◎</span><span>Trang bìa</span></button>__NAV__<a class="bootcamp-banner" href="https://academy.coachio.ai/funnels/ai-marketing-bootcamp-2026" target="_blank" rel="noopener noreferrer" aria-label="Tìm hiểu AI Marketing Bootcamp 2026 tại Coachio Academy, mở trong tab mới"><img src="ebook-assets/promo/coachio-bootcamp-2026.png" alt="Khóa E-Learning và Ebook 3D nâng cao của Coachio Academy" loading="lazy" decoding="async"><span class="bootcamp-copy"><span class="bootcamp-label">HỌC TIẾP CÙNG COACHIO</span><strong>E-Learning + Ebook 3D nâng cao</strong><span class="bootcamp-sub">AI Marketing Bootcamp 2026</span><span class="bootcamp-cta">Khám phá chương trình <span aria-hidden="true">↗</span></span></span></a><div class="premium-label">BẢN NÂNG CẤP <span class="free-badge">SẮP RA MẮT</span></div>__PREMIUM_NAV__<div class="sidebar-bottom">Bản thảo nội dung · 25.09.2026<br>Đặng Hữu Sơn và Nhóm cộng sự Coachio Academy</div></aside>
<main class="reader-wrap"><div class="paper"><section class="cover" id="cover"><div class="cover-inner"><div><div class="cover-tag">CẨM NANG THỰC HÀNH CÙNG AI · BẢN FREE</div><h1>LÀM CHỦ <span>VIBE CODE 3D</span></h1><p class="cover-sub">Từ ý tưởng đến Web, App, Game & Animation</p><p class="cover-author">Đặng Hữu Sơn và Nhóm cộng sự Coachio Academy</p><button class="start-btn" type="button" data-target="chap-01">Bắt đầu đọc <span aria-hidden="true">→</span></button></div><img class="cover-photo" src="ebook-assets/book-cover-reference.png" alt="Ảnh bìa tham khảo của ebook Vibe Code 3D"></div><div class="cover-notes"><div><strong>11</strong>chương thực hành</div><div><strong>02</strong>phụ lục dùng ngay</div><div><strong>AI + 3D</strong>cho người mới</div></div></section>__SECTIONS__</div></main>
</div>
<div class="mobile-panel" id="mobilePanel"><div class="panel-label">Điều chỉnh kích thước</div><div class="setting"><div class="setting-head"><label for="mFontSize">Cỡ chữ</label><output id="mFontValue">18px</output></div><input id="mFontSize" type="range" min="15" max="24" value="18"></div><div class="setting"><div class="setting-head"><label for="mPageWidth">Độ rộng trang</label><output id="mWidthValue">780px</output></div><input id="mPageWidth" type="range" min="620" max="1000" step="20" value="780"></div><div class="setting"><div class="setting-head"><label for="mImageSize">Kích thước hình</label><output id="mImageValue">100%</output></div><input id="mImageSize" type="range" min="60" max="100" step="5" value="100"></div><button class="reset-btn" type="button" id="mResetBtn">Khôi phục mặc định</button></div>
<dialog class="image-dialog" id="imageDialog"><div class="image-dialog-inner"><div class="image-dialog-top"><button class="image-dialog-close" id="imageClose" type="button">Đóng ✕</button></div><img id="imageZoom" alt=""><p id="imageCaption"></p></div></dialog>
</div><script>
const ids=['cover',__IDS__];let current='cover';const root=document.documentElement;
let theme=root.dataset.theme==='dark'?'dark':'light';
function applyTheme(){const dark=theme==='dark';root.dataset.theme=theme;const btn=document.getElementById('themeBtn');btn.setAttribute('aria-pressed',String(dark));btn.setAttribute('aria-label',dark?'Bật chế độ sáng':'Bật chế độ tối');btn.querySelector('.theme-icon').textContent=dark?'☀':'☾';btn.querySelector('.theme-text').textContent=dark?'Sáng':'Tối';try{localStorage.setItem('ebookColorTheme',theme)}catch{}}
const defaults={font:18,width:780,image:100};let prefs={...defaults};try{prefs={...prefs,...JSON.parse(localStorage.getItem('ebookPreviewPrefs')||'{}')}}catch{}
function applyPrefs(){prefs.font=Math.max(15,Math.min(24,Number(prefs.font)||18));prefs.width=Math.max(620,Math.min(1000,Number(prefs.width)||780));prefs.image=Math.max(60,Math.min(100,Number(prefs.image)||100));root.style.setProperty('--font-size',prefs.font+'px');root.style.setProperty('--measure',prefs.width+'px');root.style.setProperty('--image-scale',prefs.image+'%');for(const [key,val] of [['mFontSize',prefs.font],['mPageWidth',prefs.width],['mImageSize',prefs.image]])document.getElementById(key).value=val;for(const [key,val] of [['mFontValue',prefs.font+'px'],['mWidthValue',prefs.width+'px'],['mImageValue',prefs.image+'%']])document.getElementById(key).textContent=val;localStorage.setItem('ebookPreviewPrefs',JSON.stringify(prefs))}
function show(id,push=true){if(!ids.includes(id))id='cover';current=id;document.querySelectorAll('.book-section,.cover').forEach(el=>el.classList.toggle('active',el.id===id));document.querySelectorAll('.toc-link').forEach(el=>el.classList.toggle('active',el.dataset.target===id));const title=id==='cover'?'Trang bìa':document.getElementById(id).dataset.title;document.getElementById('topTitle').textContent=title;document.title=title+' · Làm chủ Vibe Code 3D';document.getElementById('sidebar').classList.remove('open');document.getElementById('mobilePanel').classList.remove('open');if(push)history.replaceState(null,'','#'+id);window.scrollTo({top:0,behavior:'instant'});progress()}
function progress(){const selected=document.querySelector('.book-section.active');if(!selected){document.getElementById('progressFill').style.width='0%';return}const max=document.documentElement.scrollHeight-innerHeight;const within=max>0?scrollY/max:0;const idx=ids.indexOf(current);const pct=((idx-1+within)/(ids.length-1))*100;document.getElementById('progressFill').style.width=Math.max(0,Math.min(100,pct))+'%'}
function zoomImage(img){const dialog=document.getElementById('imageDialog');const figure=img.closest('figure');document.getElementById('imageZoom').src=img.src;document.getElementById('imageZoom').alt=img.alt;document.getElementById('imageCaption').textContent=figure?.querySelector('figcaption')?.textContent||img.alt;dialog.showModal()}
document.addEventListener('click',e=>{const img=e.target.closest('.prose img');if(img){zoomImage(img);return}const target=e.target.closest('[data-target]');if(target){show(target.dataset.target);return}if(e.target.closest('.next-chapter')){const i=ids.indexOf(current);show(ids[Math.min(ids.length-1,i+1)]);return}});
document.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.matches('.prose img')){e.preventDefault();zoomImage(e.target)}});
document.getElementById('imageClose').addEventListener('click',()=>document.getElementById('imageDialog').close());document.getElementById('imageDialog').addEventListener('click',e=>{if(e.target.id==='imageDialog')e.target.close()});
for(const [id,key] of [['mFontSize','font'],['mPageWidth','width'],['mImageSize','image']])document.getElementById(id).addEventListener('input',e=>{prefs[key]=Number(e.target.value);applyPrefs()});
for(const id of ['mResetBtn'])document.getElementById(id).addEventListener('click',()=>{prefs={...defaults};applyPrefs()});
document.getElementById('menuBtn').addEventListener('click',()=>{document.getElementById('sidebar').classList.toggle('open');document.getElementById('mobilePanel').classList.remove('open')});document.getElementById('settingsBtn').addEventListener('click',()=>{document.getElementById('mobilePanel').classList.toggle('open');document.getElementById('sidebar').classList.remove('open')});document.getElementById('themeBtn').addEventListener('click',()=>{theme=theme==='dark'?'light':'dark';applyTheme()});document.getElementById('coverBtn').addEventListener('click',()=>show('cover'));document.getElementById('printBtn').addEventListener('click',()=>print());window.addEventListener('hashchange',()=>show(location.hash.slice(1),false));window.addEventListener('scroll',progress,{passive:true});window.addEventListener('keydown',e=>{if(e.key==='Escape'){document.getElementById('sidebar').classList.remove('open');document.getElementById('mobilePanel').classList.remove('open')}});applyTheme();applyPrefs();show(location.hash.slice(1)||'cover',false);if('scrollRestoration' in history)history.scrollRestoration='manual';window.addEventListener('load',()=>{requestAnimationFrame(()=>window.scrollTo(0,0));setTimeout(()=>window.scrollTo(0,0),120)});
</script></body></html>'''
output=TEMPLATE.replace('__NAV__',nav).replace('__PREMIUM_NAV__',premium_nav).replace('__SECTIONS__',sections).replace('__IDS__',','.join(repr(e[0]) for e in entries))
OUT.write_text(output,encoding='utf-8')
print(f'Wrote {OUT} ({OUT.stat().st_size:,} bytes; {len(CHAPTERS)} chapters + {len(APPENDICES)} appendices)')
