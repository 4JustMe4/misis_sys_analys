import click
import json
from itertools import product


@click.group()
def cli():
    pass


a_option = click.option('-a', '--path-to-a', type=str, required=True, help='Path to file a.json')
b_option = click.option('-b', '--path-to-b', type=str, required=True, help='Path to file b.json')


@cli.command(help='Read csv file and calc extensional length')
@a_option
@b_option
def run(path_to_a: str, path_to_b: str):
    with open(path_to_a) as a_file:
        with open(path_to_b) as b_file:
            result = main(a_file.read(), b_file.read())
    click.echo(result)


cli.add_command(run)

def build_index(ranking):
    index = {}
    for pos, cluster in enumerate(ranking):
        if isinstance(cluster, list):
            for item in cluster:
                index[item] = pos
        else:
            index[cluster] = pos
    return index

def main(ranking1_json, ranking2_json):
    ranking1 = json.loads(ranking1_json)
    ranking2 = json.loads(ranking2_json)

    index1 = build_index(ranking1)
    index2 = build_index(ranking2)

    contradictions = []

    # We go through all pairs of elements and look for an inversion
    all_items = set(index1.keys()).union(set(index2.keys()))
    
    for item1, item2 in product(all_items, repeat=2):
        if item1 != item2:
            pos1_first = index1.get(item1, float('inf'))
            pos2_first = index1.get(item2, float('inf'))
            pos1_second = index2.get(item1, float('inf'))
            pos2_second = index2.get(item2, float('inf'))

            # Проверяем условие противоречия
            if (pos1_first < pos2_first and pos1_second > pos2_second) or \
               (pos1_first > pos2_first and pos1_second < pos2_second):
                contradictions.append(tuple(sorted((item1, item2))))

    contradictions = sorted(set(contradictions))
    return json.dumps(contradictions)

# Пример использования
if __name__ == "__main__":
    cli()
