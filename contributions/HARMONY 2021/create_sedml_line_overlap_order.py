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

r = te.loada("""
   model case_02
       species S1=10, S2=5, S3=2
       S1 -> S2; S1*k1
       S2 -> S3; S2*k2
       k1 = 0.3
       k2 = 0.2
   end
   """)

SBML = r.getSBML()

p_str = """
    model0 = model "case_02.xml"
    sim0 = simulate uniform(0, 10, 10)
    sim0.algorithm.absolute_tolerance = 0.04
    task0 = run sim0 on model0
    plot "UniformTimecourse" time vs S1, S2, S3
"""
te.saveToFile("case_02.xml", SBML)

# phrasedml.setReferencedSBML("case_01.xml", SBML)
sed = phrasedml.convertString(p_str)
if sed is None:
    print(phrasedml.getLastError())
    sys.exit()

sedml = libsedml.readSedMLFromString(sed)
sedml.setVersion(4)

plot = sedml.getOutput(0)
curve = plot.getCurve(0)
curve.setType(libsedml.SEDML_CURVETYPE_POINTS)
curve.setStyle("purple_line")
curve.setOrder(2)
curve = plot.getCurve(1)
curve.setType(libsedml.SEDML_CURVETYPE_POINTS)
curve.setStyle("red_line")
curve.setOrder(3)
curve = plot.getCurve(2)
curve.setType(libsedml.SEDML_CURVETYPE_POINTS)
curve.setStyle("green_line")
curve.setOrder(1)

style = sedml.createStyle()
style.setId("purple_line")
line = style.createLineStyle()
line.setColor("#FF00FF")
line.setStyle(libsedml.SEDML_LINETYPE_SOLID)
line.setThickness(18)

style = sedml.createStyle()
style.setId("red_line")
line = style.createLineStyle()
line.setStyle(libsedml.SEDML_LINETYPE_SOLID)
line.setColor("#FF0000")
line.setThickness(18)


style = sedml.createStyle()
style.setId("green_line")
line = style.createLineStyle()
line.setStyle(libsedml.SEDML_LINETYPE_SOLID)
line.setColor("#00FF00")
line.setThickness(18)



sedstr = libsedml.writeSedMLToString(sedml)
print(sedstr)

te.executeSEDML(sedstr)

sedfile = os.path.basename(__file__)
sedfile = sedfile.replace(".py", ".sedml")
sedfile = sedfile.replace("create_sedml_", "")

te.saveToFile(sedfile, sedstr)
te.saveToFile("case_01.xml", SBML)
