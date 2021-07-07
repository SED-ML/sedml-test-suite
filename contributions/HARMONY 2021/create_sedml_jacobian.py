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
       species S1=10, S2=5
       S1 -> S2; S1*k
       k = 0.3
   end
   """)

SBML = r.getSBML()

p_str = """
    model0 = model "case_01.xml"
    sim0 = simulate uniform(0, 10, 10)
    task0 = run sim0 on model0
    report task0.time, task0.S1
"""
te.saveToFile("case_01.xml", SBML)

# phrasedml.setReferencedSBML("case_01.xml", SBML)
sed = phrasedml.convertString(p_str)
if sed is None:
    print(phrasedml.getLastError())
    sys.exit()

sedml = libsedml.readSedMLFromString(sed)
sedml.setVersion(4)

datagen = sedml.createDataGenerator()
datagen.setId("jacobian")
var = datagen.createDependentVariable()
var.setId("j")
var.setModelReference("model0")
var.setTaskReference("task0")
var.setTerm("KISAO:0000812")
astn = libsbml.parseL3Formula("j");
datagen.setMath(astn)

report = sedml.getOutput(0).clone()
report.removeDataSet(1)
report.setId("report_2")
ds = report.getDataSet(0)
ds.setId("Jacobian_report")
ds.setLabel("Jacobian")
ds.setDataReference("jacobian")
ret = sedml.addOutput(report)



sedstr = libsedml.writeSedMLToString(sedml)
print(sedstr)

import os
sedfile = os.path.basename(__file__)
sedfile = sedfile.replace(".py", ".sedml")
sedfile = sedfile.replace("create_sedml_", "")

te.saveToFile(sedfile, sedstr)

te.executeSEDML(sedstr, saveOutputs=True)

