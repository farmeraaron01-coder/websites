#!/usr/bin/env python3
"""
Divi front-end HTML -> clean semantic HTML, for the CFI content migration.

Why the front end and not the REST API: WordPress returns Divi pages as literal
[et_pb_*] shortcode text in content.rendered, because Divi renders on the front
end rather than through the_content in a REST context. Verified on /residential/
— 28 raw shortcode blocks with smart-quoted attributes. The front end is the
only place the real markup exists.

What this keeps: headings, paragraphs, lists, tables, blockquotes, links,
emphasis, images. What it drops: every div and its classes (Divi's entire layout
layer), scripts, styles, and the content h1 — the new template owns the h1, so
leaving one here would produce two.
"""
import re
import sys
from html.parser import HTMLParser

KEEP = {
    'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tfoot',
    'tr', 'th', 'td', 'blockquote', 'a', 'strong', 'em', 'b', 'i', 'br', 'img',
    'sup', 'sub', 'code', 'pre',
    # native disclosure widgets — statewide's 35-question FAQ lives in these
    'details', 'summary',
}
VOID = {'br', 'img'}
DROP_TREE = {'script', 'style', 'noscript', 'svg', 'form', 'button', 'iframe', 'h1'}
ATTRS = {
    'a': {'href', 'title', 'rel', 'target'},
    'img': {'src', 'alt', 'width', 'height', 'loading', 'decoding'},
    'th': {'colspan', 'rowspan', 'scope'},
    'td': {'colspan', 'rowspan'},
}


def slice_content(html):
    """
    Cut the real content region out before parsing.

    The previous version detected the region while parsing and accepted either
    .entry-content OR id="main-content". #main-content appears ~2,300 chars
    earlier in the document, so it always won on document order and capture
    began at the article header — pulling in Divi's "by | date | category"
    byline. Worse, tracking the end by counting <div> depth drifted on Divi's
    markup and ran past </article> into #sidebar, so 15 pages absorbed the
    "Recent Posts" and "Recent Comments" widgets. 51 of 84 migrated items were
    contaminated.

    Slicing on hard landmarks instead: start after .entry-content (falling back
    to #main-content only when there is no .entry-content at all), and stop at
    the first of </article>, #sidebar, <aside> or </main>.
    """
    m = re.search(r'<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>', html)
    if m:
        start = m.end()
    else:
        m2 = re.search(r'<div[^>]*id="main-content"[^>]*>', html)
        if not m2:
            return ''
        start = m2.end()
    ends = []
    for pat in (r'</article>', r'<div[^>]*id="sidebar"', r'<aside\b', r'</main>'):
        mm = re.search(pat, html[start:])
        if mm:
            ends.append(start + mm.start())
    return html[start:min(ends)] if ends else html[start:]


class Extract(HTMLParser):
    """Keep only semantic tags from an already-sliced content region."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.inside = True
        self.suppress = 0       # >0 while inside a dropped subtree
        self.dropped_h1 = []

    def handle_starttag(self, tag, attrs):
        if tag in DROP_TREE:
            self.suppress += 1
            return
        if self.suppress:
            return

        if tag in KEEP:
            keep = ATTRS.get(tag, set())
            kept = ' '.join(
                f'{k}="{v}"' for k, v in attrs
                if k in keep and v is not None and v.strip() != ''
            )
            self.out.append(f'<{tag}{" " + kept if kept else ""}>')

    def handle_startendtag(self, tag, attrs):
        if self.inside and not self.suppress and tag in VOID:
            self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if not self.inside:
            return

        if tag in DROP_TREE:
            if self.suppress:
                self.suppress -= 1
            return
        if self.suppress:
            return

        if tag in KEEP and tag not in VOID:
            self.out.append(f'</{tag}>')

    def handle_data(self, data):
        if not self.inside or self.suppress:
            return
        if data.strip() == '' and not self.out:
            return
        self.out.append(
            data.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        )


def tidy(html):
    """Collapse whitespace and remove the empty shells Divi leaves behind."""
    s = re.sub(r'[ \t]*\n[ \t]*', '\n', html)
    s = re.sub(r'\n{3,}', '\n\n', s)
    # Repeatedly drop empty containers — removing one can empty its parent.
    for _ in range(6):
        before = s
        s = re.sub(r'<(p|li|td|th|h2|h3|h4|strong|em|b|i|a)(\s[^>]*)?>(\s|&nbsp;|<br\s*/?>)*</\1>', '', s)
        s = re.sub(r'<(ul|ol|table|thead|tbody|tr|blockquote)(\s[^>]*)?>\s*</\1>', '', s)
        if s == before:
            break
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'>\s+<', '>\n<', s)
    return s.strip()


def convert(front_end_html):
    p = Extract()
    p.feed(slice_content(front_end_html))
    return tidy(''.join(p.out))


if __name__ == '__main__':
    src = open(sys.argv[1], encoding='utf-8', errors='replace').read()
    out = convert(src)
    if len(sys.argv) > 2:
        open(sys.argv[2], 'w', encoding='utf-8').write(out)
    words = len(re.sub(r'<[^>]+>', ' ', out).split())
    tags = re.findall(r'<([a-z0-9]+)', out)
    from collections import Counter
    print(f'  {len(out)} bytes, {words} words')
    print(f'  tags: {dict(sorted(Counter(tags).items(), key=lambda x: -x[1]))}')
    print(f'  divs remaining: {out.count("<div")}   shortcodes remaining: {out.count("[et_pb")}')
    print(f'  h1 remaining: {out.count("<h1")}')


def extract_takeaways(html):
    """
    Pull a "Key Takeaways" block out of the body and return it separately.

    Divi rendered these as a bare <p> label followed by a <ul>, so the semantics
    were lost. The new template has a dedicated takeaways box, so moving them
    into meta both restores the meaning and removes a duplicate heading.

    Returns (body_without_block, [takeaway, ...]).
    """
    pat = re.compile(
        r'<(p|h2|h3|h4)(?:\s[^>]*)?>\s*(?:<strong>)?\s*key\s+takeaways\s*:?\s*(?:</strong>)?\s*</\1>\s*'
        r'<ul(?:\s[^>]*)?>(.*?)</ul>',
        re.I | re.S,
    )
    m = pat.search(html)
    if not m:
        return html, []
    items = re.findall(r'<li(?:\s[^>]*)?>(.*?)</li>', m.group(2), re.I | re.S)
    items = [re.sub(r'\s+', ' ', i).strip() for i in items]
    items = [i for i in items if re.sub(r'<[^>]+>', '', i).strip()]
    return (html[:m.start()] + html[m.end():]).strip(), items
