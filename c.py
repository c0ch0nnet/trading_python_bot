class Counter:

    def __init__(self):
        self.size = 0
        self.price = 0

    def inc(self):
        self._inc()

    def __inc(self):
        return 123, 321, 1


    def __repr__(self):
        return f'size: {self.size} @ price: {self.price}'

c = Counter()
c.__inc()
print(c)


# b = Counter()
# b.price = 123
# b.size = 321
# print(b)
#
# l = [1, 2, 3]
# print(l)


