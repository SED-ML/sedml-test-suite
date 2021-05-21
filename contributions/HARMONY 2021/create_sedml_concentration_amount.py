# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:58:01 2021

@author: Lucian
"""

import tellurium as te
import phrasedml
import libsedml
import libsbml
import sys

r = te.loada("""
   model case_01
       species S1 in C, S2 in C
       S1 = 10
       S2 = 5
       C = 3
       S1 -> S2; S1*k
       k = 0.3
   end
   """)

SBML = r.getSBML()

p_str = """
    model0 = model "case_01.xml"
    sim0 = simulate uniform(0, 10, 10)
    task0 = run sim0 on model0
    plot "UniformTimecourse default" time vs S1, S2
    plot "UniformTimecourse amounts" time vs S1, S2
    plot "UniformTimecourse concentration" time vs S1, S2
"""
te.saveToFile("case_01.xml", SBML)

# phrasedml.setReferencedSBML("case_01.xml", SBML)
sed = phrasedml.convertString(p_str)
if sed is None:
    print(phrasedml.getLastError())
    sys.exit()

sedml = libsedml.readSedMLFromString(sed)
sedml.setVersion(4)

datagen = sedml.getDataGenerator(1).clone()
var = datagen.getVariable(0)
var.setSymbol("urn:sedml:symbol:amount")
datagen.setId("S1_amt")
sedml.addDataGenerator(datagen)

datagen = sedml.getDataGenerator(2).clone()
var = datagen.getVariable(0)
var.setSymbol("urn:sedml:symbol:amount")
datagen.setId("S2_amt")
sedml.addDataGenerator(datagen)

plot = sedml.getOutput(1)
curve = plot.getCurve(0)
curve.setYDataReference("S1_amt")
curve = plot.getCurve(1)
curve.setYDataReference("S2_amt")


datagen = sedml.getDataGenerator(1).clone()
var = datagen.getVariable(0)
var.setSymbol("urn:sedml:symbol:concentration")
datagen.setId("S1_conc")
sedml.addDataGenerator(datagen)

datagen = sedml.getDataGenerator(2).clone()
var = datagen.getVariable(0)
var.setSymbol("urn:sedml:symbol:concentration")
datagen.setId("S2_conc")
sedml.addDataGenerator(datagen)

plot = sedml.getOutput(2)
curve = plot.getCurve(0)
curve.setYDataReference("S1_conc")
curve = plot.getCurve(1)
curve.setYDataReference("S2_conc")



sedstr = libsedml.writeSedMLToString(sedml)
print(sedstr)

import os
sedfile = os.path.basename(__file__)
sedfile = sedfile.replace(".py", ".sedml")
sedfile = sedfile.replace("create_sedml_", "")

te.saveToFile(sedfile, sedstr)

te.executeSEDML(sedstr, saveOutputs=True)

