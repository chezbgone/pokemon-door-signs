import emoji
import string
import os

from datatypes import Doorsign

def latexify(text: str) -> str:
  replacements = {
    '\\': r'\textbackslash{}',
    '_':  r'\textunderscore{}',
    '{':  r'\{',
    '}':  r'\}',
    '~':  r'\textasciitilde{}',
    '^':  r'\^{}',
    '&':  r'\&',
    '%':  r'\%',
    '$':  r'\$',
    '#':  r'\#',
  }
  replaced = ''.join(replacements.get(c, c) for c in text)
  # people sometimes intentionally put multiple spaces in a row.
  # we want to preserve this
  return replaced.replace('  ', '~ ')

def convert_emojis(text: str) -> str:
  # TODO: write docs
  def replace(text: str, _: dict) -> str:
    codepoints: list[int] = [ord(c) for c in text]
    template = string.Template(r'{\Large\texttwemoji{$emoji}}')
    return template.substitute({
      'emoji': "-".join(hex(codepoint)[2:] for codepoint in codepoints)
    })
  return emoji.replace_emoji(text, replace)

def generate_doorsign_latex(
    doorsign: Doorsign,
    check_image: bool=True,
    default_image: str='images/tmp.png'
  ) -> str:
  template = string.Template(r'\par'.join([
    r'\vspace*{\fill}',
    r'\includegraphics[width=0.5\textwidth]{$image}',
    r'\medskip',
    r'{\Large $name}',
    r'\medskip',
    r'{Class of $class} {\textbullet} {Course $course}',
    r'{$text}',
    r'\vspace{\fill}',
  ]))
  image = f'images/{doorsign.pokemon_id}.png'
  if check_image and not os.path.exists(image):
    image = default_image
  return template.substitute({
    'image': image,
    'name': convert_emojis(latexify(doorsign.display_name)),
    'class': convert_emojis(latexify(doorsign.year)),
    'course': convert_emojis(latexify(doorsign.course)),
    'text': convert_emojis(latexify(doorsign.text)),
  })

def generate_doorsigns_latex(
    doorsigns: list[Doorsign],
    check_image: bool=True,
    default_image: str='images/tmp.png'
  ) -> str:
  with open('doorsigns.tex.template') as tex_template:
    template = string.Template(tex_template.read())
    body = '\\newpage\n'.join(
      generate_doorsign_latex(
        doorsign,
        check_image=check_image,
        default_image=default_image
      )
      for doorsign in doorsigns
    )
    return template.substitute({'body': body})
