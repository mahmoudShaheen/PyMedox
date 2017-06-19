from pythonSQL import getTotalDayBills, checkBills
from notification import notEnoughDayBillsNotification

#checks if bills in warehouse are enough for one day
#if not sends notification to care giver
def checkDay():
	totalBills = getTotalDayBills()
	enough = checkBills(totalBills)
	if (not enough):
		notEnoughDayBillsNotification()
