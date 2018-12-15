from .charge import power_square


def run() -> None:
    size = 300
    serial = 7315  # puzzle input
    result_part_1 = power_square(size, serial, 3)
    print(f"{result_part_1[0]},{result_part_1[1]}")
    result_part_2 = power_square(size, serial)
    print(",".join(str(n) for n in result_part_2))
