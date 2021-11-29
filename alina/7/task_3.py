def read_files(file_name):
    with open(file_name) as f:
        dict_info = {}
        data = f.readlines()

        dict_info['file_name'] = file_name
        dict_info['count_of_line'] = len(data)
        dict_info['data'] = data

        return dict_info


files_name = ['1.txt', '2.txt']
files_data = []

for file_name in files_name:
    files_data.append(read_files(file_name))

sorted_data = sorted(files_data, key=lambda x: x['count_of_line'])

# with open('r.txt', 'w') as f_write:
#     for data in sorted_data:
#         f_write.write(data['file_name'] + '\n')
#         f_write.write(str(data['count_of_line']) + '\n')
#         f_write.write(''.join(data['data']) + '\n')
#
lines = []
for data in sorted_data:
    lines.append(data['file_name'])
    lines.append(str(data['count_of_line']))
    lines.append(''.join(data['data']))

with open('r.txt', 'w') as f:
    f.writelines('\n'.join(lines))