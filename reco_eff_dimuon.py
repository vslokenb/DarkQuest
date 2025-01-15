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
    z_positions = []
    hit_count = []
    total_count = []
#    truth = []
 #   reco = []
  #  length = []

    # Process each file in the directory
    for file in sorted_files:
        try:
            f = uproot.open(file)
 #           print('opened')
            hits = f['Events/dimuon_matched'].array()  # Number of hits per track
#            print(hits[0])
            #track_pz = f['Events/track_pz_st3'].array()  # Track momentum
            z_pos = f['Events/truthdimuon_z_vtx'].array()  # Vertex Z positions
            # Process each event in the file
            for i in range(len(z_pos)):
                #                z_pos = vtx_z[i][0]
                try:
                #    z_pos = vtx_z[i][0]  # Get the z position for this event
                    # If the track passes the cut (track_pz < 120), it's a "hit" event
                    z_positions.append(z_pos[i][0])
#                    print("hi", track_pz[i][0])
 #                   print("ho", hits[i])
                    if hits[i] > 0:
                        hit_count.append(1)
  #                      print('hit')
                    else:
                        hit_count.append(0)
   #                     print('nah')
                    # Count the event for the z position
#                    z_positions.append(z_pos[i][0])
                    total_count.append(1)
                except Exception as e:
                    total_index_errors += 1
                    # If there's an IndexError, treat as a no-hit
                    hit_count.append(0)
#                    print('error nah: ', e)
 #                   z_positions.append(z_pos[i][0])
                    total_count.append(1)
        except: #Exception as e:
            print(f"Error processing file {file}")

    # Compute resolution statistics for the current directory
 #   bin_resols, bin_edges, _ = binned_statistic(truth, reco, statistic='std', bins=19, range=(5, 100))
    # Calculate the bin centers for plotting
  #  xaxis = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(bin_edges) - 1)]
    # Store the data for later plotting
    all_bin_resols.append(hit_count)
    all_xaxis.append(z_positions)
    
    labels.append(directory)
    #plt.plot(xaxis,bin_resols, '-', label=directory)
# Plot the results for all directories
plt.figure(figsize=(8, 6))

z_bins = np.linspace(-500, 600, 50)  # Define bins for z positions
efficiency_per_bin = []
colors = ['b', 'g', 'r', 'c']

for i, (z_pos_list, hit_count_list) in enumerate(zip(all_xaxis, all_bin_resols)):
    # Initialize an array to store the hit counts in each z-bin
    hits_in_bin = np.zeros(len(z_bins) - 1)
    total_in_bin = np.zeros(len(z_bins) - 1)

    # Loop over all events and categorize them into bins
    for z_pos, hit in zip(z_pos_list, hit_count_list):
        # Find the bin index based on z position
    #    print('hit: ', hit)
     #   print('z_pos: ', z_pos)
        bin_index = np.digitize(z_pos, z_bins) - 1  # -1 because bins are 1-indexed
      #  print('bin_index: ', bin_index)
       # print('len(hits_in_bin): ', len(hits_in_bin))
        if 0 <= bin_index < len(hits_in_bin):
            total_in_bin[bin_index] += 1
            hits_in_bin[bin_index] += hit
#        except:
 #           print(bin_index, 'bin index')
  #          print(len(hits_in_bin), 'hits in bin')

    # Calculate the efficiency for this directory
   # print(hits_in_bin)
   # print(total_in_bin)
    efficiency = hits_in_bin / total_in_bin
    efficiency_per_bin.append(efficiency)
    # Plot data for each directory
    #colors = ['b', 'g', 'r', 'c']  # Colors for different directories
    #labels = ['0cm', '-50cm', '-100cm', '-200cm']  # Labels for the directories
    #for i, (bin_resols, xaxis) in enumerate(zip(all_bin_resols, all_xaxis)):
    plt.plot(z_bins[:-1], efficiency, label=labels[i], marker='.', color=colors[i % len(colors)])


# Set plot labels and title
plt.xlabel('vtx z position (cm)')
plt.ylabel('dimuon reco efficiency')
#plt.ylim(0,1)
plt.legend()
plt.title('J/Psi dimuon vtx position vs matched efficiency for different st3 position + sagitta calib(standard track)')
plt.yscale('log')
# Save and show the plot
plt.savefig('matched/dimuon_sagitta_calib_eff_all_geom_standard_track_matched.pdf', format='pdf')
plt.show()

# Print the total number of index errors encountered
print(f"Total IndexErrors encountered: {total_index_errors}")
