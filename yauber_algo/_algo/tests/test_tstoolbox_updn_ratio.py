import unittest
from yauber_algo.errors import *


class RSITestCase(unittest.TestCase):
    def test_rsi(self):
        import yauber_algo.sanitychecks as sc
        from numpy import array, nan, inf
        import os
        import sys
        import pandas as pd
        import numpy as np

        from yauber_algo.algo import updn_ratio

        #
        # Function settings
        #
        algo = 'updn_ratio'
        func = updn_ratio

        with sc.SanityChecker(algo) as s:
            #
            # Check regular algorithm logic
            #
            s.check_regular(
                array([nan, .50, .50, .50, .50, .50, .50]),
                func,
                (
                    array([3, 3, 3, 3, 3, 3, 3]),
                    1
                ),
                suffix='no_change_means50'
            )

            s.check_regular(
                array([nan, .50, .50, .50, .50, .50, .50]),
                func,
                (
                    array([3, 3, 3, 3, 3, 3, 3]),
                    0
                ),
                suffix='period_zero',
                exception=YaUberAlgoArgumentError
            )

            s.check_regular(
                array([nan, .50, .50, .50, .50, .50, .50]),
                func,
                (
                    array([3, 3, 3, 3, 3, 3, 3]),
                    -1
                ),
                suffix='period_negative',
                exception=YaUberAlgoArgumentError
            )

            s.check_regular(
                array([nan, .50, 1.00, 0, .50, .50, .50]),
                func,
                (
                    array([3, 3, 4, 3, 3, 3, 3]),
                    1
                ),
                suffix='up_down'
            )

            s.check_regular(
                # result[i] = ((upcnt+dncnt*-1) / (dncnt + upcnt + medcnt) + 1) / 2.0
                array([nan, nan, nan, ((2 + 0*-1) / 3 + 1)/2.0,  ((2 + 1*-1) / 3 + 1)/2.0, ((1 + 1*-1) / 3 + 1)/2.0, ((0 + 1*-1) / 3 + 1)/2.0]),
                func,
                (
                    array([3, 3, 4, 5, 3, 3, 3]),
                    3
                ),
                suffix='up_averaging'
            )

            s.check_regular(
                array([nan, nan, nan, 0.83333333, nan, nan, .50]),
                func,
                (
                    array([3, 3, 4, 5, nan, 3, 3]),
                    3
                ),
                suffix='nan_skipped'
            )


            s.check_regular(
                array([nan, nan, nan, 1.00, nan, nan, .50]),
                func,
                (
                    array([nan, 3, 4, 5, nan, 3, 3]),
                    3
                ),
                suffix='nan_old_excluded'
            )

            s.check_regular(
                array([nan, nan, nan, 1.00, nan, nan, .50]),
                func,
                (
                    array([nan, nan, 4, 5, nan, 3, 3]),
                    3
                ),
                suffix='nan_old_excluded2'
            )

            s.check_regular(
                array([nan, nan, nan, 0, nan, nan, .50]),
                func,
                (
                    array([nan, nan, 6, 5, nan, 3, 3]),
                    3
                ),
                suffix='nan_old_excluded2_dn'
            )

            s.check_naninf(
                array([nan, nan, nan, 0, nan, nan, .50]),
                func,
                (
                    array([nan, inf, 6, 5, nan, 3, 3]),
                    3
                ),
                suffix='nan_old_excluded2_dn'
            )

            s.check_series(
                pd.Series(array([nan, .50, .50, .50, .50, .50, .50])),
                func,
                (
                    pd.Series(array([3, 3, 3, 3, 3, 3, 3])),
                    1
                ),
                suffix=''
            )

            s.check_dtype_float(
                array([nan, .50, 1.00, 0, .50, .50, .50], dtype=float),
                func,
                (
                    array([3, 3, 4, 3, 3, 3, 3], dtype=float),
                    1
                ),
                suffix=''
            )

            s.check_dtype_int(
                array([nan, .50, 1.00, 0, .50, .50, .50], dtype=float),
                func,
                (
                    array([3, 3, 4, 3, 3, 3, 3], dtype=np.int32),
                    1
                ),
                suffix=''
            )

            s.check_dtype_bool(
                array([nan, .50, 1.00, 0, .50, .50, .50], dtype=float),
                func,
                (
                    array([0, 1, 0, 1, 1, 1, 1], dtype=np.bool),
                    1
                ),
                suffix='',
                exception=YaUberAlgoDtypeNotSupportedError
            )

            s.check_dtype_object(
                func,
                (
                    array([0, 1, 0, 1, 1, 1, 1], dtype=np.object),
                    1
                ),
                suffix='',
            )

            s.check_futref(5, 1,
                           func,
                           (
                               np.random.random(1000),
                               15
                           ),
                           )

            s.check_window_consistency(5, 1,
                                       func,
                                       (
                                           np.random.random(1000),
                                           15
                                       ),
                                       )

