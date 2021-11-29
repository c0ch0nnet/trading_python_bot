l = [
    {'name': '2.txt', 'data': ['Строка номер 1 файла номер 2'], 'len': 1},
    {'name': '1.txt', 'data': ['Строка номер 1 файла номер 1', 'Строка номер 2 файла номер 1'], 'len': 2}]


def get_len(x):
    # return x['len']
    return x['name']

# print(sorted(l, key=lambda x: x['data'][0][-1]))



cook_book = [
    {'ingredient_name': 'Яйцо', 'quantity': 2, 'measure': 'шт.'},
    {'ingredient_name': 'Молоко', 'quantity': 100, 'measure': 'мл'},
    {'ingredient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'}
    ]


def get_len(x):
    # return x['len']
    return x['quantity']

print(sorted(cook_book, key=get_len, reverse=True))