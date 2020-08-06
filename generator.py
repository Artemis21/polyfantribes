import markdown
from markdown.extensions import smarty, toc
from pymdownx import extra, details, escapeall, smartsymbols, emoji
from MarkdownBlankLine.blankline import BlankLineExtension

from css_html_js_minify import css_minify, html_minify
from css_html_js_minify.js_minifier import js_minify_keep_comments

import os
import shutil
import re
import urllib.parse


def fill_template(template: str, **values):
    with open(f'templates/{template}.html') as f:
        raw = f.read()
    for name in values:
        raw = raw.replace(f'{{{{ {name} }}}}', values[name])
    return raw


def convert_badges(markdown: str):
    """Convert badges in markdown."""
    badges = re.findall(
        r'!\[(.+?)\]\(https://img\.shields\.io/badge/(.+?)-(.+)-(.+?)\)',
        markdown
    )
    for alt, name, value, colour in badges:
        old = '![{}](https://img.shields.io/badge/{}-{}-{})'.format(
            alt, name, value, colour
        )
        new = '{}: {}'.format(
            name.title(),
            urllib.parse.unquote(value).replace('--', '-')
        )
        markdown = markdown.replace(old, new)
    return markdown


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
    content = markdown.markdown(convert_badges(raw_md), extensions=exts)
    content = content.replace('<table>', '<div class="table-wrapper"><table>')
    content = content.replace('</table>', '</table></div>')
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
    print(' Generating tribes...')
    tribes = {}
    for file in os.listdir('tribes'):
        name = file.replace('.md', '')
        print(f'  Generating tribe {name.title()}...', end=' ')
        title = 'Home' if name == 'index' else name.title()
        tribes[f'tribes/{name}.html'] = get_document(
            f'tribes/{file}', 'tribe', title=name.title()
        )
        print('  Done')
    print(' Done')
    return tribes


def get_static():
    print(' Processing static files...')
    static = {}
    print('  Gathering from static dir...', end=' ')
    files = [f'static/{file}' for file in os.listdir('static')]
    print('Done')
    print('  Gathering from images dir...', end=' ')
    for file in os.listdir('images'):
        files.append(f'images/{file}')
    print('Done')
    print('  Minifying static files...')
    for path in files:
        print(f'   Processing static file at {path}...')
        print(f'    Reading static file at {path}...', end=' ')
        with open(path, 'rb') as f:
            raw = f.read()
        print('Done')
        if path.endswith('.js'):
            print(f'    Minifying JS file at {path}...', end=' ')
            raw = js_minify_keep_comments(raw.decode()).encode()
            print('Done')
        elif path.endswith('.css'):
            print(f'    Minifying CSS file at {path}...', end=' ')
            raw = css_minify(raw.decode()).encode()
            print('Done')
        static[path] = raw
        print('   Done')
    print('  Done')
    print(' Done')
    return static


def get_other():
    print(' Adding other files...', end=' ')
    other = {
        '.nojekyll': b'',
        'index.html': get_document(
            'README.md', 'document', title='PolyFanTribes Home'
        ),
        'CNAME': b'fantribes.polytopia.fun'
    }
    print('Done')
    return other


def write_files():
    print('Generating site...')
    files = {**get_tribes(), **get_static(), **get_other()}
    if os.path.exists('docs'):
        print(' Removing existing folder...', end=' ')
        shutil.rmtree('docs')
        print('Done')
    print(' Creating folder...', end=' ')
    os.mkdir('docs')
    print('Done')
    print(' Writing files...')
    for path in files:
        print(f'  Writing file {path}...')
        fullpath = f'docs/{path}'
        print('   Making necessary folders...', end=' ')
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        print('Done')
        print(f'   Writing file to {fullpath}...', end=' ')
        with open(fullpath, 'wb') as f:
            f.write(files[path])
        print('Done')
        print('  Done')
    print(' Done')
    print('Done')


if __name__ == '__main__':
    write_files()
