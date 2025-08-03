import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import pyautogui

# You must manually provide pixel position information for the 14 electrode graphs
# as they stream in real time on the Emotiv PRO screen.
# For the x-axis, specify the pixel range corresponding to 8 to 9 seconds on each graph.
# For the y-axis, specify the reference y=0 pixel (from the top) for each of the 14 graphs,
# and define how many pixels above and below that point should be considered the vertical range of the graph.
# This task can be done easily by taking a screenshot with PrtSc and measuring pixel positions using MS Paint or similar tools.

measurement_duration = 1 # Specify the duration of the measurement in seconds
x_range = (1526,1667) # 8 to 9 seconds
y_axis = [140,193,246,299,352,406,458,512,565,617,670,724,777,830] # y=0 reference pixel
y_half_width = 25 # half of y width
electrodes = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4'] # from the top

# Note: This information may vary depending on your monitor size and Emotiv PRO version.
def Extract_EEG(image) : # This extracts 1 second of EEG data from 14 electrodes.

    image = np.array(image)
    threshold = 240
    gray = 0.2989 * image[:, :, 0] + 0.5870 * image[:, :, 1] + 0.1140 * image[:, :, 2]
    mask = np.where(gray < threshold, gray, 0)

    df_EEG = np.empty((x_range[1]-x_range[0]+1,14))

    for i in range(14) :
        axis = y_axis[i]
        y_range = (axis-y_half_width,axis+y_half_width)

        mini_mask = mask[y_range[0]:y_range[1] + 1, x_range[0]:x_range[1] + 1]

        #plt.imshow(mini_mask, cmap='gray', vmin=0, vmax=255) # Use the following visualization code to check whether you have entered the pixel information correctly.

        # After removing pixels from the white background, calculate the y-coordinate using a weighted average based on how dark each pixel is.
        y_values = []
        for x in range(x_range[1] - x_range[0] + 1) :
            column = mini_mask[:, x]
            y_indices = np.where(column > 0)[0]
            if len(y_indices) == 0:
                y_values.append(0)
                continue
            brightness_values = column[y_indices]
            darkness_weights = 255 - brightness_values
            weighted_y = np.sum((y_indices-y_half_width ) * darkness_weights) / np.sum(darkness_weights)
            y_values.append(weighted_y)
        df_EEG[:,i] = y_values

    df_EEG = pd.DataFrame(df_EEG)

    return df_EEG

print('Delay for 2 seconds. Display the Raw EEG graph in the Emotiv PRO software.')
time.sleep(2)
print('Start')

num_file = 1
while num_file <= measurement_duration:
    start_time = time.time()

    df_EEG_extracted = Extract_EEG(pyautogui.screenshot())

    df_EEG_extracted.columns = electrodes
    df_EEG_extracted.to_csv(f"data/EEG_{num_file}.csv", index=False)
    print(f'File #{num_file} has been saved successfully')
    num_file += 1

    # Use the following visualization code to check whether you have entered the pixel information correctly.
    """
    plt.figure(figsize=(12, 8))
    for i in range(14):
        plt.plot(range(x_range[1] - x_range[0] + 1), list(df_EEG_extracted.iloc[:, i]), label=f'Graph {i + 1}')
    plt.legend()
    plt.show()
    """

    elapsed_time = time.time() - start_time
    time.sleep(max(0, 1 - elapsed_time))
