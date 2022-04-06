import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

INPUT_PATH = 'input/'
OUTPUT_PATH = 'output/'


# Initialise repository
try: os.makedirs(INPUT_PATH)
except FileExistsError: pass
try: os.makedirs(OUTPUT_PATH)
except FileExistsError: pass



# Combined plots folder
output_folder = os.path.join(OUTPUT_PATH, '_combined')
try: os.makedirs(output_folder)
except FileExistsError: pass

# Combined Cx plot
plt.figure(figsize=(20, 10))
with os.scandir(INPUT_PATH) as files:
    for file in files:
        name, ext = os.path.splitext(file.name)
        df = pd.read_csv(file.path, sep='\t')

        # Generate Cx plot
        path_cx = os.path.join(output_folder, 'drag.jpg')
        plt.plot(df['Temps'], df['Cx0'], label=name)
        plt.xlabel('Time [s]')
        plt.ylabel('Drag [N]')
plt.legend()
plt.savefig(path_cx, bbox_inches='tight')

# Combined Cy plot
plt.figure(figsize=(20, 10))
with os.scandir(INPUT_PATH) as files:
    for file in files:
        name, ext = os.path.splitext(file.name)
        df = pd.read_csv(file.path, sep='\t')

        # Generate Cx plot
        path_cx = os.path.join(output_folder, 'lift.jpg')
        plt.plot(df['Temps'], df['Cy0'], label=name)
        plt.xlabel('Time [s]')
        plt.ylabel('Lift [N]')

plt.legend()
plt.savefig(path_cx, bbox_inches='tight')
        





# Individual plots
angles, cxs, cys = list(), list(), list()
with os.scandir(INPUT_PATH) as files:
    for file in files:

        # Process file name
        print(f'Processing {file.name}')
        name, ext = os.path.splitext(file.name)
        angle = float(name.split('_')[-1])
        angles.append(angle)

        # Read file
        df = pd.read_csv(file.path, sep='\t')

        # Compute averages
        avg_cx = np.average(df['Cx0'])
        avg_cy = np.average(df['Cy0'])
        cxs.append(avg_cx)
        cys.append(avg_cy)

        # Generate output folder
        output_folder = os.path.join(OUTPUT_PATH, name)
        try: os.makedirs(output_folder)
        except FileExistsError: continue

        # Generate Cx plot
        path_cx = os.path.join(output_folder, 'drag.jpg')
        plt.figure(figsize=(20, 10))
        plt.plot(df['Temps'], df['Cx0'])
        plt.xlabel('Time [s]')
        plt.ylabel('Drag [N]')
        plt.savefig(path_cx, bbox_inches='tight')

        # Generate Cy plot
        path_cy = os.path.join(output_folder, 'lift.jpg')
        plt.figure(figsize=(20, 10))
        plt.plot(df['Temps'], df['Cy0'])
        plt.xlabel('Time [s]')
        plt.ylabel('Lift [N]')
        plt.savefig(path_cy, bbox_inches='tight')






output_folder = os.path.join(OUTPUT_PATH, '_angles')
try: os.makedirs(output_folder)
except FileExistsError: pass

# Plot averages according to angles
path_cx = os.path.join(output_folder, 'drag.jpg')
plt.figure(figsize=(20, 10))
plt.scatter(angles, cxs, label='Time-averaged drag (Cx)')
plt.xlabel('Angle [deg]')
plt.ylabel('Drag [N]')
plt.savefig(path_cx, bbox_inches='tight')

path_cx = os.path.join(output_folder, 'lift.jpg')
plt.figure(figsize=(20, 10))
plt.scatter(angles, cys, label='Time-averaged lift (Cy)')
plt.xlabel('Angle [deg]')
plt.ylabel('Lift [N]')
plt.savefig(path_cx, bbox_inches='tight')
