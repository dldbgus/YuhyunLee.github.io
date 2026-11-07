"""Build the editable portfolio from JSON, without installing Python dependencies.

Run: python3 scripts/build.py
GitHub Actions runs this automatically whenever Pages CMS saves content.
"""
from pathlib import Path
from html import escape
from urllib.parse import urlparse, unquote
import json, re, shutil, sys

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'
SITE=ROOT/'_site'

def read_json(name):
    return json.loads((DATA/f'{name}.json').read_text(encoding='utf-8'))

def e(x): return escape(str(x if x is not None else ''), quote=True)
def valid_url(url):
    url=str(url or '').strip()
    if not url: return ''
    p=urlparse(url)
    return url if p.scheme in ('https','mailto') and (p.netloc or p.scheme=='mailto') else ''

def relative_asset(path, depth=0):
    p=str(path or '').strip()
    if not p: return ''
    if p.startswith(('https://','http://')): # allow publicly hosted images
        return p if valid_url(p) else ''
    # Only allow repository-local assets so CMS cannot turn file fields into unsafe protocols.
    p=p.lstrip('/')
    if not p.startswith('assets/') or '..' in Path(unquote(p)).parts: return ''
    return '../'*depth+p

def img(path, alt, depth=0, cls=''):
    u=relative_asset(path,depth)
    return f'<img class="{e(cls)}" src="{e(u)}" alt="{e(alt)}" loading="lazy" decoding="async">' if u else ''

def link(url, text, cls=None, external=True):
    u=valid_url(url)
    if not u: return ''
    attrs=' target="_blank" rel="noopener noreferrer"' if external else ''
    c=f' class="{e(cls)}"' if cls else ''
    return f'<a{c} href="{e(u)}"{attrs}>{e(text)} ↗</a>'

def render_project_art(p, depth=0):
    slug=p.get('art') if p.get('art') in ('nasal','slice','fish','model') else 'model'
    cover=relative_asset(p.get('cover_image'), depth)
    image=img(p.get('cover_image'),p.get('title','Research project'),depth,'uploaded-art') if cover else img('assets/illustrations/'+slug+'.svg',p.get('title','Research project')+' conceptual illustration',depth,'art-fallback')
    return f'<div class="project-art art-{slug}">{image}<span class="project-art-index">{e(p.get("category","RESEARCH"))}</span></div>'

def render_projects(projects):
    out=[]
    for i,p in enumerate(projects):
        slug=p['slug']
        classes='project-card' + (' featured-project' if i==0 else '')
        tags=''.join('<span>'+e(v)+'</span>' for v in p.get('tags',[]))
        paper=link(p.get('paper_url'),p.get('paper_label') or 'Read paper','paper-link')
        out.append(f'''<article class="{classes}">
            {render_project_art(p)}
            <div class="project-content"><div class="project-meta"><span class="tag">{e(p.get('category',''))}</span><span>{e(p.get('stage',''))}</span></div>
                <h3>{e(p.get('title',''))}</h3><p>{e(p.get('summary',''))}</p>
                <div class="chip-row">{tags}</div>
                <div class="project-actions"><a class="project-link" href="projects/{e(slug)}/">Explore project <span aria-hidden="true">↗</span></a>{paper}</div>
            </div></article>''')
    return '\n'.join(out)

def render_publications(publications):
    out=[]
    for p in publications:
        u=valid_url(p.get('url'))
        # Nonlinked publication entries are supported too.
        tag='a' if u else 'div'
        href=f' href="{e(u)}" target="_blank" rel="noopener noreferrer"' if u else ''
        out.append(f'''<{tag} class="pub-row"{href}><span class="pub-year">{e(p.get('year',''))}</span>
        <span class="pub-details"><span class="pub-type">{e(p.get('venue',''))}</span><strong>{e(p.get('title',''))}</strong><small>{e(p.get('authors',''))}</small></span>
        <span class="pub-arrow" aria-hidden="true">{'↗' if u else '·'}</span></{tag}>''')
    return '\n'.join(out)

def render_expertise(expertise):
    return '\n'.join(f'''<div class="expertise-card"><div class="expertise-no">/ {i+1:02d}</div>
    <h3>{e(s.get('title',''))}</h3><p>{e(s.get('description',''))}</p>
    <div class="skill-tags">{''.join('<span>'+e(t)+'</span>' for t in s.get('tags',[]))}</div></div>'''
         for i,s in enumerate(expertise))

def render_education(education):
    return '<p class="mini-label">EDUCATION</p>\n'+'\n'.join(
        f'''<div class="timeline-row"><span class="timeline-point"></span><div><strong>{e(row.get('degree',''))}</strong><p>{e(row.get('institution',''))}</p><small>{e(row.get('detail',''))}</small></div></div>'''
        for row in education)

def render_awards(awards):
    return '<p class="mini-label">SELECTED RECOGNITION</p>\n'+'\n'.join('<p>'+e(row.get('text',''))+'</p>' for row in awards)

def render_hero(site):
    u=relative_asset(site.get('profile_photo'))
    if u:
        return f'''<div class="visual-topbar"><span><span class="tiny-dot"></span> RESEARCHER PROFILE</span><span>YUH YUN LEE</span></div>
        {img(site['profile_photo'],site.get('name','Researcher')+' profile photograph',0,'hero-portrait')}
        <div class="visual-bottombar"><span>NEURAL ENGINEERING</span><span>RESEARCH & DEVELOPMENT</span></div>'''
    return f'''<div class="visual-topbar"><span><span class="tiny-dot"></span> RESEARCH INTERFACE</span><span>01 / 03</span></div>
        {img('assets/illustrations/hero.svg','Conceptual neural recording schematic, not experimental data',0,'hero-diagram')}
        <div class="visual-bottombar"><span>DEPTH-RESOLVED NEUROPHYSIOLOGY</span><span>CONCEPTUAL SCHEMATIC</span></div>
        <div class="floating-note"><span class="floating-icon">↗</span><div><strong>From signal to insight</strong><small>Stimulation · Recording · Analysis</small></div></div>'''

def fill_token(t,key,value):
    token='{{'+key+'}}'
    if token not in t: raise ValueError('Missing token: '+key)
    return t.replace(token,str(value))

def build_index(site,projects,publications,expertise,education,awards):
    template=(ROOT/'source'/'template.html').read_text(encoding='utf-8')
    intro=f"I'm <strong>{e(site['name'])}</strong>, {e(site.get('hero_intro',''))}"
    scholar=valid_url(site.get('scholar_url',''))
    linkedin=valid_url(site.get('linkedin_url',''))
    links=link(scholar,'Google Scholar').replace(' ↗',' ↗')+'<span class="hero-separator">/</span>'+link(linkedin,'LinkedIn')+'<span class="hero-separator">/</span><span>'+e(site.get('location',''))+'</span>'
    email=site.get('email','')
    email_href='mailto:'+email
    profile={
       'brand':e(site['name'])+'<span class="brand-sub">'+e(site.get('brand_subtitle',''))+'</span>',
       'status':'<span class="status-dot"></span> '+e(site.get('status','')).upper(),
       'affiliation':e(site.get('affiliation','')),
       'hero_title':e(site.get('hero_title',''))+'<br><em>'+e(site.get('hero_highlight',''))+'</em>',
       'hero_intro':intro,
       'hero_body':e(site.get('hero_body','')),
       'hero_links':links,
       'hero_visual':render_hero(site),
       'projects_html':render_projects(projects),
       'publications_html':render_publications(publications),
       'expertise_html':render_expertise(expertise),
       'education_html':render_education(education),
       'awards_html':render_awards(awards),
       'conference_text':e(site.get('conference_text','')),
       'conference_date':e(site.get('conference_date','')),
       'about_title':e(site.get('about_title',''))+'<br><span>'+e(site.get('about_highlight',''))+'</span>',
       'about_paragraph_1':e(site.get('about_paragraph_1','')),
       'about_paragraph_2':e(site.get('about_paragraph_2','')),
       'contact_title':e(site.get('contact_title',''))+' <em>'+e(site.get('contact_highlight',''))+'</em>',
       'contact_body':e(site.get('contact_body','')),
       'contact_card':e(site.get('contact_card','')),
       'email_contact':e(email)+' <span aria-hidden="true">↗</span>',
       'email':e(email),
       'scholar_url':e(scholar),
       'linkedin_url':e(linkedin),
       'cv_url':e(relative_asset(site.get('cv_url')) or 'assets/Yuhyun_Lee_CV.pdf'),
       'meta_description':e(site.get('meta_description','')),
       'meta_title':e(site['name']+' | Neural Engineering Researcher'),
       'structured_data':json.dumps({'@context':'https://schema.org','@type':'Person','name':site['name'],'jobTitle':'Biomedical Engineering Ph.D. Candidate','affiliation':{'@type':'Organization','name':'Carnegie Mellon University'},'email':email_href,'sameAs':[x for x in [scholar,linkedin] if x],'knowsAbout':['neural engineering','electrophysiology','neural stimulation']},ensure_ascii=False).replace('<','\\u003c'),
    }
    for k,v in profile.items():
        template=fill_token(template,k,v)
    leftovers=re.findall(r'\{\{[^{}]+\}\}',template)
    if leftovers:raise ValueError(f'Unreplaced tokens: {leftovers}')
    return template

def project_detail(site,p):
    slug=e(p['slug'])
    tags=' '.join(f'<span>{e(tag)}</span>' for tag in p.get('tags',[]))
    art=render_project_art(p,depth=2)
    gallery=p.get('gallery') or []
    gallery_html='\n'.join(f'<figure>{img(image,p.get("title","Research figure")+" project image",2)}<figcaption>Research image · {e(p.get("title",""))}</figcaption></figure>' for image in gallery if relative_asset(image,2))
    paper=link(p.get('paper_url'),p.get('paper_label') or 'Related paper','detail-paper')
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="theme-color" content="#f7f8f5"><meta name="description" content="{e(p.get('summary',''))}">
    <title>{e(p.get('title',''))} | {e(site['name'])}</title><link rel="icon" type="image/svg+xml" href="../../assets/favicon.svg">
    <link rel="stylesheet" href="../../styles.css"><link rel="stylesheet" href="../../project-detail.css"></head><body>
    <a class="skip-link" href="#project-main">Skip to content</a>
    <header class="site-header"><div class="container header-inner"><a class="brand" href="../../index.html" aria-label="Home"><span class="brand-mark"><span>Y</span><span class="brand-dot"></span></span><span class="brand-name">{e(site['name'])}<span class="brand-sub">NEURAL ENGINEERING</span></span></a><a class="header-contact" href="../../index.html#research">← All research</a></div></header>
    <main id="project-main"><section class="detail-hero section-pad"><div class="container"><a href="../../index.html#research" class="detail-back">← Back to selected research</a>
    <p class="eyebrow">{e(p.get('category','RESEARCH'))} · {e(p.get('stage',''))}</p><h1>{e(p.get('title',''))}</h1><p class="detail-intro">{e(p.get('summary',''))}</p>
    <div class="chip-row">{tags}</div></div></section>
    <section class="detail-content section-pad"><div class="container detail-grid"><div class="detail-visual">{art}<p class="detail-caption">{e(p.get('image_caption',''))}</p></div>
    <div class="detail-overview"><p class="eyebrow">PROJECT OVERVIEW</p><h2>From idea to <span>evidence.</span></h2>
    <h3>My contribution</h3><p>{e(p.get('contribution',''))}</p>
    <h3>Findings &amp; significance</h3><p>{e(p.get('outcome',''))}</p>
    <div class="detail-cta">{paper}</div></div></div></section>
    {('<section class="detail-gallery section-pad"><div class="container"><p class="eyebrow">SUPPORTING IMAGES</p><h2>Inside the <span>project.</span></h2><div class="detail-gallery-grid">'+gallery_html+'</div></div></section>') if gallery_html else ''}
    <section class="detail-footer"><div class="container"><p>Interested in this work?</p><h2>Let's connect.</h2>
    <a class="btn btn-primary" href="mailto:{e(site['email'])}?subject={e('Research inquiry: '+p.get('title',''))}">Contact {e(site['name'])} ↗</a>
    <a class="detail-back" href="../../index.html#research">Explore other projects ↑</a></div></section></main>
    <footer class="site-footer"><div class="container footer-inner"><div><p>© {e(site['name'])}. Research portfolio.</p></div><a href="../../index.html">Home ↑</a></div></footer>
    </body></html>'''

def main():
    site=read_json('site');projects=read_json('projects');publications=read_json('publications');expertise=read_json('expertise');education=read_json('education');awards=read_json('awards')
    for key,array in [('projects',projects),('publications',publications),('expertise',expertise),('education',education),('awards',awards)]:
        if not isinstance(array,list):raise TypeError(f'data/{key}.json must be a list')
    slugs=[str(p.get('slug','')) for p in projects]
    if not all(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',s) for s in slugs) or len(set(slugs))!=len(slugs):
        raise ValueError('Project slugs must be unique lowercase letters/numbers/dashes, such as zebrafish-eeg')
    html=build_index(site,projects,publications,expertise,education,awards)
    (ROOT/'index.html').write_text(html,encoding='utf-8')
    # local previews: can open index.html without a server; detail pages also work.
    local_projects=ROOT/'projects'
    if local_projects.exists():shutil.rmtree(local_projects)
    for p in projects:
        d=local_projects/p['slug'];d.mkdir(parents=True,exist_ok=True)
        (d/'index.html').write_text(project_detail(site,p),encoding='utf8')
    if SITE.exists():shutil.rmtree(SITE)
    SITE.mkdir()
    for filename in ('index.html','styles.css','script.js','project-detail.css'):
        shutil.copy2(ROOT/filename,SITE/filename)
    shutil.copytree(ROOT/'assets',SITE/'assets')
    shutil.copytree(local_projects,SITE/'projects')
    (SITE/'.nojekyll').write_text('',encoding='utf8')
    print('Built: index +',len(projects),'project pages, output:',SITE)

if __name__=='__main__':
    try:main()
    except Exception as err:
        print('BUILD FAILED:',err,file=sys.stderr);raise
