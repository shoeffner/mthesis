"""Reads a LaTeX file from stdin and writes it to stdout.
Replaces all captions without a short caption but containing ;;
with a caption with a short caption. See the doctest for examples.
"""

import sys


def process_caption(caption):
    r"""Converts the captions if ;; are present.

    Short caption exists: Keep it!
    >>> process_caption('\\caption[Short]{Long caption}')
    '\\caption[Short]{Long caption}'

    No short caption but ;; contained: Split
    >>> process_caption('\\caption{Short;;Long caption}')
    '\\caption[Short]{Long caption}'

    >>> process_caption('\\caption{Short caption\nmore short;;Long caption}')
    '\\caption[Short caption\nmore short]{Long caption}'

    Long caption without ;;: Keep
    >>> process_caption('\\caption{Long caption only}')
    '\\caption{Long caption only}'
    """
    if ';;' in caption:
        start = caption.index(r'{') + 1
        split = caption.index(r';;')
        next = split + 2
        return r'\caption[' + caption[start:split] + r']{' + caption[next:]

    return caption


def process_lines(lines_in):
    """Process captions in a file, parsing it line by line.

    >>> process_lines(['\\hypertarget{', '\\caption{short;;long}', '}'])
    ['\\hypertarget{', '\\caption[short]{long}', '}']

    """
    incaption = False
    caption = None
    lines_out = []
    for line in lines_in:
        if incaption:
            caption += line
            if caption.count(r'{') - caption.count(r'}') == 0:
                lines_out.append(process_caption(caption))
                incaption = False
                caption = None
        elif r'\caption{' in line:
            incaption = True
            caption = line
        else:
            lines_out.append(line)
    return lines_out


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        lines_in = f.readlines()
    lines_out = process_lines(lines_in)
    with open(sys.argv[1], 'w') as f:
        print(''.join(lines_out), file=f, end='')
