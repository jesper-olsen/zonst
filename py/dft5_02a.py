import numpy as np
import matplotlib.pyplot as plt
from fourier_analysis import dft


def plot_data(time_domain_signal, freq_domain_signal, time_title, freq_title):
    """
    Plots the frequency and time domain data with custom titles.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.tight_layout(pad=4.0)

    Q = len(time_domain_signal)
    x_axis = np.arange(Q)

    # Plot 1: Frequency Domain (Magnitude)
    freq_magnitude = np.abs(freq_domain_signal)
    ax1.stem(x_axis, freq_magnitude, basefmt=" ")
    ax1.set_title(freq_title)
    ax1.set_xlabel("Frequency Bin")
    ax1.set_ylabel("Magnitude")
    ax1.set_xlim(0, Q - 1)
    ax1.grid(True)

    # Plot 2: Time Domain
    time_real = np.real(time_domain_signal)
    ax2.stem(x_axis, time_real, basefmt=" ")
    ax2.set_title(time_title)
    ax2.set_xlabel("Time Sample")
    ax2.set_ylabel("Amplitude")
    ax2.set_xlim(0, Q - 1)
    ax2.grid(True)

    print("--> Displaying plot. Close the plot window to continue.")
    plt.show()


def press_enter_to_continue():
    """Pauses execution until the user presses Enter."""
    input("--> Press Enter to continue...")


def addition_theorem_demo(Q):
    """
    Demonstrates the DFT Addition Theorem.
    Args:
        Q: number of samples (time and frequency)
    """
    print("\n--- DEMONSTRATING THE ADDITION THEOREM: F{f1 + f2} = F{f1} + F{f2} ---")

    # --- STEP 1: Generate f1 (rising edge) and get its transform F{f1} ---
    print("\n[PART 1] Calculating the transform of the first function, f1(t).")
    time_signal_f1 = np.zeros(Q, dtype=np.complex128)
    for i in range(Q // 2):
        time_signal_f1[i] = 1 - np.exp(-i / 5.0)

    freq_signal_f1 = dft(input_signal=time_signal_f1, direction=-1.0, scale_factor=Q)
    plot_data(
        time_signal_f1, freq_signal_f1, "Time: f1(t) [Rising Edge]", "Frequency: F{f1}"
    )

    # --- STEP 2: Generate f2 (falling edge) and get its transform F{f2} ---
    print("\n[PART 2] Calculating the transform of the second function, f2(t).")
    press_enter_to_continue()
    time_signal_f2 = np.zeros(Q, dtype=np.complex128)
    k4 = 1 - np.exp(-(Q / 2) / 5.0)  # Corrected scaling factor for continuity
    for i in range(Q // 2, Q):
        time_signal_f2[i] = k4 * np.exp(-(i - Q // 2) / 5.0)

    freq_signal_f2 = dft(input_signal=time_signal_f2, direction=-1.0, scale_factor=Q)
    plot_data(
        time_signal_f2, freq_signal_f2, "Time: f2(t) [Falling Edge]", "Frequency: F{f2}"
    )

    # --- STEP 3: Sum the transforms (F{f1} + F{f2}) and show the result ---
    print("\n[PART 3] Summing the two frequency transforms: F{f1} + F{f2}.")
    press_enter_to_continue()
    freq_sum_of_transforms = freq_signal_f1 + freq_signal_f2
    # For visualization, we plot the summed time signal f1+f2 alongside the summed transform
    time_sum_of_signals = time_signal_f1 + time_signal_f2
    plot_data(
        time_sum_of_signals,
        freq_sum_of_transforms,
        "Time: f1(t) + f2(t)",
        "Frequency: F{f1} + F{f2}",
    )

    # --- STEP 4: Sum the time signals (f1 + f2), then transform to get F{f1+f2} ---
    print("\n[PART 4] Now, summing the time signals first, then taking the transform.")
    press_enter_to_continue()
    # We already created time_sum_of_signals in the previous step
    freq_of_summed_time = dft(
        input_signal=time_sum_of_signals, direction=-1.0, scale_factor=Q
    )
    plot_data(
        time_sum_of_signals,
        freq_of_summed_time,
        "Time: f1(t) + f2(t)",
        "Frequency: F{f1 + f2}",
    )

    print("\n--- CONCLUSION ---")
    print("Notice the frequency plot from PART 4 is identical to the one from PART 3.")
    print(
        "This demonstrates that the transform of the sum is the sum of the transforms."
    )
    press_enter_to_continue()


def main():
    """Main menu loop, replaces lines 20-38"""
    while True:
        print("\n" * 3)
        print("     MAIN MENU")
        print(" 1 = ADDITION THEOREM")
        print(" 2 = EXIT")
        print()
        choice = input("      MAKE SELECTION: ")

        if choice == "1":
            addition_theorem_demo(32)
        elif choice == "2":
            print("Exiting.")
            break
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
