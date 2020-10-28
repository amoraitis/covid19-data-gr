# ferch data from the natioal public health organization of Greece
# https://eody.gov.gr/epidimiologika-statistika-dedomena/ektheseis-covid-19/

import urllib.request
from datetime import date, timedelta

templateURL = "https://eody.gov.gr/wp-content/uploads/{date.year}/{date.month:02}/covid-gr-daily-report-{date.year}{date.month:02}{date.day:02}.pdf"
templateDestinationPath = "data/covid-gr-daily-report-{date.year}{date.month:02}{date.day:02}.pdf"

start = date(2020, 10, 1)
end = date(2020, 10, 27)
currentDate = start
interval = timedelta(days=1)

while(currentDate < end):
    urllib.request.urlretrieve(templateURL.format(date=currentDate), templateDestinationPath.format(date=currentDate))
    currentDate += interval

