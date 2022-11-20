import csv

from datatypes import Doorsign

def parse_csv_line(line: dict[str, str]) -> Doorsign:
  return Doorsign(
    display_name=line['Name'],
    year=line['Class Year'],
    pokemon_id=line['Pokémon ID number'],
    course=line['Major'],
    text=line['Description of yourself/flavor text for door sign'],
  )

def load_data(filename: str) -> list[Doorsign]:
  with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    return [parse_csv_line(row) for row in reader]
