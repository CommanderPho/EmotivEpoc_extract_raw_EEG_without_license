# EmotivEpoc_extract_raw_EEG_without_license
This code extracts raw EEG data by capturing the screen of the Emotiv Epoc program in real-time.

# Overview
This code extracts EEG data from EmotivPRO **without requiring a license** from Emotiv.

It works by:
- Capturing the EmotivPRO screen (with 14 electrode graphs) at 1-second intervals
- Removing the white background
- Calculating y-values using **darkness-weighted averages** of the pixels
- Saving the result as `.csv` files

You can later combine the 1-second segments for further analysis.

---
<img width="1920" height="1080" alt="screenshot_emotivpro" src="https://github.com/user-attachments/assets/e33f99a8-0d12-4fd7-9a94-dd25ea1d1a84" />


## How to Use

1. Open EmotivPRO in full-screen mode.
2. Take a screenshot (e.g. with PrtSc) and use a tool like **MS Paint** to manually check:
   - The **x-axis pixel range** corresponding to **8–9 seconds**
   - The **y=0 pixel** for each of the 14 graphs (from top to bottom)
   - The **vertical pixel range** for each graph (a reasonable height above and below y=0)

> The top graph may be hidden at 9–10 seconds, so use 8–9 instead.  
> Coordinates depend on your monitor and EmotivPRO version.

---

## Notes

- The script gives you **2 seconds** to switch to EmotivPRO after execution.
- Sampling frequency is limited by screen resolution.
- This method has some **inherent error** due to pixel-based extraction.
- For accurate data, consider purchasing an official license.

---

## Preview

You can uncomment the visualization code to verify your pixel inputs.

For accurate and reliable data, I recommend purchasing an official Emotiv license.

I hope this tool serves as a helpful resource for your research.
