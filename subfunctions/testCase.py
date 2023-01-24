from readMesh import CylindricMeshGiven
from defineTargetField import TargetFieldGiven
from sensitivityMatrix import getSensitivityMatrix
from resistanceMatrix import getResistanceMatrix
from streamFunctionOptimization import streamFunctionOptimization
from Tester import Tester
import numpy as np
import scipy

meshFile = 'cylinder_radius500mm_length1500mm.stl'
targetMeshFile = 'sphere_radius150mm.stl'
gaussOrder = 2
tikonovFac = 100
specificConductivityMaterial = 1.8000*10**-8
conducterThickness = 0.005
materialFactor = specificConductivityMaterial/conducterThickness

# load test data from Matlab for comparison
matlabData = scipy.io.loadmat('matlabData.mat')
sensitivityMatrixMatlab = np.array(matlabData['coil_parts'][0][0][11]).transpose([0,2,1])
resistanceMatrixMatlab = np.array(matlabData['coil_parts'][0][0][14]).T
SFOptMatlab = scipy.io.loadmat('opt_stream_func.mat')['opt_stream_func'].ravel()
BFieldMatlab = scipy.io.loadmat('sf_b_field.mat')['sf_b_field']

calcWeightsGaussCorrect = [[-0.5773502691896257310588680, 0.5773502691896257310588680],[1.0000000000000004440892099, 1.0000000000000004440892099]]
gaußLegendreCorrect = [[0.21132486540518713, 0.21132486540518713, 0.7886751345948129, 0.7886751345948129], [0.16666666666666669, 0.6220084679281462, 0.044658198738520456, 0.16666666666666669], [0.19716878364870338, 0.19716878364870338, 0.052831216351296825, 0.052831216351296825]]

def calc_area(a,b,c):
    vec1 = (c-a)
    vec2 = (c-b)
    area = np.linalg.norm(np.cross(vec1, vec2))/2
    return area

def calc_current(a,b,c):
    return (c - b)/calc_area(a,b,c)/2

Test = Tester()
Mesh = CylindricMeshGiven(meshFile)

def test_triangleNodeArrays():
    for node in range(Mesh.vertices.shape[0]):
        test = np.column_stack((node*np.ones(np.array(Mesh.oneRingList[node]).shape[0]).T, np.array(Mesh.oneRingList[node]))).astype(int)
        assert np.array_equal(np.sort(test, 1), np.sort(Mesh.faces[Mesh.neighbours[node]], 1))
        if node == 1:
            pass
            # for i in range(np.array(Mesh.oneRingList[node]).shape[0]):
                # a = Mesh.vertices[Mesh.faces[Mesh.neighbours[node]]][i,0,:]
                # b = Mesh.vertices[Mesh.faces[Mesh.neighbours[node]]][i,1,:]
                # c = Mesh.vertices[Mesh.faces[Mesh.neighbours[node]]][i,2,:]
                # a = Mesh.vertices[node]
                # b = Mesh.vertices[Mesh.oneRingList[node][i]][0,:]
                # c = Mesh.vertices[Mesh.oneRingList[node][i]][1,:]
                # print(f'{Mesh.neighbours[node][i]} {calc_area(a,b,c):.17f} {calc_current(a,b,c)[0]:.17f}')
                #print(f'{Mesh.neighbours[node][i]} {Mesh.areas[Mesh.neighbours[node][i]]:.17f} {calc_current(a,b,c)[0]:.17f}')
            # for i in range(7):
            #     print(f'{Mesh.neighbours[1][i]}: [1 {Mesh.oneRingList[1][i][0]} {Mesh.oneRingList[1][i][1]}]  <-> [{Mesh.faces[Mesh.neighbours[1]][i][0]} {Mesh.faces[Mesh.neighbours[1]][i][1]} {Mesh.faces[Mesh.neighbours[1]][i][2]}]')
            # Mesh.faces[Mesh.neighbours[1]]

def test_areas():
    for node in range(Mesh.vertices.shape[0]):    
        for i in range(np.array(Mesh.oneRingList[node]).shape[0]):
            #a = Mesh.vertices[Mesh.faces[Mesh.neighbours[1]]][i,0,:]
            #b = Mesh.vertices[Mesh.faces[Mesh.neighbours[1]]][i,1,:]
            #c = Mesh.vertices[Mesh.faces[Mesh.neighbours[1]]][i,2,:]
            a = Mesh.vertices[node]
            b = Mesh.vertices[Mesh.oneRingList[node][i]][0,:]
            c = Mesh.vertices[Mesh.oneRingList[node][i]][1,:]
            # print(f'{Mesh.neighbours[node][i]} {calc_area(a,b,c):.17f} {calc_current(a,b,c)[0]:.17f}')
            precision = 10
            assert np.round(calc_area(a,b,c), precision) == np.round(Mesh.areas[Mesh.neighbours[node][i]], precision)

TargetSphere = TargetFieldGiven(targetMeshFile,1)
sensitivityMatrix = np.array(getSensitivityMatrix(Test,Mesh,TargetSphere,gaussOrder))
resistanceMatrix = np.array(getResistanceMatrix(Test,Mesh,materialFactor))
BField,SFOpt = streamFunctionOptimization(Test,Mesh,TargetSphere,sensitivityMatrix,resistanceMatrix,tikonovFac)

def test_sensitivityMatrix():
    precision = 16
    assert np.array_equal(np.round(sensitivityMatrix, precision), np.round(sensitivityMatrixMatlab, precision))

def test_resistanceMatrix():
    precision = 20
    assert np.array_equal(np.round(resistanceMatrix, precision), np.round(resistanceMatrixMatlab, precision))

def test_finalSF():
    precision = 6
    assert np.array_equal(np.round(np.array(SFOpt), precision), np.round(SFOptMatlab, precision))

def test_bFieldGeneratedByOptSF():
    precision = 12
    assert np.array_equal(np.round(np.array(BField), precision), np.round(np.array(BFieldMatlab), precision))

def test_gaußLegendre():
    assert np.array_equal(Test.gaußLegendre,np.array(gaußLegendreCorrect))

def test_WeightsGauss():
    assert np.array_equal(Test.calcWeightsGauss,np.array(calcWeightsGaussCorrect))

def main():
    test_triangleNodeArrays()
    test_areas()
    test_sensitivityMatrix()
    test_resistanceMatrix()
    test_finalSF()
    test_bFieldGeneratedByOptSF()
    test_gaußLegendre()
    test_WeightsGauss()

if __name__ == "__main__":
    main()