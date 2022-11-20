# written by Jason Chen (jchez@mit.edu, chezbgone@gmail.com) on Nov. 19, 2022

import argparse

from load_data import load_data
from fetch_pokemon_images import fetch_pokemon_images
from latex_gen import generate_doorsigns_latex

def main():
  parser = argparse.ArgumentParser(
      prog='Pokémon door sign generator',
      description='Generates door signs for Next House'
      )
  parser.add_argument('filename')
  parser.add_argument('outfile')
  parser.add_argument('--cache-images', dest='cache', action=argparse.BooleanOptionalAction)
  parser.add_argument('--threading', action=argparse.BooleanOptionalAction)
  parser.set_defaults(cache=True, threading=True)
  args = parser.parse_args()

  doorsigns = load_data(args.filename)
  pokemon_ids = [doorsign.pokemon_id for doorsign in doorsigns]
  fetch_pokemon_images(pokemon_ids, use_threads=args.threading, use_cache=args.cache)
  with open(args.outfile, 'w') as out:
    print(generate_doorsigns_latex(doorsigns, check_image=True), end='', file=out)

if __name__ == '__main__':
  main()
