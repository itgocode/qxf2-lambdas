"""
Unit tests for is_active method of work_anniversary
"""
import unittest, mock
import work_anniversary

class Test_work anniversary(unittest.TestCase):
    """
    Test class for work anniversary
    """
    
    def test_unit_is_active_employee(each_node):
        "Test the employee is active or not"
        each_node = {'node':{'isActive':'Y'}}
        result_flag = work_anniversary.is_active_employee(each_node)
        assert result_flag is True
        
    