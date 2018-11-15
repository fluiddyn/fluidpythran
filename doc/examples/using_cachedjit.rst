Cached Just-In-Time compilation
===============================

Using Just-In-Time compilation with the Ahead-Of-Time compiler Pythran is
possible with FluidPythran! It is really a "work in progress" so (i) it can be
buggy and (ii) the API is not great, but it is a good start!

.. literalinclude:: using_cachedjit.py

In the long terms, we won't need the :code:`#pythran import ...` and
:code:`@used_by_cachedjit`...

Comparison Numba vs FluidPythran
--------------------------------

Code taken from this `blog post
<https://flothesof.github.io/optimizing-python-code-numpy-cython-pythran-numba.html>`_
by Florian LE BOURDAIS.

.. literalinclude:: perf_numba.py

The warmup is much longer for FluidPythran but remember that it is a cached JIT
so it is an issue only for the first call of the function. When we reimport the
module, there is no warmup.

Then we see that **Pythran is very good to optimize high-level NumPy code!** In
contrast, (with my setup and on my computer) Numba has not been able to
optimize this function.

However, Numba is good to speedup the code with loops, but even with this code,
it is still slightly slower than Pythran with the high-level NumPy code.