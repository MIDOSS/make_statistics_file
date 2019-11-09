#  Copyright 2019, the MIDOSS project contributors, The University of British Columbia,
#  and Dalhousie University.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import numpy as np
import h5py
import os
import yaml

def make_stats_file(path, GridX, GridY, output):
    files =[]
    for r, d, f in os.walk(path):
        for file in f:
            if '.hdf5' in file:
                files.append(os.path.join(r, file))
    stats_dict = {'variable':{'mean':2, 'min':1, 'max':5, 'std':6}}
    for file in files:
        with h5py.File(file, 'r') as f:
            for group in list(f['Results'].keys()):
                timeseries = np.array([])
                for time in list(f['Results'][group].keys()):
                    if np.ndim(f['Results'][group][time][:]) == 3:
                        timeseries = np.append(timeseries, f['Results'][group][time][-1, GridX, GridY])
                    else:
                        timeseries = np.append(timeseries, f['Results'][group][time][GridX, GridY])
                stats_dict[group] = {'mean': str(np.mean(timeseries)), 
                                     'min': str(np.min(timeseries)),
                                     'max': str(np.max(timeseries)), 
                                     'std': str(np.std(timeseries))}
    del stats_dict['variable']
    with open(output, 'w') as outfile:
        yaml.dump(stats_dict, outfile, default_flow_style=False)

    
make_stats_file('/results2/MIDOSS/forcing/SalishSeaCast/MF0/03jun18-04jun18/', 249, 342, '/results2/MIDOSS/forcing/SalishSeaCast/MF0/03jun18-04jun18/stats.yaml')
