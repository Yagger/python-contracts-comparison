from typing import Protocol, runtime_checkable

@runtime_checkable
class Contract(Protocol):
    @property
    def prop(self) -> float:
        ...

    def required_method(self, a: int) -> str:
        ...
    
    def optional_method(self, a: int) -> str:
        return str(a)
    

class Foo:
    pass

def run():
    foo: Contract = Foo()
    response: str = foo.required_method(1)
    print(response)
    response = foo.optional_method(2)
    print(response)
    print(foo.prop)

if __name__ == "__main__":
    run()