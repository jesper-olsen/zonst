## Zonst

Python/rust reimplementation of the [gwbasic](https://en.wikipedia.org/wiki/GW-BASIC) Fourier demos in [1].

References
----------

[1] "Understanding the FFT, A Tutorial on the Algorithm & Software for Laymen, Students, Technicians & Working Engineers" by Anders E. Zonst


DEMOS
-----

The gwbasic demos are in [bas](bas) - some fixes, but mostly the same as in the book.

The python demos make use of numpy and matplotlib, e.g. install locally with the [uv](https://github.com/astral-sh/uv) package manager before running them individually:

```
% uv venv
% uv pip install matplotlib numpy
```

* DFT 1.0: [Discrete Fourier Transform](READMEdft.md)
* DFT5_01a: [Similarity Theorem](READMEdft5_01a.md)
* DFT5_01b: [Addition Theorem](READMEdft5_01b.md)
* DFT5_01c: [Shifting Theorem](READMEdft5_01c.md)
* DFT5_01d: [Stretching Theorem](READMEdft5_01d.md)
* FFT8_01
* FFT8_02
* FFT8_10a
