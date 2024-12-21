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
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary-color: #2563eb;
                --text-primary: #1a1a1a;
                --text-secondary: #4b5563;
                --bg-primary: #ffffff;
                --bg-secondary: #f8fafc;
                --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
                --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
                --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
            }

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Plus Jakarta Sans', sans-serif;
                line-height: 1.6;
                max-width: 1000px;
                margin: 0 auto;
                padding: 2rem;
                background-color: var(--bg-secondary);
                color: var(--text-primary);
                font-size: 0.95rem;
            }

            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 3rem;
                padding: 2rem;
                background: var(--bg-primary);
                border-radius: 1rem;
                box-shadow: var(--shadow-md);
            }

            .header-left {
                flex: 1;
            }

            .name {
                font-size: 2.2rem;
                font-weight: 600;
                margin: 0;
                background: linear-gradient(120deg, var(--primary-color), #4f46e5);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .title {
                font-size: 1.1rem;
                color: var(--text-secondary);
                margin: 0.5rem 0;
            }

            .profile-img {
                width: 150px;
                height: 150px;
                border-radius: 1rem;
                object-fit: cover;
                margin-left: 2rem;
                box-shadow: var(--shadow-lg);
                transition: transform 0.3s ease;
            }

            .profile-img:hover {
                transform: scale(1.05);
            }

            .about {
                font-size: 1rem;
                color: var(--text-primary);
                background: var(--bg-primary);
                border-radius: 1rem;
                padding: 2rem;
                margin-bottom: 3rem;
                box-shadow: var(--shadow-md);
                line-height: 1.7;
                text-align: justify;
            }

            .about a {
                color: var(--primary-color);
                text-decoration: none;
                font-weight: 500;
                transition: color 0.2s ease;
            }

            .about a:hover {
                color: #1d4ed8;
            }

            h1 {
                font-size: 1.8rem;
                font-weight: 600;
                margin: 2.5rem 0 1.5rem;
                color: var(--text-primary);
                position: relative;
                padding-bottom: 0.5rem;
            }

            h1::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 60px;
                height: 4px;
                background: var(--primary-color);
                border-radius: 2px;
            }

            .selected-publications-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 1.5rem;
                margin-bottom: 3rem;
            }

            .selected-publication-card {
                background: var(--bg-primary);
                border-radius: 1rem;
                overflow: hidden;
                box-shadow: var(--shadow-md);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .selected-publication-card:hover {
                transform: translateY(-5px);
                box-shadow: var(--shadow-lg);
            }

            .selected-publication-card img {
                width: 100%;
                height: 180px;
                object-fit: contain;
                background: #f8f8f8;
                padding: 10px;
            }

            .selected-publication-card p {
                padding: 1rem;
                font-size: 0.95rem;
                color: var(--text-primary);
            }

            .entry {
                background: var(--bg-primary);
                border-radius: 1rem;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: var(--shadow-md);
                display: flex;
                gap: 2rem;
                transition: transform 0.3s ease;
            }

            .entry:hover {
                transform: translateX(5px);
            }

            .entry-content {
                flex: 1;
            }

            .entry-title {
                font-size: 1.15rem;
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: 1rem;
            }

            .author, .year, .journal {
                color: var(--text-secondary);
                margin-bottom: 0.5rem;
                font-size: 0.95rem;
            }

            .links {
                display: flex;
                gap: 1rem;
                margin-top: 1rem;
            }

            .links a, .cite-button {
                padding: 0.4rem 0.9rem;
                border-radius: 0.5rem;
                text-decoration: none;
                font-weight: 500;
                transition: all 0.2s ease;
                font-size: 0.9rem;
            }

            .links a {
                background: #e0e7ff;
                color: var(--primary-color);
            }

            .links a:hover {
                background: #c7d2fe;
            }

            .cite-button {
                background: var(--primary-color);
                color: white;
                border: none;
                cursor: pointer;
            }

            .cite-button:hover {
                background: #1d4ed8;
            }

            .citation-text {
                margin-top: 1rem;
                padding: 1rem;
                background: var(--bg-secondary);
                border-radius: 0.5rem;
                font-family: monospace;
                font-size: 0.85rem;
                display: none;
            }

            .preview img {
                max-width: 250px;
                border-radius: 0.5rem;
                box-shadow: var(--shadow-sm);
            }

            .footer {
                margin-top: 4rem;
                padding: 2rem;
                background: var(--bg-primary);
                border-radius: 1rem;
                box-shadow: var(--shadow-md);
                text-align: center;
                color: var(--text-secondary);
                font-size: 0.9rem;
            }

            @media (max-width: 768px) {
                body {
                    padding: 1rem;
                }

                .header {
                    flex-direction: column;
                    text-align: center;
                }

                .profile-img {
                    margin: 1rem 0 0 0;
                }

                .entry {
                    flex-direction: column;
                }

                .preview img {
                    max-width: 100%;
                }

                .links {
                    flex-wrap: wrap;
                }
            }
        </style>
        <script>
            function toggleCitation(id) {
                const citationElement = document.getElementById(id);
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
