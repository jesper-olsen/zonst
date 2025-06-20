# (FFT8.10A) FFT/INV FFT - FINAL AND DEFINITIVELY CORRECTED Python Translation
import math
import os
import time
import numpy as np
import matplotlib.pyplot as plt

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class FFTAnalyzer:
    """
    A class with a new, robust, and correct FFT/IFFT implementation
    based on the standard bit-reversal iterative DIT algorithm.
    """
    def __init__(self, n):
        if n <= 0: raise ValueError("N must be a positive integer.")
        self.n = n
        self.q = 2**n
        print(f"Initializing for Q = {self.q} points (N={self.n})...")
        self.fc_data, self.fs_data, self.original_signal = None, None, None
        print("Ready.")
        time.sleep(1)

    def generate_triangle_wave(self):
        print("Preparing triangle wave data...")
        k1 = (2 * math.pi) / self.q
        c_input = np.zeros(self.q)
        for i in range(self.q):
            for j in range(1, self.q // 2, 2):
                c_input[i] += math.cos(k1 * j * i) / (j * j)
        self.original_signal = c_input.copy()
        print("Data ready.")
        return c_input

    def _bit_reverse_copy(self, signal):
        """
        Creates a new array with elements in bit-reversed order.
        This is Step 1 of the standard iterative FFT.
        """
        out = np.zeros_like(signal)
        for i in range(self.q):
            rev_i = 0
            temp_i = i
            for _ in range(self.n):
                rev_i = (rev_i << 1) | (temp_i & 1)
                temp_i >>= 1
            out[rev_i] = signal[i]
        return out

    def _perform_fft_core(self, c_in, s_in):
        """
        The core in-place butterfly calculation engine.
        This operates on the data AFTER bit-reversal.
        """
        # Work on copies
        c, s = c_in.copy(), s_in.copy()

        # Main butterfly stages
        for stage in range(1, self.n + 1):
            block_size = 2**stage
            half_block_size = block_size // 2
            
            angle_step = -2.0 * math.pi / block_size
            w_step_real = math.cos(angle_step)
            w_step_imag = math.sin(angle_step)
            
            for k in range(0, self.q, block_size):
                w_real, w_imag = 1.0, 0.0
                
                for j in range(half_block_size):
                    idx1 = k + j
                    idx2 = k + j + half_block_size
                    
                    c2, s2 = c[idx2], s[idx2]
                    
                    # temp = W * (c2 + j*s2)
                    temp_real = c2 * w_real - s2 * w_imag
                    temp_imag = c2 * w_imag + s2 * w_real
                    
                    # B[idx1] = B[idx1] + temp
                    c[idx2] = c[idx1] - temp_real
                    s[idx2] = s[idx1] - temp_imag
                    
                    # B[idx2] = B[idx1] - temp
                    c[idx1] += temp_real
                    s[idx1] += temp_imag

                    w_real, w_imag = w_real * w_step_real - w_imag * w_step_imag, \
                                     w_real * w_step_imag + w_imag * w_step_real
        return c, s

    def forward_fft(self, c_in):
        """Performs a forward FFT on a real signal."""
        # Step 1: Bit-reverse the input
        c_shuffled = self._bit_reverse_copy(c_in)
        s_shuffled = np.zeros(self.q) # Input is purely real

        # Step 2: Run the core butterfly engine
        return self._perform_fft_core(c_shuffled, s_shuffled)

    def inverse_fft(self, fc_in, fs_in):
        """
        Performs an inverse FFT using the conjugate-twice theorem on the
        now-correct forward FFT core.
        """
        # Step 1: Conjugate the input frequency data
        c_conj_in, s_conj_in = fc_in.copy(), -fs_in.copy()
        
        # Step 2: Bit-reverse the conjugated input
        c_shuffled = self._bit_reverse_copy(c_conj_in)
        s_shuffled = self._bit_reverse_copy(s_conj_in)

        # Step 3: Run the core forward FFT engine
        c_temp, s_temp = self._perform_fft_core(c_shuffled, s_shuffled)
        
        # Step 4: Conjugate the output and normalize by Q
        c_out = c_temp / self.q
        s_out = -s_temp / self.q
        
        return c_out, s_out

    def plot_results(self, data, title, is_time_domain=False):
        """Universal plotting function."""
        # This function remains the same
        freqs = np.arange(self.q)
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        if is_time_domain:
            ax.plot(freqs, data, 'o-', color='dodgerblue')
            ax.set_title(title); ax.set_xlabel('Sample Number'); ax.set_ylabel('Amplitude')
        else:
            fc, fs = data; width = 0.4
            ax.bar(freqs - width/2, fc, width, label='Cosine (Real Part)', color='coral')
            ax.bar(freqs + width/2, fs, width, label='Sine (Imaginary Part)', color='mediumseagreen')
            ax.set_title(title); ax.set_xlabel('Frequency Bin (Harmonic)'); ax.set_ylabel('Coefficient Value'); ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6); ax.set_xlim(-1, self.q)
        plt.show()

    def run(self):
        """Main menu loop."""
        while True:
            clear_screen(); print(" " * 30 + "MAIN MENU (FINAL CORRECTED VERSION)")
            print(f"\n" + " " * 5 + f"1 = ANALYZE TRIANGLE WAVE (FORWARD FFT, Q={self.q})")
            print(" " * 5 + "2 = INVERSE TRANSFORM CURRENT DATA")
            print(" " * 5 + "3 = EXIT\n")
            choice = input(" " * 10 + "MAKE SELECTION : ")

            if choice == '1':
                c_signal = self.generate_triangle_wave()
                input("Data generated. Press ENTER to perform Forward FFT...")
                start_time = time.time()
                self.fc_data, self.fs_data = self.forward_fft(c_signal)
                print(f"Forward FFT completed in {time.time() - start_time:.4f} seconds.")
                self.plot_results((self.fc_data, self.fs_data), "Forward FFT Results")

            elif choice == '2':
                if self.fc_data is None: print("\nNo data to transform. Run option 1 first."); time.sleep(2); continue
                print("Performing Corrected Inverse FFT...")
                start_time = time.time()
                c_out, s_out = self.inverse_fft(self.fc_data, self.fs_data)
                print(f"Inverse FFT completed in {time.time() - start_time:.4f} seconds.")
                # We plot the real part of the output, s_out should be negligible
                self.plot_results(c_out, "Inverse FFT Result (Recovered Signal)", is_time_domain=True)

            elif choice == '3': print("Exiting."); break
            input("Plot closed. Press ENTER to return to menu...")

if __name__ == "__main__":
    clear_screen(); n_val = 0
    while True:
        try: n_val = int(input("Enter N for Q=2^N (e.g., 4 for 16 points): ")); break
        except (ValueError, TypeError): print("Invalid input.")
    try: analyzer = FFTAnalyzer(n_val); analyzer.run()
    except Exception as e: print(f"\nAn error occurred: {e}")
