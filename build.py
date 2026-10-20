#!/usr/bin/env python3
"""Zero-dependency static site generator. Usage: SITE_URL=https://example.com python3 build.py"""
import json,os,shutil,html,sys
SITE=os.environ.get("SITE_URL","https://example.com").rstrip("/")
NAME=os.environ.get("SITE_NAME","Drama Vault")
E=html.escape
D=json.load(open("content/data.json",encoding="utf-8"))
OUT="dist"
shutil.rmtree(OUT,ignore_errors=True);os.makedirs(OUT)
shutil.copytree("static",OUT,dirs_exist_ok=True)
bc={b["slug"]:b for b in D["broadcasters"]}
pp={p["slug"]:p for p in D["people"]}
sitemap=[];errors=[]
import hashlib
PAL=[("#7a1f2b","#d9a441"),("#14403a","#d9a441"),("#1c2433","#e0a4ab"),("#5b3a1e","#f3e6c8"),("#3c2a5a","#d9a441")]
def wrap(t,n=14):
    w,l,o=t.split(),"",[]
    for x in w:
        if len(l)+len(x)+1>n and l:o.append(l);l=x
        else:l=(l+" "+x).strip()
    return o+[l]
def art(path,lines,sub,idx):
    a,b=PAL[idx%len(PAL)];os.makedirs(os.path.join(OUT,"img","covers"),exist_ok=True)
    t="".join(f'<text x="150" y="{95+i*34-(len(lines)-1)*14}" text-anchor="middle" font-family="Georgia,serif" font-size="28" fill="#faf6ef">{E(x)}</text>' for i,x in enumerate(lines))
    open(os.path.join(OUT,"img","covers",path+".svg"),"w",encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="300" height="200"><rect width="300" height="200" fill="{a}"/><rect x="10" y="10" width="280" height="180" fill="none" stroke="{b}" stroke-width="2"/>{t}<text x="150" y="178" text-anchor="middle" font-family="system-ui,sans-serif" font-size="15" fill="{b}">{E(sub)}</text></svg>')
def cover(slug,title,sub):
    art(slug,wrap(title),sub,int(hashlib.md5(slug.encode()).hexdigest(),16))
for _d in D["dramas"]:cover(_d["slug"],_d["title"],str(_d["year"]))
for _p in D["people"]:cover("person-"+_p["slug"],_p["name"].split(" (")[0],_p["role"])
def live(r):return r["status"]=="published"
for r in D["dramas"]+D["people"]:
    if live(r) and not r.get("sources"):errors.append(f"published record without sources: {r['slug']}")
if errors:sys.exit("BUILD FAILED:\n"+"\n".join(errors))
def write(path,content):
    p=os.path.join(OUT,path.strip("/"),"index.html") if not path.endswith((".html",".xml",".txt","_headers")) else os.path.join(OUT,path)
    os.makedirs(os.path.dirname(p),exist_ok=True);open(p,"w",encoding="utf-8").write(content)
def page(path,title,desc,body,index=True,crumbs=None,ld=None,extra=""):
    url=f"{SITE}{path}";ld=list(ld or [])
    if crumbs:
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+u} for i,(n,u) in enumerate([("Home","/")]+crumbs)]})
    cr=""
    if crumbs:cr='<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>'+"".join(f' › <a href="{u}">{E(n)}</a>' for n,u in crumbs[:-1])+f' › <span aria-current="page">{E(crumbs[-1][0])}</span></nav>'
    ldh="".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False).replace("</","<\\/")}</script>' for x in ld)
    robots="index,follow" if index else "noindex,follow"
    if index:sitemap.append(url)
    h=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | {E(NAME)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="{robots}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="{E(NAME)}"><meta name="twitter:card" content="summary">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css">{ldh}</head><body><a class="skip" href="#main">Skip to content</a>
<header><a class="brand" href="/"><img src="/img/logo.svg" alt="" width="36" height="36" style="vertical-align:middle;margin-right:8px">{E(NAME)}</a><nav aria-label="Primary"><a href="/dramas/">Archive</a><a href="/decades/">Decades</a><a href="/genres/">Genres</a><a href="/broadcasters/">Broadcasters</a><a href="/people/">People</a><a href="/articles/">Guides</a></nav></header>
<main id="main">{cr}{body}</main>
<footer><p>{E(NAME)} is an independent editorial site and is not affiliated with PTV or any other broadcaster. We do not host, stream or download episodes; we link to sources we have checked.</p>
<p><a href="/about/">About</a> · <a href="/contact/">Contact</a> · <a href="/editorial-policy/">Editorial policy</a> · <a href="/corrections/">Corrections</a> · <a href="/copyright/">Copyright &amp; takedown</a> · <a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/accessibility/">Accessibility</a> · <a href="/affiliate-disclosure/">Affiliate disclosure</a></p></footer>{extra}</body></html>'''
    write(path,h)
FIX='<p class="banner"><strong>Test fixture.</strong> This record has not been verified. Only the title is shown as a placeholder; no credits, synopsis or viewing links have been confirmed. It is excluded from the sitemap and marked noindex.</p>'
def card(d):
    return f'<li><a class="card" style="display:block;text-decoration:none;color:inherit" href="/dramas/{d["slug"]}/"><img src="/img/covers/{d["slug"]}.svg" alt="" width="300" height="200" loading="lazy"><h3>{E(d["title"])}</h3><p class="meta">{d["year"]} · {E(bc[d["broadcaster"]]["name"])}</p></a></li>'
def grid(ds):return '<ul class="grid">'+"".join(card(d) for d in ds)+'</ul>' if ds else '<p>No records yet.</p>'
dec=lambda d:d["year"]//10*10
# Drama pages
for d in D["dramas"]:
    ok=live(d);b=bc[d["broadcaster"]]
    rows=[("Title",d["title"]),("Original Urdu title",d["title_ur"] or "Unknown (not verified)"),("Year",d["year"]),("Broadcaster",b["name"]),("Genre",", ".join(d["genre"])),("Language",d["language"]),
          ("Writer",", ".join(d["writer"]) or "Unknown (not verified)"),("Director",", ".join(d["director"]) or "Unknown (not verified)"),("Cast",", ".join(d["cast"]) or "Unknown (not verified)"),("English subtitles","Not confirmed" if d["subtitles"]!="confirmed" else "Confirmed")]
    tbl="<table><caption>Key facts</caption><tbody>"+"".join(f"<tr><th scope='row'>{k}</th><td>{E(str(v))}</td></tr>" for k,v in rows)+"</tbody></table>"
    view="".join(f'<li><a href="{E(v["url"])}" rel="noopener nofollow" target="_blank">{E(v["label"])}</a> – {E(v["owner"])} (external site; verified {E(v["checked"])})</li>' for v in d["viewing"])
    view=f"<ul>{view}</ul>" if view else "<p>No authorized viewing source has been verified yet. We do not link to unverified uploads.</p>"
    src="".join(f'<li><a href="{E(s["url"])}" rel="noopener">{E(s["note"])}</a> (checked {E(s["checked"])})</li>' for s in d["sources"])
    src=f"<ul>{src}</ul>" if src else "<p>No sources recorded yet.</p>"
    intro=f'<p class="lead">{E(d["title"])} is a {E(d["language"])}-language Pakistani television drama that aired on {E(b["name"])} in {d["year"]}.</p>' if ok else ""
    im=d.get("image")
    pic=(f'<figure><img src="{E(im["file"])}" alt="{E(im["alt"])}" width="{im["width"]}" height="{im["height"]}"><figcaption class="meta">{E(im["credit"])} – {E(im["license"])}</figcaption></figure>' if im else f'<figure><img src="/img/covers/{d["slug"]}.svg" alt="Original placeholder cover for {E(d["title"])}; not an official poster" width="300" height="200"></figure>')
    body=f'<h1>{E(d["title"])}</h1>{pic}{"" if ok else FIX}{intro}<h2>Key facts</h2>{tbl}<h2>Where to watch</h2>{view}<h2>Sources</h2>{src}<p class="meta">Last checked: {E(d["last_checked"] or "never")}</p>'
    ld=[{"@context":"https://schema.org","@type":"TVSeries","name":d["title"],"datePublished":str(d["year"]),"inLanguage":"ur"}] if ok else []
    page(f"/dramas/{d['slug']}/",f"{d['title']} ({d['year']}) – Pakistani TV drama",f"Facts, credits and verified viewing sources for {d['title']} ({d['year']}), a classic Pakistani television drama.",body,ok,[("Archive","/dramas/"),(d["title"],f"/dramas/{d['slug']}/")],ld)
# Archive
idx=[{"slug":d["slug"],"title":d["title"],"alt":d["alt_titles"],"year":d["year"],"genre":d["genre"],"b":d["broadcaster"],"bn":bc[d["broadcaster"]]["name"],"cast":d["cast"]} for d in D["dramas"]]
decs=sorted({dec(d) for d in D["dramas"]});gens=sorted({g for d in D["dramas"] for g in d["genre"]})
opt=lambda vs,f=lambda v:v:"".join(f'<option value="{E(str(v))}">{E(str(f(v)))}</option>' for v in vs)
body=f'''<h1>Drama archive</h1><p class="lead">Search and filter every drama record. Links work without JavaScript; filters add live narrowing when it is available.</p>
<form id="f" class="filters" role="search" aria-label="Filter dramas"><label>Search title or cast<input type="search" name="q"></label>
<label>Decade<select name="decade"><option value="">All</option>{opt(decs,lambda v:f"{v}s")}</select></label>
<label>Genre<select name="genre"><option value="">All</option>{opt(gens)}</select></label>
<label>Broadcaster<select name="broadcaster"><option value="">All</option>{"".join(f'<option value="{b["slug"]}">{E(b["name"])}</option>' for b in D["broadcasters"])}</select></label>
<label>Sort<select name="sort"><option value="title">Title A–Z</option><option value="old">Oldest first</option><option value="new">Newest first</option></select></label>
<button type="reset">Reset filters</button></form><p id="status" role="status" aria-live="polite"></p>
<noscript><p>JavaScript is off, so the full list is shown below.</p>{grid(D["dramas"])}</noscript><ul id="results" class="grid"></ul>
<p class="jsonly" hidden><button id="prev" type="button">Previous page</button> <button id="next" type="button">Next page</button></p>'''
page("/dramas/","Classic Pakistani drama archive","Search and filter classic Pakistani television dramas by decade, genre, broadcaster and title.",body,True,[("Archive","/dramas/")],
 extra=f'<script>window.__DRAMAS__={json.dumps(idx).replace("</","<\\/")}</script><script src="/search.js" defer></script>')
# Categories
def cats(kind,label,items,match,fmt=lambda x:x):
    lst="".join(f'<li><a href="/{kind}/{E(str(k))}/">{E(fmt(n))}</a></li>' for k,n in items)
    page(f"/{kind}/",f"Browse by {label}",f"Browse classic Pakistani dramas by {label}.",f"<h1>Browse by {label}</h1><ul>{lst}</ul>",True,[(label.title(),f"/{kind}/")])
    for k,n in items:
        ds=[d for d in D["dramas"] if match(d,k)];pub=any(live(d) for d in ds)
        page(f"/{kind}/{k}/",f"{fmt(n)} Pakistani dramas",f"Classic Pakistani television dramas filed under {fmt(n)}.",f"<h1>{E(fmt(n))}</h1><p class='lead'>Dramas in this category. Each record shows what has been verified and what has not.</p>{grid(ds)}",pub,[(label.title(),f"/{kind}/"),(fmt(n),f"/{kind}/{k}/")])
cats("decades","decade",[(x,f"{x}s") for x in decs],lambda d,k:dec(d)==k)
cats("genres","genre",[(g.lower().replace(" ","-"),g) for g in gens],lambda d,k:k in [g.lower().replace(" ","-") for g in d["genre"]])
cats("broadcasters","broadcaster",[(b["slug"],b["name"]) for b in D["broadcasters"]],lambda d,k:d["broadcaster"]==k)
# People
page("/people/","Actors, writers and directors","Profiles of people behind classic Pakistani television dramas.","<h1>People</h1><ul>"+"".join(f'<li><a href="/people/{p["slug"]}/">{E(p["name"])}</a></li>' for p in D["people"])+"</ul>",True,[("People","/people/")])
for p in D["people"]:
    ok=live(p);page(f"/people/{p['slug']}/",p["name"],f"Profile of {p['name']}, {p['role'].lower()} in Pakistani television.",f"<h1>{E(p['name'])}</h1><img src='/img/covers/person-{p['slug']}.svg' alt='Placeholder card for {E(p['name'])}' width='300' height='200'>{'' if ok else FIX}<p>{E(p['bio'])}</p>",ok,[("People","/people/"),(p["name"],f"/people/{p['slug']}/")])
# Articles
arts=[a for a in D["articles"] if live(a)]
page("/articles/","Guides and editorial","Original guides on finding and understanding classic Pakistani television dramas.","<h1>Guides</h1><ul>"+"".join(f'<li><a href="/articles/{a["slug"]}/">{E(a["title"])}</a> <span class="meta">{a["date"]}</span></li>' for a in arts)+"</ul>",True,[("Guides","/articles/")])
for a in arts:
    body=f'<article><h1>{E(a["title"])}</h1><p class="meta">By {E(a["author"])} · Published {a["date"]}</p><p class="lead">{E(a["summary"])}</p>'+"".join(f"<p>{E(x)}</p>" for x in a["body"])+"</article>"
    ld=[{"@context":"https://schema.org","@type":"Article","headline":a["title"],"datePublished":a["date"],"author":{"@type":"Organization","name":NAME}}]
    page(f"/articles/{a['slug']}/",a["title"],a["summary"],body,True,[("Guides","/articles/"),(a["title"],f"/articles/{a['slug']}/")],ld)
# Home
ld=[{"@context":"https://schema.org","@type":"WebSite","name":NAME,"url":SITE+"/"},{"@context":"https://schema.org","@type":"Organization","name":NAME,"url":SITE+"/"}]
home=f'''<img class="hero" src="/img/hero.svg" alt="Illustration of a vintage television set" width="1000" height="360" fetchpriority="high"><h1>Discover classic Pakistani television dramas</h1><p class="lead">An independent guide to older Pakistani serials: who made them, who starred in them, and where an authorized viewing source exists.</p>
<form action="/dramas/" role="search"><label>Search the archive <input type="search" name="q" style="min-width:240px"></label> <button>Search</button></form>
<h2>Browse</h2><p><a href="/decades/">By decade</a> · <a href="/genres/">By genre</a> · <a href="/broadcasters/">By broadcaster</a> · <a href="/dramas/">Full archive</a></p>
<h2>Latest guides</h2><ul>{"".join(f'<li><a href="/articles/{a["slug"]}/">{E(a["title"])}</a></li>' for a in arts)}</ul>
<h2>Finding official viewing sources</h2><p>We only link to sources we have checked. Read <a href="/articles/how-to-check-a-viewing-source-is-official/">how to check a source</a>.</p>'''
page("/","Classic Pakistani drama discovery guide","Discover classic Pakistani television dramas, their creators and verified viewing sources.",home,True,None,ld)
# Supporting pages
DR='<p class="banner"><strong>Draft template.</strong> Replace bracketed items and have this reviewed before launch.</p>'
sp={"about":("About","<p>[Site name] is an independent editorial project about classic Pakistani television drama. It is not affiliated with any broadcaster.</p>"),
"contact":("Contact",DR+"<p>Contact details: [add your email address here].</p>"),
"privacy":("Privacy policy",DR+"<p>This site currently sets no cookies and loads no analytics or ads. Update this page before adding any.</p>"),
"terms":("Terms of use",DR+"<p>[Add terms reviewed by a legal professional.]</p>"),
"editorial-policy":("Editorial policy","<p>Facts are published only with at least one recorded source and a check date. Unverified information is labelled or omitted. Synopses and reviews are original text.</p>"),
"corrections":("Corrections policy","<p>Report errors via the contact page. We will check the claim against sources and update the record with a new check date.</p>"),
"copyright":("Copyright and takedown",DR+"<p>We do not host episodes. To report an infringing link or image, send [your contact email] the page URL, your rights claim and your contact details.</p>"),
"accessibility":("Accessibility statement","<p>We aim for WCAG 2.2 AA. Report barriers through the contact page.</p>"),
"affiliate-disclosure":("Affiliate disclosure",DR+"<p>No affiliate links are used at present. If added, they will be labelled on the page.</p>")}
for s,(t,b) in sp.items():page(f"/{s}/",t,f"{t} for {NAME}.",f"<h1>{t}</h1>{b}",True,[(t,f"/{s}/")])
write("404.html",'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found</title><link rel="stylesheet" href="/style.css"></head><body><main><h1>Page not found</h1><p><a href="/">Go to the homepage</a> or <a href="/dramas/">search the archive</a>.</p></main></body></html>')
write("sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{u}</loc></url>" for u in sorted(set(sitemap)))+"</urlset>")
write("robots.txt",f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
write("_headers","/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
print("Built",len(sitemap),"indexable URLs to",OUT)
