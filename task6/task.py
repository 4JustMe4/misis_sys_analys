import click
import json
from itertools import product


@click.group()
def cli():
    pass


t_option = click.option('-t', '--path-to-temperature', type=str, required=True, help='Path to file temperature.json')
h_option = click.option('-h', '--path-to-heating', type=str, required=True, help='Path to file heating.json')
c_option = click.option('-c', '--path-to-control', type=str, required=True, help='Path to file control.json')
r_option = click.option('-r', '--real-temperature', type=float, required=True, help='Current temperature')


@cli.command(help='Read json files and calc optimal level')
@t_option
@h_option
@c_option
@r_option
def run(path_to_temperature: str, path_to_heating: str, path_to_control: str, real_temperature: float):
    with open(path_to_temperature) as temperature:
        with open(path_to_heating) as heating:
            with open(path_to_control) as control:
                result = main(temperature.read(), heating.read(), control.read(), real_temperature)
    click.echo(result)


cli.add_command(run)


def membership_function(x, points):
    for (x0, y0), (x1, y1) in zip(points[:-1], points[1:]):
        if x0 <= x <= x1:
            if y0 == y1:
                return y0
            else:
                return y0 + (y1 - y0) * ((x - x0) / (x1 - x0))
    return 0.0


def compute_fuzzy_value(value, fuzzy_sets):
    fuzzy_values = {}
    for term, params in fuzzy_sets.items():
        fuzzy_values[term] = membership_function(value, params)
    return fuzzy_values


def main(temperature_json: str, heating_json: str, control_json: str, t: float):
    temp_sets = json.loads(temperature_json)
    heat_sets = json.loads(heating_json)
    rules = json.loads(control_json)

    temp_fuzzy_values = compute_fuzzy_value(t, temp_sets)

    heat_fuzzy_values = {}
    for rule in rules:
        temp_term, heat_term = rule
        membership_degree = temp_fuzzy_values.get(temp_term)
        if heat_term in heat_fuzzy_values:
            heat_fuzzy_values[heat_term] += membership_degree
        else:
            heat_fuzzy_values[heat_term] = membership_degree

    ## Дефаззификация методом первого максимума
    max_degree = max(heat_fuzzy_values.values(), default=0)
    first_max_term = next((term for term, degree in heat_fuzzy_values.items() if degree == max_degree), None)

    first_max_points = heat_sets[first_max_term]
    xs = [x for x, y in first_max_points if y > 0]
    centroid_value = sum(xs) / len(xs) if xs else 0
    return f"Нужно установить в {first_max_term}, значение: {centroid_value}"


if __name__ == "__main__":
    cli()


# python3 task.py run -t temperature.json -h heating.json -c control.json -r 21
