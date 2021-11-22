def get_index(suffix_array, pattern):
    index = []
    for i in suffix_array:
        if s[i: i + len(pattern)] == pattern:
            index.append(i)
    return ' '.join([str(i) for i in sorted(index)])

def get_suffix_array(str_sample):
    lis = list(str_sample)
    suffix_array = {v: k for k, v in enumerate(["".join(trim_elem) for trim_elem in [lis[-len(str_sample)+idx:] for idx in range(len(str_sample))]])}
    return [suffix_array.get(k) for k in sorted(list(suffix_array.keys()))]

s = input()
n = int(input())

patterns = []
for i in range(n):
    patterns.append(input())

suffix_array = get_suffix_array(s)
for pattern in patterns:
    print(get_index(suffix_array, pattern))
