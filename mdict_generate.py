import sys
import re
from tqdm import tqdm

# -----------------------------------------------------------------------------
# Dummy AttributedDict so that eval("AttributedDict([...])") yields a plain dict
# -----------------------------------------------------------------------------
class AttributedDict(dict):
    def __init__(self, items):
        super().__init__(items)

# -----------------------------------------------------------------------------
# Recursive renderer: dict/list/str → HTML
# -----------------------------------------------------------------------------
def json_to_html(node):
    if isinstance(node, str):
        return node
    elif isinstance(node, list):
        return ''.join(json_to_html(item) for item in node)
    elif isinstance(node, dict):
        tag     = node.get('tag', 'div')
        content = json_to_html(node.get('content', ''))
        data    = node.get('data', {})
        attrs = ''.join(
            f' {k}' if v == '' else f' {k}="{v}"'
            for k, v in data.items()
        )
        return f'<{tag}{attrs}>{content}</{tag}>'
    else:
        return ''

# -----------------------------------------------------------------------------
# Inline CSS for vertical Japanese layout (all on one line)
# -----------------------------------------------------------------------------
CSS = (
    '<style>'
    '.vertical{writing-mode:vertical-rl;text-orientation:upright;line-height:1.5;}'
    '.vertical .熟語{font-size:1.5em;line-height:1;}'
    '.vertical .S,.vertical .E{margin:0;padding:0;display:inline;letter-spacing:0;}'
    '.vertical .E{margin-block-start:-0.2em;}'
    '</style>'
)

def wrap_vertical(fragment):
    return '<div class="vertical">' + fragment + '</div>'

def wrap_as_single_line_html(vertical_div):
    return (
        '<html>'
        '<head>' + CSS + '</head>'
        '<body>' + vertical_div + '</body>'
        '</html>'
    )

# -----------------------------------------------------------------------------
# Process one headword/content block → (headword, single_line_html)
# -----------------------------------------------------------------------------
def process_block(block_text):
    m = re.search(r'^headword:\s*(.+)$', block_text, re.MULTILINE)
    if not m:
        return None
    headword = m.group(1).strip()
    m = re.search(r'^content:\s*(\[.+)$', block_text, re.DOTALL | re.MULTILINE)
    if not m:
        return None
    literal = m.group(1).strip()
    data = eval(literal, {'AttributedDict': AttributedDict})
    node = data[5][0]
    inner_html   = json_to_html(node)
    vertical_div = wrap_vertical(inner_html)
    single_line  = wrap_as_single_line_html(vertical_div)
    return headword, single_line

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} entries.txt output.txt", file=sys.stderr)
        sys.exit(1)

    in_path, out_path = sys.argv[1], sys.argv[2]
    text = open(in_path, encoding='utf-8').read().strip()
    blocks = re.split(r'\n\s*\n+', text)

    with open(out_path, 'w', encoding='utf-8') as out:
        for block in tqdm(blocks, desc="Processing entries"):
            result = process_block(block)
            if result:
                headword, html_line = result
                out.write(headword + "\n")
                out.write(html_line + "\n")
                out.write("</>\n")
    print(f"Done. Output written to {out_path}")

if __name__ == '__main__':
    main()
