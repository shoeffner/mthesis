"""
Replaces @TOKEN:reference with \Cref{reference}.
"""

import panflute as pf


def is_code(line):
    for comment in ['#', '//']:
        if line.strip().startswith(comment):
            return False
    return True


def replace_refs(elem, doc):
    if isinstance(elem, pf.CodeBlock) and 'stripcomments' in elem.classes:
        lines = elem.text.splitlines()
        if 'lines' in elem.attributes:
            pf.debug(elem.attributes['lines'])
            nl = []
            for r in elem.attributes['lines'].split(','):
                if ':' in r:
                    f, t = r.split(':')
                elif '-' in r:
                    f, t = r.split('-')
                else:
                    f, t = r, r
                f, t = int(f), int(t)
                nl += lines[f - 1:t + 1]
            lines = nl

        text = '\n'.join(l for l in lines if is_code(l))
        elem.text = text


def main(doc=None):
    return pf.run_filter(replace_refs, doc=doc)


if __name__ == "__main__":
    main()
