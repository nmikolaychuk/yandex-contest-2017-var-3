import string

from collections import OrderedDict

TASKS_ID = string.ascii_uppercase
INPUT_FILE = "input.txt"
RESULT = "Result"
SUMMARY = "SUM"
BONUS = "BONUS"
FAIL = "FAIL"
OK = "OK"
LOWER = 0
UPPER = 10000


def load_input():
    with open(INPUT_FILE, mode='r') as f:
        lines = f.readlines()
    return [line.rstrip().split() for line in lines]


def calculate_summary(parsed_dict: OrderedDict) -> OrderedDict:
    for k, v in parsed_dict.items():
        summary = 0
        for _k, _v in v.items():
            if _k != SUMMARY:
                summary += _v

        if summary < 0:
            summary = 0

        v[SUMMARY] = summary
    return parsed_dict


def remove_support_keys(parsed_dict: OrderedDict) -> OrderedDict:
    for k, v in parsed_dict.items():
        del v[BONUS]
    return parsed_dict


def add_missed_keys(parsed_dict: OrderedDict) -> OrderedDict:
    all_keys = []
    for k, v in parsed_dict.items():
        for _k, _v in v.items():
            all_keys.append(_k)

    unique_keys = set(all_keys)
    for k, v in parsed_dict.items():
        for key in unique_keys:
            if key not in list(v.keys()):
                v[key] = 0

    return parsed_dict


def sort_dict(parsed_dict: OrderedDict) -> OrderedDict:
    sorted_dict = {}
    for k, v in parsed_dict.items():
        summary = v[SUMMARY]
        v_without_sum = OrderedDict()
        for _k, _v in v.items():
            if _k != SUMMARY:
                v_without_sum[_k] = _v

        v_without_sum = OrderedDict(sorted(v_without_sum.items()))
        v_without_sum[SUMMARY] = summary
        sorted_dict[k] = v_without_sum

    return OrderedDict(sorted(sorted_dict.items(), key=lambda x: (-x[1][SUMMARY], x[0])))


def validate_name(name: str) -> bool:
    return all(map(lambda c: c in string.ascii_letters, name))


def parse_input(input_data: list) -> OrderedDict:
    parsed_dict = OrderedDict()
    # Парсинг входных данных
    for line in input_data:
        # Если строка не пустая...
        if not line:
            pass
        else:
            # Result или нет?
            first_word = line[0]
            if first_word == RESULT:
                # Обработка 1-го этапа
                # Проверка имени
                name = line[1]
                if not name.istitle() or not validate_name(name):
                    continue

                # Часть с результатами после имени: [A, 500, B, 500, D, 450]
                tasks_id = line[2::2]

                # Проверка идентификаторов на уникальность
                if len(set(tasks_id)) != len(tasks_id):
                    continue

                tasks_rating = line[3::2]

                # Проверка на равное количество идентификаторов и очков
                if len(tasks_rating) != len(tasks_id):
                    continue

                # Проверка идентификаторов задачи
                is_valid = True
                for i, task in enumerate(tasks_id):
                    # Проверка, что идентификатор задачи - заглавная латинская буква
                    if task not in TASKS_ID:
                        is_valid = False
                        break

                    # Проверка, что рейтинг - число в диапазоне 0 - 10000
                    if not tasks_rating[i].isdigit():
                        is_valid = False
                        break

                    if int(tasks_rating[i]) > UPPER or int(tasks_rating[i]) < LOWER:
                        is_valid = False
                        break

                if not is_valid:
                    continue

                exist_task_id = None
                if name in parsed_dict:
                    exist_task_id = list(parsed_dict[name].keys())

                if exist_task_id is None:
                    results_dict = OrderedDict()
                    for i, task in enumerate(tasks_id):
                        results_dict[task] = int(tasks_rating[i])

                    results_dict[BONUS] = 0
                    results_dict[SUMMARY] = 0
                    parsed_dict[name] = results_dict

                else:
                    for i, task in enumerate(tasks_id):
                        if task not in list(parsed_dict[name].keys()):
                            parsed_dict[name][task] = int(tasks_rating[i])

            elif first_word.istitle() and validate_name(first_word):
                # Если слово начинается с заглавной буквы и все остальные - строчные
                second_name = line[1]
                if not second_name.istitle() or not validate_name(second_name):
                    continue

                # Проверка идентификатора задачи
                task_id = line[2]
                if task_id not in TASKS_ID:
                    continue

                # Проверка результата взлома
                hack_result = line[3]
                if hack_result != OK and hack_result != FAIL:
                    continue

                if not parsed_dict:
                    continue

                if first_word == second_name:
                    continue

                if first_word not in list(parsed_dict.keys()):
                    parsed_dict[first_word] = OrderedDict()
                    parsed_dict[first_word][BONUS] = 0
                    parsed_dict[first_word][SUMMARY] = 0

                # Если взлом успешный
                if task_id not in list(parsed_dict[second_name].keys()):
                    continue

                if hack_result == OK:
                    parsed_dict[first_word][BONUS] += 50
                    parsed_dict[second_name][task_id] = 0
                elif hack_result == FAIL:
                    parsed_dict[first_word][BONUS] -= 25
            else:
                continue

    # Суммирование результатов
    parsed_dict = calculate_summary(parsed_dict)
    # Удаление лишних полей
    parsed_dict = remove_support_keys(parsed_dict)
    # Добавление недостающих ключей
    parsed_dict = add_missed_keys(parsed_dict)
    # Сортировка результатов
    parsed_dict = sort_dict(parsed_dict)

    for k, v in parsed_dict.items():
        keys = list(v.keys())
        if keys == [SUMMARY]:
            return OrderedDict()

    return parsed_dict


def get_row_edge(col_sym_count: OrderedDict) -> str:
    row_edge = "+"
    for k, v in col_sym_count.items():
        row_edge += '-' * v + "+"
    return row_edge


def get_table_data(parsed_data: OrderedDict, col_sym_count: OrderedDict) -> str:
    row_edge = get_row_edge(col_sym_count)

    row_data = row_edge
    identifier = 1
    for k, v in parsed_data.items():
        # Добавление идентификатора строки и имени участника
        spaces_id = col_sym_count["id"] - len(str(identifier))
        spaces_name = col_sym_count["name"] - len(str(k))
        row_data += "\n|" + ' ' * spaces_id + str(identifier) + "|" + k + ' ' * spaces_name + "|"
        # Добавление результатов
        for _k, _v in v.items():
            space_count = col_sym_count[_k] - len(str(_v))
            row_data += ' ' * space_count + str(_v) + "|"

        row_data += "\n" + row_edge
        identifier += 1
    return row_data


def print_parsed_data(parsed_data: OrderedDict) -> None:
    if list(parsed_data.keys()):
        col_sym_count = OrderedDict()
        col_sym_count["id"] = len(str(len(parsed_data)))
        col_sym_count["name"] = max([len(name) for name in list(parsed_data.keys())]) + 1

        # Добавление всех ключей в словарь учета символов.
        for key in list(list(parsed_data.values())[0].keys()):
            col_sym_count[key] = 0

        for k, v in parsed_data.items():
            for _k, _v in v.items():
                if col_sym_count[_k] < len(str(_v)):
                    col_sym_count[_k] = len(str(_v))

        # Получение строки-таблицы
        print(get_table_data(parsed_data, col_sym_count))


def main():
    # Загрузка входных данных
    input_data = load_input()
    # Парсинг данных
    parsed_data = parse_input(input_data)
    # Отображение данных
    print_parsed_data(parsed_data)


if __name__ == "__main__":
    main()
