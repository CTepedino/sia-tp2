from src.individual import Individual
from typing import Callable

def fill_all(parents: list[Individual], children: list[Individual], selection_method: Callable[[int, list[Individual]], list[Individual]]) -> list[Individual]:
    n = len(parents)
    combined = parents + children
    return selection_method(n, combined)

def fill_parent(parents: list[Individual], children: list[Individual], selection_method: Callable[[int, list[Individual]], list[Individual]]) -> list[Individual]:
    n = len(parents)
    k = len(children)

    if k > n:
        return selection_method(n, children)
    else:
        remaining = n - k
        selected_parents = selection_method(remaining, parents)
        return children + selected_parents

generation_methods = {
    "fill_all": fill_all,
    "fill_parent": fill_parent,
}