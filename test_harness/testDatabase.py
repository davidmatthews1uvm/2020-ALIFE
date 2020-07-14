import os
import sys
from unittest import TestCase
from unittest.mock import patch

sys.path.insert(0, '..')

from database.database import DATABASE


class TestDatabase(TestCase):
    testDb = DATABASE(dbFile="testDatabase.db")

    def setUp(self):
        self.testDb.Populate()

    def tearDown(self):
        self.testDb.Reset()

    def test_Add_Command_New(self):
        testCommand = "test"
        self.testDb.Add_Command(testCommand)
        executionString = "SELECT * FROM Commands WHERE command = '{}'".format(testCommand)
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        cmdList = [cmd for (cmd, date) in testQuery]
        dateList = [date for (cmd, date) in testQuery]
        self.assertEqual(len(cmdList), 1)
        self.assertEqual(len(dateList), 1)

    def test_Add_Command_Existing(self):
        executionString = "SELECT command FROM Commands ORDER BY command DESC LIMIT 1"
        self.testDb.cur.execute(executionString)
        testCommand = self.testDb.cur.fetchone()[0]
        self.testDb.Add_Command(testCommand)
        executionString = "SELECT * FROM Commands WHERE command = '{}'".format(testCommand)
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        cmdList = [cmd for (cmd, date) in testQuery]
        dateList = [date for (cmd, date) in testQuery]
        self.assertEqual(len(cmdList), 2)
        self.assertEqual(len(dateList), 2)

    def test_Add_Evaluation(self):
        testEval = (0, 'r', 'test')
        self.testDb.Add_Evaluation(*testEval)
        executionString = "SELECT * FROM Evaluations ORDER BY Id DESC LIMIT 1"
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchone()
        print(testQuery)
        robotId = testQuery[1]
        robotColor = testQuery[2]
        command = testQuery[3]
        self.assertEqual(robotId, 0)
        self.assertEqual(robotColor, 'r')
        self.assertEqual(command, 'test')

    # TODO make Id increment in reinforcements table to make this test work
    def test_Add_Reinforcement(self):
        testReinforce = (3, 2, 'n')
        self.testDb.Add_Reinforcement(*testReinforce)
        executionString = "SELECT * FROM Reinforcements ORDER BY Id DESC LIMIT 1"
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchone()
        evalId = testQuery[1]
        robotId = testQuery[2]
        reinforcement = testQuery[3]
        self.assertEqual(evalId, 3)
        self.assertEqual(robotId, 2)
        self.assertEqual(reinforcement, 'n')

    # TODO configure test with actual robot
    def test_Add_Robot(self):
        pass

    # TODO check vector encoding
    def test_Add_Unique_Command_New(self):
        testCommand = "'test'"
        self.testDb.Add_Unique_Command(testCommand)
        executionString = "SELECT * FROM UniqueCommands WHERE command = {}".format(testCommand)
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchone()
        command = testQuery[0]
        self.assertEqual(command, 'test')

    # TODO increment user Id for this to work
    def test_Add_User(self):
        testUser = "Joseph Joestar"
        self.testDb.Add_User(testUser)
        executionString = "SELECT * FROM Users ORDER BY Id DESC LIMIT 1"
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchone()
        user = testQuery[1]
        self.assertEqual(user, testUser)

    def test_Aggressor_Can_Kill_Defender_True(self):
        testRobotIds = (0, 1)
        self.assertTrue(self.testDb.Aggressor_Can_Kill_Defender(*testRobotIds))

    def test_Aggressor_Can_Kill_Defender_True(self):
        testRobotIds = (1, 2)
        self.assertFalse(self.testDb.Aggressor_Can_Kill_Defender(*testRobotIds))

    def test_Bot_Is_Dead_False(self):
        testRobotId = 0
        self.assertFalse(self.testDb.Bot_Is_Dead(testRobotId))

    def test_Bot_Is_Dead_True(self):
        testRobotId = 2
        self.assertTrue(self.testDb.Bot_Is_Dead(testRobotId))

    # TODO implement Get_Robot_Color_Index method in database.py
    def test_Color_Of_Bot(self):
        testRobotId = 0
        self.testDb.Color_Of_Bot(testRobotId)

    def test_Command_Avaliable_True(self):
        self.assertTrue(self.testDb.Command_Available())

    def test_Command_Avaliable_False(self):
        self.testDb.Reset()
        self.assertFalse(self.testDb.Command_Available())

    def test_Command_Is_New_True(self):
        self.assertTrue(self.testDb.Command_Is_New("test"))

    def test_Command_Is_New_False(self):
        self.assertFalse(self.testDb.Command_Is_New("run"))

    # TODO find a way to test this
    def test_Connect(self):
        pass

    @patch('database.database.DATABASE.Create_Tables')
    def test_Create(self, Mock_Create_Tables):
        self.testDb.Create()
        self.testDb.Create_Tables.assert_called_once_with()

    def test_Create_Tables(self):
        # Drop all tables
        executionString = "SELECT * FROM sqlite_master WHERE type = 'table'"
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        oldTableNames = [name for (table, name, *rest) in testQuery]
        [self.testDb.cur.execute("Drop Table {}".format(tableName)) for tableName in oldTableNames]
        # Recreate tables
        self.testDb.Create_Tables()
        # Assert tables were created
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        newTableNames = [name for (table, name, *rest) in testQuery]
        self.assertListEqual(newTableNames, oldTableNames)

    def test_Delete_Command_From_Queue(self):
        # Get old list of commands in Commands table
        executionString = "SELECT command FROM Commands"
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        oldCommands = [cmd for (cmd,) in testQuery]
        # Delete first command from Commands
        self.testDb.Delete_Command_From_Queue()
        # Get new list of commands in COmmands table
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        newCommands = [cmd for (cmd,) in testQuery]
        # Assert new list is one entry shorter
        self.assertEqual(len(oldCommands), len(newCommands)+1)

    # TODO
    def test_Delete_Data_Files(self):
        pass

    def test_Delete_Evaluation(self):
        # Get old list of evaluations in Evaluation table
        executionString = "SELECT Id FROM Evaluations"
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        oldEvalIds = [evalId for (evalId,) in testQuery]
        # Delete last evaluation from Evaluations
        self.testDb.Delete_Evaluation(2)
        # Get new list of evaluation in Evaluations table
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        newEvalIds = [evalId for (evalId,) in testQuery]
        # Assert new list is one entry shorter
        self.assertEqual(len(oldEvalIds), len(newEvalIds) + 1)

    def test_Delete_Evaluation_If_Non_Reinforced(self):
        import datetime
        # Add non-reinforced evaluation to Evaluations table
        Id = self.testDb.Get_Next_Available_Evaluation_ID()
        strng = 'INSERT INTO Evaluations VALUES (?,?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nonReEval = (str(Id), str(3), 'p', 'test', date)
        params = (nonReEval[0], nonReEval[1], nonReEval[2], nonReEval[3], nonReEval[4])
        self.testDb.cur.execute(strng, params)
        self.testDb.con.commit()
        # Get old list of evaluations
        executionString = "SELECT Id FROM Evaluations"
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        oldEvalIds = [evalId for (evalId,) in testQuery]
        # Delete non-reinforced entry
        self.testDb.Delete_Evaluation_If_Non_Reinforced(nonReEval[0])
        # Check if entry was deleted
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        newEvalIds = [evalId for (evalId,) in testQuery]
        self.assertEqual(len(oldEvalIds), len(newEvalIds) + 1)

    def test_Delete_Non_Reinforced_Evaluations(self):
        import datetime
        # Add non-reinforced evaluation to Evaluations table
        Id = self.testDb.Get_Next_Available_Evaluation_ID()
        strng = 'INSERT INTO Evaluations VALUES (?,?,?,?,?)'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nonReEval = (str(Id), str(3), 'p', 'test', date)
        params = (nonReEval[0], nonReEval[1], nonReEval[2], nonReEval[3], nonReEval[4])
        self.testDb.cur.execute(strng, params)
        self.testDb.con.commit()
        # Get old list of evaluations
        executionString = "SELECT Id FROM Evaluations"
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        oldEvalIds = [evalId for (evalId,) in testQuery]
        # Delete non-reinforced entry
        self.testDb.Delete_Non_Reinforced_Evaluations()
        # Check if entry was deleted
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        newEvalIds = [evalId for (evalId,) in testQuery]
        self.assertEqual(len(oldEvalIds), len(newEvalIds) + 1)

    def test_Delete_Old_And_Non_Reinforced_Evaluations(self):
        import datetime
        # Add old non-reinforced evaluation to Evaluations table
        Id = self.testDb.Get_Next_Available_Evaluation_ID()
        strng = 'INSERT INTO Evaluations VALUES (?,?,?,?,?)'
        date = (datetime.datetime.now()-datetime.timedelta(minutes=9)).strftime("%Y-%m-%d %H:%M:%S")
        nonReEval = (str(Id), str(3), 'p', 'test', date)
        params = (nonReEval[0], nonReEval[1], nonReEval[2], nonReEval[3], nonReEval[4])
        self.testDb.cur.execute(strng, params)
        self.testDb.con.commit()
        # Get old list of evaluations
        executionString = "SELECT Id FROM Evaluations"
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        oldEvalIds = [evalId for (evalId,) in testQuery]
        # Delete non-reinforced entry
        self.testDb.Delete_Old_And_Non_Reinforced_Evaluations()
        # Check if entry was deleted
        self.testDb.cur.execute(executionString)
        testQuery = self.testDb.cur.fetchall()
        newEvalIds = [evalId for (evalId,) in testQuery]
        self.assertEqual(len(oldEvalIds), len(newEvalIds) + 1)

    # TODO implement mock or patch to test this
    def test_Destroy(self):
        pass

    # TODO implement mock or patch to test this
    def test_Drop_Table(self):
        pass

    # TODO implement mock or patch to test this
    def test_Drop_Tables(self):
        pass

    def test_From_Evaluation_Record_Get_Id(self):
        testEval = (0, 1, 'r', 'walk', '2018-07-20 13:07:02')
        testId = self.testDb.From_Evaluation_Record_Get_Id(testEval)
        self.assertEqual(testId, testEval[0])

    def test_From_Evaluation_Record_Get_RobotId(self):
        testEval = (0, 1, 'r', 'walk', '2018-07-20 13:07:02')
        testRobotId = self.testDb.From_Evaluation_Record_Get_RobotId(testEval)
        self.assertEqual(testRobotId, testEval[1])

    def test_From_Evaluation_Record_Get_RobotColor(self):
        testEval = (0, 1, 'r', 'walk', '2018-07-20 13:07:02')
        testRobotColor = self.testDb.From_Evaluation_Record_Get_RobotColor(testEval)
        self.assertEqual(testRobotColor, testEval[2])

    def test_From_Evaluation_Record_Get_Command(self):
        testEval = (0, 1, 'r', 'walk', '2018-07-20 13:07:02')
        testId = self.testDb.From_Evaluation_Record_Get_Command(testEval)
        self.assertEqual(testId, testEval[3])

    def test_From_Evaluation_Record_Get_Date(self):
        testEval = (0, 1, 'r', 'walk', '2018-07-20 13:07:02')
        testDate = self.testDb.From_Evaluation_Record_Get_Date(testEval)
        self.assertEqual(testDate, testEval[4])

    def test_From_Reinforcement_Record_Get_Evaluation_Id(self):
        testReinforce = (0, 1, 2, 'n', '2018-7-20-13:11:49')
        testEvalId = self.testDb.From_Reinforcement_Record_Get_Evaluation_ID(testReinforce)
        self.assertEqual(testEvalId, testReinforce[1])

    def test_From_Reinforcement_Record_Get_Signal(self):
        testReinforce = (0, 1, 2, 'n', '2018-7-20-13:11:49')
        testSignal = self.testDb.From_Reinforcement_Record_Get_Signal(testReinforce)
        self.assertEqual(testSignal, testReinforce[3])

    def test_From_Reinforcement_Record_Get_Time(self):
        testReinforce = (0, 1, 2, 'n', '2018-7-20-13:11:49')
        testEvalTime = self.testDb.From_Reinforcement_Record_Get_Time(testReinforce)
        self.assertEqual(testEvalTime, testReinforce[4])

    def test_From_Robot_Record_Get_Id(self):
        testRobot = (2, 3, 1, '2018-07-20 13:17:38', 0)
        testId = self.testDb.From_Robot_Record_Get_ID(testRobot)
        self.assertEqual(testId, testRobot[0])

    def test_From_Robot_Record_Get_Color_Index(self):
        testRobot = (2, 3, 1, '2018-07-20 13:17:38', 0)
        testColorIndex = self.testDb.From_Robot_Record_Get_Color_Index(testRobot)
        self.assertEqual(testId, testRobot[1])

    def test_From_Robot_Record_Get_Parent_Id(self):
        testRobot = (2, 3, 1, '2018-07-20 13:17:38', 0)
        testParentId = self.testDb.From_Robot_Record_Get_Color_Index(testRobot)
        self.assertEqual(testId, testRobot[2])

    def test_From_Robot_Record_Get_Creation_Date(self):
        testRobot = (2, 3, 1, '2018-07-20 13:17:38', 0)
        testParentId = self.testDb.From_Robot_Record_Get_Creation_Date(testRobot)
        self.assertEqual(testId, testRobot[3])

    def test_From_Robot_Record_Get_Alive_Status(self):
        testRobot = (2, 3, 1, '2018-07-20 13:17:38', 0)
        testParentId = self.testDb.From_Robot_Record_Get_Alive_Status(testRobot)
        self.assertEqual(testId, testRobot[3])

    def test_From_UniqueCommand_Record_Get_String(self):
        testCommand = ('walk',)
        testCommandString = self.testDb.From_UniqueCommand_Record_Get_String(testCommand)
        self.assertEqual(testCommandString, testCommand[0])

    # TODO
    def test_Get_B_Index_For_Robot(self):
        pass

    # TODO
    def test_Get_B_Index_For_Robot_At_Time(self):
        pass

    # TODO find a way to test this
    def test_Get_Command_Encoding(self):
        # print(self.testDb.Get_Command_Encoding('jump'))
        pass

    def test_Get_Command_From_Queue(self):
        # Get first command in queue
        executionString = "SELECT * FROM Commands ORDER BY ROWID ASC LIMIT 1"
        self.testDb.cur.execute(executionString)
        row = self.testDb.cur.fetchone()
        testCommand = row[0]
        # Check if method fetches right command
        self.assertEqual(self.testDb.Get_Command_From_Queue(), testCommand)

    # TODO find a way to test this
    def test_Get_Command_Vector_Encoding(self):
        pass

    def test_Get_Commands(self):
        executionString = "SELECT * FROM Commands"
        self.testDb.cur.execute(executionString)
        cmdList = self.testDb.cur.fetchall()
        self.assertEqual(self.testDb.Get_Commands(), cmdList)

    # TODO
    def test_Get_Commands_Robot_Is_Most_Obedient_To(self):
        print(self.testDb.Get_Commands_Robot_Is_Most_Obedient_To(0))

    def test_Get_Commands_Robot_Is_Most_Obedient_To_At_Time(self):
        pass

    def test_Get_Evaluation_Id(self):
        pass

    def test_Get_Evaluation_Where_Id_Equals(self):
        pass

    def test_Get_Evaluations(self):
        pass

    def test_Get_Evaluations_Where_RobotId_Equals(self):



if __name__ == '__main__':
    unittest.main()
