## Next house Pokémon door signs scripts

This repository contains the code used to make Pokémon door signs for Next House,
with input taken from a csv exported from Google Forms.
The code downloads images of Pokémon specified by the input
and generates a XeLaTeX document for compilation.
We compile with XeLaTeX for Unicode support.
A large difficulty is dealing with special cases in the data,
so a big effort was put into producing helpful error messages.

### Dependencies
- Python (pip: requests, beautifulsoup4, emoji)
- XeLaTeX
- DejaVu Sans font
- Noto Sans font

### Instructions for making door signs
- clone repository
- Export csv from google form to `form_responses.csv`
- ensure `load_data.py` matches headers on the google form / the csv
- run `python main.py form_responses.csv out.tex`, **read the warnings**!
- clean the spreadsheet as much as you can, redownload csv
  - if there are images you can't find, just ignore them.
    we'll manually deal with them later
  - this might involve emailing people for clarifications on their image
- rerun `python main.py form_responses.csv out.tex`
- [optional] compress images: (requires imagemagick)
  run `mogrify -resize 1000\> *.png` inside the images directory.
  the `1000\>` means shrink larger images to 1000px
- run `xelatex out.tex`
  (takes around 8 minutes for ~200 signs, 3 minutes if images compressed)
  **read the warnings**!!! look at the debugging section for common errors.
- look through `out.pdf` and clean up things in the following list
  (in order of decreasing priority):
  - manually add images to images folder,
    manually edit `out.tex` file to reflect these
  - read the comments for special requests
  - "Class of GRA" -> "GRA" and other similar cases
    related to special years or courses
  - special notes like "Course [do not include]"
  - people use a lot of weird unicode.
    you can try to debug the TeX (see debugging section), or delete the corresponding lines in the tex file
    and make those manually in google docs or something.
    use a font similar to DejaVu Sans for consistency
  - text too long and overflows to next page
    (try making the image smaller,
     or adding `\small` inside of the `{}` containing the text)
  - resize some of the images that look too big/small
    (change the `width=0.5\textwidth` part)
  - fix overfull hboxes (text flowing off the right edge)
  - check that consecutive spaces in a row are intentional
- recompile `xelatex out.tex` and look over output until satisfactory
- print 6 on a page, no margins, single sided
  - remember the manually made ones
- write room numbers on back of paper for organization
- cut and distribute

### Debugging
#### Some emojis don't work
Some unicode characters have both text and picture presentations, specified by an additional Unicode codepoint. For example, (U+1f171) in text is '🅱' (U+1f171) and in emoji is '🅱️' (U+1f171 U+fe0f). However, the `twemojis` TeX package does not accept the emoji version `\texttwemoji{1f171-fe0f}`, and requires the single codepoint`\texttwemoji{1f171}`. The fix is to manually remove the `-fe0f` part of the generated TeX.

A list of emojis that this breaks for is [here](http://unicode.org/emoji/charts/emoji-variants.html).
This can probably be automated, but I don't know if all `-fe0f`s can be safely removed.

Here is an upstream issue: https://gitlab.com/rossel.jost/latex-twemojis/-/issues/6.

#### Other exotic fonts
Sometimes people use glyphs from a language not supported by DejuVu Sans.
You can try installing a font that does support it and manually select the replacements.
It's probably easier to make these in Google Docs, but in case you want to try the following code is an example that has worked:
```tex
\usepackage{newunicodechar}
\newfontfamily{\tibetanfont}{Noto Serif Tibetan}[Scale=2.5]
\DeclareTextFontCommand{\texttibetan}{\tibetanfont}
\newunicodechar{༼}{\texttibetan{༼}}
\newunicodechar{༽}{\texttibetan{༽}}
```

### Possible extensions
- auto-fix backward quotes
- Support more Unicode

#### Changing the font
- not advisable, but if you really want to,
  then make sure it supports a big portion of unicode
