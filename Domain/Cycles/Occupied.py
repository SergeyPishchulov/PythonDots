from Domain import Cell


def get_occupied_cells(cycle_dots, field):
    """returns set of occupied cells"""
    occupied_dots = set()
    dots_on_vertical = Cell.group_by_x(cycle_dots)
    for vertical in dots_on_vertical.keys():  # dict[x_coord]==set of cells
        is_inner = False
        upper, lower = Cell.bounds(dots_on_vertical[vertical])
        for y in range(lower, upper + 1):
            if Cell.contains_by_y(dots_on_vertical[vertical], y):
                is_inner = not is_inner
            elif is_inner:
                occupied_dots.add(field.field_array[vertical][y])
    return occupied_dots
