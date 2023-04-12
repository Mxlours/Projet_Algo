#!/usr/bin/env python3
"""
compute sizes of all connected composants.
sort and display.
"""

from timeit import timeit
import time
from math import sqrt
from sys import argv

from geo.point import Point

class kdTree:
    def __init__(self, P, direction = 0):
        n = len(P)
        median = n // 2
        P.sort(key = lambda x: x[direction]) # trie la liste par rapport à la bonne direction d = 0 si on trie sur x, d = 1 si on trie sur y
        self.point = P[median] # on prend le point médian et on va faire notre récursion
        self.direction = direction
        direction = (direction+1) % 2 # on change notre direction pour la prochaine itération
        self.left = self.right = None
        if median > 0:
            self.left = kdTree(P[:median], direction)
        if n - (median+1) > 0:
            self.right = kdTree(P[median+1:], direction)

    def distance(self, point1, point2):
        return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
    
    def distance2(self, point1):
        return sqrt((self.point[0]-point1[0])**2 + (self.point[1]-point1[1])**2)
    
    def distance_to(self, point):
        """
        euclidean distance between two points.
        """
        total = 0
        for c_1, c_2 in zip(self.point, point):
            diff = c_1 - c_2
            total += diff * diff

        return sqrt(total)
    
    def find_nearby_points(self, point, threshold, results=None):
        """Trouve l'ensemble des points à une distance threshold"""
        if results is None:
            results = []
        # dist = self.distance(self.point, point)
        # dist = self.distance2(point)
        dist = self.distance_to(point)
        if dist <= threshold:
            results.append(self.point)
        if self.direction == 0:
            if self.left is not None and point[0] - threshold <= self.point[0]:
                self.left.find_nearby_points(point, threshold, results)
            if self.right is not None and point[0] + threshold >= self.point[0]:
                self.right.find_nearby_points(point, threshold, results)
        else:
            if self.left is not None and point[1] - threshold <= self.point[1]:
                self.left.find_nearby_points(point, threshold, results)
            if self.right is not None and point[1] + threshold >= self.point[1]:
                self.right.find_nearby_points(point, threshold, results)
        return results

def load_instance(filename):
    """
    loads .pts file.
    returns distance limit and points.
    """
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [tuple([float(f) for f in l.split(",")]) for l in lines]

    return distance, points

def print_composants_sizes(distance, points):
    """
    affichage des tailles triees de chaque composante
    """
    tree = kdTree(points)
    visited = set()
    taille_compos_connexes = [] # au final
    for current_point in points:
        if current_point in visited:
            continue # on passe à un autre
        compo_connexe = [] # au singulier
        pile = [current_point]
        visited.add(current_point)
        while pile:
            point = pile.pop()
            compo_connexe.append(point)
            points_proches = tree.find_nearby_points(point, threshold=distance) # sinon on l'a pas vu on regarde ces compo connexes
            for elem in points_proches:
                if elem in visited:
                    continue
                else:
                    visited.add(elem)
                    pile.append(elem)
        if len(compo_connexe) == 1:
            taille_compos_connexes.append(1)
        else:
            # taille_compos_connexes=retrie_tableau_intelligent(taille_compos_connexes, len(compo_connexe))
            # méthode bète 
            # flag = False
            # if len(taille_compos_connexes) == 1:
            #     if len(compo_connexe) >= taille_compos_connexes[0]:
            #         taille_compos_connexes.insert(0, len(compo_connexe))
            #         flag = True
            # if not(flag):
            #     for k in range(len(taille_compos_connexes)-1):
            #         if taille_compos_connexes[k] <= len(compo_connexe):
            #             taille_compos_connexes.insert(k, len(compo_connexe))
            #             break
            #     flag = True
            # if not(flag):
            #     taille_compos_connexes.append(len(compo_connexe))
            flag = True
            if len(taille_compos_connexes) == 0:
                taille_compos_connexes.append(len(compo_connexe))
                flag = False
            if flag:
                a = 0
                b = len(taille_compos_connexes) - 1
                while True:
                    if b-a <= 1:
                        # 3 cas possibles
                        if taille_compos_connexes[a] >= len(compo_connexe) >= taille_compos_connexes[b]:
                            taille_compos_connexes.insert(a+1, len(compo_connexe))
                            break
                        if len(compo_connexe) >= taille_compos_connexes[a]:
                            taille_compos_connexes.insert(a, len(compo_connexe))
                            break
                        else:
                            taille_compos_connexes.insert(b+1, len(compo_connexe)) # même si on dépasse la taille de la liste ça marche
                            break
                    indice_milieu = ((b + 1 - a) // 2) + a # au début c'est bien len(taille_compos_connexes) // 2
                    milieu = taille_compos_connexes[indice_milieu]
                    if milieu >= len(compo_connexe):
                        a = indice_milieu
                    else:
                        b = indice_milieu
        
    print(taille_compos_connexes)

def retrie_tableau_intelligent(L, nombre):
    """on prend comme arg un tableau trié par ordre décroissant et on insère notre nouveau élément au bon endroit"""
    if len(L) == 0:
        L.append(nombre)
        return L
    a = 0
    b = len(L) - 1
    while True:
        if b-a <= 1:
            # 3 cas possibles
            if L[a] >= nombre >= L[b]:
                L.insert(a+1, nombre)
                break
            if nombre >= L[a]:
                L.insert(a, nombre)
                break
            else:
                L.insert(b+1, nombre) # même si on dépasse la taille de la liste ça marche
                break
        indice_milieu = ((b + 1 - a) // 2) + a # au début c'est bien len(L) // 2
        milieu = L[indice_milieu]
        if milieu >= nombre:
            a = indice_milieu
        else:
            b = indice_milieu
            
    return L

def retrie_tableau_bete(L, nombre):
    if len(L) == 1:
        if nombre >= L[0]:
            L.insert(0, nombre)
            return L 
    for k in range(len(L)-1):
        if L[k] <= nombre:
            L.insert(k, nombre)
            return L
    L.append(nombre)
    return L

def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    if len(argv) == 1:
        print("Mets le nom du fichier à regarder en argument")
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_composants_sizes(distance, points)

start = time.time()
main()
end = time.time()
temps_tot = end-start
print("Temps d'éxécution : ", temps_tot)
