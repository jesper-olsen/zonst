Shifting Theorem
==========================

Run
---

Demonstration that a shift in the time domain results in a linear phase shift
in the frequency domain, while the magnitude remains unchanged.

```
uv run dft5_03a.py




     MAIN MENU
 1 = SHIFTING THEOREM
 2 = EXIT

      MAKE SELECTION: 1

--- DEMONSTRATING THE SHIFTING THEOREM ---
A shift in the time domain results in a linear phase shift
in the frequency domain, while the magnitude remains unchanged.

[PART 1] First, we'll transform an impulse at t=0.
--> Press Enter to continue...

Plotting the unshifted impulse and its transform.
Note that the magnitude is constant and the phase is zero.
--> Displaying plots. Close the plot window to continue.

[PART 2] Now, let's shift the impulse in time.
Enter amount of time shift (1 to 31): 1

Plotting the shifted impulse and its transform.
Observe that the Magnitude plot is identical to the first one,
but the Phase plot now shows a linear ramp.
--> Displaying plots. Close the plot window to continue.
Try again with a different shift? (y/n): y

```

![PNG](https://github.com/jesper-olsen/zonst/blob/master/Assets/DFT01C_1.png)
![PNG](https://github.com/jesper-olsen/zonst/blob/master/Assets/DFT01C_2_t1.png)
![PNG](https://github.com/jesper-olsen/zonst/blob/master/Assets/DFT01C_2_t2.png)
![PNG](https://github.com/jesper-olsen/zonst/blob/master/Assets/DFT01C_2_t4.png)
![PNG](https://github.com/jesper-olsen/zonst/blob/master/Assets/DFT01C_2_t8.png)
![PNG](https://github.com/jesper-olsen/zonst/blob/master/Assets/DFT01C_2_t16.png)


