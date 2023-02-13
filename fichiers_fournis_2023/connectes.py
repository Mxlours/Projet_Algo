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
                if points[p].distance_to(points[j]) <= distance:
                    stack.append(j)
                    visited[j] = True
        
        components.append(len(component))
    
    print(sorted(components, reverse=True))


def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)

start = time.time()
main()
end = time.time()
duree = end - start
print(duree)
