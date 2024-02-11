class BaseClass:
    def __init__(self) -> None:
        self.is_cool = True


class InheritClass(BaseClass):
    pass


f = InheritClass()
# print(f.is_cool)


class MyPydantic:
    def is_valid(self, txt):
        if 'admin' in txt:
            return False
        return True


class Starlette:
    def is_valid(self, txt):
        return True


class MyFastAPI(MyPydantic, Starlette):
    pass


f = MyFastAPI()
print(f.is_valid("admin tried to sign in"))
print(MyFastAPI.__mro__)
print(MyFastAPI.__mro__[0])