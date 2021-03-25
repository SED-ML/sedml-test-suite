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
    task0 = run sim0 on model0
    plot "UniformTimecourse" time vs S1, S2, S3
    report task0.time vs task0.S1
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
curve.setStyle("purple_dash")
curve = plot.getCurve(1)
curve.setType(libsedml.SEDML_CURVETYPE_POINTS)
curve.setStyle("red_dash_dot")
curve = plot.getCurve(2)
curve.setType(libsedml.SEDML_CURVETYPE_POINTS)
curve.setStyle("green_line_orange_circles")

style = sedml.createStyle()
style.setId("dash")
line = style.createLineStyle()
line.setStyle(libsedml.SEDML_LINETYPE_DASH)
line.setThickness(4)

style = sedml.createStyle()
style.setId("purple_dash")
style.setBaseStyle("dash")
line = style.createLineStyle()
line.setColor("#FF00FF")

style = sedml.createStyle()
style.setId("red_dash_dot")
line = style.createLineStyle()
line.setStyle(libsedml.SEDML_LINETYPE_DASHDOT)
line.setColor("#FF0000")
line.setThickness(4)

style = sedml.createStyle()
style.setId("big_circles")
marker = style.createMarkerStyle()
marker.setStyle(libsedml.SEDML_MARKERTYPE_CIRCLE)
marker.setSize(16)

style = sedml.createStyle()
style.setId("orange_circles")
style.setBaseStyle("big_circles")
marker = style.createMarkerStyle()
marker.setFill("#FFa500")

style = sedml.createStyle()
style.setId("green_line_orange_circles")
style.setBaseStyle("orange_circles")
line = style.createLineStyle()
line.setStyle(libsedml.SEDML_LINETYPE_SOLID)
line.setColor("#00FF00")
line.setThickness(4)


style = sedml.createStyle()
style.setId("blue_fill")
fill = style.createFillStyle()
fill.setColor("#0000ff")



sedstr = libsedml.writeSedMLToString(sedml)
print(sedstr)

te.saveToFile("case_01", SBML)
te.executeSEDML(sedstr)

sedfile = os.path.basename(__file__)
sedfile = sedfile.replace(".py", ".sedml")
sedfile = sedfile.replace("create_sedml_", "")

te.saveToFile(sedfile, sedstr)
te.saveToFile("case_01.xml", SBML)
