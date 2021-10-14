#python bar.py | lemonbar -p | bash
#Euan Chree 
import sys, subprocess, time

fd = sys.stdout

def getTitle(windowId):
	title = subprocess.run("xprop -id " + windowId + " _OB_APP_GROUP_CLASS", shell = True, capture_output=True)

	if (title.returncode == 0):
		title = title.stdout.decode("utf-8")
		title = title[36:len(title)-2]
		return title
	else:
		return "title error"

def clock():
	clock = subprocess.run('date "+%H:%M %d/%m/%y"', shell = True, capture_output = True)

	if (clock.returncode == 0):
		clock = clock.stdout.decode("utf-8").replace("\n","")
		return clock
	else:
		return "clock error"

def taskManager():
	focwin = subprocess.run("xprop -root _NET_ACTIVE_WINDOW | cut -d ' ' -f 5", shell = True, capture_output = True)

	if (focwin.returncode == 0):
		focwin = focwin.stdout.decode("utf-8")
	else:
		return "Focused window can't be found"

	wins = subprocess.run("xprop -root _NET_CLIENT_LIST", shell = True, capture_output= True)

	if (wins.returncode == 0):

		wins = wins.stdout.decode("utf-8")
		wins = wins[38:len(wins)].replace("\n", "").replace("\n","").split(", ")
		out = ""

		for index in range(0,len(wins)):
			if (wins[index] == focwin):
				out += getTitle(wins[index])
			else:
				out += "%{A:" + "wmctrl -a " + wins[index] + " -i:}" + str(getTitle(wins[index])) + "%{A} "

		return out.replace("\n","")
	else:
		return "task manager error"

while True:
	output = "%{c}" + taskManager() + "%{r}" + clock() + "\n"
	fd.write(output)
	fd.flush()
	time.sleep(0.1)

