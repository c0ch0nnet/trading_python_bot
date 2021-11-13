# контакты для связи: @vananova - telegram, телефон - 89152346022

def gen_sequences(l):
    r = []
    head = l[0]
    for i in l[1:]:
        r.append(f'{head} {i}')
        r.append(f'{head}{i}')
    return r

l = [str(i) for i in range(1, 10)]
l_tail = l[-1:]
l_head = l[0:-1]
for i in reversed(l_head):
    l_tail = [i] + l_tail
    l_tail = gen_sequences(l_tail)

def get_operations(n_):
    operations = []
    n = 2 ** n_
    for i in range(1, n):
        operation = str(bin(i))[2:]
        if len(operation) < n-1:
            operations.append('0' * (n_ - len(operation)) + str(bin(i))[2:])
        else:
            operations.append(str(bin(i))[2:])
    return operations

def gen_expressions(s):
    expressions = []
    l = s.split()
    n = len(l) - 1
    operations = get_operations(n)
    for operation in operations:
        expression = []
        operation = operation.replace('0', '+')
        operation = operation.replace('1', '-')
        expression.append(s[0])
        for i in range(n):
            expression.append(operation[i])
            expression.append(l[1:][i])
        expressions.append(''.join(expression))
    return expressions

for s in l_tail:
    for i in gen_expressions(s):
        if eval(i) == 100:
            print(i)
