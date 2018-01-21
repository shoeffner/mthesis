"""
Replaces @file:PATH with file contents. PATH can not contain spaces.
"""
import panflute as pf


def fileinput(elem, doc):
    if (isinstance(elem, pf.Para)
            and len(elem.content) == 1
            and isinstance(elem.content[0], pf.Cite)
            and isinstance(elem.content[0].content[0], pf.Str)):
        pathstr = elem.content[0].content[0].text[6:]
        pf.debug(f'Including {pathstr}')
        with open(pathstr, 'r') as f:
            return pf.convert_text(f.read())


def main(doc=None):
    return pf.run_filter(fileinput, doc=doc)


if __name__ == "__main__":
    main()
