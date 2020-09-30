"""Turn a list into a markdown table."""
import math
import typing
import os


MIN_RATIO = 0.5    # Minimum ratio of width/height for the table.
MAX_COLUMNS = 10    # Maximum width of the table. Precedes above.


def find_shape(items: int):
    """Find a rectangle with a given area."""
    for columns in range(1, MAX_COLUMNS + 1):
        if columns / math.ceil(items / columns) >= MIN_RATIO:
            return math.ceil(items / columns), columns
    return math.ceil(items / MAX_COLUMNS), MAX_COLUMNS


def tabulate(items: typing.List[str]):
    """Turn a list into a markdown table."""
    rows, columns = find_shape(len(items))
    extra = (rows * columns) - len(items)
    items += [' '] * extra
    items = [
        [f'{items[i][0]}-{items[i + columns - 1][0]}', *items[i:i + columns]]
        for i in range(0, len(items), columns)
    ]
    items = [[column[i] for column in items] for i in range(columns + 1)]
    items = ['| ' + ' | '.join(row) + ' |' for row in items]
    items.insert(1, ('| --- ' * rows) + '|')
    return '\n'.join(items)


def tabulate_tribes():
    """Create a table for the tribes."""
    tribes = {}
    for tribe in os.listdir('tribes'):
        tribes[tribe[:-3].title()] = 'tribes/' + tribe[:-3]
    table = tabulate(list(sorted(tribes)))
    for tribe in tribes:
        table = table.replace(tribe, f'[{tribe}]({tribes[tribe]})')
    return table
