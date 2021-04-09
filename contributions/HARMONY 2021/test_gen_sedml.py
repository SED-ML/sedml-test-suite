r"""
####################################################################################################
                            tellurium 2.2.1
-+++++++++++++++++-         Python Environment for Modeling and Simulating Biological Systems
 .+++++++++++++++.
  .+++++++++++++.           Homepage:      http://tellurium.analogmachine.org/
-//++++++++++++/.   -:/-`   Documentation: https://tellurium.readthedocs.io/en/latest/index.html
.----:+++++++/.++  .++++/   Forum:         https://groups.google.com/forum/#!forum/tellurium-discuss
      :+++++:  .+:` .--++   Bug reports:   https://github.com/sys-bio/tellurium/issues
       -+++-    ./+:-://.   Repository:    https://github.com/sys-bio/tellurium
        .+.       `...`

SED-ML simulation experiments: http://www.sed-ml.org/
    # Change back to the original (with 'getName') when libsedml is fixed
    sedmlDoc: L1V4 
    inputType:      'SEDML_STRING'
    workingDir:     'C:\Users\Lucian\Desktop\tellurium'
    saveOutputs:    'False'
    outputDir:      'None'
    plottingEngine: '<MatplotlibEngine>'

Windows-10-10.0.19041-SP0
python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:37:02) [MSC v.1924 64 bit (AMD64)]
####################################################################################################
"""
import tellurium as te
from roadrunner import Config
from tellurium.sedml.mathml import *
from tellurium.sedml.tesedml import process_trace, terminate_trace, fix_endpoints

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
try:
    import libsedml
except ImportError:
    import tesedml as libsedml
import pandas
import os.path
Config.LOADSBMLOPTIONS_RECOMPILE = True

workingDir = r'C:\Users\Lucian\Desktop\tellurium'

# --------------------------------------------------------
# Models
# --------------------------------------------------------
# Model <model0>
model0 = te.loadSBMLModel(os.path.join(workingDir, 'hill.xml'))




# --------------------------------------------------------
# Tasks
# --------------------------------------------------------
# Task <task0>
# not part of any DataGenerator: task0
# Task <task1>

task1 = []
# Task: <task0>
task0 = [None]
model0.setIntegrator('cvode')
if model0.conservedMoietyAnalysis == True: model0.conservedMoietyAnalysis = False
__range__uniform_linear_for_n = np.linspace(start=1.0, stop=15.0, num=26)
for __k__uniform_linear_for_n, __value__uniform_linear_for_n in enumerate(__range__uniform_linear_for_n):
    model0.reset()
    model0['n'] = __value__uniform_linear_for_n
    model0.timeCourseSelections = ['n', 'time', '[S2]']
    model0.reset()
    task0[0] = model0.simulate(start=0.0, end=35.0, steps=30)

    task1.extend(task0)

# --------------------------------------------------------
# DataGenerators
# --------------------------------------------------------
# DataGenerator <plot_0_0_0>
__var__task1_____time = np.column_stack([sim['time'] for sim in task1])
if len(__var__task1_____time.shape) == 1:
     __var__task1_____time.shape += (1,)
plot_0_0_0 = __var__task1_____time
# DataGenerator <plot_0_0_1>
__var__task1_____n = np.column_stack([sim['n'] for sim in task1])
if len(__var__task1_____n.shape) == 1:
     __var__task1_____n.shape += (1,)
plot_0_0_1 = __var__task1_____n
# DataGenerator <plot_0_0_2>
__var__task1_____S2 = np.column_stack([sim['[S2]'] for sim in task1])
if len(__var__task1_____S2.shape) == 1:
     __var__task1_____S2.shape += (1,)
plot_0_0_2 = __var__task1_____S2

# --------------------------------------------------------
# Outputs
# --------------------------------------------------------
# Output <plot_0>
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(num=None, figsize=(9, 5), dpi=80, facecolor='w', edgecolor='k')
from matplotlib import gridspec
__gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
ax = plt.subplot(__gs[0])
ax.pcolormesh(plot_0_0_0, plot_0_0_1, plot_0_0_2, color='#1f77b4', linewidth=1.5, alpha=1.0, label='task1.S2', cmap='RdBu', shading='auto')
ax.set_title('UniformTimecourse', fontweight='bold')
ax.set_xlabel('task1.time', fontweight='bold')
ax.set_ylabel('task1.n', fontweight='bold')
plt.tick_params(axis='both', which='major', labelsize=10)
plt.tick_params(axis='both', which='minor', labelsize=8)
plt.savefig(os.path.join(workingDir, 'plot_0.png'), dpi=100)
plt.show()
####################################################################################################