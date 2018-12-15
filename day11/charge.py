from typing import Tuple, List


def power_level(x: int, y: int, serial: int) -> int:
    """Compute the power level of a fuel cell"""
    rack_id = x + 10
    return ((((rack_id * y) + serial) * rack_id) // 100 % 10) - 5


def power_square(
    size: int, serial: int, constraint: int = None
) -> Tuple[int, int, int]:
    """
    Find the top-left coordinate and size of the square with the largest
    total power. If `constraint` is passed, only squares with this size
    are considered.

    Implemented using the following pointers :
    * https://en.wikipedia.org/wiki/Maximum_subarray_problem
    * http://www.algorithmist.com/index.php/UVa_108
    * https://stackoverflow.com/a/18220549
    """
    cumulated: List[List[int]] = [[0 for _ in range(size)]]
    for y in range(1, size + 1):
        cumulated.append(
            [cumulated[y - 1][x] + power_level(x, y, serial) for x in range(size)]
        )

    # `cumulated` contains "prefix sums" and allows us to iterate on
    # (top, bottom) pairs (equivalent to iterate on the square size)
    # and apply a modified version of Kadane's algorithm
    max_total_power = 0
    max_x, max_y, max_size = 0, 0, 0
    for top in range(size):
        for bottom in range(top + 1, size + 1):
            # if `constraint` is set, we can eliminate some candidates
            square_size = bottom - top
            if constraint and square_size < constraint:
                continue
            elif constraint and square_size > constraint:
                break

            # square size is fixed, we iterate on the x axis to apply Kadane's algorithm
            total_power = sum(cumulated[bottom][:square_size]) - sum(
                cumulated[bottom - square_size][:square_size]
            )
            if total_power > max_total_power:
                max_total_power = total_power
                max_x, max_y, max_size = 1, top + 1, square_size
            for end_col in range(square_size, size):
                total_power += (
                    cumulated[bottom][end_col]
                    - cumulated[bottom - square_size][end_col]
                    - (
                        cumulated[bottom][end_col - square_size]
                        - cumulated[bottom - square_size][end_col - square_size]
                    )
                )
                if total_power > max_total_power:
                    max_total_power = total_power
                    max_x, max_y, max_size = (
                        end_col - square_size + 1,
                        top + 1,
                        square_size,
                    )

    return max_x, max_y, max_size
