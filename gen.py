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
import html

# Function to read the BibTeX string and parse it
def read_bibtex_string(bibtex_string):
    bibtex_file = StringIO(bibtex_string)
    parser = BibTexParser()
    parser.customization = bibtexparser.customization.convert_to_unicode
    bib_database = bibtexparser.load(bibtex_file, parser=parser)
    # Adapt author names to "First name Last name" format
    for entry in bib_database.entries:
        if 'author' in entry:
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

# Function to create an HTML page from the parsed BibTeX data and print it
def create_html(entries):
    # Convert the About Me section from Markdown to HTML
    about_markdown = """
I am an ML research scientist, who is passionate about pushing the research frontier in deep learing, and in particular interested in the multimodal intelligence. Some of my prior achivements include training SOTA vision models ([ImageNet SOTA in 2019](https://arxiv.org/abs/1912.11370), [ImageNet SOTA 2020](https://arxiv.org/abs/2010.11929), [ImageNet SOTA 2021](https://arxiv.org/abs/2106.04560)) and SOTA open weight models: [SigLIP](https://arxiv.org/abs/2303.15343) and [PaliGemma](https://github.com/google-research/big_vision/blob/main/big_vision/configs/proj/paligemma/README.md), as well as work in neural architectures: [BiT](https://arxiv.org/abs/1912.11370), [ViT](https://arxiv.org/abs/2010.11929), [MLP-Mixer](https://arxiv.org/abs/2105.01601) and [FlexiViT](https://arxiv.org/abs/2212.08013). Currently I am mostly focused on unifying, simplifying and scaling multimodal deep learning: [UViM](https://arxiv.org/abs/2205.10337), [Vision with rewards](https://arxiv.org/abs/2302.08242).

I also enjoy writing flexible and high-performance research infrastructure (especially in Jax). A large part of it is opensourced: [big_vision](https://github.com/google-research/big_vision).

I have been at Google Brain (now DeepMind) since 2018, working in the beautiful city of Zürich. Previously, I did my PhD at [ISTA](https://ist.ac.at/en/home/) under the supervision of [Christoph Lampert](https://cvml.ista.ac.at/), where I was working on weakly-supervised learning and generative image models.

Contact me at `a@akolesnikov.ch`.
"""
    about_html = markdown.markdown(about_markdown)

    # A simple HTML template using Jinja2 syntax
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Personal page of Alexander Kolesnikov</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: auto;
                padding: 20px;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .name {
                font-size: 2em;
                font-weight: bold;
            }
            .title {
                font-size: 1.2em;
                color: #555;
            }
            .about {
                margin-top: 20px;
                font-size: 1em;
                color: #333;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
                text-align: left;
                }
            .entry {
                margin-bottom: 20px;
                display: flex;
                align-items: flex-start;
            }
            .entry-content {
                flex: 1;
            }
            .entry-title {
                font-weight: bold;
                font-size: 1.2em;
            }
            .author, .year, .journal, .links {
                margin-top: 5px;
                color: #555;
            }
            .links {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .links a {
                text-decoration: none;
                color: #0066cc;
            }
            .preview {
                margin-left: 20px;
            }
            .preview img {
                max-width: 225px; /* 50% wider than original */
                height: auto;
                margin-top: 10px;
            }
            .cite-button {
                background-color: #0066cc;
                color: white;
                border: none;
                padding: 5px 10px;
                cursor: pointer;
                border-radius: 5px;
            }
            .citation-text {
                margin-top: 10px;
                padding: 10px;
                border: 1px solid #ccc;
                background-color: #f9f9f9;
                display: none;
                white-space: pre-wrap;
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
            <div class="name">Alexander Kolesnikov</div>
            <div class="title">Staff Research Scientist at Google DeepMind</div>
            <div class="about">
                {{ about_html | safe }}
            </div>
        </div>

        <h1>Bibliography</h1>
        {% for entry in entries %}
        <div class="entry">
            <div class="entry-content">
                <div class="entry-title">{{ entry.title }}</div>
                {% if entry.author %}<div class="author">Authors: {{ entry.author|safe }}</div>{% endif %}
                {% if entry.year %}<div class="year">Year: {{ entry.year }}</div>{% endif %}
                {% if entry.journal %}<div class="journal">Journal: {{ entry.journal }}</div>{% endif %}
                <div class="links">
                    {% if entry.arxiv %}<a href="https://arxiv.org/abs/{{ entry.arxiv }}" target="_blank">arXiv</a>{% endif %}
                    {% if entry.pdf %}<a href="{{ entry.pdf }}" target="_blank">PDF</a>{% endif %}
                    {% if entry.code %}<a href="{{ entry.code }}" target="_blank">Code</a>{% endif %}
                    <button class="cite-button" onclick="toggleCitation('citation_{{ loop.index }}')">Cite</button>
                </div>
                <div id="citation_{{ loop.index }}" class="citation-text" style="display: none;">{{ entry.bibtex | replace('\n', '<br>') | safe }}</div>
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
        entry['bibtex'] = "@{}{{{},\n  title = {{{}}},\n  author = {{{}}},\n  journal = {{{}}},\n  year = {{{}}}\n}}".format(
            entry.get('ENTRYTYPE', 'article'),
            entry.get('ID', ''),
            entry.get('title', ''),
            entry.get('author', ''),
            entry.get('journal', ''),
            entry.get('year', '')
        )

    # Using Jinja2 to populate the HTML template with entries
    template = Template(html_template)
    rendered_html = template.render(entries=entries, about_html=about_html)

    # Print the rendered HTML
    with open("index.html", "w") as f:
        f.write(rendered_html)

# Main function to convert BibTeX to HTML
def main():
    # Input BibTeX string
    with open('bibtex.bib', 'r') as f:
      bibtex_string = f.read()

    # Read BibTeX entries from string
    entries = read_bibtex_string(bibtex_string)
    # Create the HTML page and print it
    create_html(entries)

if __name__ == "__main__":
    main()
