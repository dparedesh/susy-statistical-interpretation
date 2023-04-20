#!/usr/bin/env python

import os, pathUtilities
dataDir = os.path.join(pathUtilities.histFitterTopDirectory(), 'susyGridFiles')
shareDir = os.path.join(pathUtilities.histFitterTopDirectory(), 'share')

#def main():
    #getRunnumbersMassesDictSSAllGrids()
    #print getRunnumbersMassesDictSSAllGrids()
    

def writeRunnumbersDictToFile(fileName):
    import pickle
    runnumbersDict = getRunnumbersMassesDictSSAllGrids()
    outFile = open(fileName, 'wb') 
    pickle.dump(runnumbersDict, outFile)

def getRunnumbersMassesDictSSAllGrids():
    gridDict = {}
    for file in os.listdir(dataDir):
        if file.startswith('Mc') and 'Susy' in file and 'Susy_missingPoints'\
               and not file.endswith('~') and not file.endswith('.root') and not os.path.isdir(os.path.join(dataDir,file)):
            gridDict[file] = getRunnumberMassesDictSS(file)
    return gridDict

def getRunnumberMassesDictSS(gridFileName, SigNameSchema='SP:4,LSP:5'):
    gridFile = open(os.path.join(dataDir, gridFileName))
    gridDict = {}
    for point in gridFile:
        # protection against blank lines and "#" character
        if point.startswith("mc"):
            splitName = point.split('.')
            masses = splitName[2].split('_')
            mass = getUglyCaseBashingMasses(gridFileName, splitName[1], masses, SigNameSchema)
            #gridDict['{0}_{1}_{2}'.format(splitName[1],mass[0],mass[1])] = mass
            gridDict[splitName[1]] = mass # fix the format


    return gridDict
  
def getUglyCaseBashingMasses(gridFileName, runNumber, masses, SigNameSchema="SP:4,LSP:5"):
    posM = []
    for particle in list(SigNameSchema.split(",")):
        posM.append(int(particle.split(":")[-1]))

    SP_Mass = str(masses[posM[0]].replace("p",'.'))
    LSP_Mass = str(masses[posM[1]].replace("p",'.'))

    return [SP_Mass,LSP_Mass]



def getMsugraPointsDict():
    pointsDict = {
        164435:(2600,400),#"m5200",30),
     164436:(3000,400),#"m6000",30),
     164437:(2600,350),#"m5200",30),
     166732:(400,400),#"m800",30),
     166733:(400,450),#"m800",30),
     166734:(400,500),#"m800",30),
     166735:(400,550),#"m800",30),
     166736:(400,600),#"m800",30),
     166737:(400,650),#"m800",30),
     166738:(400,700),#"m800",30),
     166739:(400,750),#"m800",30),
     166740:(400,800),#"m800",30),
     166741:(600,400),#"m1200",30),
     166742:(600,450),#"m1200",30),
     166743:(600,500),#"m1200",30),
     166744:(600,550),#"m1200",30),
     166745:(600,600),#"m1200",30),
     166746:(600,650),#"m1200",30),
     166747:(600,700),#"m1200",30),
     166748:(600,750),#"m1200",30),
     166749:(600,800),#"m1200",30),
     166750:(600,850),#"m1200",30),
     166751:(600,900),#"m1200",30),
     166752:(600,950),#"m1200",30),
     166753:(800,400),#"m1600",30),
     166754:(800,450),#"m1600",30),
     166755:(800,500),#"m1600",30),
     166756:(800,550),#"m1600",30),
     166757:(800,600),#"m1600",30),
     166758:(800,650),#"m1600",30),
     166759:(800,700),#"m1600",30),
     166760:(800,750),#"m1600",30),
     166761:(800,800),#"m1600",30),
     166762:(800,850),#"m1600",30),
     166763:(800,900),#"m1600",30),
     166764:(800,950),#"m1600",30),
     166765:(1000,400),#"m2000",30),
     166766:(1000,450),#"m2000",30),
     166767:(1000,500),#"m2000",30),
     166768:(1000,550),#"m2000",30),
     166769:(1000,600),#"m2000",30),
     166770:(1000,650),#"m2000",30),
     166771:(1000,700),#"m2000",30),
     166772:(1000,750),#"m2000",30),
     166773:(1000,800),#"m2000",30),
     166774:(1000,850),#"m2000",30),
     166775:(1000,900),#"m2000",30),
     166776:(1000,950),#"m2000",30),
     166777:(1200,400),#"m2400",30),
     166778:(1200,450),#"m2400",30),
     166779:(1200,500),#"m2400",30),
     166780:(1200,550),#"m2400",30),
     166781:(1200,600),#"m2400",30),
     166782:(1200,650),#"m2400",30),
     166783:(1200,700),#"m2400",30),
     166784:(1200,750),#"m2400",30),
     166785:(1200,800),#"m2400",30),
     166786:(1200,850),#"m2400",30),
     166787:(1200,900),#"m2400",30),
     166788:(1200,950),#"m2400",30),
     166789:(1400,400),#"m2800",30),
     166790:(1400,450),#"m2800",30),
     166791:(1400,500),#"m2800",30),
     166792:(1400,550),#"m2800",30),
     166793:(1400,600),#"m2800",30),
     166794:(1400,650),#"m2800",30),
     166795:(1400,700),#"m2800",30),
     166796:(1400,750),#"m2800",30),
     166797:(1400,800),#"m2800",30),
     166798:(1400,850),#"m2800",30),
     166799:(1400,900),#"m2800",30),
     166800:(1400,950),#"m2800",30),
     166801:(600,1000),#"m1200",30),
     166802:(800,1000),#"m1600",30),
     166803:(1000,1000),#"m2000",30),
     166804:(1200,1000),#"m2400",30),
     166805:(1400,1000),#"m2800",30),
     166806:(1600,700),#"m3200",30),
     166807:(1600,250),#"m3200",30),
     166808:(1600,300),#"m3200",30),
     166809:(1600,350),#"m3200",30),
     166810:(1600,400),#"m3200",30),
     166811:(1600,450),#"m3200",30),
     166812:(1600,500),#"m3200",30),
     166813:(1600,550),#"m3200",30),
     166814:(1600,600),#"m3200",30),
     166815:(1600,650),#"m3200",30),
     166816:(1800,250),#"m3600",30),
     166817:(1800,300),#"m3600",30),
     166818:(1800,350),#"m3600",30),
     166819:(1800,400),#"m3600",30),
     166820:(1800,450),#"m3600",30),
     166821:(1800,500),#"m3600",30),
     166822:(1800,550),#"m3600",30),
     166823:(1800,600),#"m3600",30),
     166824:(1800,650),#"m3600",30),
     166825:(1600,750),#"m3200",30),
     166826:(2000,250),#"m4000",30),
     166827:(2000,300),#"m4000",30),
     166828:(2000,350),#"m4000",30),
     166829:(2000,400),#"m4000",30),
     166830:(2000,450),#"m4000",30),
     166831:(2000,500),#"m4000",30),
     166832:(2000,550),#"m4000",30),
     166833:(2000,600),#"m4000",30),
     166834:(2000,650),#"m4000",30),
     166835:(3500,250),#"m7000",30),
     166836:(2200,250),#"m4400",30),
     166837:(2200,300),#"m4400",30),
     166838:(2200,350),#"m4400",30),
     166839:(2200,400),#"m4400",30),
     166840:(2200,450),#"m4400",30),
     166841:(2200,500),#"m4400",30),
     166842:(2200,550),#"m4400",30),
     166843:(2200,600),#"m4400",30),
     166844:(2200,650),#"m4400",30),
     166845:(3500,300),#"m7000",30),
     166846:(2400,250),#"m4800",30),
     166847:(2400,300),#"m4800",30),
     166848:(2400,350),#"m4800",30),
     166849:(2400,400),#"m4800",30),
     166850:(2400,450),#"m4800",30),
     166851:(2400,500),#"m4800",30),
     166852:(2400,550),#"m4800",30),
     166853:(2400,600),#"m4800",30),
     166854:(2400,650),#"m4800",30),
     166855:(3500,350),#"m7000",30),
     166856:(2600,250),#"m5200",30),
     166857:(2600,300),#"m5200",30),
     166858:(2600,450),#"m5200",30),
     166859:(2600,500),#"m5200",30),
     166860:(2600,550),#"m5200",30),
     166861:(2600,600),#"m5200",30),
     166862:(2600,650),#"m5200",30),
     166863:(3500,400),#"m7000",30),
     166864:(2800,250),#"m5600",30),
     166865:(2800,300),#"m5600",30),
     166866:(2800,350),#"m5600",30),
     166867:(2800,400),#"m5600",30),
     166868:(2800,450),#"m5600",30),
     166869:(2800,500),#"m5600",30),
     166870:(2800,550),#"m5600",30),
     166871:(2800,600),#"m5600",30),
     166872:(2800,650),#"m5600",30),
     166873:(3500,450),#"m7000",30),
     166874:(3000,250),#"m6000",30),
     166875:(3000,300),#"m6000",30),
     166876:(3000,350),#"m6000",30),
     166877:(3000,450),#"m6000",30),
     166878:(3000,500),#"m6000",30),
     166879:(3000,550),#"m6000",30),
     166880:(3000,600),#"m6000",30),
     166881:(3000,650),#"m6000",30),
     166882:(3500,500),#"m7000",30),
     166883:(3500,550),#"m7000",30),
     166884:(3500,600),#"m7000",30),
     166885:(3500,650),#"m7000",30),
     166886:(1600,800),#"m3200",30),
     166887:(4000,250),#"m8000",30),
     166888:(4000,300),#"m8000",30),
     166889:(4000,350),#"m8000",30),
     166890:(4000,400),#"m8000",30),
     166891:(4000,450),#"m8000",30),
     166892:(4000,500),#"m8000",30),
     166893:(4000,550),#"m8000",30),
     166894:(4000,600),#"m8000",30),
     166895:(4000,650),#"m8000",30),
     166896:(1800,800),#"m3600",30),
     166897:(4500,250),#"m9000",30),
     166898:(4500,300),#"m9000",30),
     166899:(4500,350),#"m9000",30),
     166900:(4500,400),#"m9000",30),
     166901:(4500,450),#"m9000",30),
     166902:(4500,500),#"m9000",30),
     166903:(4500,550),#"m9000",30),
     166904:(4500,600),#"m9000",30),
     166905:(4500,650),#"m9000",30),
     166906:(1800,750),#"m3600",30),
     166907:(5000,250),#"m10000",30),
     166908:(5000,300),#"m10000",30),
     166909:(5000,350),#"m10000",30),
     166910:(5000,400),#"m10000",30),
     166911:(5000,450),#"m10000",30),
     166912:(5000,500),#"m10000",30),
     166913:(5000,550),#"m10000",30),
     166914:(5000,600),#"m10000",30),
     166915:(5000,650),#"m10000",30),
     166916:(1800,700),#"m3600",30),
     166917:(5500,250),#"m11000",30),
     166918:(5500,300),#"m11000",30),
     166919:(5500,350),#"m11000",30),
     166920:(5500,400),#"m11000",30),
     166921:(5500,450),#"m11000",30),
     166922:(5500,500),#"m11000",30),
     166923:(5500,550),#"m11000",30),
     166924:(5500,600),#"m11000",30),
     166925:(5500,650),#"m11000",30),
     166926:(2000,700),#"m4000",30),
     166927:(6000,250),#"m12000",30),
     166928:(6000,300),#"m12000",30),
     166929:(6000,350),#"m12000",30),
     166930:(6000,400),#"m12000",30),
     166931:(6000,450),#"m12000",30),
     166932:(6000,500),#"m12000",30),
     166933:(6000,550),#"m12000",30),
     166934:(6000,600),#"m12000",30),
     166935:(6000,650),#"m12000",30),
     166936:(2000,750),#"m4000",30),
     166937:(2000,800),#"m4000",30),
     166938:(1200,350),#"m2400",30),
     166939:(3200,250),#"m6400",30),
     166940:(3200,300),#"m6400",30),
     166941:(3200,350),#"m6400",30),
     166942:(3200,400),#"m6400",30),
     166943:(3200,450),#"m6400",30),
     166944:(3200,500),#"m6400",30),
     166945:(3200,550),#"m6400",30),
     166946:(3200,600),#"m6400",30),
     166947:(3200,650),#"m6400",30),
     166948:(1200,300),#"m2400",30),
     166949:(1400,300),#"m2800",30),
     166950:(1400,350),#"m2800",30),
     166951:(280,550),#"m560",30),
     166952:(300,620),#"m600",30),
     166953:(320,640),#"m640",30),
     166954:(320,660),#"m640",30),
     166955:(350,550),#"m700",30),
     166956:(350,680),#"m700",30),
     166957:(230,420),#"m460",30),
     166958:(250,460),#"m500",30),
     166959:(250,500),#"m500",30),
   }

    return pointsDict


def getFilterEfficiency(runNumber):
    if runNumber == 172159: return 3.2147E-01
    elif runNumber == 172160: return 3.3821E-01
    elif runNumber == 172161: return 3.4516E-01
    elif runNumber == 172162: return 3.5946E-01
    elif runNumber == 172163: return 3.7590E-01
    elif runNumber == 172164: return 3.6691E-01
    elif runNumber == 172165: return 3.6619E-01
    elif runNumber == 172166: return 3.7817E-01
    elif runNumber == 172167: return 3.9205E-01
    elif runNumber == 172168: return 3.8807E-01
    elif runNumber == 172169: return 3.8250E-01
    elif runNumber == 172170: return 3.8458E-01
    elif runNumber == 172171: return 3.8228E-01
    elif runNumber == 172172: return 3.9364E-01
    elif runNumber == 172173: return 4.0258E-01
    elif runNumber == 172174: return 3.9423E-01
    elif runNumber == 172175: return 4.0033E-01
    elif runNumber == 172176: return 3.9924E-01
    elif runNumber == 172177: return 3.9240E-01
    elif runNumber == 172178: return 3.8218E-01
    elif runNumber == 172179: return 3.9462E-01
    elif runNumber == 172180: return 4.0652E-01
    elif runNumber == 172181: return 4.2276E-01
    elif runNumber == 172182: return 4.1375E-01
    elif runNumber == 172183: return 4.1308E-01
    elif runNumber == 172184: return 4.0715E-01
    elif runNumber == 172185: return 4.0301E-01
    elif runNumber == 172186: return 3.9701E-01
    elif runNumber == 172187: return 3.9230E-01
    elif runNumber == 172188: return 3.8870E-01
    elif runNumber == 172189: return 4.0975E-01
    elif runNumber == 172190: return 4.2105E-01
    elif runNumber == 172191: return 4.3188E-01
    elif runNumber == 172192: return 4.2628E-01
    elif runNumber == 172193: return 4.2523E-01
    elif runNumber == 172194: return 4.2238E-01
    elif runNumber == 172195: return 4.1520E-01
    elif runNumber == 172196: return 4.1309E-01
    elif runNumber == 172197: return 4.0614E-01
    elif runNumber == 172198: return 4.0597E-01
    elif runNumber == 172199: return 3.9894E-01
    elif runNumber == 172200: return 3.9022E-01
    elif runNumber == 172201: return 4.2226E-01
    elif runNumber == 172202: return 4.2944E-01
    elif runNumber == 172203: return 4.4404E-01
    elif runNumber == 172204: return 4.4026E-01
    elif runNumber == 172205: return 4.3972E-01
    elif runNumber == 172206: return 4.3576E-01
    elif runNumber == 172207: return 4.3423E-01
    elif runNumber == 172208: return 4.2658E-01
    elif runNumber == 172209: return 4.2547E-01
    elif runNumber == 172210: return 4.2057E-01
    elif runNumber == 172211: return 4.1317E-01
    elif runNumber == 172212: return 4.0705E-01
    elif runNumber == 172213: return 4.0111E-01
    elif runNumber == 172214: return 3.9588E-01
    elif runNumber == 172215: return 4.3112E-01
    elif runNumber == 172216: return 4.4365E-01
    elif runNumber == 172217: return 4.5032E-01
    elif runNumber == 172218: return 4.4773E-01
    elif runNumber == 172219: return 4.4807E-01
    elif runNumber == 172220: return 4.4377E-01
    elif runNumber == 172221: return 4.4404E-01
    elif runNumber == 172222: return 4.3605E-01
    elif runNumber == 172223: return 4.4033E-01
    elif runNumber == 172224: return 4.2884E-01
    elif runNumber == 172225: return 4.3441E-01
    elif runNumber == 172226: return 4.2299E-01
    elif runNumber == 172227: return 4.1898E-01
    elif runNumber == 172228: return 4.1295E-01
    elif runNumber == 172229: return 4.0624E-01
    elif runNumber == 172230: return 3.9401E-01
    elif runNumber == 172231: return 4.4050E-01
    elif runNumber == 172232: return 4.4611E-01
    elif runNumber == 172233: return 4.5994E-01
    elif runNumber == 172234: return 4.5605E-01
    elif runNumber == 172235: return 4.6226E-01
    elif runNumber == 172236: return 4.5356E-01
    elif runNumber == 172237: return 4.5703E-01
    elif runNumber == 172238: return 4.4997E-01
    elif runNumber == 172239: return 4.4844E-01
    elif runNumber == 172240: return 4.4602E-01
    elif runNumber == 172241: return 4.4420E-01
    elif runNumber == 172242: return 4.3330E-01
    elif runNumber == 172243: return 4.3848E-01
    elif runNumber == 172244: return 4.2682E-01
    elif runNumber == 172245: return 4.1968E-01
    elif runNumber == 172246: return 4.1255E-01
    elif runNumber == 172247: return 4.0887E-01
    elif runNumber == 172248: return 3.9880E-01
    elif runNumber == 172249: return 4.5891E-01
    elif runNumber == 172250: return 4.6278E-01
    elif runNumber == 172251: return 4.7020E-01
    elif runNumber == 172252: return 4.6627E-01
    elif runNumber == 172253: return 4.6375E-01
    elif runNumber == 172254: return 4.5824E-01
    elif runNumber == 172255: return 4.6234E-01
    elif runNumber == 172256: return 4.5909E-01
    elif runNumber == 172257: return 4.5825E-01
    elif runNumber == 172258: return 4.5667E-01
    elif runNumber == 172259: return 4.5298E-01
    elif runNumber == 172260: return 4.4787E-01
    elif runNumber == 172261: return 4.4128E-01
    elif runNumber == 172262: return 4.4145E-01
    elif runNumber == 172263: return 4.3424E-01
    elif runNumber == 172264: return 4.2883E-01
    elif runNumber == 172265: return 4.2431E-01
    elif runNumber == 172266: return 4.1646E-01
    elif runNumber == 172267: return 4.0746E-01
    elif runNumber == 172268: return 4.0079E-01
    elif runNumber == 172269: return 4.6520E-01
    elif runNumber == 172270: return 4.6768E-01
    elif runNumber == 172271: return 4.7905E-01
    elif runNumber == 172272: return 4.7020E-01
    elif runNumber == 172273: return 4.7656E-01
    elif runNumber == 172274: return 4.7095E-01
    elif runNumber == 172275: return 4.7277E-01
    elif runNumber == 172276: return 4.6688E-01
    elif runNumber == 172277: return 4.6677E-01
    elif runNumber == 172278: return 4.6305E-01
    elif runNumber == 172279: return 4.6336E-01
    elif runNumber == 172280: return 4.5615E-01
    elif runNumber == 172281: return 4.5436E-01
    elif runNumber == 172282: return 4.5554E-01
    elif runNumber == 172283: return 4.4427E-01
    elif runNumber == 172284: return 4.4540E-01
    elif runNumber == 172285: return 4.4183E-01
    elif runNumber == 172286: return 4.3289E-01
    elif runNumber == 172287: return 4.2748E-01
    elif runNumber == 172288: return 4.1985E-01
    elif runNumber == 172289: return 4.0838E-01
    elif runNumber == 172290: return 4.0397E-01
    elif runNumber == 172291: return 4.6863E-01
    elif runNumber == 172292: return 4.7842E-01
    elif runNumber == 172293: return 4.8592E-01
    elif runNumber == 172294: return 4.7965E-01
    elif runNumber == 172295: return 4.8386E-01
    elif runNumber == 172296: return 4.7664E-01
    elif runNumber == 172297: return 4.7822E-01
    elif runNumber == 172298: return 4.7666E-01
    elif runNumber == 172299: return 4.7577E-01
    elif runNumber == 172300: return 4.7394E-01
    elif runNumber == 172301: return 4.6992E-01
    elif runNumber == 172302: return 4.6372E-01
    elif runNumber == 172303: return 4.6580E-01
    elif runNumber == 172304: return 4.6231E-01
    elif runNumber == 172305: return 4.6445E-01
    elif runNumber == 172306: return 4.5094E-01
    elif runNumber == 172307: return 4.5510E-01
    elif runNumber == 172308: return 4.4483E-01
    elif runNumber == 172309: return 4.4588E-01
    elif runNumber == 172310: return 4.3088E-01
    elif runNumber == 172311: return 4.3044E-01
    elif runNumber == 172312: return 4.2448E-01
    elif runNumber == 172313: return 4.1555E-01
    elif runNumber == 172314: return 4.0856E-01
    elif runNumber == 172315: return 4.7978E-01
    elif runNumber == 172316: return 4.8412E-01
    elif runNumber == 172317: return 4.9156E-01
    elif runNumber == 172318: return 4.8748E-01
    elif runNumber == 172319: return 4.8639E-01
    elif runNumber == 172320: return 4.8470E-01
    elif runNumber == 172321: return 4.8695E-01
    elif runNumber == 172322: return 4.8518E-01
    elif runNumber == 172323: return 4.8222E-01
    elif runNumber == 172324: return 4.7871E-01
    elif runNumber == 172325: return 4.7901E-01
    elif runNumber == 172326: return 4.7430E-01
    elif runNumber == 172327: return 4.7661E-01
    elif runNumber == 172328: return 4.7327E-01
    elif runNumber == 172329: return 4.7402E-01
    elif runNumber == 172330: return 4.6034E-01
    elif runNumber == 172331: return 4.6450E-01
    elif runNumber == 172332: return 4.5662E-01
    elif runNumber == 172333: return 4.5197E-01
    elif runNumber == 172334: return 4.4976E-01
    elif runNumber == 172335: return 4.4507E-01
    elif runNumber == 172336: return 4.3514E-01
    elif runNumber == 172337: return 4.3315E-01
    elif runNumber == 172338: return 4.2569E-01
    elif runNumber == 172339: return 4.1644E-01
    elif runNumber == 172340: return 4.0760E-01
    elif runNumber == 172341: return 4.8161E-01
    elif runNumber == 172342: return 4.9023E-01
    elif runNumber == 172343: return 4.9522E-01
    elif runNumber == 172344: return 4.9624E-01
    elif runNumber == 172345: return 4.9525E-01
    elif runNumber == 172346: return 4.9397E-01
    elif runNumber == 172347: return 5.0061E-01
    elif runNumber == 172348: return 4.8721E-01
    elif runNumber == 172349: return 4.8815E-01
    elif runNumber == 172350: return 4.8438E-01
    elif runNumber == 172351: return 4.8796E-01
    elif runNumber == 172352: return 4.8616E-01
    elif runNumber == 172353: return 4.8823E-01
    elif runNumber == 172354: return 4.8028E-01
    elif runNumber == 172355: return 4.8005E-01
    elif runNumber == 172356: return 4.7057E-01
    elif runNumber == 172357: return 4.7389E-01
    elif runNumber == 172358: return 4.6652E-01
    elif runNumber == 172359: return 4.6722E-01
    elif runNumber == 172360: return 4.6176E-01
    elif runNumber == 172361: return 4.6021E-01
    elif runNumber == 172362: return 4.5441E-01
    elif runNumber == 172363: return 4.4410E-01
    elif runNumber == 172364: return 4.3972E-01
    elif runNumber == 172365: return 4.3265E-01
    elif runNumber == 172366: return 4.2408E-01
    elif runNumber == 172367: return 4.1898E-01
    elif runNumber == 172368: return 4.1006E-01
    elif runNumber == 172369: return 4.9284E-01
    elif runNumber == 172370: return 4.9615E-01
    elif runNumber == 172371: return 5.0391E-01
    elif runNumber == 172372: return 5.0054E-01
    elif runNumber == 172373: return 5.0178E-01
    elif runNumber == 172374: return 4.9809E-01
    elif runNumber == 172375: return 4.9939E-01
    elif runNumber == 172376: return 4.9433E-01
    elif runNumber == 172377: return 4.9351E-01
    elif runNumber == 172378: return 4.8970E-01
    elif runNumber == 172379: return 4.9231E-01
    elif runNumber == 172380: return 4.8820E-01
    elif runNumber == 172381: return 4.9425E-01
    elif runNumber == 172382: return 4.8405E-01
    elif runNumber == 172383: return 4.8726E-01
    elif runNumber == 172384: return 4.8099E-01
    elif runNumber == 172385: return 4.8195E-01
    elif runNumber == 172386: return 4.8271E-01
    elif runNumber == 172387: return 4.7306E-01
    elif runNumber == 172388: return 4.7223E-01
    elif runNumber == 172389: return 4.6608E-01
    elif runNumber == 172390: return 4.6106E-01
    elif runNumber == 172391: return 4.6164E-01
    elif runNumber == 172392: return 4.5558E-01
    elif runNumber == 172393: return 4.4850E-01
    elif runNumber == 172394: return 4.4469E-01
    elif runNumber == 172395: return 4.3594E-01
    elif runNumber == 172396: return 4.3211E-01
    elif runNumber == 172397: return 4.1760E-01
    elif runNumber == 172398: return 4.0976E-01
    elif runNumber == 175911: return 0.37485
    elif runNumber == 175912: return 0.37911
    elif runNumber == 175913: return 0.37779
    elif runNumber == 175914: return 0.38527
    elif runNumber == 175915: return 0.38048
    elif runNumber == 175916: return 0.3867
    elif runNumber == 175917: return 0.38159
    elif runNumber == 175918: return 0.39412
    elif runNumber == 175919: return 0.38396
    elif runNumber == 175920: return 0.39392
    elif runNumber == 175921: return 0.3919
    elif runNumber == 175922: return 0.39165
    elif runNumber == 175923: return 0.38898
    elif runNumber == 175924: return 0.39751
    return 1.0


def getRPVLoopCorrectedMasses(treeMStop, treeMGluino):
    if (treeMStop, treeMGluino) in rpvMassLookup:
        return rpvMassLookup[(treeMStop, treeMGluino)]
    else: return "None"

rpvMassLookup = {
    (700, 652): [775.25655115, 779.425385083],
    (600, 304): [658.421193384, 394.50485412],
    (900, 826): [972.533922425, 965.750928285],
    (800, 391): [850.921125641, 496.137740325],
    (100, 391): [261.741728867, 481.134886543],
    (500, 304): [566.778226332, 393.3552436],
    (400, 652): [501.581706089, 769.375534884],
    (0, 304): [230.718200637, 383.033985294],
    (700, 826): [784.806568429, 959.880363061],
    (800, 565): [860.189227676, 688.385201899],
    (700, 739): [780.50326395, 870.527875273],
    (600, 217): [654.853163667, 291.933975859],
    (0, 217): [226.239631784, 285.280769128],
    (700, 217): [749.503531347, 292.596350222],
    (500, 826): [598.267362598, 952.373987871],
    (1000, 565): [1049.93139672, 691.326105787],
    (100, 826): [255.62365414, 936.519743328],
    (100, 217): [252.586199012, 286.169081422],
    (800, 652): [866.136456681, 781.587472439],
    (100, 913): [246.446399235, 1023.2326685],
    (900, 913): [977.593474488, 1054.75640392],
    (0, 391): [234.194611285, 479.987358236],
    (800, 826): [878.788142716, 963.141914272],
    (300, 1000): [414.113738881, 1119.85999296],
    (300, 391): [402.577120377, 487.78959093],
    (600, 826): [691.151644387, 955.776560128],
    (1000, 304): [1041.21817939, 397.76270706],
    (300, 913): [416.444870691, 1033.18362984],
    (1000, 391): [1043.4230928, 498.042864538],
    (900, 739): [965.32776156, 875.342292624],
    (100, 478): [264.603994871, 575.780458555],
    (900, 304): [944.120751207, 397.089776604],
    (0, 652): [233.03077594, 757.191851376],
    (800, 478): [855.077837469, 593.334356527],
    (200, 304): [319.628555395, 388.095879977],
    (1000, 1000): [1076.73252773, 1145.43963652],
    (100, 304): [257.566958121, 385.397087115],
    (300, 304): [396.833535188, 390.265592515],
    (500, 652): [591.479931632, 773.314164333],
    (300, 565): [411.635201415, 674.512516314],
    (200, 1000): [321.545089632, 1114.71174038],
    (300, 826): [417.232567928, 945.394199143],
    (0, 478): [236.038299793, 574.368974212],
    (300, 739): [416.605813925, 856.416870385],
    (900, 391): [946.758213101, 497.144384762],
    (500, 913): [600.368919508, 1040.59956479],
    (400, 1000): [507.511195516, 1124.10504928],
    (800, 304): [847.726442363, 396.337275373],
    (700, 565): [767.460708097, 686.597006533],
    (500, 565): [586.857612243, 681.912700022],
    (200, 913): [327.678523797, 1028.5382816],
    (1000, 478): [1046.31863133, 595.743136554],
    (200, 652): [333.437676957, 762.807272724],
    (800, 913): [882.954454109, 1051.58326149],
    (700, 1000): [791.128938095, 1134.74011278],
    (900, 1000): [981.640934956, 1142.3379086],
    (600, 652): [683.034191036, 776.824260914],
    (400, 826): [506.687051584, 948.997457395],
    (600, 478): [670.494894129, 590.191624194],
    (200, 391): [324.713973853, 484.184145819],
    (400, 913): [507.675706725, 1037.08632644],
    (500, 1000): [601.548272319, 1127.81318906],
    (600, 565): [677.662792106, 684.493985763],
    (400, 304): [480.296532971, 391.973960589],
    (500, 391): [574.34130255, 492.114329461],
    (700, 391): [756.262896879, 494.994604944],
    (1000, 652): [1054.26393334, 785.097702058],
    (500, 478): [581.348353141, 588.1709719],
    (0, 565): [235.79873314, 666.663585786],
    (300, 652): [414.706329679, 766.159538633],
    (0, 1000): [185.076688836, 1105.34454851],
    (600, 739): [687.491430956, 867.155772618],
    (800, 217): [845.434438494, 293.173844867],
    (800, 1000): [886.360822155, 1138.26547884],
    (600, 1000): [696.138633275, 1131.29105313],
    (100, 739): [261.624565867, 848.560407548],
    (400, 391): [487.179300897, 490.214954669],
    (400, 217): [472.667265838, 290.23833659],
    (200, 739): [333.407725169, 852.685113427],
    (1000, 913): [1071.73395142, 1057.36335718],
    (100, 1000): [233.482179734, 1108.79098976],
    (0, 739): [227.270527382, 846.179063198],
    (0, 913): [204.311274027, 1020.14726838],
    (100, 652): [264.876063026, 759.233694839],
    (1000, 217): [1039.64602589, 294.142324638],
    (900, 478): [950.209268886, 594.60871711],
    (200, 217): [313.965523271, 287.730394849],
    (600, 391): [663.350531203, 493.674063449],
    (500, 217): [562.172892873, 291.160589865],
    (1000, 739): [1059.27297524, 877.269856798],
    (800, 739): [873.646970549, 873.136002817],
    (200, 826): [331.553670286, 941.224875471],
    (200, 565): [331.859589835, 671.447801583],
    (100, 565): [265.761577559, 668.379393881],
    (900, 652): [959.569304281, 783.452857167],
    (400, 739): [504.631602367, 859.781842281],
    (300, 217): [390.179499183, 289.113785075],
    (700, 304): [752.330421954, 395.485092644],
    (0, 826): [217.962621262, 933.789886185],
    (900, 217): [942.238567273, 293.684789003],
    (1000, 826): [1064.84277378, 967.991511564],
    (600, 913): [694.039149767, 1044.00754125],
    (700, 913): [788.336848181, 1047.47890881],
    (400, 478): [492.824601847, 585.636922592],
    (700, 478): [761.33821256, 591.88131942],
    (400, 565): [497.629653024, 678.24014609],
    (300, 478): [407.547853065, 581.838819151],
    (200, 478): [328.873107152, 578.422684868],
    (500, 739): [595.284232058, 863.100172843],
    (900, 565): [954.487865253, 689.943893139],
}


#main()
