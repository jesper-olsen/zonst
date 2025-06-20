# (FFT8.02) Q=2^N POINT FFT - FINAL CORRECTED Python Translation with Matplotlib
import math
import os
import time
import numpy as np
import matplotlib.pyplot as plt

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_results(fc, fs, q):
    """
    Prints the final FFT results in a formatted table.
    """
    q2 = q // 2
    print("-" * 65)
    print("FREQ   F(COS)      F(SIN)      |   FREQ  F(COS)      F(SIN)")
    print("=" * 65)
    for z in range(q2):
        print(f"{z:3d}   {fc[z]:+9.5f}   {fs[z]:+9.5f}    |  "
              f"{z + q2:3d}   {fc[z + q2]:+9.5f}   {fs[z + q2]:+9.5f}")
    print("-" * 65)


def plot_fft_results(input_signal, fc, fs, q):
    """
    Creates and displays plots for the input signal and its FFT spectrum.
    """
    freqs = np.arange(q)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9))
    fig.suptitle(f'Corrected FFT Analysis of a {q}-Point Signal', fontsize=16)

    ax1.plot(freqs, input_signal, 'o-', color='dodgerblue', label='Sampled Data')
    ax1.set_title('Input Signal (Time Domain)')
    ax1.set_xlabel('Sample Number'); ax1.set_ylabel('Amplitude')
    ax1.grid(True, linestyle='--', alpha=0.6); ax1.legend()

    width = 0.4
    ax2.bar(freqs - width/2, fc, width, label='Cosine (Real Part)', color='coral')
    ax2.bar(freqs + width/2, fs, width, label='Sine (Imaginary Part)', color='mediumseagreen')
    ax2.set_title('FFT Output (Frequency Domain)')
    ax2.set_xlabel('Frequency Bin (Harmonic)'); ax2.set_ylabel('Coefficient Value')
    ax2.set_xlim(-1, q); ax2.axhline(0, color='black', linewidth=0.8)
    ax2.grid(True, linestyle='--', alpha=0.6); ax2.legend()
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def generate_triangle_wave(q, k1):
    print("Preparing data input - please wait!")
    c_input = np.zeros(q)
    for i in range(q):
        for j in range(1, q // 2, 2):
            c_input[i] += math.cos(k1 * j * i) / (j * j)
    print("Data ready.")
    return c_input

def fixed_fft_routine(c_in, n, q):
    """
    A standard, correct, iterative Decimation-In-Time (DIT) FFT algorithm.
    """
    clear_screen()
    print("Running corrected general-purpose FFT routine...")
    start_time = time.perf_counter()

    # --- Step 1: Bit-Reversal Permutation ---
    # Create copies to work on, representing our complex signal
    c = c_in.copy()
    s = np.zeros(q) # Sine part is initially zero

    for i in range(q):
        # Calculate the bit-reversed index
        rev_i = 0
        temp_i = i
        for _ in range(n):
            rev_i = (rev_i << 1) | (temp_i & 1)
            temp_i >>= 1
        
        # If the reversed index is greater, swap the elements to avoid double-swapping
        if rev_i > i:
            c[i], c[rev_i] = c[rev_i], c[i]
            s[i], s[rev_i] = s[rev_i], s[i]

    # --- Step 2: Iterative Butterfly Stages ---
    for stage in range(1, n + 1):
        block_size = 2**stage
        half_block_size = block_size // 2
        
        # Calculate the twiddle factor for this stage
        angle_step = -2.0 * math.pi / block_size
        w_step_real = math.cos(angle_step)
        w_step_imag = math.sin(angle_step)
        
        for k in range(0, q, block_size):
            w_real, w_imag = 1.0, 0.0 # Start with W=1
            
            for j in range(half_block_size):
                idx1 = k + j
                idx2 = k + j + half_block_size
                
                # Calculate the product: temp = W * (c[idx2] + j*s[idx2])
                temp_real = c[idx2] * w_real - s[idx2] * w_imag
                temp_imag = c[idx2] * w_imag + s[idx2] * w_real
                
                # First part of butterfly: c[idx1] = c[idx1] + temp
                c[idx2] = c[idx1] - temp_real
                s[idx2] = s[idx1] - temp_imag
                
                # Second part of butterfly: c[idx2] = c[idx1] - temp
                c[idx1] += temp_real
                s[idx1] += temp_imag

                # Update the twiddle factor for the next butterfly in the block
                w_real, w_imag = w_real * w_step_real - w_imag * w_step_imag, \
                                 w_real * w_step_imag + w_imag * w_step_real

    # The original code normalized by dividing by Q. We do the same.
    final_c = c / q
    final_s = s / q
    
    elapsed_time = time.perf_counter() - start_time
    
    print_results(final_c, final_s, q)
    plot_fft_results(c_in, final_c, final_s, q)
    print(f"\nTIME = {elapsed_time:.6f} seconds")
    input("\nPlot window is open. Press ENTER to return to the menu...")


def main():
    clear_screen()
    n = 0
    while True:
        try:
            n_str = input("Input number of data points as 2^N.\nEnter N (e.g., 4 for 16 points, 5 for 32): ")
            n = int(n_str)
            if n > 0: break
            else: print("Please enter a positive integer.")
        except ValueError: print("Invalid input. Please enter an integer.")
            
    q = 2**n
    k1 = (2 * math.pi) / q

    while True:
        clear_screen()
        print(" " * 30 + "MAIN MENU")
        print(f"\n" + " " * 5 + f"1 = ANALYZE & PLOT TRIANGLE WAVE (Q={q})")
        print(" " * 5 + "2 = EXIT\n")
        choice = input(" " * 10 + "MAKE SELECTION : ")
        if choice == '1':
            c_signal = generate_triangle_wave(q, k1)
            input("Press ENTER to start CORRECTED FFT calculation and plotting...")
            fixed_fft_routine(c_signal, n, q)
        elif choice == '2':
            print("Exiting."); break

if __name__ == "__main__":
    main()
