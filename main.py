def print_min(s):
    print(f'Минимальное: {min(s)}')

def print_max(s):
    print(f'Максимальное: {max(s)}')

def print_sum(s):
    print(f'Сумма: {sum(s)}')

with open("file.txt", "r") as f:
    s = list(map(int, f.read().split()))
    print_min(s)
    print_max(s)
    print_sum(s)
