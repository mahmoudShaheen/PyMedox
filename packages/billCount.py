from pythonSQL import getTotalDayBills, checkBills
from notification import notEnoughDayBillsNotification

#returns whether the bills will be enough for one day
def checkDay():
	totalBills = getTotalDayBills()
	enough = checkBills(totalBills)
	if (not enough):
		notEnoughDayBillsNotification()
