# Rewards the user with points for scrolling through the info section and typing in !startInfo and !endInfo

from chatbot.chat import CHAT

class INFO_REWARD(CHAT):
	"""
	Class gives users points for entering tutorial easter eggs
	"""

	def is_valid_message(self, message):
		"""
		Checks if the message is a valid tutorial reward claim
		:param message: The message to evaluate
		:return: True if the message is a valid tutorial reward claim, false otherwise.
		"""
		if message != "!startInfo" and message != "!endInfo":
			return False
		return True

	def handle_chat_message(self, username, message):
		"""
		Stores that the prize has been claimed by the user
		Then sends a confirmation to the user
		"""
		if message == "!startInfo":
			if self.Start_Reward_Already_Claimed(username, message) == True:
				self.connection.send_message(username + ", you have already claimed this reward.")
			else:
				self.Claim_Start_Reward(username)

		elif message == "!endInfo":
			if self.End_Reward_Already_Claimed(username, message) == True:
				self.connection.send_message(username + ", you have already claimed this reward.")
			else:
				self.Claim_End_Reward(username)
	
	def handle_unlocked_achievements(self,username):
		pass

	# -------------------- Private methods ---------------------- #
	def Claim_End_Reward(self, username):
		user = self.database.Get_User_By_Name(username)

		#Add 1 to the startReward Claims
		print("Claiming endInfo Reward")
		self.database.Add_End_Info_Claim_By_Name(username)
		self.database.Set_Points_For_User_By_Name(user[6] + 10, username)

	def Claim_Start_Reward(self, username):
		user = self.database.Get_User_By_Name(username)

		#Add 1 to the startReward Claims
		print("Claiming startInfo Reward")
		self.database.Add_Start_Info_Claim_By_Name(username)
		self.database.Set_Points_For_User_By_Name(user[6] + 10, username)

	def End_Reward_Already_Claimed(self, username, message):
		user = self.database.Get_User_By_Name(username)

		# 0 - not claimed, 1 - claimed
		endInfoClaimed = user[9]

		if endInfoClaimed == 1:
			return True
		else:
			return False

	def Start_Reward_Already_Claimed(self, username, message):
		user = self.database.Get_User_By_Name(username)

		# 0 - not claimed, 1 - claimed
		startInfoClaimed = user[8]

		if startInfoClaimed >= 1:
			return True
		else:
			return False
