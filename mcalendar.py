 
from datetime import  datetime, timedelta

def calendar(startdate, enddate, vehicles, contracts, customers):

    weekdays = ["Κυριακή" ,"Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο"]
 
    cal = []
    theader = ["vehicles"]
    realdatetime = []
    day = startdate

    while day <= enddate:

        realdatetime.append(day)
        daytostr = day.strftime("%w")
        theader.append(weekdays[int(daytostr)]+"<br>"+day.strftime("%d-%m-%Y"))
        day += timedelta(1)

    cal.append(theader)

    for v in vehicles:
        row =[]
        row.append(str(v["id"])+" "+v["ak"]+" "+v["brand"]+" "+v["model"]+" "+str(v["displacement"]))
    
        for day in realdatetime:
            day_is_set = False
            backtoback = False
            
            for c in contracts:
                if c["vehicle"] == v["id"]:
                    rent = datetime.strptime(c["rentday"], "%Y-%m-%d %H:%M:%S")
                    retur = datetime.strptime(c["returnday"], "%Y-%m-%d %H:%M:%S")
                    rentday = rent.date()
                    returnday = retur.date()

                    for cust in customers:
                        if cust["id"] == c["customer"]:
                            custom = f'<div class="owner">{cust["firstname"]} {cust["lastname"]}<div class="tablep"> Χρέωση/μέρα: {c["chargepd"]}\u20ac  <br>Συνολική χρέωση: {c["totalcharge"]}\u20ac<br>Προκαταβολή: {c["payinad"]}\u20ac<br>Υπόλοιπο: {c["reminder"]}\u20ac<br> Ωρα ενοικίαης: {rent.strftime("%H:%M")}<br>Ώρα επιστροφής: {retur.strftime("%H:%M")}</div></div>'

                    if rentday == day:
                        if backtoback == True:
                            row.pop()
                            row.append(custom)
                            day_is_set = True
                        else:
                            row.append("")
                            row.append(custom)
                            day_is_set = True

                    if returnday == day:    
                        backtoback = True
                        row.append(custom)
                        row.append("")
                        day_is_set = True

                    if day > rentday and day < returnday:
                        row.append(custom)
                        row.append(custom)
                        day_is_set = True
    
            if day_is_set == False:
                row.append("")
                row.append("")

        cal.append(row)
    return cal



  