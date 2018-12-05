from tokenize import tokenize, untokenize, NAME, OP
from token import tok_name
from io import BytesIO
import inspect

import black

import numpy as np

from fluidpythran.log import logger, set_log_level
from fluidpythran.util import get_source_without_decorator
from fluidpythran.annotation import compute_pythran_types_from_valued_types

from fluidpythran import Array, Type, NDim

# set_log_level("debug")

A = Array[Type(float, int), NDim(1, 2)]


def pythran_def_method(func):
    return func


class Transmitter:
    freq: float

    def __init__(self):
        pass

    @pythran_def_method
    def __call__(self, inp: A):
        """My docstring"""
        return inp * np.exp(np.arange(len(inp)) * self.freq * 1j)


def produce_pythran_code_class(cls, func_name):

    func = cls.__dict__[func_name]
    cls_name = cls.__name__

    cls_annotations = cls.__annotations__

    signature = inspect.signature(func)
    types_func = [param.annotation for param in signature.parameters.values()][1:]
    # args_func = list(signature.parameters.keys())[1:]

    return func

    # bug IndentationError (util.strip_typehints)
    src = get_source_without_decorator(func)

    tokens = []
    attributes = set()

    using_self = False

    g = tokenize(BytesIO(src.encode("utf-8")).readline)
    for toknum, tokval, a, b, c in g:
        logger.debug((tok_name[toknum], tokval))

        if using_self == "self":
            if toknum == OP and tokval == ".":
                using_self = tokval
                continue
            elif toknum == OP and tokval == ",":
                tokens.append((NAME, "self"))
                using_self = False
            else:
                raise RuntimeError

        if using_self == ".":
            if toknum == NAME and tokval in cls_annotations:
                using_self = False
                tokens.append((NAME, "self_" + tokval))
                attributes.add(tokval)
                continue
            else:
                raise RuntimeError

        if toknum == NAME and tokval == "self":
            using_self = tokval
            continue

        tokens.append((toknum, tokval))

    attributes = sorted(attributes)

    types_attrs = [cls_annotations[attr] for attr in attributes]

    attributes = ["self_" + attr for attr in attributes]

    index_self = tokens.index((NAME, "self"))

    tokens_attr = []
    for ind, attr in enumerate(attributes):
        tokens_attr.append((NAME, attr))
        tokens_attr.append((OP, ","))

    tokens = tokens[:index_self] + tokens_attr + tokens[index_self + 2 :]

    index_func_name = tokens.index((NAME, func_name))
    name_pythran_func = f"__for_method__{cls_name}__{func_name}"
    tokens[index_func_name] = (NAME, name_pythran_func)

    new_code = untokenize(tokens).decode("utf-8")
    new_code = black.format_str(new_code, line_length=82)

    # args_pythran = attributes + args_func
    types_pythran = types_attrs + types_func

    pythran_signatures = "\n"

    for types_string_signature in compute_pythran_types_from_valued_types(
        types_pythran
    ):
        pythran_signatures += (
            "# pythran export "
            + name_pythran_func
            + "("
            + ", ".join(types_string_signature)
            + ")\n"
        )

    pythran_code = pythran_signatures + "\n" + new_code
    return pythran_code


func = pythran_code = produce_pythran_code_class(Transmitter, "__call__")
print(pythran_code)