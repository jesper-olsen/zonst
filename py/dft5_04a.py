import numpy as np
import matplotlib.pyplot as plt
from fourier_analysis import dft
import sys


def plot_data_magnitude(time_signal, freq_signal, time_title, freq_title):
    """
    Plots the time domain signal and the magnitude of the frequency domain signal.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.tight_layout(pad=4.0)

    Q = len(time_signal)
    x_axis = np.arange(Q)

    # Plot 1: Time Domain
    time_real = np.real(time_signal)
    ax1.stem(time_real, basefmt=" ")
    ax1.set_title(time_title)
    ax1.set_xlabel("Time Sample (t)")
    ax1.set_ylabel("Amplitude")
    ax1.set_xlim(-1, Q)
    ax1.grid(True)

    # Plot 2: Frequency Domain (Magnitude)
    freq_magnitude = np.abs(freq_signal)
    ax2.stem(freq_magnitude, basefmt=" ")
    ax2.set_title(freq_title)
    ax2.set_xlabel("Frequency Bin")
    ax2.set_ylabel("Magnitude |F|")
    ax2.set_xlim(-1, Q)
    ax2.grid(True)

    print("--> Displaying plots. Close the plot window to continue.")
    plt.show()


def press_enter_to_continue():
    """Pauses execution until the user presses Enter."""
    input("--> Press Enter to continue...")


def stretching_theorem_demo(Q):
    """
    Demonstrates the DFT Stretching/Similarity Theorem.
    Args:
    """
    print("\n--- DEMONSTRATING THE STRETCHING THEOREM ---")
    print("Stretching a signal in the time domain causes its frequency")
    print("spectrum to compress, and vice-versa.")

    # --- STEP 1: A compact signal and its transform ---
    print("\n[PART 1] First, a compact signal and its transform.")
    press_enter_to_continue()

    time_signal_compact = np.zeros(Q, dtype=np.complex128)
    time_signal_compact[:4] = [8, -8, 8, -8]

    freq_signal_compact = dft(time_signal_compact, -1.0, Q)

    print("\nPlotting the compact signal and its transform.")
    plot_data_magnitude(
        time_signal_compact,
        freq_signal_compact,
        "Time: Compact Signal",
        "Frequency: Transform of Compact Signal",
    )

    # --- STEP 2: The signal is stretched and then transformed ---
    print("\n[PART 2] Now, we stretch the time signal by inserting zeros.")
    press_enter_to_continue()

    time_signal_stretched = np.zeros(Q, dtype=np.complex128)
    time_signal_stretched[0] = 8
    time_signal_stretched[2] = -8
    time_signal_stretched[4] = 8
    time_signal_stretched[6] = -8

    freq_signal_stretched = dft(time_signal_stretched, -1.0, Q)

    print("\nPlotting the stretched signal and its transform.")
    plot_data_magnitude(
        time_signal_stretched,
        freq_signal_stretched,
        "Time: Stretched Signal",
        "Frequency: Transform of Stretched Signal",
    )

    print("\n--- CONCLUSION ---")
    print(
        "Notice the frequency plot in Part 2 is a compressed version of the plot from Part 1."
    )
    print(
        "This demonstrates that stretching the time signal compressed its frequency spectrum."
    )
    press_enter_to_continue()


def main():
    while True:
        print("\n" * 3)
        print("     MAIN MENU")
        print(" 1 = STRETCHING THEOREM")
        print(" 2 = EXIT")
        print()
        choice = input("      MAKE SELECTION: ")

        if choice == "1":
            stretching_theorem_demo(32)
        elif choice == "2":
            print("Exiting.")
            break
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
