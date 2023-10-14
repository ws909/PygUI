
import weakref as _weak


def weak(obj: object) -> _weak.ReferenceType:
    return _weak.WeakMethod(obj)


# Create function using 'yield' to return a generator, so that the return value is lazely constructed
def lazy(obj: object):
    pass


def overridden_methods(self, base, *functions: str) -> [str]:
    methods = []

    for method in functions:
        self_method = getattr(self, method)
        base_method = getattr(base, method)

        if self_method.__code__ is not base_method.__code__:
            methods.append(method)

    return methods


def minimum(lowest, value):
    if value < lowest:
        return lowest

    return value


def maximum(highest, value):
    if value > highest:
        return highest

    return value

print(min(10, 11))
