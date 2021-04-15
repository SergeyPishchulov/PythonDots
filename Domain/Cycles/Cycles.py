from Domain import Cell, Field
from Domain.Cycles import Occupied


def rollback(cell, parents, count):
    """Takes cell, dictionary {cell:it's_parent}
     and count times you need to move up on hierarchy tree (to older one)
     returns cell after count moves up on hierarchy tree
     and set of cells between start and aim cell"""
    if parents:
        cycle_cells = set()
        for i in range(count):
            cycle_cells.add(cell)
            cell = parents[cell]
        return cell, set(cycle_cells)
    raise ValueError


def get_cell_depth(cell, parents):
    """Returns depth of cell in hierarchy tree
    where ancestor cell has depth=0"""
    depth = 0
    while parents[cell] is not None:
        cell = parents[cell]
        depth += 1
    return depth


def move_to_same_depth(first, second, parents):
    """Moves one of the cells to the location,
    where their depth in hierarchy tree equals
    returns both cells after movement and all cells on it's path
    on hierarchy tree"""
    depth_1 = get_cell_depth(first, parents)
    depth_2 = get_cell_depth(second, parents)
    if depth_1 == depth_2:
        return first, second, set()
    if depth_1 > depth_2:
        first, path_cells = rollback(first, parents, depth_1 - depth_2)
    else:
        second, path_cells = rollback(second, parents, depth_2 - depth_1)
    return first, second, path_cells


def get_cycle_cells(cell, neighbor, parents):
    """ returns  set of cells in cycle"""
    cell, neighbor, cycle_cells = move_to_same_depth(cell, neighbor, parents)
    while not parents[cell].equals(parents[neighbor]):
        cycle_cells.update((cell, neighbor))
        cell, neighbor = parents[cell], parents[neighbor]
    cycle_cells.update((cell, neighbor))
    if parents[cell] is not None:
        cycle_cells.add(parents[cell])  # the last common ancestor
    return cycle_cells


def find_occupied_in_component(field, start_cell, looked):
    """Finds all cycles in component of dots by DFS"""
    parents = {}
    stack = [start_cell]
    visited = {start_cell}
    finished = set()
    parents[start_cell] = None
    while stack:
        cell = stack.pop()
        for neighbor in Field.Field.get_neighbors(field, cell):
            if neighbor in finished \
                    or neighbor.occupied_by_enemy():
                looked.add(neighbor)
                continue
            if neighbor.owner != start_cell.owner:
                continue
            if neighbor not in parents:
                parents[neighbor] = cell

            if neighbor in visited:  # met gray cell
                occupied_cells, cycle_dots = \
                    complete_cycle(cell, neighbor, parents, field)
                mark_as_occupied(occupied_cells, cycle_dots,
                                 start_cell.owner)
            add_neighbor(neighbor, visited, stack, looked)
        finished.add(cell)


def complete_cycle(branch_1_end, branch_2_end, parents, field):
    cycle_dots = get_cycle_cells(branch_1_end, branch_2_end, parents)
    occupied_cells = Occupied.get_occupied_cells(cycle_dots, field)
    return occupied_cells, cycle_dots


def add_neighbor(neighbor, visited, stack, looked):
    visited.add(neighbor)
    stack.append(neighbor)
    looked.add(neighbor)


def mark_as_occupied(occupied_cells, cycle_dots, occupier):
    if occupied_cells:
        Cell.mark_each_cell_as_occupied(occupied_cells, occupier)
        if Cell.contains_enemy(occupied_cells, occupier):
            for c in occupied_cells:
                c.drenched = True
            for c in cycle_dots:
                c.drenched = True


def find_occupied_dots(field):
    looked = set()  # of cells
    for x in range(field.width):
        for y in range(field.height):
            cur_cell = field.field_array[x][y]
            if not cur_cell.belongs_smb() \
                    or cur_cell in looked \
                    or cur_cell.occupied_by_enemy():
                continue
            find_occupied_in_component(field, cur_cell, looked)
            looked.add(cur_cell)
