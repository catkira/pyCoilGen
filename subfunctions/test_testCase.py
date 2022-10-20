
from readMesh import CylindricMeshGiven
from defineTargetField import TargetFieldGiven
from sensitivityMatrix import getSensitivityMatrix
from resistanceMatrix import getResistanceMatrix
from streamFunctionOptimization import streamFunctionOptimization
import numpy as np

meshFile = "cylinder_radius500mm_length1500mm.stl" 
targetMeshFile = "sphere_radius150mm.stl" 
gaussOrder = 2
tikonovFac = 100
specificConductivityMaterial = 1.8000*10**-8
conducterThickness = 0.005 
materialFactor = specificConductivityMaterial/conducterThickness

Mesh = CylindricMeshGiven(meshFile)
TargetSphere = TargetFieldGiven(targetMeshFile,1)
sensitivityMatrix = getSensitivityMatrix(Mesh,TargetSphere,gaussOrder)
resistanceMatrix = getResistanceMatrix(Mesh,materialFactor)

def test_finalSF():
    result = streamFunctionOptimization(Mesh,TargetSphere,sensitivityMatrix,resistanceMatrix,tikonovFac)
    # TODO: checky why rounding is needed!
    assert (np.round(np.array(result), 12) == np.round(np.array(SFCorrectValue), 12)).all()

SFCorrectValue = [[-4.66916988e-06, -4.69774736e-06, -3.95939995e-06, -4.82221011e-06,
       -3.96550195e-06, -3.87749966e-06, -3.82771915e-06, -2.92862968e-06,
       -3.09944588e-06, -3.26900336e-06, -4.54936400e-06, -5.58752101e-06,
       -4.08059138e-06, -3.55106401e-06, -4.35087022e-06, -6.01269263e-06,
       -4.22084204e-06, -3.18190139e-06, -4.10009974e-06, -5.96980094e-06,
       -4.37558746e-06, -2.90454752e-06, -3.82714510e-06, -5.48811576e-06,
       -4.52500225e-06, -2.89673824e-06, -3.55797908e-06, -4.72917096e-06,
       -4.64209267e-06, -3.25927841e-06, -3.31142974e-06, -3.91818849e-06,
       -2.09963438e-06, -3.34845606e-06, -4.42231665e-06, -3.40778215e-06,
       -4.96401500e-06, -3.71020589e-06, -6.47174235e-06, -3.10184059e-06,
       -7.41610960e-06, -2.30211586e-06, -7.54218056e-06, -1.66104789e-06,
       -6.88055636e-06, -1.52421125e-06, -5.70765164e-06, -8.34218389e-06,
       -8.57509678e-06, -1.71698142e-06, -8.33627056e-07, -7.79149267e-06,
       -6.11222254e-07, -6.34459330e-06, -1.32985937e-06, -4.74768270e-06,
       -2.94559946e-06, -3.49515548e-06, -5.06152149e-06, -3.63192483e-06,
       -7.05892633e-06, -2.80316638e-06, -4.84372545e-06, -3.51759447e-06,
       -2.78445555e-06, -5.06790710e-06, -3.60543134e-06, -7.23002305e-06,
       -2.70154460e-06, -8.62725221e-06, -1.51603426e-06, -8.89681845e-06,
       -5.45749437e-07, -8.07459544e-06, -2.87684156e-07, -6.53979802e-06,
       -1.04852022e-06, -1.72984724e-06, -8.39834326e-07, -8.43900812e-06,
       -7.67582118e-06, -5.97268568e-07, -6.25821689e-06, -1.28468752e-06,
       -4.69346302e-06, -2.86515300e-06, -3.47076188e-06, -4.94941957e-06,
       -3.63493590e-06, -6.92469606e-06, -2.81267864e-06, -8.19936244e-06,
       -3.17196252e-06, -4.71374718e-06, -3.71565160e-06, -3.36022806e-06,
       -6.17358952e-06, -3.11900979e-06, -7.10683809e-06, -2.32528792e-06,
       -7.25756732e-06, -1.67147731e-06, -6.64643984e-06, -1.49442711e-06,
       -5.53693026e-06, -2.00332776e-06, -4.31645829e-06, -5.52943337e-06,
       -5.13784877e-06, -2.91349222e-06, -2.84655848e-06, -4.48044830e-06,
       -3.10574163e-06, -3.76609468e-06, -3.67413552e-06, -3.20068755e-06,
       -4.41266274e-06, -3.83452939e-06, -5.10130172e-06, -3.57225423e-06,
       -5.51868767e-06, -3.20964682e-06, -3.01378878e-06, -4.10778686e-06,
       -3.88664940e-06, -3.97227445e-06, -4.10069159e-06, -3.68643252e-06,
       -4.24376923e-06, -3.52000050e-06, -4.37117894e-06, -3.37662784e-06,
       -4.44378070e-06, -3.24438745e-06, -4.42575475e-06, -3.12146444e-06,
       -4.30506141e-06, -1.62539700e-06, -2.01042117e-06, -6.02517698e-06,
       -5.74081659e-06, -2.47517126e-06, -4.94816588e-06, -2.82491005e-06,
       -3.83106879e-06, -4.10633848e-06, -2.70729373e-06, -4.62023025e-06,
       -1.88570036e-06, -5.26327669e-06, -1.53163976e-06, -5.81066383e-06,
       -4.21442728e-06, -5.04756704e-06, -1.70989697e-06, -3.68205651e-07,
       -6.10496487e-06,  1.47970715e-07, -6.99815410e-06, -1.39543256e-07,
       -7.32531127e-06, -9.57449086e-07, -6.81484750e-06, -1.91909865e-06,
       -5.46253804e-06, -2.65938289e-06, -3.58298816e-06, -8.12796084e-06,
       -7.45753777e-06, -2.34238168e-07, -1.53049770e-06, -5.73509010e-06,
       -2.53874853e-06, -3.36247188e-06, -4.27797886e-06, -1.00916025e-06,
       -5.31326814e-06,  6.65965933e-07, -6.63341610e-06,  1.28644991e-06,
       -7.74121283e-06,  8.71395950e-07, -6.86976807e-07,  1.08710647e-06,
       -5.37257430e-06, -6.76238790e-06,  1.73567337e-06, -7.92044381e-06,
        1.27289596e-06, -8.30491374e-06,  6.22669922e-08, -7.56441054e-06,
       -1.36057344e-06, -5.71394071e-06, -2.47762055e-06, -3.18552582e-06,
       -4.28507087e-06, -9.97619107e-08, -1.42722841e-06, -7.12189079e-06,
       -5.40387404e-06, -2.48162448e-06, -3.07367482e-06, -4.23231060e-06,
       -7.77199925e-07, -5.21221734e-06,  8.53268705e-07, -6.46726798e-06,
        1.45036643e-06, -7.50493729e-06,  1.02295780e-06, -7.82893957e-06,
       -4.85233345e-06, -5.78757375e-06,  2.02870803e-08,  4.94123708e-07,
       -6.55251389e-06,  1.76526386e-07, -6.76767675e-06, -6.83554917e-07,
       -6.19242409e-06, -1.71291595e-06, -4.84496278e-06, -2.54671182e-06,
       -3.03232683e-06, -4.12542168e-06, -1.24926819e-06, -4.90005523e-06,
       -4.10079205e-06, -2.16780226e-06, -2.65993509e-06, -3.04451185e-06,
       -3.97844618e-06, -2.00886521e-06, -4.34337196e-06, -1.26497306e-06,
       -4.82034514e-06, -9.70477088e-07, -5.19910821e-06, -1.12395492e-06,
       -5.26988114e-06, -1.59029778e-06, -2.79007642e-06, -2.70792053e-06,
       -3.70586140e-06, -3.63983103e-06, -2.67094055e-06, -3.54731158e-06,
       -2.67469877e-06, -3.41971439e-06, -2.71767379e-06, -3.25926598e-06,
       -2.80154957e-06, -3.08313458e-06, -3.81168789e-06, -2.91868216e-06,
       -3.75857467e-06, -3.27537144e-06, -2.94811285e-06, -2.43131872e-06,
       -3.12667996e-06, -3.64870837e-06, -3.82781653e-06, -3.18312916e-06,
       -4.31394406e-06, -2.60736864e-06, -4.44729100e-06, -2.10229290e-06,
       -4.22375511e-06, -1.84875948e-06, -3.76721906e-06, -1.96045187e-06,
       -5.92342084e-06, -5.54476071e-06, -8.14003347e-07, -4.25324423e-07,
       -4.69959170e-06, -7.37345700e-07, -3.75403551e-06, -1.73768490e-06,
       -3.07610972e-06, -3.16560221e-06, -3.51282516e-06, -4.59692140e-06,
       -2.70152777e-06, -5.60450046e-06, -1.68719999e-06, -3.42363474e-06,
       -3.16555516e-06, -3.19946793e-06, -5.11476965e-06, -2.38495263e-06,
       -6.47013588e-06, -1.08257379e-06, -6.91468568e-06,  3.16706436e-08,
       -6.43415452e-06,  5.07715209e-07, -5.32987843e-06,  6.24101534e-08,
       -4.08020987e-06, -1.28761939e-06,  3.05300963e-07,  8.04931634e-07,
       -6.75910653e-06, -5.56357340e-06,  3.10536619e-07, -4.20489142e-06,
       -1.15830495e-06, -3.20303498e-06, -3.23198101e-06, -3.39408034e-06,
       -5.31001003e-06, -2.28056364e-06, -6.78469324e-06, -8.84776552e-07,
       -7.27413323e-06, -3.26897805e-06, -5.16167893e-06, -3.42850680e-06,
       -2.40432546e-06, -6.50681217e-06, -1.12505415e-06, -6.95190054e-06,
       -3.81093807e-08, -6.47383878e-06,  4.14566471e-07, -5.36782825e-06,
       -4.03869846e-08, -4.11090341e-06, -1.38073206e-06, -3.18372807e-06,
       -5.62727529e-06, -4.77658189e-06, -6.12278459e-07, -9.48270889e-07,
       -3.81547848e-06, -1.93443874e-06, -3.11210636e-06, -3.31869797e-06,
       -3.52199795e-06, -4.70494660e-06, -2.73849507e-06, -5.68889862e-06,
       -1.76952899e-06, -6.00451786e-06, -9.51497156e-07, -3.66110090e-06,
       -3.23418559e-06, -4.02600864e-06, -4.46949585e-06, -2.72400147e-06,
       -4.58672159e-06, -2.30235149e-06, -4.35593060e-06, -2.12883305e-06,
       -3.88553992e-06, -2.28752807e-06, -3.36762097e-06, -2.75052968e-06,
       -3.00120532e-06, -3.39065697e-06, -3.91432607e-06, -3.86718982e-06,
       -2.83760084e-06, -2.84060446e-06, -3.72019917e-06, -2.87057320e-06,
       -3.49091420e-06, -3.82583235e-06, -3.24501647e-06, -3.81864180e-06,
       -3.04896794e-06, -3.84790813e-06, -2.92626513e-06, -3.89230838e-06,
       -2.86273820e-06, -2.49269458e-06, -1.65548224e-06, -4.40615534e-06,
       -4.97534078e-06, -1.28768330e-06, -5.48659396e-06, -1.38575601e-06,
       -5.70622882e-06, -1.80101518e-06, -5.45759896e-06, -2.32071833e-06,
       -4.70744495e-06, -2.74320869e-06, -3.61602066e-06, -3.99266753e-06,
       -9.43664170e-07, -1.89395963e-06, -6.82452670e-06, -5.56924459e-06,
       -2.64195148e-06, -3.75379033e-06, -4.13806093e-06, -1.89161389e-06,
       -4.91098991e-06, -5.11858972e-07, -5.94009063e-06,  6.68696984e-08,
       -6.84934767e-06, -1.62249097e-07, -7.23950493e-06,  1.91391819e-07,
        9.14529967e-07, -6.60102640e-06, -7.78004690e-06,  6.06924975e-07,
       -8.28851797e-06, -4.07243208e-07, -7.76851786e-06, -1.63268776e-06,
       -6.18425226e-06, -2.58587739e-06, -3.89496260e-06, -4.24196549e-06,
       -1.54752422e-06, -5.26036189e-06, -1.58428733e-06, -2.58725126e-06,
       -6.47735646e-06, -4.04144750e-06, -4.29081377e-06, -1.53856466e-06,
       -5.40547195e-06,  3.22772421e-07, -6.86381457e-06,  1.10565623e-06,
       -8.14501678e-06,  7.88619496e-07, -8.70371449e-06, -2.85107884e-07,
       -8.15944673e-06, -6.69537711e-06, -7.89813764e-06,  5.91116908e-07,
        3.39588975e-07, -8.43450370e-06, -6.07310207e-07, -7.95474926e-06,
       -1.76360881e-06, -6.42607693e-06, -2.64950954e-06, -4.19727137e-06,
       -4.27950624e-06, -1.89329077e-06, -5.32885580e-06, -1.62181045e-07,
       -6.05647667e-06, -4.35775686e-06, -4.21210241e-06, -2.76658645e-06,
       -2.57663456e-06, -5.04689463e-06, -1.20775749e-06, -6.12872368e-06,
       -5.67284229e-07, -7.08742265e-06, -6.85820998e-07, -7.53550742e-06,
       -1.33551003e-06, -7.20199720e-06, -2.15038969e-06, -2.20864125e-06,
       -2.14455871e-06, -5.84699542e-06, -6.15773447e-06, -2.36862927e-06,
       -6.03227634e-06, -2.69205396e-06, -5.44191021e-06, -2.92369434e-06,
       -4.51521056e-06, -4.10111253e-06, -3.50115052e-06, -4.60709538e-06,
       -2.67126967e-06, -5.25745487e-06], [ 2.36689736e-06,  5.40135421e-05,  5.36120975e-05,  2.12634387e-06,
        2.13763439e-04,  2.16019332e-04,  2.13713517e-04, -2.13003594e-04,
       -2.10615828e-04, -2.10617418e-04, -4.93487301e-05, -4.94112453e-05,
        2.06397270e-04,  2.06239154e-04, -9.67735319e-05, -9.66920418e-05,
        1.92744966e-04,  1.92447502e-04, -1.36642272e-04, -1.36485021e-04,
        1.71294275e-04,  1.70866877e-04, -1.67401238e-04, -1.67241832e-04,
        1.40841761e-04,  1.40337209e-04, -1.89147259e-04, -1.89037852e-04,
        1.01246844e-04,  1.00749102e-04, -2.03053569e-04, -2.03010047e-04,
        9.96428817e-05,  5.28318299e-05, -2.02762729e-04, -2.10563230e-04,
        1.83567463e-06,  2.13603064e-04, -4.91922004e-05,  2.05862115e-04,
       -9.60896626e-05,  1.91725694e-04, -1.35716080e-04,  1.69835368e-04,
       -1.66529005e-04,  1.39149903e-04, -1.88535033e-04, -9.50914846e-05,
       -1.34477670e-04,  1.90682240e-04,  1.68345793e-04, -1.65388688e-04,
        1.37443584e-04, -1.87726715e-04,  9.80709809e-05, -2.02356179e-04,
        5.17568102e-05, -2.10464846e-04,  1.49892188e-06,  2.13446732e-04,
       -4.87643853e-05,  2.05319073e-04, -2.01858604e-04, -2.10340372e-04,
        5.05310916e-05,  1.14154901e-06,  2.13265955e-04, -4.82214695e-05,
        2.04687954e-04, -9.38757036e-05,  1.89469199e-04, -1.32979050e-04,
        1.66616600e-04, -1.64009304e-04,  1.35467949e-04, -1.86745969e-04,
        9.62590694e-05,  1.88264519e-04,  1.64904305e-04, -1.31458843e-04,
       -1.62610430e-04,  1.33519281e-04, -1.85749834e-04,  9.44816580e-05,
       -2.01351175e-04,  4.93412437e-05, -2.10211566e-04,  8.15790807e-07,
        2.13085783e-04, -4.76524059e-05,  2.04059911e-04, -9.26369455e-05,
        4.83746684e-05,  5.81557010e-07,  2.12931160e-04, -2.10100437e-04,
       -4.71346943e-05,  2.03525491e-04, -9.15597677e-05,  1.87244228e-04,
       -1.30149914e-04,  1.63461342e-04, -1.61409760e-04,  1.31888131e-04,
       -1.84895452e-04,  9.30087928e-05, -2.00915576e-04, -1.29252705e-04,
       -1.60593503e-04,  1.62495429e-04,  1.30808092e-04, -1.84317130e-04,
        9.20503488e-05, -2.00621657e-04,  4.77686241e-05, -2.10025819e-04,
        4.70923800e-07,  2.12823222e-04, -4.67464513e-05,  2.03161017e-04,
       -9.08071107e-05,  1.86555387e-04, -2.10000457e-04,  4.68496723e-07,
       -4.65708950e-05,  2.12776184e-04,  2.03017285e-04, -9.05086597e-05,
        1.86294560e-04, -1.28912599e-04,  1.62139397e-04, -1.60291531e-04,
        1.30421088e-04, -1.84106935e-04,  9.17214483e-05, -2.00516911e-04,
        4.75804229e-05, -1.60557720e-04, -1.84300847e-04,  1.30766201e-04,
        9.20415909e-05, -2.00619234e-04,  4.77990117e-05, -2.10029015e-04,
        5.32571304e-07,  2.12795264e-04, -4.66708503e-05,  2.03112220e-04,
       -9.07351781e-05,  1.86494735e-04, -1.29196355e-04,  1.62435842e-04,
        2.12875970e-04,  2.03428421e-04, -4.70515862e-05, -9.14702013e-05,
        1.87121525e-04, -1.30073492e-04,  1.63334937e-04, -1.61358668e-04,
        1.31784713e-04, -1.84872418e-04,  9.29526436e-05, -2.00913995e-04,
        4.83768588e-05, -2.10107320e-04,  6.34559436e-07,  1.33329104e-04,
        9.43295939e-05, -1.85735538e-04, -2.01355966e-04,  4.92422354e-05,
       -2.10222977e-04,  7.71610574e-07,  2.13004829e-04, -4.76500838e-05,
        2.03915829e-04, -9.26034420e-05,  1.88078223e-04, -1.31414566e-04,
        1.64701630e-04, -1.62575441e-04, -4.83582405e-05, -9.39527127e-05,
        2.04499161e-04,  1.89219154e-04, -1.33010854e-04,  1.66331494e-04,
       -1.64020308e-04,  1.35174631e-04, -1.86756680e-04,  9.59812013e-05,
       -2.01875962e-04,  5.02870667e-05, -2.10357235e-04,  9.45831546e-07,
        2.13161469e-04, -1.87775076e-04, -2.02391315e-04,  9.76617627e-05,
        5.13611209e-05, -2.10487880e-04,  1.14226842e-06,  2.13321738e-04,
       -4.90553587e-05,  2.05089184e-04, -9.53004029e-05,  1.90370556e-04,
       -1.34609318e-04,  1.67977443e-04, -1.65465819e-04,  1.37043352e-04,
        2.05596273e-04,  1.91356881e-04, -9.64293457e-05, -1.35953324e-04,
        1.69387099e-04, -1.66680614e-04,  1.38646318e-04, -1.88627633e-04,
        9.91087138e-05, -2.02818616e-04,  5.22950079e-05, -2.10592677e-04,
        1.33035900e-06,  2.13461389e-04, -4.96286680e-05,  1.00095669e-04,
        5.29420458e-05, -2.03086749e-04, -2.10652859e-04,  1.48279723e-06,
        2.13559779e-04, -4.99818688e-05,  2.05944209e-04, -9.71529286e-05,
        1.92028478e-04, -1.36822025e-04,  1.70344497e-04, -1.67465770e-04,
        1.39735286e-04, -1.89174562e-04, -9.73408199e-05, -1.37064166e-04,
        1.92285510e-04,  1.70706340e-04, -1.67686274e-04,  1.40147361e-04,
       -1.89321597e-04,  1.00477299e-04, -2.03148152e-04,  5.32127396e-05,
       -2.10656119e-04,  1.59047387e-06,  2.13603000e-04, -5.00428453e-05,
        2.06081987e-04, -2.02986513e-04, -2.10598625e-04,  5.30872648e-05,
        1.66196931e-06,  2.13585979e-04, -4.97766112e-05,  2.05991687e-04,
       -9.69407502e-05,  1.92093693e-04, -1.36623010e-04,  1.70424909e-04,
       -1.67293129e-04,  1.39830959e-04, -1.89035333e-04,  1.00211686e-04,
       -1.35548222e-04, -1.66332457e-04,  1.69554306e-04,  1.38850912e-04,
       -1.88349099e-04,  9.93613632e-05, -2.02619622e-04,  5.26106412e-05,
       -2.10485749e-04,  1.71337391e-06,  2.13513194e-04, -4.91985024e-05,
        2.05691117e-04, -9.59920459e-05,  1.91489246e-04,  2.13397916e-04,
       -2.10331375e-04,  1.75966115e-06, -4.83772188e-05,  2.05230850e-04,
       -9.46232270e-05,  1.90572601e-04, -1.33990045e-04,  1.68240309e-04,
       -1.64939163e-04,  1.37375113e-04, -1.87358238e-04,  9.80788441e-05,
       -2.02096911e-04,  5.18799676e-05,  1.66696267e-04,  1.35646002e-04,
       -1.63315546e-04, -1.86205412e-04,  9.65801982e-05, -2.01492038e-04,
        5.10275960e-05, -2.10155904e-04,  1.81251452e-06,  2.13260092e-04,
       -4.74224418e-05,  2.04686190e-04, -9.30299880e-05,  1.89492187e-04,
       -1.32174605e-04,  1.88183097e-06, -4.64630618e-05,  2.13123202e-04,
        2.04145365e-04, -9.14405986e-05,  1.88421074e-04, -1.30366383e-04,
        1.65169328e-04, -1.61699104e-04,  1.33942039e-04, -1.85058536e-04,
        9.51109879e-05, -2.00891725e-04,  5.02016180e-05, -2.09983245e-04,
       -1.60325975e-04, -1.84085069e-04,  1.32535335e-04,  9.39097041e-05,
       -2.00382615e-04,  4.95447768e-05, -2.09837267e-04,  1.97578822e-06,
        2.13010571e-04, -4.56262778e-05,  2.03695811e-04, -9.00802204e-05,
        1.87530142e-04, -1.28827275e-04,  1.63902366e-04,  2.12941725e-04,
        2.03410651e-04, -4.50216600e-05, -8.91398897e-05,  1.86961819e-04,
       -1.27778717e-04,  1.63096946e-04, -1.59395770e-04,  1.31650598e-04,
       -1.83426778e-04,  9.31719702e-05, -2.00038204e-04,  4.91723513e-05,
       -2.09738245e-04,  2.09747381e-06,  1.31430591e-04,  9.30195972e-05,
       -1.83178585e-04, -1.99907836e-04,  4.91520639e-05, -2.09699844e-04,
        2.24057724e-06,  2.12929330e-04, -4.47286527e-05,  2.03337449e-04,
       -8.87508173e-05,  1.86808318e-04, -1.27370061e-04,  1.62882570e-04,
       -1.59042226e-04, -4.47846149e-05, -8.89644191e-05,  2.03490911e-04,
        1.87097686e-04, -1.27656118e-04,  1.63297117e-04, -1.59313367e-04,
        1.31914333e-04, -1.83374562e-04,  9.34815551e-05, -2.00009392e-04,
        4.94930663e-05, -2.09727106e-04,  2.38983051e-06,  2.12977189e-04,
       -1.83983158e-04, -2.00326754e-04,  9.44921603e-05,  5.01487089e-05,
       -2.09815721e-04,  2.52865125e-06,  2.13079608e-04, -4.51742132e-05,
        2.03850633e-04, -8.97415421e-05,  1.87789768e-04, -1.28588033e-04,
        1.64281793e-04, -1.60164524e-04,  1.33032596e-04, -9.09587325e-05,
       -1.30021815e-04,  1.88782505e-04,  1.65690802e-04, -1.61465995e-04,
        1.34620033e-04, -1.84912396e-04,  9.59035971e-05, -2.00812383e-04,
        5.10267679e-05, -2.09952706e-04,  2.64452493e-06,  2.13222204e-04,
       -4.58303193e-05,  2.04364181e-04, -2.01394571e-04, -2.10118372e-04,
        5.19982438e-05,  2.72280147e-06,  2.13384058e-04, -4.66529544e-05,
        2.04954985e-04, -9.24335213e-05,  1.89927371e-04, -1.31743507e-04,
        1.67313376e-04, -1.63023824e-04,  1.36439679e-04, -1.86024070e-04,
        9.75061124e-05,  1.91051566e-04,  1.68904901e-04, -1.33502055e-04,
       -1.64608908e-04,  1.38217075e-04, -1.87154488e-04,  9.90563412e-05,
       -2.01988248e-04,  5.29113323e-05, -2.10289277e-04,  2.74215455e-06,
        2.13540855e-04, -4.75300100e-05,  2.05533859e-04, -9.39547866e-05,
        5.36192519e-05,  2.68632338e-06,  2.13668571e-04, -2.10441731e-04,
       -4.83442238e-05,  2.06012425e-04, -9.53065266e-05,  1.91983803e-04,
       -1.35042612e-04,  1.70223203e-04, -1.65989795e-04,  1.39681355e-04,
       -1.88138727e-04,  1.00315525e-04, -2.02507742e-04, -1.36141433e-04,
       -1.66966416e-04,  1.71064615e-04,  1.40606082e-04, -1.88835220e-04,
        1.01087881e-04, -2.02879599e-04,  5.40089530e-05, -2.10555305e-04,
        2.55675348e-06,  2.13747120e-04, -4.89804547e-05,  2.06316471e-04,
       -9.62931402e-05,  1.92579975e-04], [ 2.42214224e-04,  2.35121138e-04,  2.30580579e-04,  2.37487592e-04,
        3.64207994e-05,  4.87615463e-08,  3.57377206e-05, -2.08828633e-08,
        3.64306177e-05,  3.56951791e-05,  2.35270442e-04,  2.30633325e-04,
        7.35833789e-05,  7.22044630e-05,  2.15429097e-04,  2.11146302e-04,
        1.11696296e-04,  1.09600348e-04,  1.85727369e-04,  1.82009696e-04,
        1.49770571e-04,  1.46949218e-04,  1.50036034e-04,  1.47017943e-04,
        1.85434880e-04,  1.81919407e-04,  1.11890193e-04,  1.09632751e-04,
        2.15174300e-04,  2.11060246e-04,  7.36854639e-05,  7.21972235e-05,
        1.98827411e-04,  2.17171400e-04,  6.79343190e-05,  3.35873453e-05,
        2.23628993e-04,  3.36825637e-05,  2.17131047e-04,  6.80505317e-05,
        1.98749822e-04,  1.03290238e-04,  1.71299061e-04,  1.38476237e-04,
        1.38351420e-04,  1.71406402e-04,  1.03162808e-04,  1.78715869e-04,
        1.54008945e-04,  9.30051611e-05,  1.24671839e-04,  1.24372088e-04,
        1.54293068e-04,  9.27311244e-05,  1.78938911e-04,  6.10617468e-05,
        1.95402576e-04,  3.01884425e-05,  2.01166220e-04,  3.03339955e-05,
        1.95279734e-04,  6.12798140e-05,  5.18446263e-05,  2.56293500e-05,
        1.66106424e-04,  1.70960963e-04,  2.58204840e-05,  1.65919825e-04,
        5.21515229e-05,  1.51816502e-04,  7.91378803e-05,  1.30806666e-04,
        1.06062017e-04,  1.05619922e-04,  1.31230960e-04,  7.87405675e-05,
        1.52152936e-04,  6.22204068e-05,  8.33595955e-05,  1.02586328e-04,
        8.28178103e-05,  1.03101968e-04,  6.17303228e-05,  1.19492987e-04,
        4.06378967e-05,  1.30403262e-04,  2.00854567e-05,  1.34170787e-04,
        2.03154402e-05,  1.30179289e-04,  4.10161955e-05,  1.19087149e-04,
        8.96612951e-05,  9.22050575e-05,  1.40305624e-05,  1.37698927e-05,
        8.94286661e-05,  2.83023401e-05,  8.17848659e-05,  4.29040595e-05,
        7.04331018e-05,  5.74384700e-05,  5.68429989e-05,  7.09876532e-05,
        4.23547626e-05,  8.22125942e-05,  2.78725384e-05,  3.55824238e-05,
        2.86934276e-05,  2.93008405e-05,  3.61307262e-05,  2.13582367e-05,
        4.17536033e-05,  1.40389798e-05,  4.54533400e-05,  6.92532427e-06,
        4.66801597e-05,  7.20767129e-06,  4.52350084e-05,  1.44999005e-05,
        4.13431466e-05,  2.19344847e-05, -1.85362755e-07, -6.35550883e-07,
       -6.91051121e-07,  1.09370651e-07,  1.41125854e-07, -6.78194846e-07,
        1.22235523e-07, -6.25207551e-07,  3.73396731e-08, -5.49854790e-07,
       -1.14061211e-07, -4.53355052e-07, -3.08729750e-07, -3.31732715e-07,
       -4.99616199e-07, -2.97639121e-05, -2.22433249e-05, -3.63382480e-05,
       -4.23353827e-05, -1.46882262e-05, -4.64041630e-05, -7.28913627e-06,
       -4.78969235e-05, -6.99111979e-06, -4.65646067e-05, -1.42202736e-05,
       -4.26538619e-05, -2.16897174e-05, -3.67955251e-05, -2.92181713e-05,
       -1.38205387e-05, -2.80308042e-05, -9.06099076e-05, -8.29642422e-05,
       -4.26596178e-05, -7.15375835e-05, -5.73353344e-05, -5.78278080e-05,
       -7.11405871e-05, -4.31762107e-05, -8.26985161e-05, -2.84798412e-05,
       -9.04802392e-05, -1.41132771e-05, -9.32712166e-05, -1.03183311e-04,
       -1.19849260e-04, -6.24497642e-05, -4.11776250e-05, -1.31038936e-04,
       -2.03958119e-05, -1.35021061e-04, -2.01161482e-05, -1.31140603e-04,
       -4.07587269e-05, -1.20065684e-04, -6.19798788e-05, -1.03520746e-04,
       -8.32319263e-05, -8.36664747e-05, -1.66619824e-04, -1.52547203e-04,
       -5.19145915e-05, -7.89080398e-05, -1.31524543e-04, -1.05914502e-04,
       -1.06291312e-04, -1.31240845e-04, -7.93253751e-05, -1.52372195e-04,
       -5.22944991e-05, -1.66540757e-04, -2.58955381e-05, -1.71564781e-04,
       -2.56358684e-05, -9.31558831e-05, -6.14037883e-05, -1.79029775e-04,
       -1.95638862e-04, -3.04012577e-05, -2.01517954e-04, -3.01675895e-05,
       -1.95702179e-04, -6.10699697e-05, -1.79173365e-04, -9.27948164e-05,
       -1.54479980e-04, -1.24514742e-04, -1.24836124e-04, -1.54242060e-04,
       -6.78737941e-05, -1.03108469e-04, -1.98923175e-04, -1.71506104e-04,
       -1.38321328e-04, -1.38588785e-04, -1.71307917e-04, -1.03410011e-04,
       -1.98803167e-04, -6.81555756e-05, -2.17220258e-04, -3.37398783e-05,
       -2.23733747e-04, -3.35373214e-05, -2.17273314e-04, -2.10931449e-04,
       -2.30450091e-04, -7.22901367e-05, -3.57830587e-05, -2.37349558e-04,
       -3.56158322e-05, -2.30494924e-04, -7.20656701e-05, -2.11030472e-04,
       -1.09454826e-04, -1.81944326e-04, -1.46806506e-04, -1.47018696e-04,
       -1.81784605e-04, -1.09692885e-04, -2.15020532e-04, -1.85387538e-04,
       -1.11592100e-04, -1.49646404e-04, -1.49798794e-04, -1.85269871e-04,
       -1.11761628e-04, -2.14944873e-04, -7.36480306e-05, -2.34811495e-04,
       -3.64521462e-05, -2.41830433e-04, -3.63235894e-05, -2.34846973e-04,
       -7.34857007e-05, -7.21763746e-05, -3.57212313e-05, -2.30131939e-04,
       -2.36997503e-04, -3.56337505e-05, -2.30155415e-04, -7.20805142e-05,
       -2.10734413e-04, -1.09440150e-04, -1.81699479e-04, -1.46733884e-04,
       -1.46819744e-04, -1.81630396e-04, -1.09535302e-04, -2.10687148e-04,
       -1.71021437e-04, -1.38194850e-04, -1.38183244e-04, -1.71008629e-04,
       -1.03098248e-04, -1.98324595e-04, -6.79309620e-05, -2.16593948e-04,
       -3.36181722e-05, -2.23038888e-04, -3.35731670e-05, -2.16602385e-04,
       -6.79052145e-05, -1.98337575e-04, -1.03083551e-04, -3.02212928e-05,
       -3.02235419e-05, -2.00502242e-04, -1.94717992e-04, -6.11211946e-05,
       -1.78312102e-04, -9.27684318e-05, -1.53765806e-04, -1.24326187e-04,
       -1.24255310e-04, -1.53817930e-04, -9.26968620e-05, -1.78340297e-04,
       -6.10741956e-05, -1.94728337e-04, -1.05698725e-04, -1.30725427e-04,
       -1.05536380e-04, -7.87298177e-05, -1.51512567e-04, -5.18688619e-05,
       -1.65388682e-04, -2.56675722e-05, -1.70267158e-04, -2.57071151e-05,
       -1.65353689e-04, -5.19898340e-05, -1.51433349e-04, -7.88928378e-05,
       -1.30597503e-04, -1.33503401e-04, -1.29642710e-04, -2.02041577e-05,
       -4.08623661e-05, -1.18735694e-04, -6.19911582e-05, -1.02406126e-04,
       -8.30196017e-05, -8.27559570e-05, -1.02624054e-04, -6.17326685e-05,
       -1.18880409e-04, -4.06680821e-05, -1.29711612e-04, -2.01251751e-05,
       -5.67870960e-05, -4.23573649e-05, -7.05961110e-05, -8.17008546e-05,
       -2.79018337e-05, -8.90703754e-05, -1.38092417e-05, -9.16239456e-05,
       -1.39238088e-05, -8.89552518e-05, -2.81662616e-05, -8.14721791e-05,
       -4.27130918e-05, -7.02716235e-05, -5.71615057e-05, -7.10720187e-06,
       -1.43887388e-05, -4.48488068e-05, -4.10690391e-05, -2.17983492e-05,
       -3.54246934e-05, -2.91166433e-05, -2.86254898e-05, -3.58704646e-05,
       -2.13476551e-05, -4.13999313e-05, -1.40605459e-05, -4.50228545e-05,
       -6.96249190e-06, -4.62329109e-05,  2.24679115e-07,  4.81674926e-07,
        4.88995186e-07,  3.23634630e-07,  7.47066687e-07,  1.51861058e-07,
        9.33699330e-07, -1.59752593e-08,  9.88500670e-07, -5.80925197e-08,
        9.25770029e-07, -4.82007876e-08,  7.97976233e-07,  4.14524326e-08,
        6.47374912e-07,  4.68003574e-05,  4.28996744e-05,  1.42764608e-05,
        2.17049147e-05,  3.70033369e-05,  2.91983437e-05,  2.99049533e-05,
        3.63113091e-05,  2.23121665e-05,  4.23458595e-05,  1.46972701e-05,
        4.64921028e-05,  7.26022600e-06,  4.80725599e-05,  7.07774194e-06,
        4.32810107e-05,  2.85069911e-05,  8.25950906e-05,  9.04650431e-05,
        1.40891773e-05,  9.33793434e-05,  1.39017279e-05,  9.08280565e-05,
        2.80656396e-05,  8.32370280e-05,  4.26287285e-05,  7.17957917e-05,
        5.72400858e-05,  5.80192953e-05,  7.10120904e-05,  1.20383338e-04,
        1.03833068e-04,  6.19224067e-05,  8.30946953e-05,  8.39057879e-05,
        1.03001218e-04,  6.25871588e-05,  1.19691064e-04,  4.12209653e-05,
        1.30983031e-04,  2.03759986e-05,  1.35116353e-04,  2.01940708e-05,
        1.31378573e-04,  4.07809353e-05,  5.23495447e-05,  2.58788313e-05,
        1.66493494e-04,  1.71681859e-04,  2.57131776e-05,  1.66893174e-04,
        5.19346629e-05,  1.52908573e-04,  7.88467568e-05,  1.31880421e-04,
        1.05772469e-04,  1.06566303e-04,  1.31054681e-04,  7.94864657e-05,
        1.52213855e-04,  9.27522343e-05,  1.24403556e-04,  1.54859013e-04,
        1.25128300e-04,  1.54097105e-04,  9.33280281e-05,  1.78917472e-04,
        6.14642924e-05,  1.95636247e-04,  3.03860063e-05,  2.01674834e-04,
        3.02470232e-05,  1.96009834e-04,  6.10985367e-05,  1.79563554e-04,
        2.17293868e-04,  2.23946232e-04,  3.36212801e-05,  3.37242163e-05,
        2.17612871e-04,  6.79200734e-05,  1.99325972e-04,  1.03103766e-04,
        1.71886449e-04,  1.38270972e-04,  1.38878149e-04,  1.71242318e-04,
        1.03579342e-04,  1.98776410e-04,  6.82145526e-05,  1.82309254e-04,
        1.47288088e-04,  1.46838219e-04,  1.81826569e-04,  1.09846711e-04,
        2.11022430e-04,  7.23409760e-05,  2.30630083e-04,  3.57651910e-05,
        2.37637836e-04,  3.57060309e-05,  2.30871392e-04,  7.21361699e-05,
        2.11436884e-04,  1.09501453e-04]]


def main():
    test_finalSF()

if __name__ == "__main__":
    main()