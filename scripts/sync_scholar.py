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


README_HEADER = """# Zhuoran Xiong

_PhD Candidate, McGill University_

I am a PhD candidate in the Department of Electrical and Computer Engineering at McGill University, advised by [Brett H. Meyer](https://www.mcgill.ca/ece/brett-meyer) and [Warren J. Gross](https://www.mcgill.ca/ece/warren-gross). My research lies broadly in **deep learning**, **efficient AI systems**, and **machine learning optimization**, with interests in topics such as TinyML, model compression, and neural architecture search.

---

## Biography

Welcome to my academic homepage: <https://paulxiongfree.github.io>. I am currently pursuing my PhD at McGill University, where I work on machine learning systems and efficient deep learning methods. My goal is to build practical AI models that are not only accurate, but also efficient, deployable, and scalable.

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
    t = re.sub(r'\.\s*arxiv(\s*\d{4})?$', '', t)
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
    return sorted(dedup.values(), key=lambda p: p['year'] or '0000', reverse=True)


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


def render_pub_html(pubs):
    by_year = {}
    for pub in pubs:
        by_year.setdefault(pub['year'] or 'Other', []).append(pub)

    year_sections = []
    for year, year_pubs in by_year.items():
        items = []
        for pub in year_pubs:
            cite_html = f"\n                <p><strong>Citations:</strong> {pub['cites']}</p>" if pub['cites'] else ''
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
    return "\n\n".join(year_sections)


def update_index(pubs):
    # The homepage is a single page; only the block between the PUBS markers is regenerated.
    index = REPO / 'index.html'
    page = index.read_text()
    page = re.sub(
        r'(<!-- PUBS:START -->\n).*?(<!-- PUBS:END -->)',
        lambda m: m.group(1) + render_pub_html(pubs) + "\n" + m.group(2),
        page,
        flags=re.S,
    )
    index.write_text(page)


def main():
    page = fetch(SCHOLAR_URL)
    photo_ok = download_photo(page)
    pubs = parse_pubs(page)
    (REPO / 'README.md').write_text(README_HEADER + render_readme_publications(pubs) + README_FOOTER)
    update_index(pubs)
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
