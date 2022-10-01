INPUT_FILE = "input.txt"
MODULE = 1000000007
UPPER = 1000000
LOWER = 1


def _mul_list(units: list):
    result = 1
    # Перемножение элементов массива
    for x in units:
        result *= x
        # От результата берется модуль
        result = result % MODULE
    return int(result)


def load_input():
    # Получение данных из файла
    data = open(INPUT_FILE, mode='r').readlines()
    # Количество строк в файле: должно быть равно 1
    count = len(data)

    # Проверка на количество строк
    if count > 1:
        exit(0)

    # Проверка на количество пробелов
    line = None
    try:
        line = data[0]
    except IndexError:
        exit(0)

    if line.count(" ") > 1:
        exit(0)

    # Разделение строки на два ожидаемых числа
    n, a = None, None
    try:
        n, a = line.rstrip().split()
    except ValueError:
        exit(0)

    # Приведение к целочисленному типу
    try:
        n, a = int(n), int(a)
    # Если неудачно - некорректный ввод
    except ValueError:
        exit(0)

    # Валидация входных значений
    if n < LOWER or n > UPPER:
        exit(0)
    if a < LOWER or a > UPPER:
        exit(0)
    if a == n:
        exit(0)

    # Обработка граничного случая
    if n == 1:
        print(int(n % MODULE))
        exit(0)

    return n, a


def calc_max_damage(n, a):
    # Алгоритм
    # Число юнитов в группе, дающее максимальный результат
    best_unit_group_size = 3
    units = []
    # Если ограничение равно 2...
    if a == 2:
        # Используем алгоритм деления на группы по 3 юнита
        remainder = n % best_unit_group_size
        # Если нацело делится на 3: делим на группы по 3 юнита
        if remainder == 0:
            for i in range(n // best_unit_group_size):
                units.append(best_unit_group_size)
        else:
            if n == 5:
                units.append(5)
            else:
                while n % best_unit_group_size != 0:
                    units.append(4)
                    n -= 4
                for i in range(n // best_unit_group_size):
                    units.append(best_unit_group_size)
    elif a == 3:
        # Если не делится нацело на 2: отделяем группу из 5 юнитов + делим по 2
        if n % 2 == 1:
            units.append(5)
            n -= 5
            for i in range(n // 2):
                units.append(2)
        # Иначе: просто делим по 2 юнита
        else:
            for i in range(n // 2):
                units.append(2)
    else:
        # Остаток от общего числа юнитов
        remainder = n % best_unit_group_size
        # Если нацело - делим все группы по 3 юнита
        if remainder == 0:
            for i in range(n // best_unit_group_size):
                units.append(best_unit_group_size)
        # Если 1 - делим по 3 юнита + группа с 4 юнитами
        elif remainder == 1:
            units.append(4)
            n -= 4
            for i in range(n // best_unit_group_size):
                units.append(best_unit_group_size)
        # Если 2 - отделяем группу из 2х юнитов + делим по 3 юнита
        elif remainder == 2:
            units.append(2)
            n -= 2
            for i in range(n // best_unit_group_size):
                units.append(best_unit_group_size)

    return _mul_list(units)


def main():
    # Загрузка данных
    n, a = load_input()
    # Вычисление максимального урона
    print(calc_max_damage(n, a))


if __name__ == "__main__":
    main()
