# premier truc un peu classique 

from typing import List

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def get_components(points: List[Point], d: float) -> List[int]:
    def distance(p1, p2):
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5
    
    visited = [False for _ in range(len(points))]
    components = []
    
    for i in range(len(points)):
        if visited[i]:
            continue
        
        component = []
        stack = [i]
        visited[i] = True
        
        while stack:
            p = stack.pop()
            component.append(p)
            
            for j in range(len(points)):
                if visited[j]:
                    continue
                if distance(points[p], points[j]) <= d:
                    stack.append(j)
                    visited[j] = True
        
        components.append(len(component))
    
    return components

#deuxième algo avec quadrillage de distance d 

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def grid_index(point, d):
    x_index = int(point.x / d)
    y_index = int(point.y / d)
    return x_index, y_index

def find_composantes(points, d):
    grid = {}
    composantes = []
    component_id = 0
    for point in points:
        x_index, y_index = grid_index(point, d)
        if (x_index, y_index) in grid:
            component_id = grid[(x_index, y_index)]
        else:
            component_id = len(composantes)
            composantes.append([point])
            grid[(x_index, y_index)] = component_id
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x_neighbour, y_neighbour = x_index + dx, y_index + dy
                if (x_neighbour, y_neighbour) in grid:
                    neighbour_id = grid[(x_neighbour, y_neighbour)]
                    if component_id != neighbour_id:
                        if len(composantes[component_id]) < len(composantes[neighbour_id]):
                            component_id, neighbour_id = neighbour_id, component_id
                        composantes[component_id].extend(composantes[neighbour_id])
                        for neighbour in composantes[neighbour_id]:
                            grid[grid_index(neighbour, d)] = component_id
                        composantes[neighbour_id] = []
    return [c for c in composantes if c]

#algo de fou en O(nlogn) mais utilise un truc d'hyperplan je comprend rien mdr

from scipy.spatial import KDTree

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def find_components(points, d):
    kdtree = KDTree([[point.x, point.y] for point in points])
    components = []
    visited = [False for _ in range(len(points))]
    
    for i in range(len(points)):
        if visited[i]:
            continue
        component = []
        stack = [i]
        while stack:
            current = stack.pop()
            if visited[current]:
                continue
            visited[current] = True
            component.append(current)
            neighbors = kdtree.query_ball_point([points[current].x, points[current].y], d)
            stack.extend(neighbors)
        components.append(component)
    return components

#

def find_components(points, distance):
    def grid_index(point, d):
        x_index = int(point.x() / d)
        y_index = int(point.y() / d)
        return x_index, y_index
    
    def mark_component_dfs(x, y, component_id, grid, component_sizes):
        grid[x][y] = component_id
        component_sizes[component_id] += 1
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x_neighbour, y_neighbour = x + dx, y + dy
                if 0 <= x_neighbour < grid_size and 0 <= y_neighbour < grid_size and grid[x_neighbour][y_neighbour] is None:
                    mark_component_dfs(x_neighbour, y_neighbour, component_id, grid, component_sizes)
    
    grid_size = int(1 / distance)
    grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    component_sizes = [0 for _ in range(len(points))]
    component_id = 0
    for point in points:
        x, y = grid_index(point, distance)
        if grid[x][y] is None:
            mark_component_dfs(x, y, component_id, grid, component_sizes)
            component_id += 1
    return sorted(component_sizes, reverse=True)

def main():
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        result = find_components(points, distance)
        print(result)
