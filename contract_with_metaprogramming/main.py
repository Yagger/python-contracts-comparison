from metaclass import CoreMetaclass

class MyCoreMetaclass(CoreMetaclass):
    pass

class Contract(
    metaclass=MyCoreMetaclass,
    enforced_functions={"required_method"},  # type: ignore
):
    def required_method(self, a: int) -> str:
        ...
    
    def optional_method(self, a: int) -> str:
        return str(a)
    

class Foo(Contract):
    pass

def run():
    foo: Foo = Foo()
    response: str = foo.required_method(1)
    print(response)
    response = foo.optional_method(2)
    print(response)

if __name__ == "__main__":
    run()