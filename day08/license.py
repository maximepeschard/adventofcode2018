from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Tree:
    metadata: List[int]
    children: List["Tree"]


def make_tree(values: List[int]) -> Tree:
    """Parse and build a tree object from a list of integer values"""
    parent_stack = []
    tree = None
    pos = 0
    size = len(values)
    levels_nodes: Dict[int, int] = {}
    levels_meta: Dict[int, int] = {}
    level = 0

    while pos < size:
        remaining_nodes = levels_nodes.get(level, 0)
        remaining_metadata = levels_meta.get(level, 0)
        if remaining_nodes > 0 or remaining_metadata == 0:
            # new node
            if values[pos] > 0:
                # parent node : add it to the tree and go one level deeper
                node = Tree([], [])
                if tree:
                    tree.children.append(node)
                else:
                    tree = node
                parent_stack.append(tree)
                tree = node
                levels_meta[level] = values[pos + 1]
                levels_nodes[level] = levels_nodes.get(level, 0) + values[pos]
                level += 1
                pos += 2
            else:
                # leaf node : add it to the tree and go one level up if last
                # node of current level
                nb_metadata = values[pos + 1]
                meta = values[(pos + 2) : (pos + nb_metadata + 2)]  # noqa
                node = Tree(meta, [])
                if tree:
                    tree.children.append(node)
                else:
                    tree = node
                if level - 1 >= 0:
                    levels_nodes[level - 1] -= 1
                pos += nb_metadata + 2
                if levels_nodes.get(level - 1) == 0:
                    level -= 1
        else:
            # process metadata of a node
            meta = values[pos : (pos + remaining_metadata)]  # noqa
            if tree:
                tree.metadata = meta
            pos += remaining_metadata
            levels_meta[level] -= remaining_metadata
            if level - 1 >= 0:
                levels_nodes[level - 1] -= 1
            if levels_nodes.get(level - 1) == 0:
                level -= 1
            tree = parent_stack.pop()

    if not tree:
        raise Exception("failed to parse tree")
    return tree


def total_metadata(tree: Tree) -> int:
    """Compute the sum of all metadata entries of all the nodes of a tree"""
    return sum(tree.metadata) + sum(total_metadata(c) for c in tree.children)


def value(tree: Tree) -> int:
    """Compute the value of the root of a tree"""
    if tree.children:
        valid = [index for index in tree.metadata if index <= len(tree.children)]
        children_values = {
            index: value(tree.children[index - 1]) for index in set(valid)
        }
        return sum(children_values[index] for index in valid)
    else:
        return sum(tree.metadata)
