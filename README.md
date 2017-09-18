# sedml-test-suite
A test suite for SED-ML, modeled after the SBML test suite.

The test suite contains of two main parts:
* archives: combine archives containing SED-ML bases simulation experiments
* cases: individual test cases similar to the SBML test suite


Each test is in a numbered directory in the `cases/` directory.  When possible, both SBML and CellML versions are present; the focus being on the SED-ML itself rather than the modeling language it points to.  Each directory may contain the following files, where `xxxxx` is the number of the directory (i.e. `00001`):

|file                     | description|
|-------------------------|------------|
|`xxxxx-info.txt`           | Information about the test itself, including a summary of what is being tested (see below).  |
|`xxxxx-sedml-cellml.xml`   | The version of the SED-ML test that points to the CellML model  |
|`xxxxx-sedml-sbml.xml`     | The version of the SED-ML test that points to the SBML model  |
|`xxxxx-results.csv`        | The output from any `<report>` element in the SED-ML  |
|`xxxxx-cellml[xx].xml`     | Any CellML models|
|`xxxxx-sbml[xx].xml`       | Any SBML models  |


The format of the `info` file is as follows:

|title                    | description|
|-------------------------|------------|
|`category:`     | Test *Not sure if this is needed--taken from the SBML test suite, and they're all 'test' there*  |
|`synopsis:`     | *A short text description of the test.*  |
|`sbml:`         | xxxxx-sedml-sbml.xml    *The version of the test that points to SBML*  |
|`cellml:`       | xxxxx-sedml-cellml.xml  *The version of the test that points to CellML*  |
|`componentTags:`| *A list of the actual SED-ML classes used in the file*  |
|`testTags:`     | *A list of particular SED-ML interactions or uses that cannot be summarized by simply listing the components*  |
|`testType:`     | TimeCourse  *Not sure if this is needed either--might be covered by the componentTags?*  |
|`description:`  | *A longer description of the test.  May include an Antimony version of the model, and a phraSED-ML version of the SED-ML, if people don't think it's too cheesy to include my own stuff here ;-)  This is exactly the sort of context where those languages are particularly useful, though.*|

The `contributions` folder is for people to upload SED-ML files or Combine Archives they think might be useful to add to the suite proper.
