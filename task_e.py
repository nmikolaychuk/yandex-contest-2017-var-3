import math
import random


def _read_input():
    """
    Чтение входных данных.

    :return: Входные данные.
    """
    with open("input.txt", mode='r') as f:
        data = f.read().splitlines()

    # Получение количества точек
    n = int(data[0])
    # Получение координат
    points = []
    points_idx = []
    for i, line in enumerate(data[1:]):
        point = [int(j) for j in line.split()]
        points.append(point)
        points_idx.append(i + 1)

    return n, points, points_idx


def _get_projection_sequence(points: list, plane: int):
    # plane = 0: Oyz
    # plane = 1: Oxz
    # plane = 2: Oxy
    if plane == 0:
        return [dot[1:] for dot in points]
    elif plane == 1:
        return [dot[::2] for dot in points]
    elif plane == 2:
        return [dot[:2] for dot in points]


def _calc_distance_between_points(p1: list, p2: list):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def _is_ordered_seq(seq: list):
    # Проверка на строгое возрастание/убывание
    is_increasing_seq = all(i < j for i, j in zip(seq, seq[1:]))
    is_decreasing_seq = all(i > j for i, j in zip(seq, seq[1:]))
    if is_decreasing_seq or is_increasing_seq:
        return True
    return False


def _is_trivial_sequence(proj_seq: list):
    # В качестве опорной точки - левая и правая
    general_point_left = proj_seq[0]
    general_point_right = proj_seq[-1]

    distances_left = []
    distances_right = []
    for p in proj_seq:
        distances_left.append(_calc_distance_between_points(general_point_left, p))
        distances_right.append(_calc_distance_between_points(general_point_right, p))

    is_left_trivial = _is_ordered_seq(distances_left)
    is_right_trivial = _is_ordered_seq(distances_right)

    if is_right_trivial or is_left_trivial:
        return True
    return False


def _is_good_sequence(points):
    # Получение последовательностей-проекций
    o_xy = _get_projection_sequence(points, 2)
    o_xz = _get_projection_sequence(points, 1)
    o_yz = _get_projection_sequence(points, 0)

    is_trivial_seq_xy = _is_trivial_sequence(o_xy)
    is_trivial_seq_xz = _is_trivial_sequence(o_xz)
    is_trivial_seq_yz = _is_trivial_sequence(o_yz)
    if not is_trivial_seq_yz and not is_trivial_seq_xy and not is_trivial_seq_xz:
        return True
    return False


def _algorithm(n: int, points: list, points_idx: list):
    # Пока последовательность не является хорошей...
    def_first = 0
    def_second = 1
    def_third = 2

    first_idx = def_first
    second_idx = def_second
    third_idx = def_third

    is_second_finish = False
    is_third_finish = False
    while not _is_good_sequence(points):
        # Первая перестановка
        points[first_idx], points[second_idx] = points[second_idx], points[first_idx]
        points_idx[first_idx], points_idx[second_idx] = points_idx[second_idx], points_idx[first_idx]
        # Вторая перестановка
        points[second_idx], points[third_idx] = points[third_idx], points[second_idx]
        points_idx[second_idx], points_idx[third_idx] = points_idx[third_idx], points_idx[second_idx]

        # Если точек всего 3 - поменяем местами второй и третий индексы
        if n == 3:
            second_idx, third_idx = third_idx, second_idx
        elif third_idx < n - 1:
            third_idx += 1
        elif third_idx == n - 1:
            third_idx = def_third
            is_third_finish = True

        if is_third_finish:
            if second_idx < n - 2:
                second_idx += 1
            elif second_idx == n - 2:
                second_idx = def_second
                is_second_finish = True

        if is_second_finish and is_third_finish:
            if third_idx < n - 1:
                third_idx += 1
                second_idx += 1
            elif third_idx == n - 1:
                def_first += 1
                def_second += 1
                def_third += 1
                first_idx = def_first
                second_idx = def_second
                third_idx = def_third

    return points_idx


def _format_list(points_idx: list):
    output = ""
    for idx in points_idx:
        output += str(idx) + " "
    return output.rstrip()


def main():
    n, points, points_idx = _read_input()
    good_points = _algorithm(n, points, points_idx)
    print(_format_list(good_points))


if __name__ == "__main__":
    main()
