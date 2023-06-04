"""Поиск кратчайшего пути в связном взвешенном графе по алгоритму Дейкстры"""

from random import choice
from typing import Tuple, List

class Vertex:
    def __init__(self):
        self._id = choice(range(9999))
        self.cost = float('inf')
        self.parent = None
        self.neighbours = {}

    def __hash__(self):
        return self._id
    

class Link:
    def __init__(self, v1, v2):
        self._v1 = v1  # ЭК Vertex
        self._v2 = v2  # ЭК Vertex
        self._dist = 1  # длина ребра

    @property
    def v1(self):
        return self._v1
    
    @property
    def v2(self):
        return self._v2
    
    @property
    def dist(self):
        return self._dist

    def __hash__(self):
        return hash(self._v1) + hash(self._v2)
    

class LinkedGraph:
    def __init__(self):
        self._vertex = []  # список ЭК Vertex
        self._links = []  # список ЭК Link

    def add_vertex(self, v):
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link):
        if not any(filter(lambda x: hash(x) == hash(link), self._links)):
            self._links.append(link)
            self.add_vertex(link.v1)
            self.add_vertex(link.v2)

    def find_lowest_node(self, done):
        lowest = float('inf')
        node = None
        for n in self._vertex:
            if n not in done and n.cost < lowest:
                lowest = n.cost
                node = n
        return node

    def get_route(self, fin):
        route = []
        node = fin
        while node:
            route.append(node)
            node = node.parent
        return route[::-1]

    def get_links(self, route):
        links = []
        for i in range(len(route) - 1):
            for link in self._links:
                if hash(link) == hash(route[i]) + hash(route[i+1]):
                    links.append(link)
        return links

    def find_path(self, start_v: Vertex, stop_v: Vertex) -> Tuple[List[Vertex], List[Link]]:
        "-> tuple (list ЭК вершин, list ЭК ребер)"
        for v in self._vertex:  # обнуляем начальные данные
            v.cost = float('inf')
            v.parent = None
            v.neighbours = {}

        for link in self._links:  # находим соседей каждой вершины
            link.v1.neighbours[link.v2] = link.dist
            link.v2.neighbours[link.v1] = link.dist

        # алгоритм Дейкстра заполняет лок атрибуты вершин
        done = []  # список обработанных вершин
        done.append(start_v)  # старт вершину вносим в список обработанных
        
        # соседям старта заносим веса и родителей
        for n, c in start_v.neighbours.items():  
            n.cost = c
            n.parent = start_v

        node = self.find_lowest_node(done)  # находим ближайшую вершину
        while node:
            cost = node.cost  # стоимость вершины
            for n, c in node.neighbours.items():  # среди соседей вершины
                if n not in done:  # если сосед не в списке обработанных
                    new_cost = cost + c  # считаем новую стоимость
                    if new_cost < n.cost:  # если новая меньше прежней
                        n.cost = new_cost  # новую вносим в вершину и
                        n.parent = node  # меняем родителя
            done.append(node)  # вершину вносим в список обработанных
            node = self.find_lowest_node(done)  # находим ближайшую вершину
        
        # после отработки алгоритма Дейкстра собираем маршрут
        route = self.get_route(stop_v)  # -> list; собираем вершины
        links = self.get_links(route)  # -> list; собираем ребра
        
        return route, links


class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return self.name


class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2)
        self._dist = dist


map_metro = LinkedGraph()

v1 = Station("Сретенский бульвар")
v2 = Station("Тургеневская")
v3 = Station("Чистые пруды")
v4 = Station("Лубянка")
v5 = Station("Кузнецкий мост")
v6 = Station("Китай-город 1")
v7 = Station("Китай-город 2")

map_metro.add_link(LinkMetro(v1, v2, 1))
map_metro.add_link(LinkMetro(v2, v3, 1))
map_metro.add_link(LinkMetro(v1, v3, 1))
map_metro.add_link(LinkMetro(v4, v5, 1))
map_metro.add_link(LinkMetro(v6, v7, 1))
map_metro.add_link(LinkMetro(v2, v7, 5))
map_metro.add_link(LinkMetro(v3, v4, 3))
map_metro.add_link(LinkMetro(v5, v6, 3))

print(len(map_metro._vertex), 'stations')  # количество вершин
print(len(map_metro._links), 'links')  # количество ребер
print('-------------------------------------------------------------------')
path = map_metro.find_path(v1, v6)  # от сретенского бульвара до китай-город 1
print(f'shortest route {v1} - {v6}:', path[0])    # [Сретенский бульвар, Тургеневская, Китай-город 2, Китай-город 1]
print('total distance:', sum([x.dist for x in path[1]]))  # 7 общая дистанция
print('links distances:', [x.dist for x in path[1]])  # [1, 5, 1] длины ребер
print('-------------------------------------------------------------------')
path2 = map_metro.find_path(v1, v7)  # от сретенского бульвара до китай-город 2
print(f'shortest route {v1} - {v7}:', path2[0])    # [Сретенский бульвар, Тургеневская, Китай-город 2]
print('total distance:', sum([x.dist for x in path2[1]]))  # 6 общая дистанция
print('links distances:', [x.dist for x in path2[1]])  # [1, 5] длины ребер
print('-------------------------------------------------------------------')

# замер времени поиска 100000 маршрутов
from timeit import timeit

def foo():
    map_metro.find_path(v1, v6)

print(timeit(foo, number=100000))

