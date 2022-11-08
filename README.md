<div id="top"></div>


 <img src="./Documentation/GoilGen_Logo.png" width="300">

## Python Implementation
 
This project is the python implementation of the matlab project: [CoilGen (https://github.com/Philipp-MR/CoilGen)](https://github.com/Philipp-MR/CoilGen).

The python project reprogrammed the functionalitys starting in the Heard file: `CoilGen\CoilGen.m`. When the functionality is fine the stucture and the code itself was cleaned up and changes that do not change the results were made.

State 2022-11-07 working was stopped in calcCountoursByTriangularPotentialCuts.py (there is a TODO with further explaintation). Until there in a testcase the results are similar to the ones in the matlab implementation. The testcase in Matlab could be found in: `CoilGen\Examples\ygradient_coil.m`.


## Testing with Pytest

There is a testcase implemented in testCase.py, on which it could be evaluated if the program still does what it should do. The results there are checked against the ones of the same case in the matlab project. For testing pytest is used. 

1. If not already installed run: pip install -U pytest
2. To run the tests, navigate to the Py_Coilgen folder and run: pytest 


## Citation

For citation of this work, please refer to the following publication:
https://onlinelibrary.wiley.com/doi/10.1002/mrm.29294
https://doi.org/10.1002/mrm.29294

<p align="right">(<a href="#top">back to top</a>)</p>
