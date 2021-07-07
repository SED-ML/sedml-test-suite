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
function MM(S1, S2, Vm, Km1, Km2, Keq)
  (Vm/Km1)*(S1 - S2/Keq)/(1 + S1/Km1 + S2/Km2);
end

model *Cycle()

  // Compartments and Species:
  species $X0, S2, S1, S3, $X1;

  // Reactions:
  J0: $X0 + S2 -> S1; Vmax*X0*S2 - 2.65*S1;
  J1: S1 -> S2 + S3; 9.21*S1 - 4.4*S2*S3;
  J2: S3 -> $X1; MM(S3, X1, 6.13, 3.42, 4.14, 4.78);

  // Species initializations:
  X0 = 0.29;
  S2 = 5.26;
  S1 = 0.26;
  S3 = 4.44;
  X1 = 4.63;
  Vmax = 7.61
end
   """)

SBML = r.getSBML()

p_str = """
    model0 = model "cycle.xml"
    sim0 = simulate steadystate()
    task0 = run sim0 on model0
    report S1, S2, S3
"""
te.saveToFile("cycle.xml", SBML)

# phrasedml.setReferencedSBML("case_01.xml", SBML)
sed = phrasedml.convertString(p_str)
if sed is None:
    print(phrasedml.getLastError())
    sys.exit()

sedml = libsedml.readSedMLFromString(sed)
sedml.setVersion(4)

#Data generators:  scalars

#Control coefficient of S1 wrt. X0
datagen = sedml.getDataGenerator(0).clone()
datagen.setId("cc_S1_X0")
ovar = datagen.removeVariable(0)
var = datagen.createDependentVariable()
var.setId("S1")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000802")
var.setSymbol("KISAO:0000836")
var.setTarget(ovar.getTarget())
var.setTarget2(ovar.getTarget().replace("S1", "X0"))
sedml.addDataGenerator(datagen)

#Control coefficient of J1 wrt. Vmax
datagen = sedml.createDataGenerator()
datagen.setId("cc_J0_Vmax")
var = datagen.createDependentVariable()
var.setId("J0Vmax")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000802")
var.setTarget("/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id=&apos;J0&apos;]")
var.setTarget2("/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id=&apos;Vmax&apos;]")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("J0Vmax")
datagen.setMath(astn)

#Control coefficient of S1 wrt. X0
datagen = sedml.getDataGenerator(0).clone()
datagen.setId("ucc_S1_X0")
ovar = datagen.removeVariable(0)
var = datagen.createDependentVariable()
var.setId("S1")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000803")
var.setSymbol("KISAO:0000836")
var.setTarget(ovar.getTarget())
var.setTarget2(ovar.getTarget().replace("S1", "X0"))
sedml.addDataGenerator(datagen)

#Control coefficient of J1 wrt. Vmax
datagen = sedml.createDataGenerator()
datagen.setId("ucc_J0_Vmax")
var = datagen.createDependentVariable()
var.setId("uJ0Vmax")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000803")
var.setTarget("/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id=&apos;J0&apos;]")
var.setTarget2("/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id=&apos;Vmax&apos;]")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("uJ0Vmax")
datagen.setMath(astn)

#Elasticity coefficient of J0 wrt. Vmax
datagen = sedml.createDataGenerator()
datagen.setId("ec_J0_Vmax")
var = datagen.createDependentVariable()
var.setId("eJ0Vmax")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000807")
var.setTarget("/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id=&apos;J0&apos;]")
var.setTarget2("/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id=&apos;Vmax&apos;]")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("eJ0Vmax")
datagen.setMath(astn)

#Unscaled elasticity coefficient of J0 wrt. Vmax
datagen = sedml.createDataGenerator()
datagen.setId("uec_J0_Vmax")
var = datagen.createDependentVariable()
var.setId("ueJ0Vmax")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000805")
var.setTarget("/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id=&apos;J0&apos;]")
var.setTarget2("/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id=&apos;Vmax&apos;]")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("ueJ0Vmax")
datagen.setMath(astn)

#Scalar reports on the above
report = sedml.createReport()
report.setId("scalar_MCA")
report.setName("Scalar MCA elements")
ds = report.createDataSet()
ds.setDataReference("cc_S1_X0")
ds.setLabel("Control coefficient of S1 for X0")
ds = report.createDataSet()
ds.setDataReference("cc_J0_Vmax")
ds.setLabel("Control coefficient of J0 for Vmax")
ds = report.createDataSet()
ds.setDataReference("ucc_J0_Vmax")
ds.setLabel("Unscaled control coefficient of S1 for X0")
ds = report.createDataSet()
ds.setDataReference("ucc_J0_Vmax")
ds.setLabel("Unscaled control coefficient of J0 for Vmax")
ds = report.createDataSet()
ds.setDataReference("ec_J0_Vmax")
ds.setLabel("Elasticity coefficient of J0 for Vmax")
ds = report.createDataSet()
ds.setDataReference("uec_J0_Vmax")
ds.setLabel("Unscaled elasticity coefficient of J0 for Vmax")



#Data generators:  matrices

#Jacobian matrix (full)
datagen = sedml.createDataGenerator()
datagen.setId("full_jacobian")
var = datagen.createDependentVariable()
var.setId("fulljacobian")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000812")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("fulljacobian")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("full_jacobian")
report.setName("jacobian")
ds = report.createDataSet()
ds.setDataReference("full_jacobian")


#Jacobian matrix (reduced)
datagen = sedml.createDataGenerator()
datagen.setId("reduced_jacobian")
var = datagen.createDependentVariable()
var.setId("reducedjacobian")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000809")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("reducedjacobian")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("reduced_jacobian")
report.setName("Reduced Jacobian")
ds = report.createDataSet()
ds.setDataReference("reduced_jacobian")


#Eigenvalue matrix (full)
datagen = sedml.createDataGenerator()
datagen.setId("full_eigens")
var = datagen.createDependentVariable()
var.setId("fulleigen")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000813")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("fulleigen")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("full_eigenvalues")
report.setName("Eigenvalues")
ds = report.createDataSet()
ds.setDataReference("full_eigens")


#Eigenvalue matrix (reduced)
datagen = sedml.createDataGenerator()
datagen.setId("reduced_eigens")
var = datagen.createDependentVariable()
var.setId("reducedeigen")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000810")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("reducedeigen")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("reduced_eigenvalues")
report.setName("Reduced Eigenvalues")
ds = report.createDataSet()
ds.setDataReference("reduced_eigens")


#Control coefficient matrix (scaled, concentration)
datagen = sedml.createDataGenerator()
datagen.setId("sc_controls")
var = datagen.createDependentVariable()
var.setId("sc_c")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000835")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("sc_c")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("sc_control_matrix")
report.setName("Control Coefficient Matrix (scaled, concentration)")
ds = report.createDataSet()
ds.setDataReference("sc_controls")


#Control coefficient matrix (unscaled, concentration)
datagen = sedml.createDataGenerator()
datagen.setId("uc_controls")
var = datagen.createDependentVariable()
var.setId("uc_c")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000801")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("uc_c")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("uc_control_matrix")
report.setName("Control Coefficient Matrix (unscaled, concentration)")
ds = report.createDataSet()
ds.setDataReference("uc_controls")


#Control coefficient matrix (scaled, flux)
datagen = sedml.createDataGenerator()
datagen.setId("sf_controls")
var = datagen.createDependentVariable()
var.setId("sf_c")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000815")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("sf_c")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("sf_control_matrix")
report.setName("Control Coefficient Matrix (scaled, flux)")
ds = report.createDataSet()
ds.setDataReference("sf_controls")


#Control coefficient matrix (unscaled, flux)
datagen = sedml.createDataGenerator()
datagen.setId("uf_controls")
var = datagen.createDependentVariable()
var.setId("uf_c")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000814")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("uf_c")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("uf_control_matrix")
report.setName("Control Coefficient Matrix (unscaled, flux)")
ds = report.createDataSet()
ds.setDataReference("uf_controls")


#Elasticity matrix (scaled)
datagen = sedml.createDataGenerator()
datagen.setId("sElasticities")
var = datagen.createDependentVariable()
var.setId("sEs")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000806")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("sEs")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("s_elasticities")
report.setName("Elasticity Matrix (scaled)")
ds = report.createDataSet()
ds.setDataReference("sElasticities")


#Elasticity matrix (unscaled)
datagen = sedml.createDataGenerator()
datagen.setId("uElasticities")
var = datagen.createDependentVariable()
var.setId("uEs")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000804")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("uEs")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("u_elasticities")
report.setName("Elasticity Matrix (unscaled)")
ds = report.createDataSet()
ds.setDataReference("uElasticities")


#Stoichiometry matrix (full)
datagen = sedml.createDataGenerator()
datagen.setId("stoichiometries")
var = datagen.createDependentVariable()
var.setId("stoichs")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000811")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("stoichs")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("stoichiometryMatrix")
report.setName("Stoichiometry Matrix (full)")
ds = report.createDataSet()
ds.setDataReference("stoichiometries")


#Stoichiometry matrix (reduced)
datagen = sedml.createDataGenerator()
datagen.setId("r_stoichiometries")
var = datagen.createDependentVariable()
var.setId("rstoichs")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000808")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("rstoichs")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("red_stoichiometryMatrix")
report.setName("Stoichiometry Matrix (reduced)")
ds = report.createDataSet()
ds.setDataReference("r_stoichiometries")


#Link matrix
datagen = sedml.createDataGenerator()
datagen.setId("linkmat")
var = datagen.createDependentVariable()
var.setId("lmat")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000816")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("lmat")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("linkMatrix")
report.setName("Link Matrix")
ds = report.createDataSet()
ds.setDataReference("linkmat")


#Kernel matrix
datagen = sedml.createDataGenerator()
datagen.setId("kernelmat")
var = datagen.createDependentVariable()
var.setId("kmat")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000817")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("kmat")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("kernelMatrix")
report.setName("Kernel Matrix")
ds = report.createDataSet()
ds.setDataReference("kernelmat")


#Conservation matrix
datagen = sedml.createDataGenerator()
datagen.setId("conservationmat")
var = datagen.createDependentVariable()
var.setId("kmat")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("urn:sedml:analysis:conservationMatrix")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("kmat")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("conservationMatrix")
report.setName("Conservation Matrix")
ds = report.createDataSet()
ds.setDataReference("conservationmat")


#L0 matrix
datagen = sedml.createDataGenerator()
datagen.setId("L0mat")
var = datagen.createDependentVariable()
var.setId("kmat")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000818")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("kmat")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("L0Matrix")
report.setName("L0 Matrix")
ds = report.createDataSet()
ds.setDataReference("L0mat")


#Nr matrix
datagen = sedml.createDataGenerator()
datagen.setId("Nrmat")
var = datagen.createDependentVariable()
var.setId("kmat")
var.setTaskReference("task0")
var.setModelReference("model0")
var.setTerm("KISAO:0000819")
sedml.addDataGenerator(datagen)
astn = libsedml.ASTNode()
astn.setName("kmat")
datagen.setMath(astn)

report = sedml.createReport()
report.setId("NrMatrix")
report.setName("Nr Matrix")
ds = report.createDataSet()
ds.setDataReference("Nrmat")


sedstr = libsedml.writeSedMLToString(sedml)
print(sedstr)

import os
sedfile = os.path.basename(__file__)
sedfile = sedfile.replace(".py", ".sedml")
sedfile = sedfile.replace("create_sedml_", "")

te.saveToFile(sedfile, sedstr)

te.executeSEDML(sedstr, saveOutputs=True)

