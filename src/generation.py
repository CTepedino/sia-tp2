from individual import Individual
from typing import Callable

def fill_all(current_gen: list[Individual], children: list[Individual], selection_method: Callable[[int, list[Individual]], list[Individual]]) -> list[Individual]:
    n = len(current_gen)
    combined = current_gen + children
    return selection_method(n, combined)

def fill_parent(current_gen: list[Individual], children: list[Individual], selection_method: Callable[[int, list[Individual]], list[Individual]]) -> list[Individual]:
    n = len(current_gen)
    k = len(children)

    if k > n:
        return selection_method(n, children)
    else:
        remaining = n - k
        selected_current_gen = selection_method(remaining, current_gen)
        return children + selected_current_gen

generation_methods = {
    "fill_all": fill_all,
    "fill_parent": fill_parent,
}