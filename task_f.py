def _read_input():
    with open("input.txt", mode='r') as f:
        data = f.read().splitlines()

    # Получение чисел
    n = int(data[0])
    numbers = [int(i) for i in data[1].split()]

    return n, numbers


def _is_unique(numbers: list):
    """
    Проверка на уникальность всех чисел.

    :param numbers: Числа.
    :return: True/False
    """
    min_num = min(numbers)
    max_num = max(numbers)
    if min_num != max_num:
        return True, min_num, max_num
    return False, min_num, max_num


def _downgrading_large_numbers(n: int, numbers: list, min_num: int):
    """
    Понижение больших чисел до >= текущему min значению.

    :param numbers: Числа.
    :return: Новые числа, количество операций.
    """
    operation_count = 0
    for i in range(n):
        if numbers[i] >= 2 * min_num:
            del_op = numbers[i] // min_num - 1
            operation_count += del_op
            numbers[i] -= del_op * min_num

    return numbers, operation_count


def _change_min(numbers: list, min_num: int, max_num: int):
    """
    Понизить минимальное значение посредством вычитания max - min.

    :param numbers: Числа.
    :return: Новые числа, количество операций.
    """
    max_ind = numbers.index(max_num)
    numbers[max_ind] -= min_num
    op_count = 1
    return numbers, op_count


def _do_operation(n, numbers: list, operations: int):
    """
    Алгоритм.

    :param numbers: Числа.
    :return: None.
    """
    while True:
        is_unique, min_num, max_num = _is_unique(numbers)
        if not is_unique:
            break

        if max_num < 2 * min_num:
            # Если не кратные, не одинаковые и нет чисел >= 2 * min
            # Понижаем минимальное значение посредством вычитания max - min
            # (2N + 3N)
            numbers, op_count = _change_min(numbers, min_num, max_num)
            operations += op_count
        else:
            # Если не кратные и не одинаковые...
            # Для чисел, которые больше min считаем количество операций,
            # пока они не будут менять min...
            # (2N)
            numbers, op_count = _downgrading_large_numbers(n, numbers, min_num)
            operations += op_count

    # Вывод количества операций
    print(operations)


def main():
    operation_count = 0
    n, numbers = _read_input()
    _do_operation(n, numbers, operation_count)


if __name__ == "__main__":
    main()
