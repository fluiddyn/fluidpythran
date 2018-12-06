import numpy as np

# pythran import numpy as np

from fluidpythran import pythran_class, pythran_def


@pythran_class
class Transmitter:

    freq: float

    def __init__(self, freq):
        self.freq = float(freq)

    @pythran_def
    def __call__(self, inp: "float[]"):
        """My docstring"""
        return inp * np.exp(np.arange(len(inp)) * self.freq * 1j)


if __name__ == "__main__":
    inp = np.ones(2)
    freq = 1.0
    trans = Transmitter(freq)

    def for_check(freq, inp):
        return inp * np.exp(np.arange(len(inp)) * freq * 1j)

    assert np.allclose(trans(inp), for_check(freq, inp))
