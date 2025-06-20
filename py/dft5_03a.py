import numpy as np
import matplotlib.pyplot as plt
from fourier_analysis import dft


def plot_data_with_phase(time_signal, freq_signal, time_title):
    """
    Plots time domain, frequency magnitude, AND frequency phase.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    fig.tight_layout(pad=5.0)

    Q = len(time_signal)
    x_axis = np.arange(Q)

    # Plot 1: Time Domain
    time_real = np.real(time_signal)
    ax1.stem(x_axis, time_real, basefmt=" ")
    ax1.set_title(time_title)
    ax1.set_xlabel("Time Sample (t)")
    ax1.set_ylabel("Amplitude")
    ax1.set_xlim(-1, Q)
    ax1.grid(True)

    # Plot 2: Frequency Domain (Magnitude)
    freq_magnitude = np.abs(freq_signal)
    ax2.stem(x_axis, freq_magnitude, basefmt=" ")
    ax2.set_title("Frequency: Magnitude")
    ax2.set_xlabel("Frequency Bin")
    ax2.set_ylabel("Magnitude |F|")
    ax2.set_xlim(-1, Q)
    ax2.grid(True)

    # Plot 3: Frequency Domain (Phase)
    freq_phase = np.angle(freq_signal)
    ax3.stem(x_axis, freq_phase, basefmt=" ")
    ax3.set_title("Frequency: Phase")
    ax3.set_xlabel("Frequency Bin")
    ax3.set_ylabel("Phase (radians)")
    ax3.set_xlim(-1, Q)
    ax3.set_ylim(-np.pi - 0.5, np.pi + 0.5)  # Set y-axis limits for phase
    ax3.grid(True)

    print("--> Displaying plots. Close the plot window to continue.")
    plt.show()


def press_enter_to_continue():
    """Pauses execution until the user presses Enter."""
    input("--> Press Enter to continue...")


def shifting_theorem_demo(Q):
    """
    Demonstrates the DFT Shifting Theorem.
    Args:
        Q: number of samples (time and frequency)
    """
    print("\n--- DEMONSTRATING THE SHIFTING THEOREM ---")
    print("A shift in the time domain results in a linear phase shift")
    print("in the frequency domain, while the magnitude remains unchanged.")

    # --- STEP 1: Generate an unshifted impulse at t=0 and transform it ---
    print("\n[PART 1] First, we'll transform an impulse at t=0.")
    press_enter_to_continue()
    time_signal_unshifted = np.zeros(Q, dtype=np.complex128)
    time_signal_unshifted[0] = Q  # Using Q for amplitude for better scaling

    freq_signal_unshifted = dft(time_signal_unshifted, -1.0, Q)

    print("\nPlotting the unshifted impulse and its transform.")
    print("Note that the magnitude is constant and the phase is zero.")
    plot_data_with_phase(
        time_signal_unshifted, freq_signal_unshifted, "Time: Impulse at t=0"
    )

    # --- STEP 2: Loop to let the user shift the impulse and see the result ---
    while True:
        print("\n[PART 2] Now, let's shift the impulse in time.")
        shift_amount = -1
        while shift_amount < 1 or shift_amount > Q - 1:
            try:
                val = input(f"Enter amount of time shift (1 to {Q-1}): ")
                shift_amount = int(val)
                if shift_amount < 1 or shift_amount > Q - 1:
                    print("Value out of range.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        time_signal_shifted = np.zeros(Q, dtype=np.complex128)
        time_signal_shifted[shift_amount] = Q

        freq_signal_shifted = dft(time_signal_shifted, -1.0, Q)

        print("\nPlotting the shifted impulse and its transform.")
        print("Observe that the Magnitude plot is identical to the first one,")
        print("but the Phase plot now shows a linear ramp.")
        plot_data_with_phase(
            time_signal_shifted,
            freq_signal_shifted,
            f"Time: Impulse at t={shift_amount}",
        )

        another = input("Try again with a different shift? (y/n): ").lower()
        if another != "y":
            break


def main():
    """Main menu loop"""
    while True:
        print("\n" * 3)
        print("     MAIN MENU")
        print(" 1 = SHIFTING THEOREM")
        print(" 2 = EXIT")
        print()
        choice = input("      MAKE SELECTION: ")

        if choice == "1":
            shifting_theorem_demo(32)
        elif choice == "2":
            print("Exiting.")
            break
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
