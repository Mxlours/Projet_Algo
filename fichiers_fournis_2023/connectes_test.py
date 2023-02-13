#!/usr/bin/env python3
"""
compute sizes of all connected components.
sort and display.
"""

from timeit import timeit
from sys import argv

from geo.point import Point
from geo.quadrant import Quadrant 



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
    #étape une trouver un carré qui contient tout les points
    print(points)
    print(points[0].x())
    print([elem.x() for elem in points])

    min_x = min([elem.x() for elem in points])
    min_y = min([elem.y() for elem in points])
    max_x = max([elem.x() for elem in points])
    max_y = max([elem.y() for elem in points])
    if max_x - min_x > max_y - min_y:
        distance_max = max_x - min_x
    else:
        distance_max = max_y - min_y


    Test = Quadrant((min_x,min_y), (distance_max + min_x, distance_max + min_y), points)
    #étape 1 c'est ok 
    #ensuite on fait une fonction récursive

    def Decoupage(quadrant, distance):
        min_x = quadrant.min_coordinates[0]
        min_y = quadrant.min_coordinates[1]
        d = quadrant.max_coordinates[0] - min_x
        max_y = min_y + d
        max_x = min_x + d

        if d > distance and d/2 < distance:
            pass
            #on regarde les carrées au tour, cas de base
        else:
            #4 liste pour chacun des petits carrées

            milieu_x = (min_x + max_x) / 2
            # milieu x = (min_x + max_x_y) / 2
            milieu_y = (min_y + max_y) / 2
            # milieu x = (min_y + max_x_y) / 2
            #on initialise les listes

            L_haut_droite = []
            L_bas_droite = []
            L_haut_gauche = []
            L_bas_gauche = []

            for elem in quadrant.points():
                if elem.x() > milieu_x and elem.y() > milieu_y:
                    L_haut_droite += [elem]
                if elem.x() > milieu_x and elem.y() < milieu_y:
                    L_bas_droite += [elem]
                if elem.x() < milieu_x and elem.y() > milieu_y:
                    L_haut_gauche += [elem]
                if elem.x() < milieu_x and elem.y() < milieu_y:
                    L_bas_gauche += [elem]

            for elem in quadrant.points():
                if elem.x() > milieu_x:
                    if elem.y() > milieu_y:
                        L_haut_droite += [elem]
                    else:
                        L_bas_droite += [elem]
                else:
                    if elem.y() > milieu_y:
                        L_haut_gauche += [elem]
                    else:
                        L_bas_gauche += [elem]
            #variable muette interne à la fonction
            quadrant_haut_droite = Quadrant((milieu_x,milieu_y),(max_x,max_y), L_haut_droite)
            quadrant_bas_droite = Quadrant((milieu_x, min_y),(max_x,milieu_y), L_bas_droite)
            quadrant_bas_gauche = Quadrant((min_x, min_y),(milieu_x,milieu_y), L_bas_gauche)
            quadrant_haut_gauche = Quadrant((min_x, milieu_y),(milieu_x,max_y), L_bas_droite)

            #on rapelle tout le monde
            Decoupage(quadrant_bas_droite, distance)
            Decoupage(quadrant_bas_gauche, distance)
            Decoupage(quadrant_haut_gauche, distance)
            Decoupage(quadrant_haut_droite, distance)
                

    print(Test)


def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)


main()
