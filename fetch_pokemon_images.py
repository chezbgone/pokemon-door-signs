import requests
import os
import sys

from bs4 import BeautifulSoup, Tag

def warn(message: str):
  print(f'\033[93mWARNING\033[0m: {message}', file=sys.stderr)
  ']]' # fixes editor autoindent ??

def get_pokemon_image_link(pokemon_id: str) -> str | None:
  link = f'https://pokewiki.de/Datei:Sugimori_{pokemon_id}.png'
  response = requests.get(link)
  # wow i really wish i had monads
  if not response.ok:
    warn(f'[{pokemon_id=}] {link} not found')
    return None
  page = BeautifulSoup(response.text, 'html.parser')
  file = page.find(id='file')
  if not file:
    warn(f'[{pokemon_id=}] unexpected page format (unable to find id=file)')
    return None
  if not isinstance(file, Tag):
    warn(f'[{pokemon_id=}] unexpected page format (file is not a Tag)')
    return None
  image_link = file.a
  if not image_link:
    warn(f'[{pokemon_id=}] unexpected page format (unable to find image link)')
    return None
  image_href = image_link.get('href', None)
  if not image_href:
    warn(f'[{pokemon_id=}] unexpected page format (unable to find image href)')
    return None
  return f'http://pokewiki.de{image_href}'

def fetch_pokemon_image(pokemon_id: str, use_cache: bool=True) -> str | None:
  filename = f'images/{pokemon_id}.png'
  if os.path.exists(filename) and use_cache: return filename
  link = get_pokemon_image_link(pokemon_id)
  if link is None: return None
  response = requests.get(link)
  if not response.ok:
    warn(f'{link} not found')
    return None
  with open(filename, 'wb') as img:
    img.write(response.content)
  return filename

def fetch_pokemon_images(
    pokemon_ids: list[str],
    use_threads: bool=True,
    use_cache: bool=True):
  if use_threads:
    import threading
    threads = [
      threading.Thread(
        target=fetch_pokemon_image,
        args=(id,),
        kwargs={ 'use_cache': use_cache },
      ) for id in pokemon_ids
    ]
    for thread in threads:
      thread.start()
    for thread in threads:
      thread.join()
  else:
    for id in pokemon_ids:
      fetch_pokemon_image(id, use_cache=use_cache)
