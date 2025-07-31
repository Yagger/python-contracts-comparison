"""
Core metaclass and the baseclasses for drivers are defined here
"""

import warnings
from typing import Any, cast


class CoreMetaclass(type):
    """
    Metaclass with enforcement

    Checks
        1. whether enforced_functions (kwargs) are defined
        2. whether their arguments are typed as in the base class
        3. checks at a runtime if the arguments passed to and returned from the functions are of the correct type

    Baseclass definition:

        class DriverMetaclass(CoreMetaclass):
        # copy of the CoreMetaclass
            pass

        class SomeBaseClass(metaclass = DriverMetaclass, enforced_functions={'function_1', 'function_2'})

            def function_1(self, argument:type, argument:type)-> type:
                ...

            def function_2(self, argument:type, argument:type)-> type:
                ...
    Implementations are subclassing the baseclasses and are enforced
    to implement the enforced_functions with correct types

    !! Important !!
    The base class must have the 'Base' in its name, as the checks are performed only
    on the class inheriting from it, this way, all classes inherit from the class derived
    from the base class are skipping the function implementation checks
    """

    def __new__(cls, name: str, bases: tuple[type, ...], body: dict[str, Any], **kwargs: dict[str, Any]):
        cls.enforced_functions: set[str] = set()
        if kwargs and "enforced_functions" in kwargs and isinstance(kwargs["enforced_functions"], set):
            cls.enforced_functions = kwargs["enforced_functions"]
        if bases:
            cls.base: type = bases[0]
            if "Base" in cls.base.__name__:
                # check if the enforced functions are present
                missing_functions: set[str] = cast(set[str], cls.enforced_functions.difference(body))
                if missing_functions:
                    raise NotImplementedError(f"Please implement {missing_functions} in {name}")
                # if the base class is defined, check whether the implementation defines the same types
                # loop over functions defined in the baseclass base[0], check the annotations:
                for enforced_function in cls.enforced_functions:
                    base_method = getattr(cls.base, enforced_function, None)
                    child_method = body.get(enforced_function)
                    for argument, argument_type in base_method.__annotations__.items():
                        try:
                            child_argument_type = child_method.__annotations__[argument]
                            if argument_type != child_argument_type:
                                raise Exception(
                                    f"Argument {argument} in {name}.{enforced_function} should be of type "
                                    f"{argument_type}, not {child_argument_type}"
                                )
                        except KeyError:
                            warnings.warn(
                                f"{name}.{enforced_function} is missing {argument}; "
                                f"All required arguments: {base_method.__annotations__}",
                                stacklevel=2,
                            )
                    body[enforced_function] = child_method  # beartype(child_method) # perform type checking at runtime
        return super().__new__(cls, name, bases, body)
