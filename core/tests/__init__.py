"""
We are using django 1.4 so we need to load all the tests here
if we want to split them in different modules.
"""
import unittest


def suite():
    return unittest.TestLoader().discover('core.tests', pattern='*.py')
