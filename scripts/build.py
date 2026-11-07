# Build a clean academic portfolio using only Python standard library.
# Content is in data/*.json and can be edited with Pages CMS.
# Run: python3 scripts/build.py
from pathlib import Path
from html import escape
from urllib.parse import urlparse,unquote
from itertools import groupby
import json,re,shutil,sys
ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'
SITE=ROOT/'_site'

def read_json(name):
    return json.loads((DATA/f'{name}.json').read_text(encoding='utf8'))

def h(v): return escape(str(v if v is not None else ''),quote=True)

def safe_url(url):
    u=str(url or '').strip()
    p=urlparse(u)
    return u if p.scheme in ('https','mailto') and (p.netloc or p.scheme=='mailto') else ''

def asset(path,depth=0):
    u=str(path or '').strip()
    if not u:return ''
    if u.startswith('https://'):return safe_url(u)
    u=u.lstrip('/')
    if not u.startswith('assets/') or '..' in Path(unquote(u)).parts:return ''
    return '../'*depth + u

def image_html(path,alt,depth=0,klass=''):
    src=asset(path,depth)
    return f'<img src="{h(src)}" alt="{h(alt)}" class="{h(klass)}" loading="lazy" decoding="async">' if src else ''

def ext_link(url,label):
    u=safe_url(url)
    return f'<a href="{h(u)}" rel="noopener noreferrer" target="_blank">{h(label)}</a>' if u else ''

def fill(template,values):
    for key,value in values.items():
        token='{{'+key+'}}'
        if token not in template:raise ValueError('Missing template token: '+token)
        template=template.replace(token,str(value))
    missing=re.findall(r'\{\{[^{}]+\}\}',template)
    if missing: raise ValueError('Unused template placeholders: '+str(missing))
    return template

def render_news(news):
    return '\n'.join(f'<li><time>{h(n.get("date",""))}</time><span>{h(n.get("text",""))}{(" "+ext_link(n.get("url"),n.get("link_label","More"))) if safe_url(n.get("url")) else ""}</span></li>' for n in news)

def render_projects(projects):
    out=[]
    for p in projects:
        name=h(p.get('title',''))
        url='projects/'+h(p['slug'])+'/'
        cover=image_html(p.get('cover_image'),p.get('image_caption') or p.get('title','Research figure'),0,'research-cover')
        media=f'<a class="research-media" href="{url}" aria-label="View {name}">{cover}</a>' if cover else ''
        out.append(f'''<article class="research-item{(' has-cover' if cover else '')}">
          {media}<div class="research-text">
          <p class="research-eyebrow">{h(p.get('category',''))}</p>
          <h3><a href="{url}">{name}</a></h3>
          <p>{h(p.get('summary',''))}</p>
          <div class="research-links"><a href="{url}">Project details →</a>{(' · '+ext_link(p.get('paper_url'),p.get('paper_label') or 'Related paper')) if safe_url(p.get('paper_url')) else ''}</div>
          </div></article>''')
    return '\n'.join(out)

def render_publications(publications):
    years=[]
    for p in publications:
        year=str(p.get('year',''))
        if year not in years:years.append(year)
    out=[]
    for year in years:
        rows=[p for p in publications if str(p.get('year',''))==year]
        out.append(f'<h3 class="pub-year">{h(year)}</h3><ol class="publication-list">')
        for p in rows:
            u=safe_url(p.get('url'))
            title=h(p.get('title',''))
            title=f'<a href="{h(u)}" target="_blank" rel="noopener noreferrer">{title}</a>' if u else title
            out.append(f'<li><div class="pub-title">{title}</div><div class="pub-authors">{h(p.get("authors",""))}</div><div class="pub-venue">{h(p.get("venue",""))}</div></li>')
        out.append('</ol>')
    return '\n'.join(out)

def render_education(items):
    return '\n'.join(f'<div class="education-row"><div><strong>{h(item.get("degree",""))}</strong><span>{h(item.get("institution",""))}</span></div><small>{h(item.get("detail",""))}</small></div>' for item in items)

def render_expertise(items):
    return '\n'.join(f'<div class="skill-row"><strong>{h(item.get("title",""))}</strong><p>{h(item.get("description",""))}</p></div>' for item in items)

def render_awards(items):
    return '\n'.join(f'<li>{h(item.get("text",""))}</li>' for item in items)

def page_head(title,desc,depth=0):
    lead='../'*depth
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#ffffff"><meta name="description" content="{h(desc)}"><title>{h(title)}</title><link rel="icon" href="{lead}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{lead}styles.css"><link rel="stylesheet" href="{lead}project-detail.css"></head>'''

def project_detail(site,p):
    lead='../../'
    title=p.get('title','Research project')
    cover=image_html(p.get('cover_image'),p.get('image_caption') or title,depth=2,klass='detail-cover-image')
    cover_html=f'<figure class="detail-cover">{cover}{("<figcaption>"+h(p.get("image_caption"))+"</figcaption>") if p.get("image_caption") else ""}</figure>' if cover else ''
    gallery=''.join(f'<figure>{image_html(path,title+" additional figure",depth=2)}<figcaption>Research figure</figcaption></figure>' for path in p.get('gallery') or [] if asset(path,2))
    tags=''.join(f'<span>{h(t)}</span>' for t in p.get('tags',[]))
    paper=ext_link(p.get('paper_url'),p.get('paper_label') or 'Related publication')
    return f'''{page_head(title+' | '+site.get('name','Yuhyun Lee'),p.get('summary',''),2)}<body><a class="skip-link" href="#project">Skip to content</a>
      <div class="page"><header class="site-header"><a href="{lead}index.html" class="site-name">{h(site.get('name','Yuhyun Lee'))}</a><nav class="site-nav" aria-label="Page navigation"><a href="{lead}index.html#research">← Research</a><a href="{lead}index.html#publications">Publications</a><a href="{lead}index.html#contact">Contact</a></nav></header>
      <main id="project" class="detail-page"><a href="{lead}index.html#research" class="detail-back">← Back to selected research</a><div class="detail-kicker">{h(p.get('category',''))}</div><h1>{h(title)}</h1>
      <p class="detail-summary">{h(p.get('summary',''))}</p>{('<div class="detail-tags">'+tags+'</div>') if tags else ''}
      {cover_html}<section><h2>My contribution</h2><p>{h(p.get('contribution',''))}</p></section>
      <section><h2>Findings &amp; significance</h2><p>{h(p.get('outcome',''))}</p></section>
      {('<p class="detail-paper">'+paper+'</p>') if paper else ''}
      {('<section><h2>Research figures</h2><div class="detail-gallery">'+gallery+'</div></section>') if gallery else ''}
      </main><footer class="site-footer"><span>© 2026 {h(site.get('name','Yuhyun Lee'))}</span><a href="{lead}index.html#research">All research ↑</a></footer></div></body></html>'''

def build_index(site,projects,publications,expertise,education,awards,news):
    template=(ROOT/'source/template.html').read_text(encoding='utf8')
    photo=image_html(site.get('profile_photo'),site.get('name','Yuhyun Lee')+' profile photograph',0,'portrait')
    portrait=f'<div class="portrait-wrap">{photo}</div>' if photo else ''
    scholar=safe_url(site.get('scholar_url'))
    linkedin=safe_url(site.get('linkedin_url'))
    cv=asset(site.get('cv_url')) or 'assets/Yuhyun_Lee_CV.pdf'
    email=site.get('email','')
    social=[f'<a href="mailto:{h(email)}">Email</a>',f'<a href="{h(cv)}" download>CV</a>']
    if scholar:social.append(ext_link(scholar,'Google Scholar'))
    if linkedin:social.append(ext_link(linkedin,'LinkedIn'))
    return fill(template,{
        'name':h(site.get('name','Yuhyun Lee')), 'meta_title':h(site.get('name','Yuhyun Lee')+' | Academic Profile'),
        'meta_description':h(site.get('meta_description','')),'status':h(site.get('status','')),
        'position':h(site.get('position','Ph.D. Candidate')),'department':h(site.get('department','Biomedical Engineering')),'institution':h(site.get('institution','Carnegie Mellon University')),
        'hero_intro':h(site.get('hero_intro','')),'hero_body':h(site.get('hero_body','')),
        'about_paragraph_2':h(site.get('about_paragraph_2','')),'location':h(site.get('location','')),
        'social_links':'<span class="link-dot"> · </span>'.join(social),'profile_html':portrait,
        'news_html':render_news(news),'projects_html':render_projects(projects),
        'publications_html':render_publications(publications), 'scholar_more':ext_link(scholar,'Google Scholar ↗'),
        'education_html':render_education(education),'expertise_html':render_expertise(expertise),'awards_html':render_awards(awards),
        'email':h(email),'linkedin_url':h(linkedin or '#'),'scholar_url':h(scholar or '#'),
        'contact_body':h(site.get('contact_body','')),
        'structured_data':json.dumps({'@context':'https://schema.org','@type':'Person','name':site.get('name','Yuhyun Lee'),'jobTitle':'Biomedical Engineering Ph.D. Candidate','affiliation':{'@type':'Organization','name':'Carnegie Mellon University'},'email':'mailto:'+email,'sameAs':[x for x in [scholar,linkedin] if x]},ensure_ascii=False).replace('<','\u003c')
    })

def main():
    site=read_json('site');projects=read_json('projects');publications=read_json('publications');expertise=read_json('expertise');education=read_json('education');awards=read_json('awards');news=read_json('news')
    for name,arr in [('projects',projects),('publications',publications),('expertise',expertise),('education',education),('awards',awards),('news',news)]:
        if not isinstance(arr,list):raise TypeError('data/'+name+'.json must be a list')
    slugs=[str(p.get('slug','')) for p in projects]
    if not all(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',s) for s in slugs) or len(set(slugs))!=len(slugs):raise ValueError('Project slugs must be unique lowercase letters/numbers/dashes')
    (ROOT/'index.html').write_text(build_index(site,projects,publications,expertise,education,awards,news),encoding='utf8')
    projects_dir=ROOT/'projects'
    if projects_dir.exists():shutil.rmtree(projects_dir)
    for project in projects:
        folder=projects_dir/project['slug'];folder.mkdir(parents=True,exist_ok=True)
        (folder/'index.html').write_text(project_detail(site,project),encoding='utf8')
    if SITE.exists():shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    for f in ('index.html','styles.css','project-detail.css'):
        shutil.copy2(ROOT/f,SITE/f)
    shutil.copytree(ROOT/'assets',SITE/'assets')
    shutil.copytree(projects_dir,SITE/'projects')
    (SITE/'.nojekyll').write_text('',encoding='utf8')
    print('Built minimalist academic portfolio,',len(projects),'projects,',len(publications),'publications,',len(news),'news items')

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('BUILD FAILED',exc,file=sys.stderr);raise
