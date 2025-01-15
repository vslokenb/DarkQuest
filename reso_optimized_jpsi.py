import uproot
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import awkward as ak
from scipy.stats import binned_statistic

# Directory paths (adjust these as needed)
directories = [
    '/seaquest/users/vsloken/scratch/adjust_sagitta_samp/pro_m0_std/',
    '/seaquest/users/vsloken/scratch/adjust_sagitta_samp/pro_m50_std/',
    '/seaquest/users/vsloken/scratch/adjust_sagitta_samp/pro_m100_std/',
    '/seaquest/users/vsloken/scratch/adjust_sagitta_samp/pro_m200_std/'
]

# List to store the plot data for all directories
all_bin_resols = []
all_xaxis = []

# Helper function to extract numbers from filenames
def number_sort(file,directory):
    version = re.search(r'pro_m(\d+)_std', directory)
    
    if version:
        # Use the extracted geometry to update the regex dynamically
        version_number = version.group(1)
        
        # Update the regex to reflect the correct version number
        pattern = rf'reco_muongun_1930_-{version_number}_([+-]?\d+)'
        
        # Now apply this dynamic pattern to the filename
        label = re.search(pattern, file)
        
    if label:
        return int(label.group(1))
    return None
labels=[]
# Loop through each directory
total_index_errors = 0
for directory in directories:
    print(directory)
    files = glob.glob(directory + '/*.root')

    # Sort files by the number extracted from filenames
    sorted_files = sorted(filter(lambda file: number_sort(file,directory) is not None, files), key=lambda file: number_sort(file, directory))

    truth = []
    reco = []
    length = []

    # Process each file in the directory
    for file in sorted_files:
        try:
            f = uproot.open(file)
            track_pz = f['Events/track_pz_st3'].array()
            truth_track_pz = f['Events/truthtrack_pz_st3'].array()

            # Loop over the events in the file
            for i in range(len(track_pz)):
                try:
                    blah = truth_track_pz[i][0]/track_pz[i][0] #CHECL TO REMOVE NULL RECO PZ ENTRIES HEEHEE
                    truth.append(truth_track_pz[i][0])
                    reco.append(track_pz[i][0])
                except IndexError:
                    length.append(1)
                    total_index_errors += 1
        except: #Exception as e:
            print(f"Error processing file {file}")

    # Compute resolution statistics for the current directory
    bin_resols, bin_edges, _ = binned_statistic(truth, reco, statistic='std', bins=19, range=(5, 100))

    # Calculate the bin centers for plotting
    xaxis = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(bin_edges) - 1)]

    # Store the data for later plotting
    all_bin_resols.append(bin_resols)
    all_xaxis.append(xaxis)
    labels.append(directory)
    #plt.plot(xaxis,bin_resols, '-', label=directory)
# Plot the results for all directories
plt.figure(figsize=(8, 6))

# Plot data for each directory
colors = ['b', 'g', 'r', 'c']  # Colors for different directories
#labels = ['0cm', '-50cm', '-100cm', '-200cm']  # Labels for the directories
for i, (bin_resols, xaxis) in enumerate(zip(all_bin_resols, all_xaxis)):
    plt.plot(xaxis, bin_resols, label=labels[i], marker='o',color=colors[i % len(colors)])


# Set plot labels and title
plt.xlabel('pz truth (GeV)')
plt.ylabel('pz resolution (std) [GeV]')
plt.legend()
plt.title('J/Psi Momentum vs Resolution at st3 for different st3 position + sagitta calib (standard tracking)')

# Save and show the plot
plt.savefig('jpsi_sagitta_calib_resolution_pz_st3_all_geom_standard.pdf', format='pdf')
plt.show()

# Print the total number of index errors encountered
print(f"Total IndexErrors encountered: {total_index_errors}")
