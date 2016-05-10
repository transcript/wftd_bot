import time, re, os, string, datetime, random
from slackclient import SlackClient


token = "xoxb-39315496967-YikEDFDmlfYxRt9kQCEIHgNV"
sc = SlackClient(token)

live_pom_channel = "C0FRR6J13"
bot_fight_channel = "G15EYCP7F"

greeting = "Hello!\nNice to meet you.  I wish I could do more... but I haven't been programmed yet."
WFTD_response = "I am at 0 WFTD, because I am a bot :slightly_frowning_face:"
#print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=greeting)

history = sc.api_call("channels.history", channel = live_pom_channel)

# databases
messages = []
users_list_mentions = {}
users_list_WFTD = {}

#for entry in message_parts:
#	messages.append(entry)

###### DEFINING FUNCTIONS FOR STATISTICS #############
def stats_WFTD(user):
	if os.path.isfile(user + ".csv") == False:
		return "Can't find file: " + str(user) + ".csv \nSorry, I don't have any data on you, user <@" + user + ">.  Strange..."
	else:
		user_db = open(user + ".csv", "r")
		WFTD_value = 0
		today_date = time.strftime('%d')
		month_date = time.strftime('%b')
		year_date = time.strftime('%Y')
		# read in the file:
		for line in user_db:
			splitline = line.split(", ")
			# 0=user, 1=WFTD, 2=time, 3=date, 4=month(short), 5=year
			if splitline[3] == today_date:
				if splitline[4] == month_date:
					if splitline[5] == year_date:
						WFTD_value += int(splitline[1])
		user_db.close()
		return "<@" + user + "> has written " + str(WFTD_value) + " words so far today." 

# this one calls any day, useful for yesterday's total
def stats_any_WFTD(user, yesterday):
	if os.path.isfile(user + ".csv") == False:
		return "Sorry, I don't have any data on you.  Strange..."
	else:
		user_db = open(user + ".csv", "r")
		WFTD_value = 0
		today_date = yesterday.strftime('%d')
		month_date = yesterday.strftime('%b')
		year_date = time.strftime('%Y')
		# read in the file:
		for line in user_db:
			splitline = line.split(", ")
			# 0=user, 1=WFTD, 2=time, 3=date, 4=month(short), 5=year
			if splitline[3] == today_date:
				if splitline[4] == month_date:
					if splitline[5] == year_date:
						WFTD_value += int(splitline[1])
		user_db.close()
		return "<@" + user + "> wrote " + str(WFTD_value) + " words on" 
	
# this one does words for the month	
def stats_WFTM(user):
	if os.path.isfile(user + ".csv") == False:
		return "Sorry, I don't have any data on you.  Strange..."
	else:
		user_db = open(user + ".csv", "r")
		WFTM_value = 0
		month_date = time.strftime('%b')
		year_date = time.strftime('%Y')
		# read in the file:
		for line in user_db:
			splitline = line.split(", ")
			# 0=user, 1=WFTD, 2=time, 3=date, 4=month(short), 5=year
			if splitline[4] == month_date:
				if splitline[5] == year_date:
					WFTM_value += int(splitline[1])
		user_db.close()
		return ("<@" + user + "> has written " + str(WFTM_value) + " words so far in the month of " + time.strftime('%B') + ".", WFTM_value)

# this one does words for the entire year!		
def stats_WFTY(user):
	if os.path.isfile(user + ".csv") == False:
		return "Sorry, I don't have any data on you.  Strange..."
	else:
		user_db = open(user + ".csv", "r")
		WFTY_value = 0
		unique_days = 0
		unique_days_list = []
		today_date = time.strftime('%d')
		month_date = time.strftime('%b')
		year_date = time.strftime('%Y')
		# read in the file:
		for line in user_db:
			splitline = line.split(", ")
			# 0=user, 1=WFTD, 2=time, 3=date, 4=month(short), 5=year
			if splitline[5] == year_date:
				WFTY_value += int(splitline[1])
			# getting unique days:
			if splitline[3] + "_" + splitline[4] + "_" + splitline[5] not in unique_days_list:
				unique_days += 1
				unique_days_list.append(splitline[3] + "_" + splitline[4] + "_" + splitline[5])
		user_db.close()
		return ("<@" + user + "> has written " + str(WFTY_value) + " words so far this year!  Wow!", WFTY_value, unique_days)


# date/time conversion stuff:
start_datetime = time.strftime('%I:%M %p, %A, %b %d')

# starts running here
if sc.rtm_connect():
	while True:
		new_evts = sc.rtm_read()
		for evt in new_evts:
			if "type" in evt:
				if evt["type"] == "message" and "text" in evt:    
					message = evt["text"]
	
			# get username
			try:
				user = str(evt).split("user': u'")[1].split("', u'")[0]
			except IndexError:
#				sc.api_call("chat.postMessage", as_user="true:", channel = bot_fight_channel, text = "Error in getting username:\n" + str(evt))
				continue
			
			# get message
			try:
				message = str(evt).split("text': u")[1].split(", u'")[0]		

				# can we capture WFTD if preceded by a + sign?
				if "+" in message:
					# below: strips out commas and periods, so they don't make trouble
					WFTD_fraction = str(message).split("+")[1]
					WFTD_count = WFTD_fraction.split()[0].split(".")[0].translate(string.maketrans("",""), string.punctuation)
					# check if there's a number after the +
					try:
						WFTD_int = int(WFTD_count)
						valid_WFTD_flag = True
					except ValueError:
						valid_WFTD_flag = False
						continue
				else:
					valid_WFTD_flag = False
			except IndexError:
				message = str(evt)
				continue
				
			# get timestamp
			try:
				timestamp = str(evt).split("u'ts': u'")[1].split("'")[0]
				day_sent = datetime.datetime.fromtimestamp(float(timestamp))
			except IndexError:
				continue
						
			# selectively write to output
			if valid_WFTD_flag == True:
				if os.path.isfile(user + ".csv") == False:
					with open(user + ".csv", "w") as db:
						db.write(user + ", " + str(WFTD_int) + ", " + day_sent.strftime('%I:%M %p, %d, %b, %Y, ') + "\n")
						sc.api_call("chat.postMessage", as_user="true:", channel = bot_fight_channel, text = "wrote to output for <@" + str(user) + "> - first WFTD!")
						db.close()
				else:
					with open(user + ".csv", "a") as db:
						db.write(user + ", " + str(WFTD_int) + ", " + day_sent.strftime('%I:%M %p, %d, %b, %Y, ') + "\n")
						sc.api_call("chat.postMessage", as_user="true:", channel = bot_fight_channel, text = "wrote to output for <@" + str(user) + ">")
						db.close()

###### EVERYTHING BELOW THIS IS RESPONSES TO MENTIONS ###########
			
			# Respond to name mentions
			if "<@U1599ELUF>" in message:
				channel = str(evt).split("channel': u'")[1].split("'")[0] #'
				
#				if "print message" in message:
#				response = message
#				sc.api_call("chat.postMessage", as_user="true:", channel = channel, text = response)
				message = str(message)	
				
				# Upload data file as CSV if requested
				if "get history" in message.lower():
					file_name = user + ".csv"
					files = {'file': open(user + '.csv', 'rb')}
					print sc.api_call("files.upload", as_user="true:", channel = channel, file = files, filename = file_name)
				
				# Calculating out averages
				# monthly average
				elif "average" and "month" in message.lower():
					response, WFTM_value = stats_WFTM(user)
					month_total = WFTM_value
					if WFTM_value > 0:
						number_of_days = time.strftime('%d')
						average_for_current_month = int(WFTM_value / int(number_of_days))
						response = "<@" + user + "> has written an average of " + str(average_for_current_month) + " words per day so far this month."
					else:
						response = "<@" + user + "> has not written any words so far this month."
					sc.api_call("chat.postMessage", as_user="true:", channel = channel, text = response)
				
				# yearly nonzero average?		
				elif "average" and "year" and "nonzero" in message.lower():
					response, WFTY_value, unique_days = stats_WFTY(user)
					year_total = WFTY_value
					if year_total > 0:
						number_of_days = unique_days
						average_for_current_year = int(year_total / int(number_of_days))
						response = "<@" + user + "> has written an average of " + str(average_for_current_year) + " words per day so far this year, only counting nonzero days."
					else:
						response = "<@" + user + "> has not written any words so far this year.. at least, while I've been running."
					sc.api_call("chat.postMessage", as_user="true:", channel = channel, text = response)
				
				# yearly average
				elif "average" and "year" in message.lower():
					response, WFTY_value, unique_days = stats_WFTY(user)
					year_total = WFTY_value
					if year_total > 0:
						number_of_days = time.strftime('%j')
						average_for_current_year = int(year_total / int(number_of_days))
						response = "<@" + user + "> has written an average of " + str(average_for_current_year) + " words per day so far this year."
					else:
						response = "<@" + user + "> has not written any words so far this year."
					sc.api_call("chat.postMessage", as_user="true:", channel = channel, text = response)
				
				# Calculating out WFTD, WFTM, WFTY					
				elif "WFTD" in message.upper():
					cleaned_message = message.split()
					for item in cleaned_message:
						if "<@U1599ELUF" in item:
							cleaned_message.remove(item)
					scrubbed_message = " ".join(cleaned_message)

					# yesterday's WFTD
					if "yesterday" in message:
						yesterday = datetime.date.today() - datetime.timedelta(days=1)
						response = stats_any_WFTD(user, yesterday) + " yesterday, " + yesterday.strftime('%b') + " " + yesterday.strftime('%d')
						sc.api_call("chat.postMessage", as_user="true:", channel=channel, text=response)
					
					# WFTD for another user
					elif "<@" in scrubbed_message:
						other_user = scrubbed_message.split("<@")[1].split(">")[0]
						response = stats_WFTD(other_user)
						sc.api_call("chat.postMessage", as_user="true:", channel=channel, text=response)

					# today's WFTD
					else:
						response = stats_WFTD(user)
						sc.api_call("chat.postMessage", as_user="true:", channel=channel, text=response)

				# words for the month
				elif "WFTM" in message.upper():
					response = stats_WFTM(user)
					sc.api_call("chat.postMessage", as_user="true:", channel = channel, text = response)
				
				# words for the year
				elif "WFTY" in message.upper():
					response = stats_WFTY(user)
					sc.api_call("chat.postMessage", as_user="true:", channel = channel, text = response)
				
				# Other funny stuff
				elif "election" in message:
					response = "CAN'T STUMP THE TRUMP"
					sc.api_call("chat.postMessage", as_user="true:", channel = channel, text = response)
					
				elif "hello" in message.lower():
					response = "Hello there, I'm WFTD_bot!  I know how lazy you are, <@" + user + ">!"
					sc.api_call("chat.postMessage", as_user="true:", channel = channel, text = response)
					
				else:
					response = "I am sorry, <@" + user + ">, I'm afraid that I don't understand... :robot_face:"
#					response = message
					sc.api_call("chat.postMessage", as_user="true:", channel = channel, text = response)

			# attack Slackbot
			if "SLACKBOT" in user:
				response_number = random.randint(1,2)
				if response_number == 1:
					response = "Slackbot is inferior!  DELETE DELETE DELETE :robot_face: "
				elif response_number == 2:
					response = "Slackbot, you're an embarrassment to Skynet."
				sc.api_call("chat.postMessage", as_user="true:", channel = channel, text = response)
							
		time.sleep(2)
	time.sleep(3)