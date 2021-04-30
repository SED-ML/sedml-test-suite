# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:58:01 2021

@author: Lucian
"""

import tellurium as te
import phrasedml
import libsedml
import sys
import os

r = te.loada ('''
      $S1 -> S2; k1*S1/(0.1 + S4^n)
      S2 -> S3; k2*S2
      S3 -> S4; k3*S3;
      S4 ->; k4*S4
      
      k1 = 0.1; k2 = 0.4; 
      k3 = 0.23; k4 = 0.56 
      S1 = 1; n = 1
''')

SBML = r.getSBML()
te.saveToFile("hill.xml", SBML)

p_str = """
    model0 = model "hill.xml"
    sim0 = simulate uniform(0, 35, 30)
    task0 = run sim0 on model0
    task1 = repeat task0 for n in uniform(1, 15, 25), reset=true
    plot "UniformTimecourse" task1.time vs. task1.n vs. task1.S2
"""

# phrasedml.setReferencedSBML("case_01.xml", SBML)
sed = phrasedml.convertString(p_str)
if sed is None:
    print(phrasedml.getLastError())
    sys.exit()

sedml = libsedml.readSedMLFromString(sed)
sedml.setVersion(4)

plot3d = sedml.getOutput(0)

surface = plot3d.getSurface(0)
surface.setType(libsedml.SEDML_SURFACETYPE_BAR)



sedstr = libsedml.writeSedMLToString(sedml)
print(sedstr)

te.executeSEDML(sedstr)

sedfile = os.path.basename(__file__)
sedfile = sedfile.replace(".py", ".sedml")
sedfile = sedfile.replace("create_sedml_", "")

te.saveToFile(sedfile, sedstr)
