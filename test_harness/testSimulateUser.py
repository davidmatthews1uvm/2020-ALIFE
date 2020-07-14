import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
import os
import sys

sys.path.insert(0, '..')


class TestSimulateUser(TestCase):

    # TODO set up test database
    def setUp(self):
        self.db = Mock(spec=DATABASE())

    # TODO delete test database
    def tearDown(self):
        del self.db

    # TODO format test to check database
    def test_Add_User(self):
        from chatbot.simulateUser import Add_User
        self.assertTrue(1 == 1)

    # TODO format test to check database
    def test_Handle_Command_From_User(self):
        from chatbot.simulateUser import Handle_Reinforcement_From_User
        self.assertTrue(1 == 1)

    # TODO format test to check database
    def test_Handle_Reinforcement_From_User(self):
        from chatbot.simulateUser import Handle_Reinforcement_From_User
        self.assertTrue(1 == 1)

    def test_Is_Command(self):
        from chatbot.simulateUser import Is_Command
        self.assertTrue(Is_Command("!test"))
        self.assertFalse(Is_Command("test"))

    def test_Is_Reinforcement(self):
        from chatbot.simulateUser import Is_Reinforcement
        self.assertTrue(Is_Reinforcement("ry"))
        self.assertTrue(Is_Reinforcement("rn"))
        self.assertFalse(Is_Reinforcement("dy"))
        self.assertFalse(Is_Reinforcement("og"))

    def test_Send_Command_Receipt_Response(self):
        from chatbot.simulateUser import Send_Command_Receipt_Response
        pass


if __name__ == '__main__':
    unittest.main()
