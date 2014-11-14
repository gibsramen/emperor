#!/usr/bin/env python
# File created on 16 Apr 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "0.9.5-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from unittest import TestCase, main

from numpy import array
from numpy.testing import assert_almost_equal

from emperor.qiime_backports.parse import parse_classic_otu_table
from emperor.util import EmperorUnsupportedComputation
from emperor.biplots import extract_taxa_data, preprocess_otu_table


class TopLevelTests(TestCase):
    
    def setUp(self):
        self.biplot_coords = array([[-0.0520990488006, -0.0108550868341,
            0.00118513950438, -0.0195647012451, -0.0437589801599,
            0.000848245309189, -0.0122035463608, 0.0288287964617,
            -4.84141986706e-09], [-0.00406501716894, -0.0300693128299,
            -0.090316974427, 0.0559730983008, -0.0597265944801, 0.0456519002902,
            -0.054142291901, 0.0668355273511, -4.84141986706e-09],[
            0.0965087039672, -0.0164113801126, 0.0168583314836, 0.0103732287638,
            -0.0225710882818, 0.0283857610935, 3.22664794516e-05,
            0.0290430321474, -4.84141986706e-09], [0.126316230269,
            0.0263889076329, 0.0330227792131, 0.0885396607535, -0.0372547601153,
            0.0638622448577, -0.0224927101495, 0.0902626098256,
            -4.84141986706e-09], [-0.0672105325806, 0.0105941468738,
            -0.00527647509456, -0.0131631383518, 0.0315560857565,
            -0.0199787562498, 0.00815726904809, -0.0175931838803,
            -4.84141986706e-09], [0.118424097634, -0.00197525147278,
            -0.0399274159763, 0.0211233039391, -0.124633799325, 0.0133749785777,
            -0.0384382665152, -0.0584384149046, -4.84141986706e-09],
            [0.228820399536, -0.130142097093, -0.287149447883, 0.0864498846421,
            0.0442951919304, 0.20604260722, 0.0310003571386, 0.0719920436501,
            -4.84141986706e-09], [-0.000909430629502, 0.0116559690557,
            -0.049810186364, 0.0452278786773, -0.12933257558, -0.0214449951683,
            -0.0693407019638, -0.062534332665, -4.84141986706e-09]])

        self.otu_table = array([[0.02739726, 0.04697987, 0.02, 0.04697987, 0.01,
            0.02027027, 0.01360544, 0.01342282, 0.02666667], [0.00684932,
            0.02013423, 0.02, 0.00671141,  0., 0.00675676, 0., 0., 0.], [
            0.14383562, 0.27516779, 0.65333333, 0.52348993, 0.38926174,
            0.69594595, 0.28571429, 0.0738255, 0.19333333], [0., 0.02013423,
            0.03333333, 0.01342282, 0., 0.0472973, 0., 0., 0.], [0.78767123,
            0.45637584, 0.22, 0.39597315, 0.41610738, 0.20945946, 0.70068027,
            0.89932886, 0.77333333], [0.,0.02013423, 0.01333333, 0.00671141,
            0.03355705, 0.00675676, 0., 0., 0.],[0., 0., 0.01333333, 0., 0., 0.,
            0., 0., 0.], [0.03424658, 0.16107383, 0.02666667, 0.00671141,
            0.14765101, 0.01351351, 0., 0.01342282, 0.00666667]])

        self.lineages = ['Root;k__Bacteria;Other',
            'Root;k__Bacteria;p__Actinobacteria', 
            'Root;k__Bacteria;p__Bacteroidetes',
            'Root;k__Bacteria;p__Deferribacteres',
            'Root;k__Bacteria;p__Firmicutes',
            'Root;k__Bacteria;p__Proteobacteria','Root;k__Bacteria;p__TM7',
            'Root;k__Bacteria;p__Tenericutes']

        self.prevalence = array([0.04445514, 0.00972396, 0.6646394, 0.02081361,
            1., 0.01385989, 0., 0.08185147])
        self.otu_sample_ids = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354',
            'PC.593', 'PC.355', 'PC.607', 'PC.634']
        self.coords = COORDS
        self.coords_header = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354',
            'PC.593', 'PC.355', 'PC.607', 'PC.634']

        # data used to test a case where an exception should be raised
        self.otu_table_broken = array([[0.02739726, 0.04697987, 0.02,
            0.04697987, 0.01, 0.02027027, 0.01360544, 0.01342282, 0.02666667]])
        self.lineages_broken = ['Root;k__Bacteria']

    def test_filter_taxa(self):
        """Check the appropriate number of elements are extracted"""
        # test the simple case where you want to retain 5 taxonomic groups
        o_coords, o_table, o_lineages, o_prevalence = extract_taxa_data(
            self.biplot_coords, self.otu_table, self.lineages,self.prevalence,3)

        assert_almost_equal(o_coords, array([[-0.0672105325806, 0.0105941468738,
            -0.00527647509456, -0.0131631383518, 0.0315560857565,
            -0.0199787562498, 0.00815726904809, -0.0175931838803,
            -4.84141986706e-09],[0.0965087039672, -0.0164113801126,
            0.0168583314836, 0.0103732287638, -0.0225710882818, 0.0283857610935,
            3.22664794516e-05, 0.0290430321474, -4.84141986706e-09], [
            -0.000909430629502, 0.0116559690557, -0.049810186364,
            0.0452278786773, -0.12933257558, -0.0214449951683,
            -0.0693407019638, -0.062534332665, -4.84141986706e-09]]))
        assert_almost_equal(o_table, array([[0.78767123, 0.45637584, 0.22,
            0.39597315, 0.41610738, 0.20945946, 0.70068027, 0.89932886,
            0.77333333], [0.14383562, 0.27516779, 0.65333333, 0.52348993,
            0.38926174, 0.69594595, 0.28571429, 0.0738255, 0.19333333],
            [0.03424658, 0.16107383, 0.02666667, 0.00671141, 0.14765101,
            0.01351351, 0., 0.01342282, 0.00666667]]))
        self.assertEquals(o_lineages, ['Root;k__Bacteria;p__Firmicutes',
            'Root;k__Bacteria;p__Bacteroidetes',
            'Root;k__Bacteria;p__Tenericutes'])
        assert_almost_equal(o_prevalence,  array([ 1., 0.6646394, 0.08185147]))

        # test the case where all the elements are requested
        o_coords, o_table, o_lineages, o_prevalence = extract_taxa_data(
            self.biplot_coords,self.otu_table,self.lineages,self.prevalence,-1)

        assert_almost_equal(o_coords, array([[-6.72105326e-02, 1.05941469e-02,
            -5.27647509e-03, -1.31631384e-02, 3.15560858e-02, -1.99787562e-02,
            8.15726905e-03, -1.75931839e-02, -4.84141987e-09], [9.65087040e-02,
            -1.64113801e-02, 1.68583315e-02, 1.03732288e-02, -2.25710883e-02,
            2.83857611e-02, 3.22664795e-05, 2.90430321e-02, -4.84141987e-09],
            [-9.09430630e-04, 1.16559691e-02, -4.98101864e-02, 4.52278787e-02,
            -1.29332576e-01, -2.14449952e-02, -6.93407020e-02, -6.25343327e-02,
            -4.84141987e-09], [-5.20990488e-02, -1.08550868e-02, 1.18513950e-03,
            -1.95647012e-02, -4.37589802e-02, 8.48245309e-04, -1.22035464e-02,
            2.88287965e-02, -4.84141987e-09], [1.26316230e-01, 2.63889076e-02,
            3.30227792e-02, 8.85396608e-02, -3.72547601e-02, 6.38622449e-02,
            -2.24927101e-02, 9.02626098e-02, -4.84141987e-09], [1.18424098e-01,
            -1.97525147e-03, -3.99274160e-02, 2.11233039e-02, -1.24633799e-01,
            1.33749786e-02, -3.84382665e-02, -5.84384149e-02, -4.84141987e-09],
            [-4.06501717e-03, -3.00693128e-02, -9.03169744e-02, 5.59730983e-02,
            -5.97265945e-02, 4.56519003e-02, -5.41422919e-02, 6.68355274e-02,
            -4.84141987e-09], [2.28820400e-01, -1.30142097e-01, -2.87149448e-01,
            8.64498846e-02, 4.42951919e-02, 2.06042607e-01, 3.10003571e-02,
            7.19920437e-02, -4.84141987e-09]]))
        assert_almost_equal(o_table, array([[ 0.78767123, 0.45637584, 0.22,
            0.39597315, 0.41610738, 0.20945946, 0.70068027, 0.89932886,
            0.77333333], [0.14383562, 0.27516779, 0.65333333, 0.52348993,
            0.38926174, 0.69594595, 0.28571429, 0.0738255, 0.19333333],
            [0.03424658, 0.16107383, 0.02666667, 0.00671141, 0.14765101,
            0.01351351, 0., 0.01342282, 0.00666667], [0.02739726, 0.04697987,
            0.02, 0.04697987, 0.01, 0.02027027, 0.01360544, 0.01342282,
            0.02666667], [ 0., 0.02013423, 0.03333333, 0.01342282, 0.,
            0.0472973, 0., 0., 0.], [ 0. , 0.02013423, 0.01333333, 0.00671141,
            0.03355705, 0.00675676, 0., 0., 0.], [ 0.00684932, 0.02013423,
            0.02, 0.00671141, 0., 0.00675676, 0., 0., 0.], [ 0., 0., 0.01333333,
            0., 0., 0., 0., 0., 0.]]))
        self.assertEquals(o_lineages, ['Root;k__Bacteria;p__Firmicutes',
            'Root;k__Bacteria;p__Bacteroidetes',
            'Root;k__Bacteria;p__Tenericutes', 'Root;k__Bacteria;Other',
            'Root;k__Bacteria;p__Deferribacteres',
            'Root;k__Bacteria;p__Proteobacteria',
            'Root;k__Bacteria;p__Actinobacteria','Root;k__Bacteria;p__TM7'])
        assert_almost_equal(o_prevalence, array([ 1., 0.6646394, 0.08185147,
            0.04445514, 0.02081361, 0.01385989, 0.00972396, 0.]))

    def test_preprocess_otu_table(self):
        """Check the coords and otu table are processed correctly"""

        # processing only the four most prevalent taxa
        o_otu_coords, o_otu_table, o_otu_lineages, o_prevalence, lines =\
            preprocess_otu_table(self.otu_sample_ids, self.otu_table,
                self.lineages, self.coords, self.coords_header, 4)

        assert_almost_equal(o_otu_coords, array([[ -6.71083200e-02,
            1.05892642e-02, -5.26801821e-03, -1.31730322e-02, 3.15036935e-02,
            -1.99712144e-02, 8.14445313e-03, -1.76632227e-02, -4.84141987e-09],
            [ 9.65846961e-02, -1.64070839e-02, 1.68610695e-02, 1.03495979e-02,
            -2.26223522e-02, 2.83763737e-02, 1.76116225e-05, 2.89253284e-02,
            -4.84141987e-09], [-5.61881305e-04, 1.16341355e-02, -4.97196330e-02,
            4.51141625e-02, -1.29353935e-01, -2.14114921e-02, -6.92988035e-02,
            -6.27730937e-02, -4.84141987e-09], [-5.70985165e-02,
            -1.09278921e-02, 8.49830390e-04, -1.91550282e-02, -4.22122952e-02,
            7.75750297e-04, -1.18543093e-02, 3.31082777e-02, -4.84141987e-09]]))
        assert_almost_equal(o_otu_table, array([[ 0.78767123, 0.45637584, 0.22,
            0.39597315, 0.41610738, 0.20945946, 0.70068027, 0.89932886,
            0.77333333], [0.14383562, 0.27516779, 0.65333333, 0.52348993,
            0.38926174, 0.69594595, 0.28571429, 0.0738255, 0.19333333], [
            0.03424658, 0.16107383, 0.02666667, 0.00671141, 0.14765101,
            0.01351351, 0., 0.01342282, 0.00666667], [0.02739726, 0.04697987,
            0.02, 0.04697987, 0.01, 0.02027027, 0.01360544, 0.01342282,
            0.02666667]]))
        self.assertEquals(o_otu_lineages, ['Root;k__Bacteria;p__Firmicutes',
            'Root;k__Bacteria;p__Bacteroidetes',
            'Root;k__Bacteria;p__Tenericutes', 'Root;k__Bacteria;Other'])
        assert_almost_equal(o_prevalence, array([ 1., 0.66471926, 0.08193196,
            0.04374296]))
        self.assertEquals(lines, LINES)

        # tests for correct outputs of empty inputs
        o_otu_coords, o_otu_table, o_otu_lineages, o_prevalence, lines =\
            preprocess_otu_table([],[], [], self.coords, self.coords_header, 4)
        self.assertEquals(o_otu_coords, [])
        self.assertEquals(o_otu_table, [])
        self.assertEquals(o_otu_lineages, [])
        self.assertEquals(o_prevalence, [])
        self.assertEquals(lines, '')

    def test_preprocess_otu_table_exceptions(self):
        """Check the exceptions are raised appropriately"""
        # should raise an exception because the inputs contain a single row
        with self.assertRaises(EmperorUnsupportedComputation):
            o_otu_coords, o_otu_table, o_otu_lineages, o_prevalence, lines =\
                preprocess_otu_table(self.otu_sample_ids, self.otu_table_broken,
                self.lineages_broken, self.coords, self.coords_header, 4)

        # some inputs are completely wrong but should still fail because the
        # contingency table has one row only, hence scores cannot be computed
        with self.assertRaises(EmperorUnsupportedComputation):
            o_otu_coords, o_otu_table, o_otu_lineages, o_prevalence, lines =\
                preprocess_otu_table(self.otu_sample_ids, self.otu_table_broken,
                [[]], self.coords, self.coords_header, 4)
        with self.assertRaises(EmperorUnsupportedComputation):
            o_otu_coords, o_otu_table, o_otu_lineages, o_prevalence, lines =\
                preprocess_otu_table(self.otu_sample_ids, array([]),
                self.lineages_broken, self.coords, self.coords_header, 4)


OTU_TABLE = """Taxon\tPC.636\tPC.635\tPC.356\tPC.481\tPC.354\tPC.593\tPC.355\tPC.607\tPC.634
Root;k__Bacteria;Other\t0.0202702702703\t0.0469798657718\t0.0266666666667\t0.027397260274\t0.0134228187919\t0.0134228187919\t0.0136054421769\t0.0469798657718\t0.02
Root;k__Bacteria;p__Actinobacteria\t0.00675675675676\t0.00671140939597\t0.0\t0.00684931506849\t0.0\t0.0\t0.0\t0.0201342281879\t0.02
Root;k__Bacteria;p__Bacteroidetes\t0.695945945946\t0.523489932886\t0.193333333333\t0.143835616438\t0.0738255033557\t0.389261744966\t0.285714285714\t0.275167785235\t0.653333333333
Root;k__Bacteria;p__Deferribacteres\t0.0472972972973\t0.0134228187919\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0201342281879\t0.0333333333333
Root;k__Bacteria;p__Firmicutes\t0.209459459459\t0.395973154362\t0.773333333333\t0.787671232877\t0.89932885906\t0.41610738255\t0.700680272109\t0.456375838926\t0.22
Root;k__Bacteria;p__Proteobacteria\t0.00675675675676\t0.00671140939597\t0.0\t0.0\t0.0\t0.0335570469799\t0.0\t0.0201342281879\t0.0133333333333
Root;k__Bacteria;p__TM7\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0133333333333
Root;k__Bacteria;p__Tenericutes\t0.0135135135135\t0.00671140939597\t0.00666666666667\t0.0342465753425\t0.0134228187919\t0.147651006711\t0.0\t0.161073825503\t0.0266666666667
"""

COORDS = array([[-0.276542163845, -0.144964375408, 0.0666467344429, -0.0677109454288, 0.176070269506, 0.072969390136, -0.229889463523, -0.0465989416581, -4.84141986706e-09],
[-0.237661393984, 0.0460527772512, -0.138135814766, 0.159061025229, -0.247484698646, -0.115211468101, -0.112864033263, 0.0647940729676, -4.84141986706e-09],
[0.228820399536, -0.130142097093, -0.287149447883, 0.0864498846421, 0.0442951919304, 0.20604260722, 0.0310003571386, 0.0719920436501, -4.84141986706e-09],
[0.0422628480532, -0.0139681511889, 0.0635314615517, -0.346120552134, -0.127813807608, 0.0139350721063, 0.0300206887328, 0.140147849223, -4.84141986706e-09],
[0.280399117569, -0.0060128286014, 0.0234854344148, -0.0468109474823, -0.146624450094, 0.00566979124596, -0.0354299634191, -0.255785794275, -4.84141986706e-09],
[0.232872767451, 0.139788385269, 0.322871079774, 0.18334700682, 0.0204661596818, 0.0540589147147, -0.0366250872041, 0.0998235721267, -4.84141986706e-09],
[0.170517581885, -0.194113268955, -0.0308965283066, 0.0198086158783, 0.155100062794, -0.279923941712, 0.0576092515759, 0.0242481862127, -4.84141986706e-09],
[-0.0913299284215, 0.424147148265, -0.135627421345, -0.057519480907, 0.151363490722, -0.0253935675552, 0.0517306152066, -0.038738217609, -4.84141986706e-09],
[-0.349339228244, -0.120787589539, 0.115274502117, 0.0694953933826, -0.0253722182853, 0.067853201946, 0.244447634756, -0.0598827706386, -4.84141986706e-09]])

LINES = """#Taxon\tpc0\tpc1\tpc2\tpc3\tpc4\tpc5\tpc6\tpc7\tpc8
Root;k__Bacteria;p__Firmicutes\t-0.0671083199539\t0.010589264186\t-0.00526801821358\t-0.0131730321859\t0.0315036934893\t-0.0199712144464\t0.00814445312587\t-0.0176632227289\t-4.84141986706e-09
Root;k__Bacteria;p__Bacteroidetes\t0.0965846961434\t-0.0164070839162\t0.0168610695358\t0.010349597944\t-0.0226223521782\t0.0283763736987\t1.76116225444e-05\t0.0289253284365\t-4.84141986706e-09
Root;k__Bacteria;p__Tenericutes\t-0.000561881304886\t0.0116341354761\t-0.0497196329856\t0.0451141625418\t-0.129353934943\t-0.0214114921223\t-0.0692988035087\t-0.0627730937042\t-4.84141986706e-09
Root;k__Bacteria;Other\t-0.0570985164756\t-0.0109278921351\t0.00084983039019\t-0.0191550282339\t-0.0422122952074\t0.000775750296682\t-0.0118543093074\t0.0331082776958\t-4.84141986706e-09"""

if __name__ == "__main__":
    main()
