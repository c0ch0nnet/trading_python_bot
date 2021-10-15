def print_min(s):
    return min(s)

def print_max(s):
    return max(s)

def print_sum(s):
    return sum(s)

assert print_min([1, 4, 2, 3]) == 1
assert print_max([1, 4, 2, 3]) == 4
assert print_sum([1, 4, 2, 3]) == 10

with open("file.txt", "r") as f:
    try:
        l = f.read().split()
        s = list(map(int, l))
        print(f'Минимальное: {print_min(s)}')
        print(f'Максимальное: {print_max(s)}')
        print(f'Сумма: {print_sum(s)}')
    except:
        print(l)

