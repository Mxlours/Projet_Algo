#!/usr/bin/env python3
"""
compute sizes of all connected components.
sort and display.
"""

from timeit import timeit
import time
from sys import argv

from geo.point import Point


def load_instance(filename):
    """
    loads .pts file.
    returns distance limit and points.
    """
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [Point([float(f) for f in l.split(",")]) for l in lines]

    return distance, points


def print_components_sizes(distance, points):
    """
    affichage des tailles triees de chaque composante
    """
    
    def grid_index(point, d):
        """return l'indice de la grille en commençant en haut à gauche puis sur la droite"""
        x,y = point.coordinates
        x_index = int(x / d)
        y_index = int(y / d)
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

    return find_composantes(points, distance)


def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        resultat = print_components_sizes(distance, points)
        print(resultat)
        bon_result = [len(elem) for elem in resultat]
        bon_result = sorted(bon_result, reverse=True)
        print(bon_result)

start = time.time()
main()
end = time.time()
duree = end - start
print(duree)
