import numpy as np
import re
import wfdb

class test_rdann():

    # Test 1 - Annotation file 100.atr
    # Target file created with: rdann -r sampledata/100 -a atr > anntarget1
    def test_1(self):

        # Read data using WFDB python package
        annotation = wfdb.rdann('sampledata/100', 'atr')

        
        # This is not the fault of the script. The annotation file specifies a
        # length 3
        annotation.aux[0] = '(N'
        # aux field with a null written after '(N' which the script correctly picks up. I am just
        # getting rid of the null in this unit test to compare with the regexp output below which has
        # no null to detect in the output text file of rdann.

        # Target data from WFDB software package
        lines = tuple(open('tests/targetoutputdata/anntarget1', 'r'))
        nannot = len(lines)

        Ttime = [None] * nannot
        Tannsamp = np.empty(nannot, dtype='object')
        Tanntype = [None] * nannot
        Tsubtype = np.empty(nannot, dtype='object')
        Tchan = np.empty(nannot, dtype='object')
        Tnum = np.empty(nannot, dtype='object')
        Taux = [None] * nannot

        RXannot = re.compile(
            '[ \t]*(?P<time>[\[\]\w\.:]+) +(?P<annsamp>\d+) +(?P<anntype>.) +(?P<subtype>\d+) +(?P<chan>\d+) +(?P<num>\d+)\t?(?P<aux>.*)')

        for i in range(0, nannot):
            Ttime[i], Tannsamp[i], Tanntype[i], Tsubtype[i], Tchan[
                i], Tnum[i], Taux[i] = RXannot.findall(lines[i])[0]

        # Convert objects into integers
        Tannsamp = Tannsamp.astype('int')
        Tnum = Tnum.astype('int')
        Tsubtype = Tsubtype.astype('int')
        Tchan = Tchan.astype('int')

        # Compare
        comp = [np.array_equal(annotation.annsamp, Tannsamp), 
                np.array_equal(annotation.anntype, Tanntype), 
                np.array_equal(annotation.subtype, Tsubtype), 
                np.array_equal(annotation.chan, Tchan), 
                np.array_equal(annotation.num, Tnum), 
                annotation.aux == Taux]

        # Test file streaming
        pbannotation = wfdb.rdann('100', 'atr', pbdir = 'mitdb')
        pbannotation.aux[0] = '(N'
        
        # Test file writing
        annotation.wrann()
        annotationwrite = wfdb.rdann('100', 'atr')

        assert (comp == [True] * 6)
        assert annotation.__eq__(pbannotation)
        assert annotation.__eq__(annotationwrite)

    # Test 2 - Annotation file 12726.anI with many aux strings.
    # Target file created with: rdann -r sampledata/100 -a atr > anntarget2
    def test_2(self):

        # Read data from WFDB python package
        annotation = wfdb.rdann('sampledata/12726', 'anI')

        # Target data from WFDB software package
        lines = tuple(open('tests/targetoutputdata/anntarget2', 'r'))
        nannot = len(lines)

        Ttime = [None] * nannot
        Tannsamp = np.empty(nannot, dtype='object')
        Tanntype = [None] * nannot
        Tsubtype = np.empty(nannot, dtype='object')
        Tchan = np.empty(nannot, dtype='object')
        Tnum = np.empty(nannot, dtype='object')
        Taux = [None] * nannot

        RXannot = re.compile(
            '[ \t]*(?P<time>[\[\]\w\.:]+) +(?P<annsamp>\d+) +(?P<anntype>.) +(?P<subtype>\d+) +(?P<chan>\d+) +(?P<num>\d+)\t?(?P<aux>.*)')

        for i in range(0, nannot):
            Ttime[i], Tannsamp[i], Tanntype[i], Tsubtype[i], Tchan[
                i], Tnum[i], Taux[i] = RXannot.findall(lines[i])[0]

        # Convert objects into integers
        Tannsamp = Tannsamp.astype('int')
        Tnum = Tnum.astype('int')
        Tsubtype = Tsubtype.astype('int')
        Tchan = Tchan.astype('int')

        # Compare
        comp = [np.array_equal(annotation.annsamp, Tannsamp), 
                np.array_equal(annotation.anntype, Tanntype), 
                np.array_equal(annotation.subtype, Tsubtype), 
                np.array_equal(annotation.chan, Tchan), 
                np.array_equal(annotation.num, Tnum), 
                annotation.aux == Taux]
        # Test file streaming
        pbannotation = wfdb.rdann('12726', 'anI', pbdir = 'prcp')

        # Test file writing
        annotation.wrann()
        annotationwrite = wfdb.rdann('12726', 'anI')

        assert (comp == [True] * 6)
        assert annotation.__eq__(pbannotation)
        assert annotation.__eq__(annotationwrite)
