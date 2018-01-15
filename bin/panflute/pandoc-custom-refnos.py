"""
Replaces @TOKEN:reference with \Cref{reference}.
"""

import panflute as pf

TOKENS = {
    'sl': lambda x: x,
    'cl': lambda x: x,
    'sc': lambda x: x,
    'eq': lambda x: x,
    'sec': lambda x: x[4:],
    'chap': lambda x: x[5:],
}


def replace_refs(elem, doc):
    if isinstance(elem, pf.Cite):
        ref = elem.content[0].text[1:]
        for token in TOKENS.keys():
            if ref.startswith(f'{token}:'):
                ref = TOKENS[token](ref)
                return pf.RawInline(f'\\Cref{{{ref}}}', format='tex')


def main(doc=None):
    return pf.run_filter(replace_refs, doc=doc)


if __name__ == "__main__":
    main()
