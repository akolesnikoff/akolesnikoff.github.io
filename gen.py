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
I am an ML research scientist, who is passionate about pushing the research frontier in deep learning, and in particular interested in multimodal intelligence. Currently I am a member of technical staff at OpenAI, working on multimodal intelligence.

Some of my prior achievements include training SOTA vision models ([ImageNet SOTA in 2019](https://arxiv.org/abs/1912.11370), [ImageNet SOTA 2020](https://arxiv.org/abs/2010.11929), [ImageNet SOTA 2021](https://arxiv.org/abs/2106.04560)) and SOTA open weight models: [SigLIP](https://arxiv.org/abs/2303.15343) and [PaliGemma](https://github.com/google-research/big_vision/blob/main/big_vision/configs/proj/paligemma/README.md), as well as work in neural architectures: [BiT](https://arxiv.org/abs/1912.11370), [ViT](https://arxiv.org/abs/2010.11929), [MLP-Mixer](https://arxiv.org/abs/2105.01601) and [FlexiViT](https://arxiv.org/abs/2212.08013). Recently, I have been focused on unifying, simplifying, and scaling multimodal deep learning: [UViM](https://arxiv.org/abs/2205.10337), [Vision with Rewards](https://arxiv.org/abs/2302.08242), [JetFormer](https://arxiv.org/abs/2411.19722).

I also enjoy writing flexible and high-performance research infrastructure (especially in Jax). A large part of it is open-sourced: [big_vision](https://github.com/google-research/big_vision).

Previously, I have been at Google Brain (now Google DeepMind) did my PhD at [ISTA](https://ist.ac.at/en/home/) under the supervision of [Christoph Lampert](https://cvml.ista.ac.at/), where I worked on weakly-supervised learning and generative image models.

Contact me at `a@kolesnikov.ch`.
"""
    about_html = markdown.markdown(about_markdown)

    # A simple HTML template using Jinja2 syntax
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Personal Page of Alexander Kolesnikov</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background-color: #f9f9f9;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 20px;
            }
            .header-left {
                flex: 1;
                /* Ensures that name/title are left aligned */
            }
            .name {
                font-size: 2em;
                font-weight: bold;
                margin: 0;
            }
            .title {
                font-size: 1.2em;
                color: #555;
                margin: 5px 0 0 0;
            }
            .profile-img {
                width: 120px;
                height: 120px;
                border-radius: 50%;
                object-fit: cover;
                margin-left: 20px;
            }
            .about {
                font-size: 1em;
                color: #333;
                background-color: #fff;
                border-radius: 5px;
                text-align: justify;
                padding: 10px;
                margin-bottom: 40px;
            }
            .entry {
                margin-bottom: 20px;
                display: flex;
                align-items: flex-start;
                background-color: #fff;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .entry-content {
                flex: 1;
                text-align: justify;
            }
            .entry-title {
                font-weight: bold;
                font-size: 1.2em;
                margin-bottom: 5px;
            }
            .author, .year, .journal, .links {
                margin-top: 5px;
                color: #555;
            }
            .links {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-top: 10px;
            }
            .links a {
                text-decoration: none;
                color: #0066cc;
            }
            .preview {
                margin-left: 20px;
            }
            .preview img {
                max-width: 225px;
                height: auto;
                margin-top: 10px;
                border-radius: 5px;
            }
            .cite-button {
                background-color: #0066cc;
                color: white;
                border: none;
                padding: 5px 10px;
                cursor: pointer;
                border-radius: 5px;
                transition: background-color 0.3s;
            }
            .cite-button:hover {
                background-color: #004999;
            }
            .citation-text {
                margin-top: 10px;
                padding: 10px;
                border: 1px solid #ccc;
                background-color: #f9f9f9;
                display: none;
                white-space: pre-wrap;
                border-radius: 5px;
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

        <h1>Bibliography</h1>
        {% for entry in entries %}
        <div class="entry">
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
    </body>
    </html>
    """

    # Prepare BibTeX entries for each citation button
    for entry in entries:
        entry_type = entry.get('ENTRYTYPE', 'article').capitalize()
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
    rendered_html = template.render(entries=entries, about_html=about_html)

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

