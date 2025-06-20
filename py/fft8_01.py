import math
import time
import os
import numpy as np
import matplotlib.pyplot as plt

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_triangle_wave_numpy(q, k1):
    """
    Generates a 4-component triangle wave and returns its components.
    """
    i = np.arange(q)
    j = np.arange(1, q // 2, 2)  # j will be [1, 3, 5, 7]
    
    components = np.cos(k1 * j[:, np.newaxis] * i) / (j[:, np.newaxis]**2)
    y = np.sum(components, axis=0)
    
    return y, components, j

def translated_fft_routine(y, q, kc, ks):
    """
    A direct, literal translation of the GW-BASIC FFT algorithm.
    This is NOT using numpy.fft. It is the user's original algorithm.
    """
    q2 = q // 2

    # --- Dimension all intermediate arrays ---
    a0, a1, a2, a3, a4, a5, a6, a7 = ([0.0]*2 for _ in range(8))
    bc0, bs0, bc1, bs1, bc2, bs2, bc3, bs3 = ([0.0]*4 for _ in range(8))
    cc1, cs1, cc2, cs2 = ([0.0]*8 for _ in range(4))
    
    fc = [0.0] * q
    fs = [0.0] * q

    # --- STAGE A ---
    a0[0]=(y[0]+y[8])/2;   a0[1]=(y[0]-y[8])/2
    a1[0]=(y[1]+y[9])/2;   a1[1]=(y[1]-y[9])/2
    a2[0]=(y[2]+y[10])/2;  a2[1]=(y[2]-y[10])/2
    a3[0]=(y[3]+y[11])/2;  a3[1]=(y[3]-y[11])/2
    a4[0]=(y[4]+y[12])/2;  a4[1]=(y[4]-y[12])/2
    a5[0]=(y[5]+y[13])/2;  a5[1]=(y[5]-y[13])/2
    a6[0]=(y[6]+y[14])/2;  a6[1]=(y[6]-y[14])/2
    a7[0]=(y[7]+y[15])/2;  a7[1]=(y[7]-y[15])/2

    # --- STAGE B ---
    bc0[0]=(a0[0]+a4[0])/2; bc0[1]=a0[1]/2; bs0[1]=a4[1]/2
    bc0[2]=(a0[0]-a4[0])/2; bc0[3]=a0[1]/2; bs0[3]=-a4[1]/2
    bc1[0]=(a1[0]+a5[0])/2; bc1[1]=a1[1]/2; bs1[1]=a5[1]/2
    bc1[2]=(a1[0]-a5[0])/2; bc1[3]=a1[1]/2; bs1[3]=-a5[1]/2
    bc2[0]=(a2[0]+a6[0])/2; bc2[1]=a2[1]/2; bs2[1]=a6[1]/2
    bc2[2]=(a2[0]-a6[0])/2; bc2[3]=a2[1]/2; bs2[3]=-a6[1]/2
    bc3[0]=(a3[0]+a7[0])/2; bc3[1]=a3[1]/2; bs3[1]=a7[1]/2
    bc3[2]=(a3[0]-a7[0])/2; bc3[3]=a3[1]/2; bs3[3]=-a7[1]/2

    # --- STAGE C ---
    for i in range(4):
        j = 2 * i
        cc1[i]=(bc0[i]+bc2[i]*kc[j]-bs2[i]*ks[j])/2
        cc2[i]=(bc1[i]+bc3[i]*kc[j]-bs3[i]*ks[j])/2
        cs1[i]=(bs0[i]+bc2[i]*ks[j]+bs2[i]*kc[j])/2
        cs2[i]=(bs1[i]+bc3[i]*ks[j]+bs3[i]*kc[j])/2
    
    for i in range(4, 8):
        j = 2 * i
        k = i - 4
        cc1[i]=(bc0[k] - (bc2[k]*kc[j] - bs2[k]*ks[j]))/2
        cc2[i]=(bc1[k] - (bc3[k]*kc[j] - bs3[k]*ks[j]))/2
        cs1[i]=(bs0[k] - (bc2[k]*ks[j] + bs2[k]*kc[j]))/2
        cs2[i]=(bs1[k] - (bc3[k]*ks[j] + bs3[k]*kc[j]))/2
        # cc1[i]=(bc0[k]+bc2[k]*kc[j]-bs2[k]*ks[j])/2
        # cc2[i]=(bc1[k]+bc3[k]*kc[j]-bs3[k]*ks[j])/2
        # cs1[i]=(bs0[k]+bc2[k]*ks[j]+bs2[k]*kc[j])/2
        # cs2[i]=(bs1[k]+bc3[k]*ks[j]+bs3[k]*kc[j])/2

    # --- STAGE F (Final) ---
    for i in range(q2):
        fc[i]=(cc1[i]+cc2[i]*kc[i]-cs2[i]*ks[i])/2
        fs[i]=(cs1[i]+cc2[i]*ks[i]+cs2[i]*kc[i])/2
        
    for i in range(q2, q):
        # fc[i]=(cc1[i-q2]+cc2[i-q2]*kc[i]-cs2[i-q2]*ks[i])/2
        # fs[i]=(cs1[i-q2]+cc2[i-q2]*ks[i]+cs2[i-q2]*kc[i])/2
        fc[i]=(cc1[k] - (cc2[k]*kc[i] - cs2[k]*ks[i]))/2
        fs[i]=(cs1[k] - (cc2[k]*ks[i] + cs2[k]*kc[i]))/2
    
    return np.array(fc), np.array(fs) # Return as numpy arrays for plotting

def plot_analysis_results(signal, components, harmonics, fc, fs):
    """
    Creates the advanced grid of plots to show each component on its own scale.
    This function doesn't care how fc and fs were calculated.
    """
    q = len(signal)
    freqs = np.arange(q)
    fig, axes = plt.subplots(3, 2, figsize=(15, 12), constrained_layout=True)
    fig.suptitle('Analysis using the Translated GW-BASIC Algorithm', fontsize=20)

    axes[0, 0].set_title('Final Combined Signal', fontsize=14)
    axes[0, 0].plot(freqs, signal, 'o-', color='black', linewidth=2)
    axes[0, 0].set_ylabel('Amplitude')
    axes[0, 0].grid(True, linestyle='--', alpha=0.6)

    axes[0, 1].set_title('FFT Spectrum (from Translated Algorithm)', fontsize=14)
    width = 0.4
    axes[0, 1].bar(freqs - width/2, fc, width, label='Cosine Part', color='coral')
    axes[0, 1].bar(freqs + width/2, fs, width, label='Sine Part', color='mediumseagreen') # Note Sine part is now plotted
    axes[0, 1].set_xlabel('Frequency Bin')
    axes[0, 1].set_ylabel('Coefficient Value')
    axes[0, 1].set_xticks(freqs)
    axes[0, 1].legend()
    axes[0, 1].grid(True, linestyle='--', alpha=0.6)

    for i, ax in enumerate(axes.ravel()[2:]):
        harmonic_num = harmonics[i]
        amplitude = 1 / harmonic_num**2
        ax.plot(freqs, components[i], 'o-', color=f'C{i+1}')
        ax.set_title(f'Harmonic {harmonic_num} (Amplitude ≈ {amplitude:.3f})', fontsize=12)
        ax.set_ylim(-amplitude*1.2, amplitude*1.2)
        ax.grid(True, linestyle='--', alpha=0.6)

    plt.show()

def analyze_with_translated_fft(signal, components, harmonics, q, kc, ks):
    """
    The main analysis bridge function.
    It calls the TRANSLATED routine and then the plotting function.
    """
    clear_screen()
    print("Analyzing signal using the literal GW-BASIC algorithm translation...")
    
    # NO CHEATING: Call the translated routine
    fc, fs = translated_fft_routine(signal, q, kc, ks)
    
    print("\nDisplaying detailed plots...")
    plot_analysis_results(signal, components, harmonics, fc, fs)

    input("\nPlot window displayed. Press ENTER to return to menu...")

def main():
    """Main program loop."""
    # --- Constants and Pre-computation ---
    q = 16
    pi = math.pi
    p2 = 2 * pi
    k1 = p2 / q
    
    # We need these for the translated routine
    kc = [math.cos(k1 * i) for i in range(q + 1)]
    ks = [math.sin(k1 * i) for i in range(q + 1)]

    while True:
        clear_screen()
        print(" " * 20 + "FFT ANALYSIS: ORIGINAL GW-BASIC ALGORITHM")
        print(" " * 30 + "MAIN MENU")
        print("\n" + " " * 5 + "1 = ANALYZE & PLOT 4-COMPONENT TRIANGLE")
        print(" " * 5 + "2 = EXIT\n")
        choice = input(" " * 10 + "MAKE SELECTION : ")
        if choice == '1':
            # Use numpy to generate the wave, because it's convenient
            import numpy as np 
            signal, components, harmonics = generate_triangle_wave_numpy(q, k1)
            analyze_with_translated_fft(signal, components, harmonics, q, kc, ks)
        elif choice == '2':
            print("Exiting.")
            break

if __name__ == "__main__":
    try:
        import numpy
    except ImportError:
        print("This script requires numpy for wave generation. Please run: pip install numpy")
    main()
