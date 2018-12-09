from typing import NamedTuple, Sequence, List, Dict, Set, Tuple
import re


class Requirement(NamedTuple):
    parent: str
    child: str


def parse_requirement(instruction: str) -> Requirement:
    """Parse a requirement between steps from an instruction"""
    match = re.match(
        r"Step (?P<parent>[A-Z]) must be finished before step (?P<child>[A-Z]) can begin.",
        instruction,
    )
    if not match:
        raise Exception("invalid instruction")
    parsed = match.groupdict()
    return Requirement(parsed["parent"], parsed["child"])


def get_ready(
    queue: Set[str], done: Sequence[str], parents: Dict[str, Set[str]], limit: int
) -> List[str]:
    """
    Find the set of steps ready to be executed in a queue, given their
    dependencies and already executed steps.
    """
    ready: List[str] = []
    for step in sorted(queue):
        if any(parent not in done for parent in parents.get(step, set())):
            continue
        else:
            ready.append(step)
        if len(ready) == limit:
            break
    return ready


def duration(step: str, base_duration: int) -> int:
    """Get the duration of a step"""
    return base_duration + ord(step.lower()) - 96


def complete(
    requirements: Sequence[Requirement], workers: int, base_duration: int
) -> Tuple[str, int]:
    """
    Complete a set of instructions and return the order of completion
    and the total duration.
    """
    children: Dict[str, Set[str]] = {}
    parents: Dict[str, Set[str]] = {}
    for req in requirements:
        children[req.parent] = children.get(req.parent, set()) | {req.child}
        parents[req.child] = parents.get(req.child, set()) | {req.parent}

    queue = set(children.keys()) - set(parents.keys())
    done: List[str] = []
    second = -1
    eta: Dict[int, Tuple[str, int]] = {w: (".", second - 1) for w in range(workers)}
    while queue:
        # Find finishing steps and already idle workers
        finished = []
        idle_workers = set()
        for w, task in eta.items():
            if task[1] == second:
                finished.append(task[0])
                idle_workers.add(w)
            elif task[1] < second:
                idle_workers.add(w)
        done += sorted(finished)

        # Find available steps (ie. with all dependencies satisfied)
        ready = get_ready(queue, done, parents, len(idle_workers))
        if not ready:
            second += 1
            continue

        # Assign available steps to available workers
        launched = set()
        for worker, step in zip(idle_workers, ready):
            eta[worker] = (step, second + duration(step, base_duration))
            launched.add(step)
            queue |= children.get(step, set())

        queue -= launched
        second += 1

    # All steps have been assigned : the total duration is the maximum ETA
    # in the future, incremented by one.
    last_eta = 0
    for w, task in sorted(eta.items(), key=lambda kv: (kv[1][1], kv[1][0])):
        last_eta = task[1]
        if task[1] < second:
            continue
        else:
            done.append(task[0])

    return "".join(done), last_eta + 1
