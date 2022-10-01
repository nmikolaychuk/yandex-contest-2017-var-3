def load_input_data():
    n = int(input())
    values = list(map(int, input().strip().split()))
    return n, values


def main():
    # Загрузка входных данных
    n, values = load_input_data()

    # 1-й ход
    petya_values = []
    vasya_values = []

    # Пока есть карты в колоде...
    while values:
        # Ход Пети
        petya_values.append(values[0])
        del values[0]

        # Ход Васи
        vasya_values.append(values[0])
        del values[0]

        # Сравнение карт
        if petya_values[-1] > vasya_values[-1]:
            # Берет Петя
            petya_values.append(values[0])
            del values[0]

        else:
            # Берет Вася
            vasya_values.append(values[0])
            del values[0]


    if sum(petya_values) > sum(vasya_values):
        return "Vasya"
    return "Petya"


if __name__ == "__main__":
    print(main())
