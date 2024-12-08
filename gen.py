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
    # Adapt author names to "First name Last name" format for display and "Last name, First name" for BibTeX
    for entry in bib_database.entries:
        if 'author' in entry:
            authors = entry['author'].split(' and ')
            formatted_authors_display = []
            formatted_authors_bibtex = []
            for author in authors:
                names = author.split(', ')
                if len(names) == 2:
                    first_last = f"{names[1]} {names[0]}"
                    last_first = f"{names[0]}, {names[1]}"
                    # Bold Alexander Kolesnikov's name in display format
                    if 'Alexander Kolesnikov' in first_last:
                        first_last = f"<b>{first_last}</b>"
                    formatted_authors_display.append(first_last)
                    formatted_authors_bibtex.append(last_first)
                else:
                    formatted_authors_display.append(author)
                    formatted_authors_bibtex.append(author)
            entry['author_display'] = ', '.join(formatted_authors_display)
            entry['author_bibtex'] = ' and '.join(formatted_authors_bibtex)
    return bib_database.entries

# Function to create an HTML page from the parsed BibTeX data and print it
def create_html(entries):
    # Convert the About Me section from Markdown to HTML
    about_markdown = """
    I am an ML research scientist, who is passionate about pushing the research frontier in deep learing, and in particular interested in the multimodal intelligence. Some of my prior achivements include training SOTA vision models ([ImageNet SOTA in 2019](https://arxiv.org/abs/1912.11370), [ImageNet SOTA 2020](https://arxiv.org/abs/2010.11929), [ImageNet SOTA 2021](https://arxiv.org/abs/2106.04560)) and SOTA open weight models: [SigLIP](https://arxiv.org/abs/2303.15343) and [PaliGemma](https://github.com/google-research/big_vision/blob/main/big_vision/configs/proj/paligemma/README.md), as well as work in neural architectures: [BiT](https://arxiv.org/abs/1912.11370), [ViT](https://arxiv.org/abs/2010.11929), [MLP-Mixer](https://arxiv.org/abs/2105.01601) and [FlexiViT](https://arxiv.org/abs/2212.08013). Recently I have been focused in unifying, simplifying and scaling multimodal deep learning: [UViM](https://arxiv.org/abs/2205.10337), [Vision with rewards](https://arxiv.org/abs/2302.08242), [JetFormer](https://arxiv.org/abs/2411.19722).

    I also enjoy writing flexible and high-performance research infrastructure (especially in Jax). A large part of it is opensourced: [big_vision](https://github.com/google-research/big_vision).

    I have been at Google Brain (now DeepMind) since 2018, working in the beautiful city of Zürich. Previously, I did my PhD at [ISTA](https://ist.ac.at/en/home/) under the supervision of [Christoph Lampert](https://cvml.ista.ac.at/), where I was working on weakly-supervised learning and generative image models.

    Contact me at `a@kolesnikov.ch`.
    """
    about_html = markdown.markdown(about_markdown)

    # A simple HTML template using Jinja2 syntax
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Personal page of Alexander Kolesnikov</title>
        <style>
            /* Your existing CSS here */
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
                {% if entry.author_display %}<div class="author">Authors: {{ entry.author_display|safe }}</div>{% endif %}
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
            entry.get('author_bibtex', ''),
            entry.get('journal', ''),
            entry.get('year', '')
        )

    # Using Jinja2 to populate the HTML template with entries
    template = Template(html_template)
    rendered_html = template.render(entries=entries, about_html=about_html)

    # Write the rendered HTML to a file
    with open("index.html", "w") as f:
        f.write(rendered_html)

# Main function to convert BibTeX to HTML
def main():
    # Input BibTeX string
    with open('bibtex.bib', 'r') as f:
        bibtex_string = f.read()

    # Read BibTeX entries from string
    entries = read_bibtex_string(bibtex_string)
    # Create the HTML page
    create_html(entries)

if __name__ == "__main__":
    main()

