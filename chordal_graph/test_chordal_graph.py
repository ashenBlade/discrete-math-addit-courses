import pytest

from chordal_graph import is_chordal


@pytest.mark.parametrize('graph', [
    {},
    {'A': tuple()},
    {'A': ('B',), 'B': ('A',)},
    {'A': ('B', 'C'), 'B': ('A', 'C'), 'C': ('A', 'B')},
    {'A': ('B', 'C', 'D'), 'B': ('A', 'C'), 'C': ('A', 'B', 'D'), 'D': ('A', 'C')},
    {'A': ('B', 'F'), 'B': ('A', 'C', 'F'), 'C': ('B', 'F', 'D', 'E'), 'D': ('C', 'E'), 'E': ('D', 'F', 'C'), 'F': ('A', 'B', 'C', 'E')}
])
def test_is_chordal(graph):
    chordal = is_chordal(graph)
    assert chordal
