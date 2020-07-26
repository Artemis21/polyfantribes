import markdown
from markdown.extensions import smarty, toc
from pymdownx import extra, details, escapeall, smartsymbols, emoji
from MarkdownBlankLine.blankline import BlankLineExtension

from css_html_js_minify import css_minify, html_minify
from css_html_js_minify.js_minifier import js_minify_keep_comments

import os
import shutil


def fill_template(template: str, **values):
    with open(f'templates/{template}.html') as f:
        raw = f.read()
    for name in values:
        raw = raw.replace(f'{{{{ {name} }}}}', values[name])
    return raw


def md2html(raw_md):
    """Markdown to HTML converter."""
    exts = [
        smarty.SmartyExtension(),
        toc.TocExtension(anchorlink=True),
        emoji.EmojiExtension(emoji_index=emoji.gemoji),
        BlankLineExtension(),
        extra.ExtraExtension(),
        details.DetailsExtension(),
        escapeall.EscapeAllExtension(),
        smartsymbols.SmartSymbolsExtension(),
    ]
    content = markdown.markdown(raw_md, extensions=exts)
    return content


def get_document(document: str, template: str, **values):
    """Get a markdown document (as HTML)."""
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        document
    )
    with open(path) as f:
        raw = f.read()
    return html_minify(
        fill_template(template, document=md2html(raw), **values)
    ).encode()


def get_tribes():
    tribes = {}
    for file in os.listdir('tribes'):
        name = file.replace('.md', '')
        title = 'Home' if name == 'index' else name.title()
        tribes[f'tribes/{name}.html'] = get_document(
            f'tribes/{file}', 'tribe', name=name
        )
    return tribes


def get_static():
    static = {}
    files = [f'static/{file}' for file in os.listdir('static')]
    for file in os.listdir('images'):
        files.append(f'images/{file}')
    for path in files:
        with open(path, 'rb') as f:
            raw = f.read()
        if path.endswith('.js'):
            raw = js_minify_keep_comments(raw.decode()).encode()
        elif path.endswith('.css'):
            raw = css_minify(raw.decode()).encode()
        static[path] = raw
    return static


def get_other():
    return {
        '.nojekyll': b'',
        'index.html': get_document(
            'README.md', 'document', name='PolyFanTribes Home'
        ),
    #    'CNAME': b'polytopia.fun'
    }


def write_files():
    files = {**get_tribes(), **get_static(), **get_other()}
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.mkdir('docs')
    for path in files:
        fullpath = f'docs/{path}'
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        with open(fullpath, 'wb') as f:
            f.write(files[path])


if __name__ == '__main__':
    write_files()
