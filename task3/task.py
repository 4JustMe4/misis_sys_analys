import click
import csv
import math


@click.group()
def cli():
    pass


path_option = click.option('-p', '--file-path', type=str, required=True, help='Path to csv file')


@cli.command(help='Read csv file and calc entropy of graph')
@path_option
def run(file_path):
    with open(file_path, newline='') as raw_file:
        result = main(raw_file.read())
    click.echo(result)


cli.add_command(run)


def read_matrix(raw_string: str):
    reader = csv.reader(raw_string.split('\n'))
    matrix = []
    for row in reader:
        matrix.append([int(value) for value in row])
    return matrix


def task(raw_string: str):
    matrix = read_matrix(raw_string)
    entropy = 0
    number = len(matrix)
    for j in range(number):
        for i in range(len(matrix[j])):
            value = matrix[j][i]
            if value > 0:
                # calc H_j_i
                probability = value / (number - 1)
                entropy -= probability * math.log2(probability)
    return entropy


def main(raw_string: str):
    return task(raw_string)


if __name__ == '__main__':
    cli()
