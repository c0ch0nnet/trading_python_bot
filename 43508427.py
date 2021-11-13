# контакты для связи: @vananova - telegramm

import re

class RomanNumber():
    @staticmethod
    def is_roman(num):
        pattern = re.compile(r"""   ^M{0,3}
                                    (CM|CD|D?C{0,3})?
                                    (XC|XL|L?X{0,3})?
                                    (IX|IV|V?I{0,3})?$
                                    """, re.VERBOSE)
        if re.match(pattern, num):
            return True
        return False

    def __init__(self, value):
        if self.is_roman(value):
            self.rov_value = value
        else:
            print('ошибка')
            self.rov_value = None

    def decimal_number(self):
        if self.rov_value is None:
            print('ошибка')
            return None
        result = 0
        f = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        i = 0
        while i < len(self.rov_value) - 1:
            if f[self.rov_value[i + 1]] > f[self.rov_value[i]]:  # Смотрите, если применяются специальные правила
                result += f[self.rov_value[i + 1]] - f[self.rov_value[i]]
                i += 2
            else:  # Если не сделано, вывод напрямую
                result += f[self.rov_value[i]]
                i += 1
        if i < len(self.rov_value):  # Второе-последнее специальное правило (используйте i, чтобы судить)
            result += f[self.rov_value[len(self.rov_value) - 1]]
        return result

    def __repr__(self):
        return f'{self.rov_value}'


num_1 = RomanNumber('VI')
print(num_1.rov_value)
print(num_1.decimal_number())
print(num_1)
num_2 = RomanNumber('IIII')
print(num_2.rov_value)
num_3 = RomanNumber('XXIV')
print(num_3.decimal_number())
num_4 = RomanNumber('QER2')
nums = []
nums.append(num_1)
nums.append(num_2)
nums.append(num_3)
nums.append(num_4)
print(nums)
print(RomanNumber.is_roman('MMMCMLXXXVI'))
print(RomanNumber.is_roman('MMMMMLXXXVI'))

