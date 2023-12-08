import pytest

from chordal_graph import is_chordal, get_max_clique_size


@pytest.mark.parametrize('graph', [
    {},
    {'A': tuple()},
    {'A': ('B',), 'B': ('A',)},
    {'A': ('B', 'C'), 'B': ('A', 'C'), 'C': ('A', 'B')},
    {'A': ('B', 'C', 'D'), 'B': ('A', 'C'), 'C': ('A', 'B', 'D'), 'D': ('A', 'C')},
    {'A': ('B', 'F'), 'B': ('A', 'C', 'F'), 'C': ('B', 'F', 'D', 'E'), 'D': ('C', 'E'), 'E': ('D', 'F', 'C'), 'F': ('A', 'B', 'C', 'E')},
    {'A': ('B', 'C', 'D'), 'B': ('A', 'C', 'D'), 'C': ('A', 'B', 'D'), 'D': ('A', 'B', 'C')}
])
def test_is_chordal(graph):
    chordal = is_chordal(graph)
    assert chordal


@pytest.mark.parametrize('graph, expected_size', [
    ({'A': ('B',), 'B': ('A',)}, 2),
    ({'A': ('B', 'C'), 'B': ('A', 'C'), 'C': ('A', 'B')}, 3),
    ({'A': ('B', 'C', 'D'), 'B': ('A', 'C'), 'C': ('A', 'B', 'D'), 'D': ('A', 'C')}, 3),
    ({'A': ('B', 'F'), 'B': ('A', 'C', 'F'), 'C': ('B', 'F', 'D', 'E'), 'D': ('C', 'E'), 'E': ('D', 'F', 'C'), 'F': ('A', 'B', 'C', 'E')}, 3),
    ({'A': ('B', 'C', 'D'), 'B': ('A', 'C', 'D'), 'C': ('A', 'B', 'D'), 'D': ('A', 'B', 'C')}, 4)
])
def test_clique_size(graph, expected_size):
    size = get_max_clique_size(graph)
    assert size == expected_size, f"ожидаемый размер клики: {expected_size}. получен размер: {size}"
