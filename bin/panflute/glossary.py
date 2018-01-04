"""
Replaces +label with \gls{label} .
"""
import panflute as pf

PUNCTUATION = r'.,?!:;-_\/'


def replace_glossary(elem, doc):
    if hasattr(elem, 'text') and elem.text.startswith('+'):
        end = -1 if elem.text[-1] in PUNCTUATION else len(elem.text)
        inl = pf.RawInline(f'\gls{{{elem.text[1:end]}}}', format='tex')
        if end < 0:
            return [inl, pf.Str(elem.text[-1])]
        return inl


def main(doc=None):
    return pf.run_filter(replace_glossary, doc=doc)


if __name__ == "__main__":
    main()
