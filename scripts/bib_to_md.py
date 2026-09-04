#run as py static/scripts/bib_to_md.py
import bibtexparser
import os
import re

INPUT = "static/data/publications.bib"
OUTPUT = "content/publications"

os.makedirs(OUTPUT, exist_ok=True)

def clean(text):
    return text.replace("{", "").replace("}", "") if text else ""

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')[:60]

def format_authors_apa(author_str):
    authors = []
    for a in author_str.split(" and "):
        if "," in a:
            last, first = a.split(",", 1)
            initials = " ".join([f"{x.strip()[0]}." for x in first.strip().split()])
            authors.append(f"{last.strip()}, {initials}")
        else:
            authors.append(a)
    return ", ".join(authors)

with open(INPUT, encoding="utf-8") as bibfile:
    bib_database = bibtexparser.load(bibfile)

for entry in bib_database.entries:

    title = clean(entry.get("title", "No title"))
    authors_raw = entry.get("author", "")
    authors = [a.strip() for a in authors_raw.split(" and ")]
    journal = clean(entry.get("journal") or entry.get("booktitle") or "")
    year = entry.get("year", "")
    pages = entry.get("pages", entry.get("eid", ""))
    doi = entry.get("doi", "")
    
    slug = slugify(title)
    filename = f"{year}-{slug}.md"
    filepath = os.path.join(OUTPUT, filename)

    # APA citation
    apa_authors = format_authors_apa(authors_raw)
    apa = f"{apa_authors} ({year}). {title}. {journal}."
    if doi:
        apa += f" https://doi.org/{doi}"

    # BibTeX block
    from bibtexparser.bibdatabase import BibDatabase
    db = BibDatabase()
    db.entries = [entry]
    bibtex_str = bibtexparser.dumps(db)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("+++\n")
        f.write(f'title = "{title}"\n')
        f.write(f'date = "{year}-01-01"\n')
        f.write("draft = false\n\n")

        f.write(f'authors = {authors}\n')
        f.write(f'journal = "{journal}"\n')
        f.write(f'year = {year}\n')
        f.write(f'pages = "{pages}"\n')
        f.write(f'doi = "{doi}"\n')
        f.write('pdf = ""\n\n')

        f.write("# Additional links\n")
        f.write('audio = ""\n')
        f.write('video = ""\n')
        f.write('news = ""\n')
        f.write('data = ""\n')
        f.write('infographic = ""\n\n')

        f.write(f'apa = """{apa}"""\n')
        f.write(f'bibtex = """{bibtex_str.strip()}"""\n')

        f.write("+++\n\n")