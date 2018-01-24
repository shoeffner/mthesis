"""
Replaces @file:PATH with file contents. PATH can not contain spaces.
"""
import panflute as pf


def fileinput(elem, doc):
    pathstr = None
    if (isinstance(elem, pf.Para)
            and len(elem.content) == 1
            and isinstance(elem.content[0], pf.Cite)
            and isinstance(elem.content[0].content[0], pf.Str)):
        pathstr = elem.content[0].content[0].text
        if not pathstr.startswith('@file:'):
            return
        pathstr = pathstr[6:]
        try:
            with open(pathstr, 'r') as f:
                return pf.convert_text(f.read())
        except FileNotFoundError:
            pf.debug(f'Can not include {pathstr}: File not found.')
    elif isinstance(elem, pf.Cite) and elem.content[0].text.startswith('@file:'):
        if '.si' in elem.content[0].text:
            pathstr = elem.content[0].text[6:]
            try:
                with open(pathstr, 'r') as f:
                    return pf.RawInline(f.read().strip(), format='tex')
            except FileNotFoundError:
                pf.debug(f'Can not include {pathstr}: File not found.')


def main(doc=None):
    return pf.run_filter(fileinput, doc=doc)


if __name__ == "__main__":
    main()
