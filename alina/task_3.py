with open('3.txt') as f:
    data = f.read()
    print(type(data))
    print(data)




# 'name_file': 2.txt
# 'count_of_line': 1
# 'data': Строка номер 1 файла номер 2

# 1.txt
# 2
# Строка номер 1 файла номер 1
# Строка номер 2 файла номер 1

# with open('1.txt') as f:
#     data = f.readline()
#     print(type(data))
#     print(data)

def read_file_to_list(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        # print(lines)
        return lines

file_names = ['2.txt', '1.txt']
files_data = []
for file_name in file_names:
    file_data = {}
    file_data['name'] = file_name
    file_data['data'] = read_file_to_list(file_name)
    file_data['len'] = len(read_file_to_list(file_name))
    files_data.append(file_data)


print(files_data)
sorted_data = sorted(files_data, key=lambda x: x['len'])

lines = []
for data in sorted_data:
    lines.append(data['name'])
    lines.append(str(data['len']))
    lines.append(''.join(data['data']))
    # f.write(data['name'] + '\n')
    # f.write(str(data['len']) + '\n')
    # f.write(''.join(data['data']) + '\n')

with open('r.txt', 'w') as f:
    f.writelines('\n'.join(lines))

