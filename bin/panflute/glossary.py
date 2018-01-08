"""
Replaces +label with \gls{label} .
Replaces ++label with \glspl{label} .
Replaces +Label with \Gls{label} .
Replaces ++Label with \Glspl{label} .
"""
import string

import panflute as pf

PUNCTUATION = r'.,?!:;-_\/'


def replace_glossary(elem, doc):
    if hasattr(elem, 'text') and len(elem.text) > 1 and \
            elem.text.startswith('+'):
        # Plural if ++
        pl = 'pl' if elem.text.startswith('++') else ''

        # Last + is the start, punctuation at end not included
        start = elem.text.rfind('+') + 1
        text = elem.text[start:]
        end = min([text.find(p) for p in PUNCTUATION if text.find(p) > -1]
                  or [len(text)])

        # Extract text and determine if capitalized or not
        text, punctuation = text[:end], text[end:]
        gls = 'Gls' if text[0] in string.ascii_uppercase else 'gls'
        # lowercase text to match key
        text = text.lower()

        inl = pf.RawInline(f'\{gls}{pl}{{{text}}}', format='tex')
        if punctuation:
            return [inl, pf.Str(punctuation)]
        return inl


def main(doc=None):
    return pf.run_filter(replace_glossary, doc=doc)


if __name__ == "__main__":
    main()
