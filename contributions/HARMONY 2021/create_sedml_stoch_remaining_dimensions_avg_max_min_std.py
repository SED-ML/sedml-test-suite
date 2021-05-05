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
    sim0.algorithm = gillespie
    task0 = run sim0 on model0
    task1 = repeat task0 for n in uniform(1, 250, 250), reset=true
    plot "UniformTimecourse" task1.time vs. task1.S2
"""

# phrasedml.setReferencedSBML("case_01.xml", SBML)
sed = phrasedml.convertString(p_str)
if sed is None:
    print(phrasedml.getLastError())
    sys.exit()

sedml = libsedml.readSedMLFromString(sed)
sedml.setVersion(4)

dg = sedml.getDataGenerator(1)
var = dg.getVariable(0)
var.setSymbol("urn:sedml:function:average")
rd = var.createRemainingDimension()
rd.setTarget("task0")

dg2 = dg.clone()
dg2.setId("S2_max")
dg2.setName("S2_max")
var = dg2.getVariable(0)
var.setSymbol("urn:sedml:function:max")
sedml.addDataGenerator(dg2)

dg2.setId("S2_min")
dg2.setName("S2_min")
var.setSymbol("urn:sedml:function:min")
sedml.addDataGenerator(dg2)

dg2.setId("S2_std")
dg2.setName("S2_std")
var.setSymbol("urn:sedml:function:std")
sedml.addDataGenerator(dg2)

plot2d = sedml.getOutput(0)
curve = plot2d.getCurve(0)
curve.setType(libsedml.SEDML_CURVETYPE_POINTS)
curve.setYErrorUpper("S2_std")
curve.setYErrorLower("S2_std")


curve = curve.clone()
curve.unsetYErrorUpper()
curve.unsetYErrorLower()
curve.setId("S2_max_curve")
curve.setYDataReference("S2_max")
plot2d.addCurve(curve)

curve.setId("S2_min_curve")
curve.setYDataReference("S2_min")
plot2d.addCurve(curve)


sedstr = libsedml.writeSedMLToString(sedml)
print(sedstr)

te.executeSEDML(sedstr)

sedfile = os.path.basename(__file__)
sedfile = sedfile.replace(".py", ".sedml")
sedfile = sedfile.replace("create_sedml_", "")

te.saveToFile(sedfile, sedstr)
