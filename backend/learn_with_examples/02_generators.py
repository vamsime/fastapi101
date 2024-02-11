price = [1, 2, 3, 9, 10]

price_iter=price.__iter__()

print(price_iter.__next__())
print(price_iter.__next__())

while True:
    try:
        print(price_iter.__next__())
    except StopIteration:
        break


class InfiniteNaturalNumbers:
    def __init__(self) -> None:
        self.num = 1

    def __iter__(self):
        return self

    def __next__(self):
        num = self.num
        self.num += 1
        return num


print("+"*100)
values = iter(InfiniteNaturalNumbers())
print(next(values))
print(values.__next__())


print("+"*100)


def return_values():
    """This is an example of a simple generator"""
    yield 1
    yield 20
    yield "thirty"


value = return_values()
print(value.__next__())
print(next(value))
print(value.__next__())


def even_numbers():
    # generate  the even_numbers < 20
    for i in range(1, 11):
        yield 2 * i


evens = even_numbers()

while True:
    try:
        print(evens.__next__())
    except StopIteration:
        break

