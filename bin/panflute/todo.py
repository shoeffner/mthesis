"""
Replaces

TODO: some todo note

with

\todo{some todo note}

and

TODO(shoeffner): some todo note

with

\todo[author=shoeffner]{some todo note}

If at least one TODO was found, a list of todo notes is included at the
top of the document (\listoftodos{}).
Optionally adds the todonotes packages to the metadata's header-includes.
"""
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
    if (isinstance(elem, pf.RawBlock)
            and elem.text.startswith(r'\missingfigure')) \
        or \
       (isinstance(elem, pf.RawInline)
            and elem.text.startswith(r'\todo')):
        doc.todocount += 1


def finalize(doc):
    todo_found = False
    for inc in doc.metadata['header-includes']:
        if isinstance(inc, pf.MetaInlines):
            for li in inc.content:
                if li.format == 'tex' and '{todonotes}' in li.text:
                    todo_found = True
    if not todo_found:
        todo_inline = pf.RawInline(r'\usepackage[]{todonotes}', format='tex')
        doc.metadata['header-includes'].append(pf.MetaInlines(todo_inline))

    if doc.todocount:
        doc.content.insert(0, pf.RawBlock(r'\listoftodos{}', format='latex'))


def main(doc=None):
    doc.todocount = 0
    return pf.run_filter(create_todos, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
