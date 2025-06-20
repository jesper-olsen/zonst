import numpy as np
import matplotlib.pyplot as plt
from fourier_analysis import dft


def plot_data(time_domain_signal, freq_domain_signal):
    """
    Plots the frequency and time domain data.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.tight_layout(pad=4.0)

    Q = len(time_domain_signal)
    x_axis = np.arange(Q)

    # Plot 1: Frequency Domain (Magnitude)
    freq_magnitude = np.abs(freq_domain_signal)
    ax1.stem(x_axis, freq_magnitude, basefmt=" ")
    ax1.set_title("Frequency Domain (Magnitude)")
    ax1.set_xlabel("Frequency Bin")
    ax1.set_ylabel("Magnitude")
    ax1.set_xlim(0, Q - 1)
    ax1.grid(True)

    # Plot 2: Time Domain
    time_real = np.real(time_domain_signal)
    ax2.stem(x_axis, time_real, basefmt=" ")
    ax2.set_title("Time Domain")
    ax2.set_xlabel("Time Sample")
    ax2.set_ylabel("Amplitude")
    ax2.set_xlim(0, Q - 1)
    ax2.grid(True)

    print("Close the plot window to continue.")
    plt.show()


def similarity_theorem_demo(Q):
    """
    Generates a signal to demonstrate the DFT Similarity Theorem.
    Args:
        Q: number of samples (time and frequency)
    """
    width = int(Q / 2)  # Default width

    while True:
        print(f"\nCurrent signal width = {width} (max: {int(Q/2)}, min: 1)")
        try:
            new_width_str = input("Enter new width: ")
            width = int(new_width_str)
            if width > Q / 2:
                width = int(Q / 2)
                print(f"Width clipped to maximum of {width}")
            if width < 1:
                width = 1
                print(f"Width clipped to minimum of {width}")
        except ValueError:
            print("Invalid input. Please enter an integer.")
            continue

        # --- Generate Input Function
        time_signal = np.zeros(Q, dtype=np.complex128)
        start_index = Q // 2 - width
        end_index = Q // 2 + width
        for i in range(start_index, end_index):
            # The original formula is for a raised cosine pulse (Hanning window shape)
            val = (np.sin(np.pi * (i - start_index) / (2 * width))) ** 2
            time_signal[i] = Q * val

        freq_signal = dft(input_signal=time_signal, direction=-1.0, scale_factor=Q)

        plot_data(time_signal, freq_signal)

        if input("More (y/n)? ").lower() != "y":
            break


def main():
    """Main menu loop, replaces lines 20-38"""
    while True:
        print("\n" * 3)
        print("     MAIN MENU")
        print(" 1 = SIMILARITY THEOREM")
        print(" 2 = EXIT")
        print()
        choice = input("      MAKE SELECTION: ")

        if choice == "1":
            similarity_theorem_demo(32)
        elif choice == "2":
            print("Exiting.")
            break
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
