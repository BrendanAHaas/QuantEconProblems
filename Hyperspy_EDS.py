#All hyperspy code requires these 3 imports/packages
import numpy as np
import matplotlib.pyplot as plot
import hyperspy.api as hs


"""Note: preferences can be adjusted via hs.preferences.gui() in terminal
so long as numpy, matplotlib, and hyperspy have been imported"""
#Is the signal EDS_SEM or EDS_TEM?
"""signaltype = raw_input("Is signal type SEM or TEM?  ")
if signaltype !="TEM" and signaltype !="SEM":
    while signaltype !="TEM" and signaltype !="SEM":
        signaltype = raw_input("Please enter SEM or TEM.  ")"""
        
#If you don't want to be repeatedly asked in the terminal for SEM or TEM,
#comment out the previous 4 lines, and uncomment this one:
signaltype = "SEM"

#Load the spectrum to be analyzed, define its signal type
filepath="G:\StardustResearch\SEM\Acfer3A_SEM\Acfer3ASmallCraterEMSA\Crater16(1)_pt1.emsa"
s = hs.load(filepath, signal_type =("EDS_" + signaltype), signal_origin = "experiment").as_spectrum(0)[0.0:7.0]

#This is for TEM only - Insert sample thickness (in nm?)
#s.metadata.Sample.thickness = 100

"""Write the microscope parameters.  Includes azimuth/elevation angles,
energy resolution, acquisition time (live time), real time (live time +
dead time), beam current, and beam energy"""
s.metadata.Acquisition_instrument
print(s.metadata.Acquisition_instrument)
#Obtain and set beam energy, this is necessary for setting x-ray lines automatically
if signaltype == "SEM":
    beamenergy = s.metadata.Acquisition_instrument.SEM.beam_energy
if signaltype == "TEM":
    beamenergy = s.metadata.Acquisition_instrument.TEM.beam_energy
s.set_microscope_parameters(beam_energy=beamenergy)

#Set elements present in sample
#s.set_elements(['Fe', 'Al', 'Si'])
s.add_elements(['Ca', 'Mg', 'Fe', 'Si', 'Al'])
s.add_lines()
kfactors = [2.301, 4.201, 1.450226, 5.075602, 8.2013]

#Set X-ray lines manually
#s.set_lines(['Fe_Ka', 'Fe_La', 'Si_Ka']
#Note:  A warning will be raised if setting X-ray lines higher than beam energy

#Print data about X-ray lines (energy values, Ka/La/Lb/etc., and weights)
print(hs.material.elements.Ca.Atomic_properties.Xray_lines)
print(hs.material.elements.Si.Atomic_properties.Xray_lines)

#Set X-ray lines automatically based on elements stated above
#Note: Beam energy must be defined for this to work (done above)
s.set_lines([])
bw = s.estimate_background_windows(line_width=[1.0,2.0], windows_width=0.5)
print("Background Energy Windows:")
print(bw)
intensities=s.get_lines_intensity(background_windows = bw)
#weight_percent = s.quantification(intensities, kfactors, plot_result = True, composition_units='atomic')

#print inputted sample info
print(s.metadata.Sample)

#Define the spectrum axes
"""Note: axes can be adjusted through gui as well, using si.axes_manager.gui(),
so long as si has been properly defined as above"""
s.axes_manager[0].name='E'
s.axes_manager['E'].units='keV'
s.axes_manager['E'].scale=0.01
#s.axes_manager['E'].offset=-0.01

print(s.axes_manager)

#Plot EDS spectrum, select which lines to show
#True = show location of lines
s.plot(True, background_windows=bw)

