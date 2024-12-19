import click
import csv
import json


@click.group()
def cli():
    pass


path_option = click.option('-p', '--file-path', type=str, required=True, help='Path to file')
raw_option = click.option('-r', '--row', type=int, required=True, help='Raw number')
col_option = click.option('-c', '--column', type=int, required=True, help='Column number')


@cli.command(help='Read value of csv table by indexes')
@path_option
@raw_option
@col_option
def read(file_path, row, column):
    with open(file_path, newline='') as raw_file:
        reader = csv.reader(raw_file)
        for i, line in enumerate(reader, start=1):
            if i == row:
                if len(line) >= column:
                    value = line[column - 1]
                    if value.strip() == '':
                        value = "Empty value"
                    click.echo(value)
                else:
                    click.echo(f"Error: column num: {column} is our of range")
                return
    click.echo(f"Error: row num: {row} is our of range")


cli.add_command(read)


def main():
    cli()


if __name__ == '__main__':
    main()
