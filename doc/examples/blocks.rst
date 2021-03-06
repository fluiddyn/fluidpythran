Use blocks of code to define Pythran functions
==============================================

.. warning ::

   I'm not satisfied by the syntax for Pythran blocks so I (PA) proposed an
   alternative syntax in `issue #29
   <https://bitbucket.org/fluiddyn/fluidpythran/issues/29>`_.


FluidPythran blocks can be used with classes and more generally in functions
with lines that cannot be compiled by Pythran.

.. literalinclude:: blocks.py

For blocks, we need a little bit more of Python.

- At import time, we have :code:`fp = FluidPythran()`, which detects which
  Pythran module should be used and imports it. This is done at import time
  since we want to be very fast at run time.

- In the function, we define a block with three lines of Python and special
  Pythran annotations (:code:`# pythran block`). The 3 lines of Python are used
  (i) at run time to choose between the two branches (:code:`is_transpiled` or
  not) and (ii) at compile time to detect the blocks.

Note that the annotations in the command :code:`# pythran block` are different
(and somehow easier to write) than in the standard command :code:`# pythran
export`.

.. note ::

    Moreover, for the time being, one needs to explicitly write the "returned"
    variables (after :code:`->`). However, it is a redundant information so we
    could avoid this in future (see `issue #1
    <https://bitbucket.org/fluiddyn/fluidpythran/issues/1/no-need-for-explicit-return-values-in>`_).

.. warning ::

    The two branches of the :code:`if fp.is_transpiled` are not equivalent! The
    user has to be careful because it is not difficult to write such buggy code:

    .. code :: python

        c = 0
        if fp.is_transpiled:
            a, b = fp.use_pythranized_block("buggy_block")
        else:
            # pythran block () -> (a, b)
            a = b = c = 1

        assert c == 1

.. note ::

    The Pythran keyword :code:`or` cannot be used in block annotations (not yet
    implemented, see `issue #2
    <https://bitbucket.org/fluiddyn/fluidpythran/issues/2/implement-keyword-or-in-block-annotation>`_).

Blocks can now also be defined with type hints!

.. literalinclude:: blocks_type_hints.py
