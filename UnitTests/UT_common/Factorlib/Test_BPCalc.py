import numpy as np
from nose.tools import assert_almost_equal
from common.Factorlib.BPCalc import *



def test_BPCalc():
	assert_almost_equal (BPCalc('600230.SH', '20140808'), np.float64(0.597657183839), 4)