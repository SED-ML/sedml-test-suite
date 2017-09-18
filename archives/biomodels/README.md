# SED-ML BioModel examples
This folder contains SED-ML examples from BioModels (https://www.ebi.ac.uk/biomodels-main/).

Credits to Markus Wolfien & Ron Henkel for creating a subset of these example files.
See also: 
	Henkel R, Wolkenhauer O, Waltemath D
    Combining computational models, semantic annotations and simulation experiments in a graph database.
    Database (Oxford). 2015 Mar 8;2015. pii: bau130. doi: 10.1093/database/bau130. Print 2015.
    https://academic.oup.com/database/article-lookup/doi/10.1093/database/bau130 
    PMID:25754863 

The combine archives are created from the SED-ML files with python script in this folder.


## Issues tellurium
* BIOMD0000000409_fig7bsedml: Integration error (https://github.com/sys-bio/roadrunner/issues/410)  
RuntimeError: CVODE Error: CV_CONV_FAILURE: Convergence test failures occurred too many times (= MXNCF = 10) during one internal timestep or occurred with |h| = hmin.; In virtual double rr::CVODEIntegrator::integrate(double, double)

* BIOMD0000000265_fig2_sedml: model missing
RuntimeError: static std::string rr::SBMLReader::read(const string&), could not open /tmp/tmp2npwm438/sedml/model1.xml as a file or uri

* BIOMD0000000242_fig2_sedml.omex: Incorrect start and end time (
    model1.simulate(start=200.0, end=0.0, points=2)
  File "/home/mkoenig/envs/tellurium-web/lib/python3.5/site-packages/roadrunner/roadrunner.py", line 3578, in simulate
    result = self._simulate(o)
  File "/home/mkoenig/envs/tellurium-web/lib/python3.5/site-packages/roadrunner/roadrunner.py", line 3332, in _simulate
    return _roadrunner.RoadRunner__simulate(self, opt)
RuntimeError: duration, startTime and steps must be non-negative


