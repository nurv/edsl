from abc import ABC, abstractmethod, ABCMeta

import gzip
import json


class PersistenceMixin:
    def save(self, filename):
        with gzip.open(filename, "wb") as f:
            f.write(json.dumps(self.to_dict()).encode("utf-8"))

    @classmethod
    def load(cls, filename):
        with gzip.open(filename, "rb") as f:
            d = json.loads(f.read().decode("utf-8"))
        return cls.from_dict(d)

    def post(self):
        from edsl.utilities.pastebin import post

        post(self)


class RegisterSubclassesMeta(ABCMeta):
    _registry = {}

    def __init__(cls, name, bases, nmspc):
        super(RegisterSubclassesMeta, cls).__init__(name, bases, nmspc)
        if cls.__name__ != "Base":
            RegisterSubclassesMeta._registry[cls.__name__] = cls

    @staticmethod
    def get_registry():
        return dict(RegisterSubclassesMeta._registry)


class Base(PersistenceMixin, ABC, metaclass=RegisterSubclassesMeta):
    @abstractmethod
    def example():
        """This method should be implemented by subclasses."""
        raise NotImplementedError("This method is not implemented yet.")

    @abstractmethod
    def to_dict():
        """This method should be implemented by subclasses."""
        raise NotImplementedError("This method is not implemented yet.")

    @abstractmethod
    def from_dict():
        """This method should be implemented by subclasses."""
        raise NotImplementedError("This method is not implemented yet.")

    @abstractmethod
    def code():
        """This method should be implemented by subclasses."""
        raise NotImplementedError("This method is not implemented yet.")

    def show_methods(self, show_docstrings=True):
        public_methods_with_docstrings = [
            (method, getattr(self, method).__doc__)
            for method in dir(self)
            if callable(getattr(self, method)) and not method.startswith("_")
        ]
        if show_docstrings:
            for method, documentation in public_methods_with_docstrings:
                print(f"{method}: {documentation}")
        else:
            return [x[0] for x in public_methods_with_docstrings]
