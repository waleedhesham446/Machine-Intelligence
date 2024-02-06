from typing import Any, Set, Tuple
from grid import Grid
import utils

def locate(grid: Grid, item: Any) -> Set[Tuple[int,int]]:
    '''
    This function takes a 2D grid and an item
    It should return a list of (x, y) coordinates that specify the locations that contain the given item
    To know how to use the Grid class, see the file "grid.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    locations = set()
    w = grid.width
    h = grid.height
    for x in range(w):
        for y in range(h):
            if grid.__getitem__((x, y)) == item:
                locations.add((x,y))
    return locations