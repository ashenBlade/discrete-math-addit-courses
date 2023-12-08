from collections import deque


def sort_lbfs(graph):
    """
    Отсортировать граф с помощью лексикографического поиска в ширину
    """
    if len(graph) == 0:
        return []

    queue = deque()
    result = []
    visited = set()

    start_node = next(iter(graph))
    queue.append(start_node)
    visited.add(start_node)

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result


def is_chordal(graph):
    # 1. Выполняем лексикографическую сортировку графа
    reversed_bfs_order = sort_lbfs(graph)[::-1]

    # 2. Проверяем, что при этой сортировке, создаются клики
    for i, u in enumerate(reversed_bfs_order):
        neighbors_u = set(graph[u]).intersection(reversed_bfs_order[i + 1:])

        for j, v in enumerate(reversed_bfs_order[i + 1:]):
            if v in neighbors_u:
                neighbors_v = set(graph[v]).intersection(reversed_bfs_order[i + j + 1:])
                neighbors_u.remove(v)
                if not neighbors_u.issubset(neighbors_v):
                    return False
    return True


def get_max_clique_size(graph) -> int:
    """
    Найти клику максимального размера
    """

    assert is_chordal(graph)

    if len(graph) == 0:
        return 0

    if len(graph) == 1:
        return 1

    # 1. Выполняем лексикографическую сортировку графа
    reversed_bfs_order = sort_lbfs(graph)[::-1]
    max_clique_size = 1

    # 2. Обходим каждую клику в поисках максимальной по размеру
    for i, u in enumerate(reversed_bfs_order):
        # Находим всех соседей "слева"
        u_neighbors = set(graph[u]).intersection(reversed_bfs_order[i + 1:])
        # По теореме, все соседи "слева" вместе с текущим узлом образуют клику
        clique_size = len(u_neighbors) + 1
        # Проверяем превышение размера клики
        if clique_size > max_clique_size:
            max_clique_size = clique_size
    return max_clique_size


def color_chordal_graph(graph):
    """
    Раскрасить хордальный граф
    """
    if len(graph) == 0:
        return []

    all_possible_colors = set(range(len(graph)))

    # 1. PEO
    # 2. Разворот
    vertices_peo = sort_lbfs(graph)

    # Отображение - узел на его цвет
    result = {}
    # 3. Каждый узел красим наименьшим цветом, который не был у наших соседей
    for i, u in enumerate(vertices_peo):
        # Находим всех соседей "справа" т.е. те которых уже прошли
        u_neighbors = set(graph[u]).intersection(vertices_peo[:i])
        neighbor_colors = set()
        # Получаем какие у них цвета
        for neighbor in u_neighbors:
            try:
                neighbor_colors.add(result[neighbor])
            except KeyError:
                pass

        # Находим наименьший цвет из всех возможных
        result[u] = min(all_possible_colors - set(neighbor_colors))

    return result

