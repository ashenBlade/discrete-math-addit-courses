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
