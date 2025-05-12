# use index.json as input to generate the title.html and description.html needed by mdict-utils
import sys, json, html

def render(obj):
    """
    Recursively render a Python object as HTML.
    - dict → <ul> of <li><strong>key</strong>: value</li>
    - list → <ol> of <li>item</li>
    - other → escaped text
    """
    if isinstance(obj, dict):
        items = []
        for k, v in obj.items():
            key = html.escape(str(k))
            items.append(f'<li><strong>{key}</strong>: {render(v)}</li>')
        return '<ul>' + ''.join(items) + '</ul>'

    elif isinstance(obj, list):
        items = ''.join(f'<li>{render(v)}</li>' for v in obj)
        return '<ol>' + items + '</ol>'

    else:
        # primitives: str, int, bool, None, etc.
        return html.escape(str(obj))

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} input.json", file=sys.stderr)
        sys.exit(1)

    in_path = sys.argv[1]
    # 1) Load JSON
    with open(in_path, encoding='utf-8') as f:
        data = json.load(f)

    # 2) Render full HTML → description.html
    body_html = render(data)
    doc = (
        '<!DOCTYPE html>'
        '<html lang="en">'
        '<head>'
          '<meta charset="UTF-8">'
          f'<title>{html.escape(in_path)}</title>'
        '</head>'
        '<body>'
          f'{body_html}'
        '</body>'
        '</html>'
    )
    with open('description.html', 'w', encoding='utf-8') as out:
        out.write(doc)

    # 3) Extract title string → title.html (no HTML tags)
    title = data.get('title', '')
    with open('title.html', 'w', encoding='utf-8') as out:
        out.write(title)

    print("Generated:")
    print("  • description.html (full HTML)")
    print("  • title.html       (just the title)")

if __name__ == '__main__':
    main()
