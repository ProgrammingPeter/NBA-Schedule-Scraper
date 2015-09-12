import scrapy
import time
import csv
from datetime import datetime

class ESPNSpider(scrapy.Spider):
    name = "espn"
    allowed_domains = ["espn.go.com"]
    start_urls = [
        "http://espn.go.com/nba/team/schedule/_/name/bos/seasontype/2/boston-celtics",
        "http://espn.go.com/nba/team/schedule/_/name/bkn/seasontype/2/brooklyn-nets",
        "http://espn.go.com/nba/team/schedule/_/name/ny/seasontype/2/new-york-knicks",
        "http://espn.go.com/nba/team/schedule/_/name/phi/seasontype/2/philadelphia-76ers",
        "http://espn.go.com/nba/team/schedule/_/name/tor/seasontype/2/toronto-raptors",
        "http://espn.go.com/nba/team/schedule/_/name/gs/seasontype/2/golden-state-warriors",
        "http://espn.go.com/nba/team/schedule/_/name/lac/seasontype/2/los-angeles-clippers",
        "http://espn.go.com/nba/team/schedule/_/name/lal/seasontype/2/los-angeles-lakers",
        "http://espn.go.com/nba/team/schedule/_/name/phx/seasontype/2/phoenix-suns",
        "http://espn.go.com/nba/team/schedule/_/name/sac/seasontype/2/sacramento-kings",
        "http://espn.go.com/nba/team/schedule/_/name/chi/seasontype/2/chicago-bulls",
        "http://espn.go.com/nba/team/schedule/_/name/cle/seasontype/2/cleveland-cavaliers",
        "http://espn.go.com/nba/team/schedule/_/name/det/seasontype/2/detroit-pistons",
        "http://espn.go.com/nba/team/schedule/_/name/ind/seasontype/2/indiana-pacers",
        "http://espn.go.com/nba/team/schedule/_/name/mil/seasontype/2/milwaukee-bucks",
        "http://espn.go.com/nba/team/schedule/_/name/dal/seasontype/2/dallas-mavericks",
        "http://espn.go.com/nba/team/schedule/_/name/hou/seasontype/2/houston-rockets",
        "http://espn.go.com/nba/team/schedule/_/name/mem/seasontype/2/memphis-grizzlies",
        "http://espn.go.com/nba/team/schedule/_/name/no/seasontype/2/new-orleans-pelicans",
        "http://espn.go.com/nba/team/schedule/_/name/sa/seasontype/2/san-antonio-spurs",
        "http://espn.go.com/nba/team/schedule/_/name/atl/seasontype/2/atlanta-hawks",
        "http://espn.go.com/nba/team/schedule/_/name/cha/seasontype/2/charlotte-hornets",
        "http://espn.go.com/nba/team/schedule/_/name/mia/seasontype/2/miami-heat",
        "http://espn.go.com/nba/team/schedule/_/name/orl/seasontype/2/orlando-magic",
        "http://espn.go.com/nba/team/schedule/_/name/wsh/seasontype/2/washington-wizards",
        "http://espn.go.com/nba/team/schedule/_/name/den/seasontype/2/denver-nuggets",
        "http://espn.go.com/nba/team/schedule/_/name/min/seasontype/2/minnesota-timberwolves",
        "http://espn.go.com/nba/team/schedule/_/name/okc/seasontype/2/oklahoma-city-thunder",
        "http://espn.go.com/nba/team/schedule/_/name/por/seasontype/2/portland-trail-blazers",
        "http://espn.go.com/nba/team/schedule/_/name/utah/seasontype/2/utah-jazz"
    ]

    def getConvertDateFormat(self, date):
        parsedArray = date[0].split(' ')

        if parsedArray[1] == 'Oct':
            month = '10'
        elif parsedArray[1] == 'Nov':
            month = '11'
        elif parsedArray[1] == 'Dec':
            month = '12'
        elif parsedArray[1] == 'Jan':
            month = '01'
        elif parsedArray[1] == 'Feb':
            month = '02'
        elif parsedArray[1] == 'Mar':
            month = '03'
        else:
            month = '04'

        day = parsedArray[2] #select day from array - 23

        time = date[1].split(' ') #selects time - 7:00 PM

        if month in ['10', '11', '12']:
            year = '15'
        else:
            year = '16'

        date = year + month + day + ' ' + time[0] # 15 05 23 7:00 

        return datetime.strptime(date, "%y%m%d %H:%M") #2015-05-23 7:00:00

    def parse(self, response):
        gameNetwork = []
        televized = []
        homeOrAway = []
        location = []
        teams = []
        links = []
        dateTimes = []
        homeTeamArray = []
        awayTeamArray = []
        linkCounter = 0
        homeAwayCounter = 0

        teamName = str(response)
        teamName = teamName[65:]
        if teamName not in ['new-york-knicks>', 'new-orleans-pelicans>', 'golden-state-warriors>', 'san-antonio-spurs>']:
            index = teamName.index('/')
            teamName = teamName[index+1:]
        teamName = teamName[:-1]
        teamName = teamName.replace("-", " ")
        teamName = teamName.title()

        for sel in response.xpath('//tr'):
            title = sel.xpath('td/text()').extract()
            if title[0] not in ['2016 Regular Season Schedule', 'OCTOBER', 'NOVEMBER', 'DECEMBER', 'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL']:
                dateTimes.append(self.getConvertDateFormat(title))

                if len(title) == 3:
                    if title[2] in ['TNT', 'NBATV']:
                        gameNetwork.append(title[2])
                    else:
                        gameNetwork.append('Local')
                else: # there is no ESPN string in the array so we need to manually insert it
                    gameNetwork.append('ESPN')
        for sel in response.xpath('//ul/li'):
            desc = sel.xpath('text()').extract()

            if desc:
                homeOrAway.append(desc[0]) #if 'vs' or '@' is set add to array

        for sel in response.xpath('//ul/li/a'):
            link = sel.xpath('//ul/li/a/@href').extract()
            desc = sel.xpath('text()').extract()
            if desc and desc[0] in ['Denver', 'Houston', 'Oklahoma City', 'Los Angeles', 'Utah', 'Golden State','Portland', 'Phoenix', 'New Orleans', 'San Antonio', 'Los Angeles','Dallas', 'Milwaukee', 'Chicago', 'Toronto', 'Philadelphia','Orlando', 'Minnesota', 'NY Knicks', 'Brooklyn', 'Boston','Cleveland', 'Charlotte', 'Atlanta', 'Miami', 'Memphis','Indiana', 'Washington', 'Sacramento', 'Detroit']:
                location.append(desc[0])
                oppoTeam = str(link[linkCounter]) #getting opponents name from the link, ESPN just gives the teams city, and with Los Angeles being ambigious, we need to know which team they are specifying
                oppoTeam = oppoTeam[35:] # Hardcoded value to reach the end the part of the string we want
                index = oppoTeam.index('/')
                oppoTeam = oppoTeam[index+1:]
                for char in oppoTeam:
                    if char == '-':
                        oppoTeam = oppoTeam.replace("-", " ") #Link has teams as - 'orlando-magic'

                if homeOrAway[homeAwayCounter] == 'vs':
                    homeTeamArray.append(teamName)
                    awayTeamArray.append(oppoTeam.title())
                else:
                    homeTeamArray.append(oppoTeam.title())
                    awayTeamArray.append(teamName)
                homeAwayCounter += 1
            linkCounter +=1


        teamFileName = str(response)
        teamFileName = teamFileName[65:]
        if teamFileName not in ['new-york-knicks>', 'new-orleans-pelicans>', 'golden-state-warriors>', 'san-antonio-spurs>']: #teams with three words in the link are handled differently
	        index = teamFileName.index('/')
	        teamFileName = teamFileName[index+1:]
        teamFileName = teamFileName[:-1]
        fileName = teamFileName

        with open(fileName + '.csv', 'w') as fp:
            for x in range(0, len(dateTimes)):
                if gameNetwork[x] in ['TNT', 'ESPN', 'NBATV']:
                    gameNetWorkFlag = 1
                else:
                    gameNetWorkFlag = 0
                a = csv.writer(fp, delimiter=',')
                data = [homeTeamArray[x], awayTeamArray[x], dateTimes[x], gameNetWorkFlag, gameNetwork[x]]
                a.writerow(data)
