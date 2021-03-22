# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:58:01 2021

@author: Lucian
"""

import tellurium as te
import phrasedml
import libsedml
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
    plot "UniformTimecourse" time vs S1, S2
    report task0.time vs task0.S1
"""
te.saveToFile("case_01.xml", SBML)

# phrasedml.setReferencedSBML("case_01.xml", SBML)
sed = phrasedml.convertString(p_str)
if sed is None:
    print(phrasedml.getLastError())
    sys.exit()

sedml = libsedml.readSedMLFromString(sed)
sedml.setVersion(4)

plot = sedml.getOutput(0)
curve = plot.getCurve(0)
curve.setType(libsedml.SEDML_CURVETYPE_BAR)
curve.setStyle("blue_fill")
curve = plot.getCurve(1)
curve.setType(libsedml.SEDML_CURVETYPE_BAR)
curve.setStyle("red_dashed_line")

style = sedml.createStyle()
style.setId("blue_fill")
line = style.createLineStyle()
line.setColor("#FF00FF")
line.setStyle(libsedml.SEDML_LINETYPE_DASHDOT)
line.setThickness(4)
fill = style.createFillStyle()
fill.setColor("#0000FF")


style = sedml.createStyle()
style.setId("red_dashed_line")
line = style.createLineStyle()
line.setColor("#FF0000")
line.setStyle(libsedml.SEDML_LINETYPE_DASH)


sedstr = sedml.toSed()
print(sedstr)

te.saveToFile("case_01", SBML)
te.executeSEDML(sedstr)

import os
sedfile = os.path.basename(__file__)
sedfile = sedfile.replace(".py", ".sedml")
sedfile = sedfile.replace("create_sedml_", "")

te.saveToFile(sedfile, sedstr)
