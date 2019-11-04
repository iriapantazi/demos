#! /usr/bin/python 

import unittest
from unittest.mock import Mock, patch
import nose
import requests_mock
from nose.tools import assert_is_not_none
from trainsLinesStatus import TFLAPI, HEADERS
import trainsLinesStatus as tls
from colorama import Fore
import requests

class Testing(unittest.TestCase):

    def test_getLineIDs(self):
        """
        Test the line IDs  
        """
        foo = {'id': 'foo', 'name': 'foo'}
        bar = {'id': 'bar', 'name': 'bar'}
        list_entries = [[foo, bar], [foo], [], '']
        # some additions here about the list [''],
        list_expect = ['foo,bar', 'foo', 'error', 'error']
        for entry, expect in zip(list_entries, list_expect):
            if type(entry) != list:
                continue
            elif len(entry) < 1:
                continue
            elif entry == '':
                continue
            elif entry == []:
                continue
            else:
                returned = tls.getLineIDs(entry)
                expected = expect
                self.assertEqual(returned, expected)            

    # how to use patches? 
    def test_getTubeLinesNames(self):
        """
        test_getTubeLines: mock testing of the url
        """
        mock = Mock()
        returned = mock.tls.getTubeLinesNames('dlr,tram')
        # test the output?

    def test_tubeStatusURL(self):
        """ 

        """
        in_list = ['foo', 'bar', '']
        for inp in in_list:
            if inp == '':
                continue
            returned = tls.tubeStatusURL(inp)
            expected = '{}/Line/{}/Status'.format(TFLAPI, inp)
            self.assertEqual(returned, expected)

    def test_getTubeStatus(self):
        mock = Mock()
        returned = mock.tls.getTubeStatus('foo,bar,baz')
        # I am missing something here. Help me pleaaaaase <3

    def test_printTubeNameStatusFormatted(self): 
        """
        Test the printed message and color.
        """
        list_status = ['Good Service', 'Minor Delays', 'Planned Closure', 'Part Closure', 'Part Suspended', 'bar']
        list_colors = [Fore.CYAN, Fore.RED, Fore.YELLOW, Fore.MAGENTA, Fore.GREEN, Fore.BLUE]
        for s, c in zip(list_status, list_colors):
            returned = tls.printTubeNameStatusFormatted('foo', s)  
            expected = 'Line foo reports '+c+s+'\033[0m'
            self.assertEqual(returned, expected)

    #def test_getTubeStatus(self):
    ##    """
    ##    Test  
    ##    """
    ##    returned = 
    ##    expected = 

if __name__=='__main__':
    unittest.main()
