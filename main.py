def print_min(s):
    print(f'Минимальное: {min(s)}')

def print_max(s):
    print(f'Максимальное: {max(s)}')

def print_sum(s):
    print(f'Сумма: {sum(s)}')

with open("file.txt", "r") as f:
    try:
        l = f.read().split()
        s = list(map(int, l))
        print_min(s)
        print_max(s)
        print_sum(s)
    except:
        print(l)
