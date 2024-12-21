# /// script
# dependencies = [
#   "bibtexparser",
#   "jinja2", 
#   "markdown",
# ]
# ///

import bibtexparser
from bibtexparser.bparser import BibTexParser
from jinja2 import Template
from io import StringIO
import markdown
from datetime import datetime

# Function to read the BibTeX string and parse it
def read_bibtex_string(bibtex_string):
    bibtex_file = StringIO(bibtex_string)
    parser = BibTexParser()
    parser.customization = bibtexparser.customization.convert_to_unicode
    bib_database = bibtexparser.load(bibtex_file, parser=parser)

    # Adapt author names to "First name Last name" format, but keep original authors for citation
    for entry in bib_database.entries:
        if 'author' in entry:
            entry['original_author'] = entry['author']
            authors = entry['author'].split(' and ')
            formatted_authors = []
            for author in authors:
                names = author.split(', ')
                if len(names) == 2:
                    formatted_author = f"{names[1]} {names[0]}"
                    # Bold Alexander Kolesnikov's name
                    if 'Alexander Kolesnikov' in formatted_author:
                        formatted_author = f"<b>{formatted_author}</b>"
                    formatted_authors.append(formatted_author)
                else:
                    formatted_authors.append(author)
            entry['author'] = ', '.join(formatted_authors)
    return bib_database.entries

# Function to create an HTML page from the parsed BibTeX data and save it
def create_html(entries):
    # Convert the About Me section from Markdown to HTML
    about_markdown = """
I am a machine learning researcher focused on advancing deep learning, with a particular interest in multimodal intelligence. Currently, I am working as a member of technical staff at OpenAI, where I contribute to multimodal AI research.

Throughout my career, I've had the opportunity to work on various aspects of computer vision and machine learning. This includes contributing to vision model development (ImageNet state-of-the-art results in [2019](https://arxiv.org/abs/1912.11370), [2020](https://arxiv.org/abs/2010.11929), and [2021](https://arxiv.org/abs/2106.04560)) and developing open models like [SigLIP](https://arxiv.org/abs/2303.15343) and [PaliGemma](https://github.com/google-research/big_vision/blob/main/big_vision/configs/proj/paligemma/README.md). I've also worked on neural architectures including [BiT](https://arxiv.org/abs/1912.11370), [ViT](https://arxiv.org/abs/2010.11929), [MLP-Mixer](https://arxiv.org/abs/2105.01601), and [FlexiViT](https://arxiv.org/abs/2212.08013). My recent work has focused on making multimodal deep learning more accessible and scalable through projects like [UViM](https://arxiv.org/abs/2205.10337), [Vision with Rewards](https://arxiv.org/abs/2302.08242), and [JetFormer](https://arxiv.org/abs/2411.19722).

I enjoy developing efficient research infrastructure, particularly using Jax. Some of this work is available in the open-source [big_vision](https://github.com/google-research/big_vision) repository.

Before joining OpenAI, I was at Google Brain (now Google DeepMind). I completed my PhD at [ISTA](https://ist.ac.at/en/home/) under [Christoph Lampert](https://cvml.ista.ac.at/)'s supervision, where I studied weakly-supervised learning and generative image models.

You can reach me at `a@kolesnikov.ch`.
"""
    about_html = markdown.markdown(about_markdown)

    # Separate selected entries
    selected_entries = [entry for entry in entries if entry.get('selected', '').lower() == 'true']

    # A simple HTML template using Jinja2 syntax
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Personal Page of Alexander Kolesnikov</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary-color: #2563eb;
                --text-primary: #1a1a1a;
                --text-secondary: #4b5563;
                --bg-primary: #ffffff;
                --bg-secondary: #f8fafc;
                --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
                --shadow-md: 0 4px 12px rgba(0,0,0,0.05);
                --shadow-lg: 0 20px 25px -5px rgba(0,0,0,0.05);
                --gradient-primary: linear-gradient(135deg, #2563eb, #4f46e5);
            }

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
                line-height: 1.7;
                max-width: 1100px;
                margin: 0 auto;
                padding: 3rem 2rem;
                background-color: var(--bg-secondary);
                color: var(--text-primary);
                font-size: 1rem;
                letter-spacing: -0.01em;
            }

            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 4rem;
                padding: 3rem;
                background: var(--bg-primary);
                border-radius: 1.5rem;
                box-shadow: var(--shadow-lg);
                position: relative;
                overflow: hidden;
            }

            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 5px;
                background: var(--gradient-primary);
            }

            .header-left {
                flex: 1;
            }

            .name {
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.03em;
            }

            .title {
                font-size: 1.2rem;
                color: var(--text-secondary);
                margin: 0.7rem 0;
                font-weight: 500;
            }

            .profile-img {
                width: 180px;
                height: 180px;
                border-radius: 1.5rem;
                object-fit: cover;
                margin-left: 3rem;
                box-shadow: var(--shadow-lg);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                border: 4px solid var(--bg-primary);
            }

            .profile-img:hover {
                transform: scale(1.05) rotate(2deg);
            }

            .about {
                font-size: 1.05rem;
                color: var(--text-primary);
                background: var(--bg-primary);
                border-radius: 1.5rem;
                padding: 3rem;
                margin-bottom: 4rem;
                box-shadow: var(--shadow-lg);
                line-height: 1.8;
                text-align: justify;
                position: relative;
            }

            .about a {
                color: var(--primary-color);
                text-decoration: none;
                font-weight: 600;
                transition: all 0.2s ease;
                padding-bottom: 1px;
                border-bottom: 2px solid transparent;
            }

            .about a:hover {
                border-bottom: 2px solid var(--primary-color);
            }

            h1 {
                font-size: 2rem;
                font-weight: 700;
                margin: 3rem 0 2rem;
                color: var(--text-primary);
                position: relative;
                padding-bottom: 0.7rem;
                letter-spacing: -0.02em;
            }

            h1::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 70px;
                height: 5px;
                background: var(--gradient-primary);
                border-radius: 3px;
            }

            .selected-publications-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 2rem;
                margin-bottom: 4rem;
            }

            .selected-publication-card {
                background: var(--bg-primary);
                border-radius: 1.2rem;
                overflow: hidden;
                box-shadow: var(--shadow-lg);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                border: 1px solid rgba(0,0,0,0.05);
            }

            .selected-publication-card:hover {
                transform: translateY(-8px);
                box-shadow: var(--shadow-lg), 0 25px 50px -12px rgba(0,0,0,0.1);
            }

            .selected-publication-card img {
                width: 100%;
                height: 200px;
                object-fit: cover;
                background: #f8f8f8;
                padding: 1rem;
                transition: all 0.3s ease;
            }

            .selected-publication-card:hover img {
                transform: scale(1.05);
            }

            .selected-publication-card p {
                padding: 1.5rem;
                font-size: 1rem;
                color: var(--text-primary);
                font-weight: 500;
            }

            .entry {
                background: var(--bg-primary);
                border-radius: 1.2rem;
                padding: 2rem;
                margin-bottom: 2rem;
                box-shadow: var(--shadow-lg);
                display: flex;
                gap: 3rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                border: 1px solid rgba(0,0,0,0.05);
            }

            .entry:hover {
                transform: translateX(8px);
                box-shadow: var(--shadow-lg), 0 20px 40px -12px rgba(0,0,0,0.1);
            }

            .entry-content {
                flex: 1;
            }

            .entry-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 1.2rem;
                line-height: 1.4;
            }

            .author, .year, .journal {
                color: var(--text-secondary);
                margin-bottom: 0.7rem;
                font-size: 1rem;
            }

            .links {
                display: flex;
                gap: 1rem;
                margin-top: 1.5rem;
                flex-wrap: wrap;
            }

            .links a, .cite-button {
                padding: 0.6rem 1.2rem;
                border-radius: 0.8rem;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
                font-size: 0.95rem;
            }

            .links a {
                background: #e0e7ff;
                color: var(--primary-color);
            }

            .links a:hover {
                background: #c7d2fe;
                transform: translateY(-2px);
            }

            .cite-button {
                background: var(--gradient-primary);
                color: white;
                border: none;
                cursor: pointer;
            }

            .cite-button:hover {
                opacity: 0.9;
                transform: translateY(-2px);
            }

            .citation-text {
                margin-top: 1.5rem;
                padding: 1.5rem;
                background: var(--bg-secondary);
                border-radius: 1rem;
                font-family: 'SF Mono', Consolas, Monaco, monospace;
                font-size: 0.9rem;
                display: none;
                border: 1px solid rgba(0,0,0,0.1);
            }

            .preview img {
                max-width: 280px;
                border-radius: 1rem;
                box-shadow: var(--shadow-md);
                transition: all 0.3s ease;
            }

            .preview img:hover {
                transform: scale(1.05);
            }

            .footer {
                margin-top: 5rem;
                padding: 3rem;
                background: var(--bg-primary);
                border-radius: 1.5rem;
                box-shadow: var(--shadow-lg);
                text-align: center;
                color: var(--text-secondary);
                font-size: 0.95rem;
                position: relative;
            }

            .footer::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 5px;
                background: var(--gradient-primary);
                border-bottom-left-radius: 1.5rem;
                border-bottom-right-radius: 1.5rem;
            }

            @media (max-width: 768px) {
                body {
                    padding: 1.5rem;
                }

                .header {
                    flex-direction: column;
                    text-align: center;
                    padding: 2rem;
                }

                .profile-img {
                    margin: 2rem 0 0 0;
                }

                .entry {
                    flex-direction: column;
                    gap: 1.5rem;
                }

                .preview img {
                    max-width: 100%;
                }

                .links {
                    justify-content: center;
                }

                .name {
                    font-size: 2rem;
                }
            }

            @media (prefers-color-scheme: dark) {
                :root {
                    --bg-primary: #1a1a1a;
                    --bg-secondary: #111111;
                    --text-primary: #ffffff;
                    --text-secondary: #a0a0a0;
                }

                .links a {
                    background: rgba(37, 99, 235, 0.2);
                }

                .links a:hover {
                    background: rgba(37, 99, 235, 0.3);
                }

                .citation-text {
                    background: rgba(255, 255, 255, 0.05);
                }
            }
        </style>
        <script>
            function toggleCitation(id) {
                const citationElement = document.getElementById(id);
                const allCitations = document.querySelectorAll('.citation-text');
                
                allCitations.forEach(citation => {
                    if (citation.id !== id) {
                        citation.style.display = "none";
                    }
                });

                if (citationElement.style.display === "none" || citationElement.style.display === "") {
                    citationElement.style.display = "block";
                } else {
                    citationElement.style.display = "none";
                }
            }
        </script>
    </head>
    <body>
        <div class="header">
            <div class="header-left">
                <p class="name">Alexander Kolesnikov</p>
                <p class="title">Member of Technical Staff at OpenAI</p>
            </div>
            <img src="/assets/img/profile.jpg" class="profile-img" alt="Profile Image"/>
        </div>

        <div class="about">
            {{ about_html | safe }}
        </div>

        {% if selected_entries %}
        <h1>Selected Publications</h1>
        <div class="selected-publications-grid">
        {% for entry in selected_entries %}
            <div class="selected-publication-card">
                {% if entry.preview %}
                <a href="#pub_{{ entry.ID }}">
                    <img src="/assets/img/publication_preview/{{ entry.preview }}" alt="Preview image">
                </a>
                {% endif %}
                <p><a href="#pub_{{ entry.ID }}">{{ entry.title }}</a></p>
            </div>
        {% endfor %}
        </div>
        {% endif %}

        <h1>Publications</h1>
        {% for entry in entries %}
        <div class="entry" id="pub_{{ entry.ID }}">
            <div class="entry-content">
                <div class="entry-title">{{ entry.title }}</div>
                {% if entry.author %}
                    <div class="author">Authors: {{ entry.author | safe }}</div>
                {% endif %}
                {% if entry.year %}
                    <div class="year">Year: {{ entry.year }}</div>
                {% endif %}
                {% if entry.journal %}
                    <div class="journal">Journal: {{ entry.journal }}</div>
                {% endif %}
                <div class="links">
                    {% if entry.arxiv %}
                        <a href="https://arxiv.org/abs/{{ entry.arxiv }}" target="_blank">arXiv</a>
                    {% endif %}
                    {% if entry.pdf %}
                        <a href="{{ entry.pdf }}" target="_blank">PDF</a>
                    {% endif %}
                    {% if entry.code %}
                        <a href="{{ entry.code }}" target="_blank">Code</a>
                    {% endif %}
                    <button class="cite-button" onclick="toggleCitation('citation_{{ loop.index }}')">Cite</button>
                </div>
                <div id="citation_{{ loop.index }}" class="citation-text">{{ entry.bibtex | replace('\\n', '<br>') | safe }}</div>
            </div>
            {% if entry.preview %}
                <div class="preview">
                    <img src="/assets/img/publication_preview/{{ entry.preview }}" alt="Preview image">
                </div>
            {% endif %}
        </div>
        {% endfor %}

        <div class="footer">
            <p>Last updated: {{ current_date }}</p>
            <p>This website was generated with the assistance of Large Language Models.</p>
            <p>© {{ current_year }} Alexander Kolesnikov.</p>
        </div>
    </body>
    </html>
    """

    # Prepare BibTeX entries for each citation button
    for entry in entries:
        entry_type = entry.get('ENTRYTYPE', 'article')
        entry_id = entry.get('ID', entry.get('id', ''))
        title = entry.get('title', 'No Title').replace('{', '').replace('}', '')
        # Use original_author here to keep BibTeX format
        author = entry.get('original_author', 'No Author')
        journal = entry.get('journal', 'No Journal').replace('{', '').replace('}', '')
        year = entry.get('year', 'No Year').replace('{', '').replace('}', '')

        # Construct the BibTeX entry string
        entry['bibtex'] = f"@{entry_type}{{{entry_id},\n  title = {{{title}}},\n  author = {{{author}}},\n  journal = {{{journal}}},\n  year = {{{year}}}\n}}"

    # Using Jinja2 to populate the HTML template with entries
    template = Template(html_template)
    rendered_html = template.render(
        entries=entries, 
        about_html=about_html, 
        selected_entries=selected_entries,
        current_date=datetime.now().strftime("%B %d, %Y"),
        current_year=datetime.now().year
    )

    # Write the rendered HTML to a file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)

# Main function to convert BibTeX to HTML
def main():
    try:
        # Input BibTeX string
        with open('bibtex.bib', 'r', encoding='utf-8') as f:
            bibtex_string = f.read()
    except FileNotFoundError:
        print("Error: 'bibtex.bib' file not found. Please ensure the file exists in the current directory.")
        return

    # Read BibTeX entries from string
    entries = read_bibtex_string(bibtex_string)
    # Create the HTML page and save it
    create_html(entries)
    print("Successfully generated 'index.html'.")

if __name__ == "__main__":
    main()
