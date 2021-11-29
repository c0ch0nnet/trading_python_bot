def read_recipe(f):
    dish_name = f.readline().strip()
    count_of_ingredients = int(f.readline().strip())
    cook_book = {dish_name: []}
    for i in range(count_of_ingredients):
        line = f.readline().strip()
        data = line.split(' | ')
        cook_book[dish_name].append({'ingredient_name': data[0], 'quantity':  data[1], 'measure': data[2]})
    return cook_book

cook_book = {}
with open('recipes.txt') as f_read:
    while True:
        cook_book.update(read_recipe(f_read))
        line = f_read.readline()
        if line == '':
            break

print("cook_book = {")
for k, v in cook_book.items():
    print(f"  '{k}': [")
    for i in v:
        print(f'    {i}')
    print(f"    ],")
print("  }")


def get_shop_list_by_dishes(dishes, person_count):
    products_list = []
    for dish in dishes:
        products_list += cook_book[dish] * person_count

    shop_list = {}
    for product in products_list:
        product_name = product['ingredient_name']
        if product_name in shop_list:
            shop_list[product_name]['quantity'] += int(product['quantity'])
        else:
            shop_list[product_name] = {}
            shop_list[product_name]['measure'] = product['measure']
            shop_list[product_name]['quantity'] = int(product['quantity'])
    return shop_list

print()
for i in get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2).items():
    print(i)