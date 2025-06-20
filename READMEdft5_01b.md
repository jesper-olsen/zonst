Addition Theorem
==========================

Run
---

This demo shows how changing the width of a time-domain pulse affects its frequency-domain spectrum.

Below widths of 16, 8, 4, 2 and 1 are illustrated.

```
uv run dft5_02a.py




     MAIN MENU
 1 = ADDITION THEOREM
 2 = EXIT

      MAKE SELECTION: 1

--- DEMONSTRATING THE ADDITION THEOREM: F{f1 + f2} = F{f1} + F{f2} ---

[PART 1] Calculating the transform of the first function, f1(t).
--> Displaying plot. Close the plot window to continue.

[PART 2] Calculating the transform of the second function, f2(t).
--> Press Enter to continue...
--> Displaying plot. Close the plot window to continue.

[PART 3] Summing the two frequency transforms: F{f1} + F{f2}.
--> Press Enter to continue...
--> Displaying plot. Close the plot window to continue.

[PART 4] Now, summing the time signals first, then taking the transform.
--> Press Enter to continue...
--> Displaying plot. Close the plot window to continue.

--- CONCLUSION ---
Notice the frequency plot from PART 4 is identical to the one from PART 3.
This demonstrates that the transform of the sum is the sum of the transforms.
```

![PNG](https://github.com/jesper-olsen/zonst/blob/master/Assets/DFT01B_1.png)
![PNG](https://github.com/jesper-olsen/zonst/blob/master/Assets/DFT01B_2.png)
![PNG](https://github.com/jesper-olsen/zonst/blob/master/Assets/DFT01B_3.png)
![PNG](https://github.com/jesper-olsen/zonst/blob/master/Assets/DFT01B_4.png)


