from typing import List, Tuple, Dict, Union, Annotated, Optional, Callable

price: Annotated[int, float] = [10, 12, 14, 16.2, 17.5, 20]
print(price)
price: Tuple[int, int, float] = [10, 12, 14]
print(price)
price: Dict[str, int] = {'item1': 23, 'item2': 45}
print(price)


def inr_to_usd(inp: float) -> Union[float, None]:  # the data type that we will return can be float or None!
    try:
        conversion_factor=75
        final_value=inp/conversion_factor
        return final_value
    except TypeError:
        return None


print(round(inr_to_usd(20), 2))


Image = List[List[int]]


def flatten_image(pic_inp: Image) -> List:
    flat_list = []
    for sl in pic_inp:
        for itm in sl:
            flat_list.append(itm)
    return flat_list


img = [[1, 2, 3], [4, 5, 6]]
print(img, " => ", flatten_image(img))


class Job:

    def __init__(self, title: str, description: Optional[str]) -> None:
        self.title = title
        self.description = description

    def __repr__(self):
        return self.title


j1 = Job(title="Team Lead", description="Leads a team of 20")
j2 = Job(title="Lead Data Engineer", description="Leads the data team of 4")

print(f"{j1.title} {j1.description}")
print(f"{j2.title} {j2.description}")

jobs: List[Job] = [j1, j2]
print(type(jobs), type(jobs[0]))


def smart_divide(func: Callable[[int, int], float]):
    def inner(a, b):
        if b == 0:
            print("Oops! Division by 0 is not permitted!")
            return None
        return func(a, b)
    return inner


@smart_divide
def divide(a, b):
    print(a/b)


divide(9, 0)
divide(9, 2)
