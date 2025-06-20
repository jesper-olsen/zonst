import numpy as np


def dft(input_signal, direction, scale_factor):
    """
    Performs a Discrete Fourier Transform or its inverse.
    This function replaces the GWBASIC subroutine at line 200.

    Args:
        input_signal (np.ndarray): The complex input signal.
        direction (int): -1 for forward transform, +1 for inverse.
        scale_factor (float): The scaling factor (signal length for forward, 1 for inverse).

    Returns:
        np.ndarray: The complex output signal.
    """
    n_points = len(input_signal)

    output_signal = np.zeros(n_points, dtype=np.complex128)

    for j in range(n_points):  # Loop for each output frequency component
        for i in range(n_points):  # Loop to sum over each input point
            # This implements the corrected DFT formula: C_in * e^(-i*theta) for forward
            # The direction variable flips the sign for the inverse transform.
            angle = direction * j * i * 2 * np.pi / n_points
            twiddle_factor = np.exp(1j * angle)
            output_signal[j] += input_signal[i] * twiddle_factor

    return output_signal / scale_factor


# def fft(input_signal):
#     pass
#
# def ifft(input_signal):
#     pass
