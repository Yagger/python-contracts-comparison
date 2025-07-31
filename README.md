Multiple ways exist to achieve contract functionality in Python, also known as interface, protocol, typeclass, type alias, etc. Different name but the idea is similar. The function that accepts a type as argument, need to be sure the type implements certain properties and methods.

aka

```python
def foo(x: OpenableClosable) -> None:
    x.open()
    x.close()
```

In Python, this can be achieved using:
- `abc` module (Abstract Base Classes)
- `typing.Protocol` type
- using metaprogramming directly

Disclaimer about metaprogramming: while it's definitely doable to metaprogram the contracts directly, and this is how `abc` and `typing.Protocol` are done internally, I couldn't achieve good results with it in my tests. Didn't spend much time on it, because since version 3.8 Python supports contract functionality natively via first two methods.


|Feature|ABC (Abstract Base Class)|Protocol (Structural Typing)|
|-|-|-|
|Type of typing|Nominal (explicit inheritance)|Structural (duck typing with structure)|
|Needs inheritance?|Yes|No|
|Part of stdlib?|Yes (`abc` module)|Yes (`typing` module)|
|Supports default implementation/optional props|Yes|No|
|Runtime checking|Yes (will fail at initialization)|No (will pass initialization and only fail at using the missing method)|
|Static checking|Yes|Yes|
|Can enforce both methods and properties|Methods only|Both|
|[Callback interface](https://mypy.readthedocs.io/en/stable/protocols.html#callback-protocols)|No|Yes|
|Lines of code|More|Less (no decorators)|
|Composable|Yes (via multiple inheritance, but here it's ok)|Yes (via multiple inheritance, but here it's ok)|

Note about multiple inheritance: while generally a bag of bugs to avoid, in this particular case of simple contract composition it's ok to use.
```python
# ABC
class OpenCloseable(Openable, Closable):
    pass

# Protocol (always put Protocol last in the inheritance list)
class OpenCloseable(Openable, Closable, Protocol):
    pass
```

For development and testing I used VS Code with Pylance extension. The `pyrightconfig.json` file in this project sets the mode of the type checker (Pylance uses pyright) to `strict`. This files is used both by Pylance extension and by command-line `pyright` tool.

This project contains 3 directories. It does not depend on any libraries outside of Python 3.10 native tools. You can download it, open in you IDE, try them all and make a pick based on your needs and feelings.

Or you can see the screenshots from my testing for a quick pick:

### ABC
IDE check (Pylance)

<img width="1044" height="652" alt="Screenshot 2025-07-30 at 17 32 58" src="https://github.com/user-attachments/assets/910b2318-759a-411f-8fe8-304e02ff1757" />

Command line static check (`pyright`)

<img width="628" height="88" alt="Screenshot 2025-07-30 at 17 37 15" src="https://github.com/user-attachments/assets/ebca6f4f-351a-42a6-b02c-19d0998d8f14" />

Running with Python interpreter

<img width="602" height="122" alt="Screenshot 2025-07-30 at 17 34 36" src="https://github.com/user-attachments/assets/9b34a0e5-d9ce-4b5b-bfe7-8d1c52a1946b" />

### Protocol
IDE check (Pylance)

<img width="973" height="683" alt="Screenshot 2025-07-30 at 17 31 30" src="https://github.com/user-attachments/assets/00bedc72-a149-40df-b0c9-772bada918f2" />

Command line static check (`pyright`)

<img width="793" height="138" alt="Screenshot 2025-07-30 at 17 37 31" src="https://github.com/user-attachments/assets/62bb5e23-e6f7-46b6-8b85-95395361f584" />

Running with Python interpreter

<img width="483" height="121" alt="Screenshot 2025-07-30 at 17 32 11" src="https://github.com/user-attachments/assets/8e0d6db2-93c9-4b22-bbef-b58451de9343" />

### Metaprogramming
IDE check (Pylance)

<img width="931" height="708" alt="Screenshot 2025-07-31 at 08 32 01" src="https://github.com/user-attachments/assets/95477eb1-c7d9-4f28-9119-86cbefe861f9" />

Command line static check (`pyright`)

<img width="511" height="40" alt="Screenshot 2025-07-31 at 10 02 07" src="https://github.com/user-attachments/assets/8c8dde48-0c31-4334-933b-02094fe42029" />

Running with Python interpreter

<img width="503" height="54" alt="Screenshot 2025-07-30 at 17 36 55" src="https://github.com/user-attachments/assets/866e2347-d2fb-468c-8d2d-4452f902b563" />
