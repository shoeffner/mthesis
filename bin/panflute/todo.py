import panflute as pf


def create_todos(elem, doc):
    if isinstance(elem, pf.Para) and len(elem.content):
        first = elem.content[0]
        if isinstance(first, pf.Str) and first.text.startswith('TODO'):
            doc.todocount += 1
            content = pf.stringify(pf.Para(*elem.content[1:])).strip()
            author = first.text[5:-2] if first.text[4] == '(' else ''
            if author:
                author = f'[author={author}]'
            return pf.RawBlock('\\todo' + author + '{' + content + '}',
                               format='latex')


def finalize(doc):
    if doc.todocount:
        doc.content.insert(0, pf.RawBlock(r'\listoftodos{}', format='latex'))


def main(doc=None):
    doc.todocount = 0
    return pf.run_filter(create_todos, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
