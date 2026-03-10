#!/usr/bin/env python3
import html
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCHOLAR_URL = "https://scholar.google.com/citations?hl=en&user=NRkFv4EAAAAJ&view_op=list_works&sortby=pubdate&pagesize=100"
PROFILE_URL = "https://scholar.google.com/citations?user=NRkFv4EAAAAJ&hl=en&oi=sra"
LINKEDIN_URL = "https://www.linkedin.com/in/paul-zhuoran-xiong-56567a90/"
PHOTO_RE = r'https://scholar\.googleusercontent\.com/citations\?view_op=medium_photo&amp;user=NRkFv4EAAAAJ&amp;citpid=1'

ABOUT_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>About | Zhuoran Xiong</title>
    <meta name="description" content="Zhuoran Xiong — PhD Candidate at McGill University" />
    <link rel="icon" href="/thumbnail.png" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
    <link rel="stylesheet" href="/styles.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="nav-wrap">
        <a class="site-title" href="/">Zhuoran Xiong</a>
        <nav class="top-nav">
          <a class="nav-link active" href="/">About</a>
          <a class="nav-link" href="/publications.html">Publications</a>
          <a class="nav-link" href="/contact.html">Contact</a>
        </nav>
      </div>
    </header>

    <main class="layout">
      <aside class="sidebar">
        <div class="avatar-ring">
          <img src="/thumbnail.png" alt="Zhuoran Xiong" class="avatar" />
        </div>
        <h1 class="name">Zhuoran Xiong</h1>
        <p class="title">PhD Candidate<br />McGill University</p>
        <p class="location">Montreal, QC, Canada</p>

        <div class="link-list">
          <a class="link-item" href="mailto:zhuoran.xiong@mail.mcgill.ca"><i class="fa-solid fa-envelope"></i><span>Email</span></a>
          <a class="link-item" href="{PROFILE_URL}" target="_blank" rel="noreferrer"><i class="fa-solid fa-graduation-cap"></i><span>Google Scholar</span></a>
          <a class="link-item" href="https://github.com/paulxiongfree" target="_blank" rel="noreferrer"><i class="fa-brands fa-github"></i><span>GitHub</span></a>
          <a class="link-item" href="{LINKEDIN_URL}" target="_blank" rel="noreferrer"><i class="fa-brands fa-linkedin"></i><span>LinkedIn</span></a>
        </div>
      </aside>

      <section class="content">
        <section class="panel">
          <h2>About</h2>
          <p>
            I am a PhD candidate in the Department of Electrical and Computer Engineering at McGill University,
            advised by <strong>Brett H. Meyer</strong>. My research lies broadly in <strong>deep learning</strong>,
            <strong>efficient AI systems</strong>, and <strong>machine learning optimization</strong>, with interests in
            TinyML, model compression, and neural architecture search.
          </p>
          <p>
            My goal is to build practical AI models that are not only accurate, but also efficient, deployable,
            and scalable for real-world systems.
          </p>

          <h3>Research Interests</h3>
          <ul>
            <li>Deep Learning</li>
            <li>Efficient AI / TinyML</li>
            <li>Neural Architecture Search</li>
            <li>Model Compression and Optimization</li>
            <li>Embedded and Resource-Constrained Machine Learning</li>
          </ul>

          <h3>Education</h3>
          <ul>
            <li><strong>PhD Candidate</strong>, McGill University, Canada</li>
            <li><strong>M.S.</strong>, Columbia University, USA, 2017–2018</li>
            <li><strong>B.Eng.</strong>, Xidian University, China, 2013–2018</li>
          </ul>
        </section>
      </section>
    </main>
  </body>
</html>
""".format(PROFILE_URL=PROFILE_URL, LINKEDIN_URL=LINKEDIN_URL)

CONTACT_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Contact | Zhuoran Xiong</title>
    <meta name="description" content="Contact Zhuoran Xiong" />
    <link rel="icon" href="/thumbnail.png" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
    <link rel="stylesheet" href="/styles.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="nav-wrap">
        <a class="site-title" href="/">Zhuoran Xiong</a>
        <nav class="top-nav">
          <a class="nav-link" href="/">About</a>
          <a class="nav-link" href="/publications.html">Publications</a>
          <a class="nav-link active" href="/contact.html">Contact</a>
        </nav>
      </div>
    </header>

    <main class="layout">
      <aside class="sidebar">
        <div class="avatar-ring">
          <img src="/thumbnail.png" alt="Zhuoran Xiong" class="avatar" />
        </div>
        <h1 class="name">Zhuoran Xiong</h1>
        <p class="title">PhD Candidate<br />McGill University</p>
        <p class="location">Montreal, QC, Canada</p>

        <div class="link-list">
          <a class="link-item" href="mailto:zhuoran.xiong@mail.mcgill.ca"><i class="fa-solid fa-envelope"></i><span>Email</span></a>
          <a class="link-item" href="{PROFILE_URL}" target="_blank" rel="noreferrer"><i class="fa-solid fa-graduation-cap"></i><span>Google Scholar</span></a>
          <a class="link-item" href="https://github.com/paulxiongfree" target="_blank" rel="noreferrer"><i class="fa-brands fa-github"></i><span>GitHub</span></a>
          <a class="link-item" href="{LINKEDIN_URL}" target="_blank" rel="noreferrer"><i class="fa-brands fa-linkedin"></i><span>LinkedIn</span></a>
        </div>
      </aside>

      <section class="content">
        <section class="panel">
          <h2>Contact</h2>
          <p>Please feel free to reach out for academic collaboration, research discussion, or related inquiries.</p>
          <p><strong>Email:</strong> <a href="mailto:zhuoran.xiong@mail.mcgill.ca">zhuoran.xiong@mail.mcgill.ca</a></p>
          <p><strong>Google Scholar:</strong> <a href="{PROFILE_URL}" target="_blank" rel="noreferrer">Profile</a></p>
          <p><strong>GitHub:</strong> <a href="https://github.com/paulxiongfree" target="_blank" rel="noreferrer">paulxiongfree</a></p>
          <p><strong>LinkedIn:</strong> <a href="{LINKEDIN_URL}" target="_blank" rel="noreferrer">Profile</a></p>
        </section>
      </section>
    </main>
  </body>
</html>
""".format(PROFILE_URL=PROFILE_URL, LINKEDIN_URL=LINKEDIN_URL)

README_HEADER = """# Zhuoran Xiong

_PhD Candidate, McGill University_

I am a PhD candidate in the Department of Electrical and Computer Engineering at McGill University, advised by **Brett H. Meyer**. My research lies broadly in **deep learning**, **efficient AI systems**, and **machine learning optimization**, with interests in topics such as TinyML, model compression, and neural architecture search.

---

## Biography

Welcome to my academic homepage. I am currently pursuing my PhD at McGill University, where I work on machine learning systems and efficient deep learning methods. My goal is to build practical AI models that are not only accurate, but also efficient, deployable, and scalable.

---

## Research Interests

- **Deep Learning**
- **Efficient AI / TinyML**
- **Neural Architecture Search**
- **Model Compression and Optimization**
- **Embedded and Resource-Constrained Machine Learning**

---

## Education

- **PhD Candidate**, McGill University, Canada  
- **M.S.**, Columbia University, USA, 2017–2018  
- **B.Eng.**, Xidian University, China, 2013–2018  

---

## Publications

The list below is synchronized from my Google Scholar profile.

"""

README_FOOTER = f"""
---

## Links

- Academic Email: [zhuoran.xiong@mail.mcgill.ca](mailto:zhuoran.xiong@mail.mcgill.ca)
- Google Scholar: [Profile]({PROFILE_URL})
- GitHub: [paulxiongfree](https://github.com/paulxiongfree)
- LinkedIn: [Profile]({LINKEDIN_URL})
- CV

---

## Contact

Please feel free to reach out for academic collaboration, research discussion, or related inquiries.

**Email:** [zhuoran.xiong@mail.mcgill.ca](mailto:zhuoran.xiong@mail.mcgill.ca)
"""


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")


def download_photo(page: str) -> bool:
    m = re.search(PHOTO_RE, page)
    if not m:
        return False
    img_url = html.unescape(m.group(0))
    data = urllib.request.urlopen(urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()
    (REPO / "thumbnail.png").write_bytes(data)
    return True


def normalize_title(title: str) -> str:
    t = title.lower().strip()
    t = re.sub(r'\.\s*arxiv\s*\d{4}$', '', t)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'[^a-z0-9 ]', '', t)
    return t


def clean_venue(venue: str, year: str) -> str:
    venue = venue.replace('&amp;', '&').strip()
    venue = re.sub(r',\s*' + re.escape(year) + r'\s*$', '', venue).strip() if year else venue
    venue = re.sub(r',\s*0\s*$', '', venue).strip()
    return venue


def parse_pubs(page: str):
    pubs = []
    for row in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, re.S):
        title_m = re.search(r'class="gsc_a_at"[^>]*>(.*?)</a>', row, re.S)
        blocks = re.findall(r'<div class="gs_gray">(.*?)</div>', row, re.S)
        year_m = re.search(r'<span class="gsc_a_h gsc_a_hc gs_ibl">(\d{4})</span>', row)
        cites_m = re.search(r'class="gsc_a_ac gs_ibl">(.*?)</a>', row, re.S)
        if not title_m:
            continue
        title = re.sub(r'<.*?>', '', title_m.group(1)).strip()
        authors = re.sub(r'<.*?>', '', blocks[0]).strip() if len(blocks) > 0 else ''
        venue = re.sub(r'<.*?>', '', blocks[1]).strip() if len(blocks) > 1 else ''
        year = year_m.group(1) if year_m else ''
        cites = re.sub(r'<.*?>', '', cites_m.group(1)).strip() if cites_m else ''
        pubs.append({
            'title': title,
            'authors': authors,
            'venue': clean_venue(venue, year),
            'year': year,
            'cites': int(cites) if cites.isdigit() else 0,
        })

    dedup = {}
    for pub in pubs:
        key = normalize_title(pub['title'])
        prev = dedup.get(key)
        if not prev or pub['cites'] > prev['cites'] or len(pub['year']) > len(prev['year']):
            dedup[key] = pub
    return sorted(dedup.values(), key=lambda p: (p['year'] or '0000', p['cites']), reverse=True)


def venue_year(pub):
    venue = pub['venue']
    year = pub['year']
    if year and year not in venue:
        return f"{venue}, {year}" if venue else year
    return venue or year


def render_readme_publications(pubs):
    blocks = []
    for pub in pubs:
        block = (
            f"- **{pub['title']}**  \n"
            f"  {pub['authors']}.  \n"
            f"  _{venue_year(pub)}_."
        )
        if pub['cites']:
            block += f"  \n  **Citations:** {pub['cites']}"
        blocks.append(block)
    return "\n\n".join(blocks) + "\n"


def render_publications_page(pubs):
    groups = {}
    for pub in pubs:
        groups.setdefault(pub['year'] or 'Other', []).append(pub)
    years = sorted(groups.keys(), reverse=True)

    year_sections = []
    for year in years:
        items = []
        for pub in groups[year]:
            cite_html = f"\n                <p><strong>Citations:</strong> {pub['cites']}</p>" if pub['cites'] else ""
            items.append(
                "\n".join([
                    '              <article class="pub-item">',
                    f"                <h3>{html.escape(pub['title'])}</h3>",
                    f"                <p>{html.escape(pub['authors'])}</p>",
                    f"                <p><em>{html.escape(venue_year(pub))}</em></p>{cite_html}",
                    '              </article>',
                ])
            )
        year_sections.append(
            "\n".join([
                '          <div class="year-group">',
                f"            <h3 class=\"year-heading\">{year}</h3>",
                '            <div class="pub-list">',
                "\n".join(items),
                '            </div>',
                '          </div>',
            ])
        )

    html_page = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Publications | Zhuoran Xiong</title>
    <meta name="description" content="Publications of Zhuoran Xiong" />
    <link rel="icon" href="/thumbnail.png" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
    <link rel="stylesheet" href="/styles.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="nav-wrap">
        <a class="site-title" href="/">Zhuoran Xiong</a>
        <nav class="top-nav">
          <a class="nav-link" href="/">About</a>
          <a class="nav-link active" href="/publications.html">Publications</a>
          <a class="nav-link" href="/contact.html">Contact</a>
        </nav>
      </div>
    </header>

    <main class="layout">
      <aside class="sidebar">
        <div class="avatar-ring">
          <img src="/thumbnail.png" alt="Zhuoran Xiong" class="avatar" />
        </div>
        <h1 class="name">Zhuoran Xiong</h1>
        <p class="title">PhD Candidate<br />McGill University</p>
        <p class="location">Montreal, QC, Canada</p>

        <div class="link-list">
          <a class="link-item" href="mailto:zhuoran.xiong@mail.mcgill.ca"><i class="fa-solid fa-envelope"></i><span>Email</span></a>
          <a class="link-item" href="{profile}" target="_blank" rel="noreferrer"><i class="fa-solid fa-graduation-cap"></i><span>Google Scholar</span></a>
          <a class="link-item" href="https://github.com/paulxiongfree" target="_blank" rel="noreferrer"><i class="fa-brands fa-github"></i><span>GitHub</span></a>
          <a class="link-item" href="{linkedin}" target="_blank" rel="noreferrer"><i class="fa-brands fa-linkedin"></i><span>LinkedIn</span></a>
        </div>
      </aside>

      <section class="content">
        <section class="panel">
          <h2>Publications</h2>
          <p class="note">This page is synchronized from my Google Scholar profile.</p>

{year_sections}

          <p class="note">For the latest updates, see my <a href="{profile}" target="_blank" rel="noreferrer">Google Scholar profile</a>.</p>
        </section>
      </section>
    </main>
  </body>
</html>
""".format(profile=PROFILE_URL, linkedin=LINKEDIN_URL, year_sections="\n\n".join(year_sections))
    (REPO / 'publications.html').write_text(html_page)


def main():
    page = fetch(SCHOLAR_URL)
    photo_ok = download_photo(page)
    pubs = parse_pubs(page)
    (REPO / 'README.md').write_text(README_HEADER + render_readme_publications(pubs) + README_FOOTER)
    (REPO / 'index.html').write_text(ABOUT_HTML)
    (REPO / 'contact.html').write_text(CONTACT_HTML)
    render_publications_page(pubs)
    print(f"photo_downloaded={photo_ok}")
    print(f"publications={len(pubs)}")
    for pub in pubs:
        print(f"- {pub['year']} | {pub['title']}")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"sync failed: {e}", file=sys.stderr)
        sys.exit(1)
