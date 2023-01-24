[![CI](https://github.com/catkira/pyCoilGen/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/catkira/pyCoilGen/actions/workflows/lint_and_test.yml)
[![Pylint](https://catkira.github.io/pyCoilGen/pylint.svg)](https://github.com/catkira/pyCoilGen/actions/workflows/CI.yml)

## Overview
 
This is a Python implementation of: [CoilGen (https://github.com/Philipp-MR/CoilGen)](https://github.com/Philipp-MR/CoilGen).

State 2022-11-07: working was stopped in calcCountoursByTriangularPotentialCuts.py (there is a TODO with further explaintation).


## Testing

There is a testcase implemented in testCase.py, on which it could be evaluated if the program still does what it should do. The results there are checked against the ones of the same case in the matlab project. For testing pytest is used. 

1. If not already installed run: pip install -U pytest
2. To run the tests, navigate to the Py_Coilgen folder and run: pytest 

The testdata is generated in Matlab with `CoilGen\Examples\ygradient_coil.m`.


## Citation

For citation of this work, please refer to the following publication:
https://onlinelibrary.wiley.com/doi/10.1002/mrm.29294
https://doi.org/10.1002/mrm.29294
