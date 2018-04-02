#!/usr/bin/env python
"""
%prog MODE FILES...

Post-processes HTML and Latex files output by Sphinx.
MODE is either 'html' or 'tex'.

"""
import re, optparse

def main():
    p = optparse.OptionParser(__doc__)
    options, args = p.parse_args()

    if len(args) < 1:
        p.error('no mode given')

    mode = args.pop(0)

    if mode not in ('html', 'tex'):
        p.error('unknown mode %s' % mode)

    for fn in args:
        f = open(fn, 'r')
        try:
            if mode == 'html':
                lines = process_html(fn, f.readlines())
            elif mode == 'tex':
                lines = process_tex(f.readlines())
        finally:
            f.close()

        f = open(fn, 'w')
        f.write("".join(lines))
        f.close()

def process_html(fn, lines):
    return lines

def process_tex(lines):
    """
    Remove unnecessary section titles from the LaTeX file.

    And fix autosummary LaTeX bug in Sphinx < 1.7.3
    (cf https://github.com/sphinx-doc/sphinx/issues/4790)

    Force description of parameters to line after parameter name itself.
    """
    new_lines = []
    for line in lines:
        line = re.sub(r'^\s*\\strong{See Also:}\s*$', r'\paragraph{See Also}', line)

        line = line.replace(r'p{0.5\linewidth}', r'\X{1}{2}')

        line = re.sub(r'^(\\item\[.*\] \\leavevmode)(^{)', '\g<1>\g<2>\\par ', line)

        line = re.sub(r'^(\\item\[.*\] \\leavevmode{\[}.*{\]})', '\g<1>\\par ', line)

        if (line.startswith(r'\section{scipy.')
            or line.startswith(r'\subsection{scipy.')
            or line.startswith(r'\subsubsection{scipy.')
            or line.startswith(r'\paragraph{scipy.')
            or line.startswith(r'\subparagraph{scipy.')
            ):
            pass # skip!
        else:
            new_lines.append(line)
    return new_lines


if __name__ == "__main__":
    main()
