import uproot
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import awkward as ak
from scipy.stats import binned_statistic

# Directory paths (adjust these as needed)
directories = [
    '/seaquest/users/xinlongl/semi-persistent/jpsi/pro_m0_v2/',
    '/seaquest/users/xinlongl/semi-persistent/jpsi/pro_m50_v2/',
    '/seaquest/users/xinlongl/semi-persistent/jpsi/pro_m100_v2/',
    '/seaquest/users/xinlongl/semi-persistent/jpsi/pro_m200_v2/'
]

# List to store the plot data for all directories
all_bin_resols = []
all_xaxis = []

# Helper function to extract numbers from filenames
def number_sort(file,directory):
    version = re.search(r'pro_m(\d+)_v2', directory)
    
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
#def compute_std_in_bins(truth, reco, bins):
        # Calculate the difference between truth and reco
 #       diff = np.array(truth) - np.array(reco)
        
        # Use binned_statistic to compute the standard deviation of differences within bins
  #      bin_resols, bin_edges, _ = binned_statistic(xaxis, diff, statistic='std', bins=bins)
        
   #     return bin_resols, bin_edges
labels=[]
# Loop through each directory
total_index_errors = 0
for directory in directories:
    print(directory)
    files = glob.glob(directory + '/*.root')

    # Sort files by the number extracted from filenames
    sorted_files = sorted(filter(lambda file: number_sort(file,directory) is not None, files), key=lambda file: number_sort(file, directory))
    test=[]
    truth = []
    reco = []
    length = []
    xaxis=[]
    bad=[]
    # Process each file in the directory
    for file in sorted_files:
        try:
            f = uproot.open(file)
            track_pz = f['Events/track_pz_st3'].array()
            truth_track_pz = f['Events/truthtrack_pz_st3'].array()
#            dimu_z = f['Events/truthtrack_z_vtx'].array()
            #match = f['Events/dimuon_matched'].array()
            # Loop over the events in the file
            for i in range(len(track_pz)):
                try:
                    blah = truth_track_pz[i][0]/track_pz[i][0]#CHECL TO REMOVE NULL RECO PZ ENTRIES HEEHEE
                    if track_pz[i][0] > 0 and track_pz[i][0] < 120: #and match[i][0] == 1 and track_pz[i][0] < 120:
                        truth.append(truth_track_pz[i][0])
                        reco.append(track_pz[i][0])
                        xaxis.append(truth_track_pz[i][0])
 #                       if dimu_z[i][0] < 0:
#                            bad.append(1)
#                    print(xaxis[i], reco[i], truth[i], ' z, reco mass, truth mass')
                except IndexError:
                    length.append(1)
                    total_index_errors += 1
        except: #Exception as e:
            print(f"Error processing file {file}")
#        print(truth, ' truth mass')
 #       print(reco, ' reco mass')
  #      print(xaxis,' dimuon z vtx pos')
    print(len(bad), 'how many events?')
    z_bins = np.linspace(0,100,51)
    diff = (np.array(reco) - np.array(truth))
    test.append(diff)
    test.append(xaxis)
#    for i in range(len(xaxis)):
 #       if test[1][i] < 0:
  #          print(test[0][i],' trouble region')
            
#    print(len(test[0]), len(test[1]))
    # Compute resolution statistics for the current directory
    bin_resols, bin_edges, _ = binned_statistic(xaxis, diff, statistic='mean', bins=z_bins)

    # Calculate the bin centers for plotting
    axis = (bin_edges[:-1] + bin_edges[1:]) / 2
    print(axis)
    # Store the data for later plotting
    all_bin_resols.append(bin_resols)
    all_xaxis.append(axis)
    labels.append(directory)
    #plt.plot(xaxis,bin_resols, '-', label=directory)
# Plot the results for all directories
plt.figure(figsize=(8, 6))

# Plot data for each directory
colors = ['b', 'g', 'r', 'c']  # Colors for different directories
#labels = ['0cm', '-50cm', '-100cm', '-200cm']  # Labels for the directories
for i, (bin_resols, axis) in enumerate(zip(all_bin_resols, all_xaxis)):
    plt.plot(axis, bin_resols, label=labels[i], marker='o', color=colors[i % len(colors)])


# Set plot labels and title
plt.xlabel('J/Psi truth pz [GeV]')
plt.ylabel('pz bias (mean difference) [GeV]')
#plt.ylim(-0.5,0.4)
plt.legend()
plt.title('J/Psi track st3 pz bias for different st3 position (disp track)')

# Save and show the plot
plt.savefig('matched/jpsi_binned_pz_bias_matched_all_geom_disp.pdf', format='pdf')
plt.show()

# Print the total number of index errors encountered
print(f"Total IndexErrors encountered: {total_index_errors}")
