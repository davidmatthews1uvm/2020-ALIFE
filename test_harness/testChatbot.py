import unittest
from unittest import TestCase
from unittest.mock import Mock, call
import os
import sys

sys.path.insert(0, '..')

file_name = "../credentials.credentials_tprTwo"
file = open(file_name, "r")
PASS = file.readline().rstrip()
CHAN = file.readline().rstrip()
file.close()


class TestChatbot(TestCase):

    def test_Command_From_User(self):
        from chatbot.chatbot import Command_From_User
        self.assertTrue(Command_From_User("!test"))
        self.assertFalse(Command_From_User(":test"))
        self.assertFalse(Command_From_User("test"))

    def test_Help_From_User(self):
        from chatbot.chatbot import Help_From_User
        self.assertTrue(Help_From_User("?\r\n"))
        self.assertFalse(Help_From_User("?"))

    def test_More_Help_From_User(self):
        from chatbot.chatbot import More_Help_From_User
        self.assertTrue(More_Help_From_User("?1\r\n"))
        self.assertTrue(More_Help_From_User("?2\r\n"))
        self.assertTrue(More_Help_From_User("?3\r\n"))
        self.assertTrue(More_Help_From_User("?4\r\n"))
        self.assertTrue(More_Help_From_User("?5\r\n"))
        self.assertTrue(More_Help_From_User("?6\r\n"))
        self.assertFalse(More_Help_From_User("?7\r\n"))

    def test_Stats_From_User(self):
        from chatbot.chatbot import Stats_From_User
        self.assertTrue(Stats_From_User("?s\r\n"))

    def test_Reinforcement_From_User(self):
        from chatbot.chatbot import Reinforcement_From_User
        self.assertTrue(Reinforcement_From_User("ry"))
        self.assertTrue(Reinforcement_From_User("sy"))
        self.assertTrue(Reinforcement_From_User("pn"))
        self.assertFalse(Reinforcement_From_User("zy"))
        self.assertFalse(Reinforcement_From_User("rz"))

    def test_chat(self):
        from chatbot.chatbot import chat, socket
        mockSock = Mock(spec=socket.socket())
        chat(mockSock, "cool guy")
        mockSock.send.assert_called_once_with("PRIVMSG #{} :{}".format(CHAN, "cool guy"))

    # TODO Make this work
    # @patch('chatbot.Initialize()')
    # def test_Initialize(self):
    #     from chatbot.chatbot import Initialize
    #     mockInit = Initialize()
    #     mockInit.send.assert_called_once_with("PASS {}\r\n".format("").encode("utf-8"))

    # TODO make mock chat call
    def test_Ping_From_Server(self):
        from chatbot.chatbot import Ping_From_Server
        self.assertTrue(Ping_From_Server("PING :tmi.twitch.tv\r\n"))
        self.assertFalse(Ping_From_Server("PONG :tmi.twitch.tv\r\n"))

    def test_Pong_Back(self):
        from chatbot.chatbot import Pong_Back, socket
        mockSock = Mock(spec=socket.socket())
        Pong_Back(mockSock)
        mockSock.send.assert_called_once_with("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

    # TODO make test functions for each if statement
    def test_Handle_Chat(self):
        pass

    """
    MOCK PATCHING METHODS REFERENCE CODE
    >>> class ProductionClass:
    ...     def method(self):
    ...         self.something(1, 2, 3)
    ...     def something(self, a, b, c):
    ...         pass
    ...
    >>> real = ProductionClass()
    >>> real.something = MagicMock()
    >>> real.method()
    >>> real.something.assert_called_once_with(1, 2, 3)
    """

    # # TODO convert chatbot to callable object to make this work
    # def test_Handle_Help_From_User(self):
    #     import chatbot.chatbot, socket
    #     mockSock = Mock(spec=socket.socket())
    #     testChatbot = chatbot()
    #     testChatbot.Write_Help_Message = MagicMock()
    #     testChatbot.Handle_Help_From_User(mockSock)
    #     testChatbot.Write_Help_Message.called_once_with(mockSock,
    #                                                     "This is the Twitch Plays Robotics project, ",
    #                                                     "where robots evolve to become more obedient.",
    #                                                     "Type ?stats or ?1 for more.")

    # # TODO convert chatbot to callable object to make this work
    # def test_Handle_More_Help_From_User_Level_1(self):
    #     import chatbot.chatbot, socket
    #     mockSock = Mock(spec=socket.socket())
    #     testChatbot = chatbot()
    #     testChatbot.Write_Help_Message = MagicMock()
    #     testChatbot.Handle_More_Help_From_User(mockSock, 1)
    #     testChatbot.Write_Help_Message.called_once_with(mockSock,
    #                                                     "You can increase the chance of a robot spawning ",
    #                                                     "by typing its color and 'y', as written at left. ",
    #                                                     "Type ?2 for more.")

    # # TODO convert chatbot to callable object to make this work
    # def test_Handle_More_Help_From_User_Level_2(self):
    #     import chatbot.chatbot, socket
    #     mockSock = Mock(spec=socket.socket())
    #     testChatbot = chatbot()
    #     testChatbot.Write_Help_Message = MagicMock()
    #     testChatbot.Handle_More_Help_From_User(mockSock, 2)
    #     testChatbot.Write_Help_Message.called_once_with(mockSock,
    #                                                     "You can increase the chance of a robot dying ",
    #                                                     "by typing its color and 'n', as written at left. ",
    #                                                     "Type ?3 for more.")

    # # TODO convert chatbot to callable object to make this work
    # def test_Handle_More_Help_From_User_Level_3(self):
    #     import chatbot.chatbot, socket
    #     mockSock = Mock(spec=socket.socket())
    #     testChatbot = chatbot()
    #     testChatbot.Write_Help_Message = MagicMock()
    #     testChatbot.Handle_More_Help_From_User(mockSock, 3)
    #     testChatbot.Write_Help_Message.called_once_with(mockSock,
    #                                                     "Alternatively, you can try to teach the robots ",
    #                                                     "new commands by typing ! and some words, such as !jump up",
    #                                                     "Type ?4 for more.")

    # # TODO convert chatbot to callable object to make this work
    # def test_Handle_More_Help_From_User_Level_4(self):
    #     import chatbot.chatbot, socket
    #     mockSock = Mock(spec=socket.socket())
    #     testChatbot = chatbot()
    #     testChatbot.Write_Help_Message = MagicMock()
    #     testChatbot.Handle_More_Help_From_User(mockSock, 4)
    #     testChatbot.Write_Help_Message.called_once_with(mockSock,
    #                                                     "Alternatively, you can try to teach the robots ",
    #                                                     "new commands by typing ! and some words, such as !jump up",
    #                                                     "Type ?5 for more.")

    # # TODO convert chatbot to callable object to make this work
    # def test_Handle_More_Help_From_User_Level_5(self):
    #     import chatbot.chatbot, socket
    #     mockSock = Mock(spec=socket.socket())
    #     testChatbot = chatbot()
    #     testChatbot.Write_Help_Message = MagicMock()
    #     testChatbot.Handle_More_Help_From_User(mockSock, 5)
    #     testChatbot.Write_Help_Message.called_once_with(mockSock,
    #                                                     "Alternatively, you can try to teach the robots ",
    #                                                     "new commands by typing ! and some words, such as !jump up",
    #                                                     "Type ?6 for more.")

    # # TODO convert chatbot to callable object to make this work
    # def test_Handle_More_Help_From_User_Level_6(self):
    #     import chatbot.chatbot, socket
    #     mockSock = Mock(spec=socket.socket())
    #     testChatbot = chatbot()
    #     testChatbot.Write_Help_Message = MagicMock()
    #     testChatbot.Handle_More_Help_From_User(mockSock, 6)
    #     testChatbot.Write_Help_Message.called_once_with(mockSock,
    #                                                     "Alternatively, you can try to teach the robots ",
    #                                                     "new commands by typing ! and some words, such as !jump up",
    #                                                     "")

    """
    MOCK DATABASE CURSOR REFERENCE CODE
    >>> mock = Mock()
    >>> cursor = mock.connection.cursor.return_value
    >>> cursor.execute.return_value = ['foo']
    >>> mock.connection.cursor().execute("SELECT 1")
    ['foo']
    >>> expected = call.connection.cursor().execute("SELECT 1").call_list()
    >>> mock.mock_calls
    [call.connection.cursor(), call.connection.cursor().execute('SELECT 1')]
    >>> mock.mock_calls == expected
    True
    """

    # # TODO complete this test
    # def test_Handle_Stats_From_User(self):
    #     from database.database import DATABASE
    #     mockDB = Mock(spec=DATABASE())
    #     mockCursor = mockDB.connection.cursor.return_value
    #     mockCursor.execute.return_value = [1]

    # TODO
    def test_Handle_Command_From_User(self):
        pass

    # TODO
    def test_Handle_Reinforcement_From_User(self):
        pass

    # TODO
    def test_Handle_User(self):
        pass

    def test_Is_Positive_Reinforcement(self):
        from chatbot.chatbot import Is_Positive_Reinforcement
        self.assertTrue(Is_Positive_Reinforcement('y'))
        self.assertFalse(Is_Positive_Reinforcement('n'))
        self.assertFalse(Is_Positive_Reinforcement('yo'))
        self.assertFalse(Is_Positive_Reinforcement('x'))

    # TODO fix formatting of test to make it more flexible
    def test_Send_Command_Receipt_Response(self):
        from chatbot.chatbot import Send_Command_Receipt_Response, socket
        mockSock = Mock(spec=socket.socket())
        Send_Command_Receipt_Response(mockSock, "coolguy")
        mockSock.send.assert_called_once_with(("PRIVMSG {} :Thanks @coolguy. " +
                                               "Your command will be sent to the robots shortly.\r\n").format(CHAN).encode("utf-8"))

    def test_Send_Negative_Reinforcement_Response(self):
        from chatbot.chatbot import Send_Negative_Reinforcement_Response, socket
        import constants as c
        mockSock = Mock(spec=socket.socket())
        testUsername = "coolguy"
        testColor = "r"
        Send_Negative_Reinforcement_Response(mockSock, testUsername, testColor)
        testMessage = ("@{0} just scolded the {1} bot.\r\n").format(testUsername, c.colorNameDict[testColor])
        testMessage = ("PRIVMSG {} :" + testMessage).format(CHAN)
        mockSock.send.assert_called_once_with(testMessage.encode("utf-8"))

    def test_Send_New_User_Message(self):
        from chatbot.chatbot import Send_New_User_Message, socket
        mockSock = Mock(spec=socket.socket())
        testUsername = "coolguy"
        Send_New_User_Message(mockSock, testUsername)
        testMessage = ("Welcome to TPR, @{}!\r\n").format(testUsername)
        testMessage = ("PRIVMSG {} :" + testMessage).format(CHAN)
        mockSock.send.assert_called_once_with(testMessage.encode("utf-8"))

    def test_Send_NotFound_Response(self):
        from chatbot.chatbot import Send_NotFound_Response, socket
        mockSock = Mock(spec=socket.socket())
        testUsername = "coolguy"
        Send_NotFound_Response(mockSock, testUsername)
        testMessage = ("@{}, a robot with that color does not exist or has not been shown yet.\r\n").format(testUsername)
        testMessage = ("PRIVMSG {} :" + testMessage).format(CHAN)
        mockSock.send.assert_called_once_with(testMessage.encode("utf-8"))

    def test_Send_Positive_Reinforcement_Response(self):
        from chatbot.chatbot import Send_Positive_Reinforcement_Response, socket
        import constants as c
        mockSock = Mock(spec=socket.socket())
        testUsername = "coolguy"
        testColor = "r"
        Send_Positive_Reinforcement_Response(mockSock, testUsername, testColor)
        testMessage = ("@{0} just rewarded the {1} bot.\r\n").format(testUsername, c.colorNameDict[testColor])
        testMessage = ("PRIVMSG {} :" + testMessage).format(CHAN)
        mockSock.send.assert_called_once_with(testMessage.encode("utf-8"))

    def test_Send_Returning_User_Message(self):
        from chatbot.chatbot import Send_Returning_User_Message, socket
        mockSock = Mock(spec=socket.socket())
        testUsername = "coolguy"
        Send_Returning_User_Message(mockSock, testUsername)
        testMessage = ("Welcome back, @{}!\r\n").format(testUsername)
        testMessage = ("PRIVMSG {} :" + testMessage).format(CHAN)
        mockSock.send.assert_called_once_with(testMessage.encode("utf-8"))

    def test_Write_Help_Message(self):
        from chatbot.chatbot import Write_Help_Message, socket
        mockSock = Mock(spec=socket.socket())
        Write_Help_Message(mockSock, "veni! ", "vidi! ", "vici!")
        expectedMockCalls = [call(("PRIVMSG {} :veni! vidi! \r\n").format(CHAN).encode("utf-8")),
                             call(("PRIVMSG {} :vici!\r\n").format(CHAN).encode("utf-8"))]
        self.assertListEqual(mockSock.send.call_args_list, expectedMockCalls)

if __name__ == '__main__':
    unittest.main()
