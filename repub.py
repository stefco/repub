# (c) Stefan Countryman, 2020

"(Re)port (Pub)lisher: report serialization types for structured inputs"

__version__ = '0.1.0'

from typing import (
    OrderedDict,
    Optional,
    Union,
    Iterable,
    Any,
    Tuple,
    Callable,
    Dict,
)


class Reportable:
    "Base class for report serializers."

    def _repr_html_():
        "Define this function to make this class summarizable in HTML."
        raise NotImplementedError()

    def _repr_latex_():
        "Define this function to make this class summarizable in LaTeX."
        raise NotImplementedError()

    def __str__():
        "Define this function to make this class summarizable as plain text."
        raise NotImplementedError()


class TabularCollectionMeta(type):

    def __getitem__(
            self,
            columns: Union[
                Iterable[str],
                Tuple[Iterable[str], Iterable[str]],
                Tuple[
                    Iterable[str],
                    Iterable[str],
                    Iterable[Optional[Callable]]
                ],
                Tuple[Iterable[str], Dict[str, Any]],
                Tuple[Iterable[str], Iterable[str], Dict[str, Any]],
                Tuple[
                    Iterable[str],
                    Iterable[str],
                    Iterable[Optional[Callable]],
                    Dict[str, Any]
                ],
            ]
    ):
        if (not isinstance(columns, tuple)) or isinstance(columns[0], str):
            cols = props = columns
            trans = tuple([None]*len(cols))
        else:
            if isinstance(columns[-1], dict):
                *columns, opts = columns
            else:
                opts = {}
            cols = tuple(columns[0])
            props = tuple(columns[1]) if len(columns) > 1 else cols
            trans = tuple(columns[2]) if len(columns) > 2 else tuple([None]*len(cols))
        return self.__class__(
            self.__name__+'Derived',
            (self,),
            {
                'columns': cols,
                'properties': props,
                'transforms': trans,
                'opts': opts,
            }
        )


class TabularCollection(Reportable, metaclass=TabularCollectionMeta):
    """
    Serialize any iterable of objects and present a table of their
    arbitrarily transformed properties in various formats.
    """
    loader: Callable
    columns: Iterable[str]
    properties: Iterable[str]
    transforms: Iterable[Optional[Callable]]
    opts: Dict[str, Any]

    def __init__(self, target: Iterable[Any]):
        self._tabargs = (
            [
                [
                    (t or (lambda x: x))(self.loader(m, p))
                    for p, t in zip(self.properties, self.transforms)
                ]
                for m in target
            ],
            self.columns,
        )

    def _repr_html_(self):
        from tabulate import tabulate
        return tabulate(*self._tabargs, **self.opts, tablefmt='html')

    def _repr_latex_(self):
        from tabulate import tabulate
        return tabulate(*self._tabargs, **self.opts, tablefmt='latex')

    def __str__(self):
        from tabulate import tabulate
        return tabulate(*self._tabargs, **self.opts, tablefmt='presto')


class TabularModelCollection(TabularCollection):
    loader = getattr


class TabularListCollection(TabularCollection):
    loader = lambda x, k: x[k]
