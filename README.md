# NBA-Schedule-Scraper
The scraper takes links from ESPN for the current season, and creates .csv files for every
teams regular season schedule. At the moment, it only handles current seasons. Feature will be added
to handle past seasons in the future.

# How to create the CSV
From the root of NBA-Schedule-Scraper run 'scrapy crawl espn' from the command line and the .csv files will be generated.
Be sure to have scrappy, and python installed.

Format of the .csv files.

Column 1, Column 2, Column 3, Column 4, Column 5, Column 6
homeTeam, awayTeam, dateTime, televizedGameFlag, gameNetwork

televizedGameFlag is true for games televized on ESPN, TNT, or NBAtv

http://espn.go.com/nba/team/schedule/_/name/bkn/seasontype/2/new-york-knicks - this is one of the links used to
gather the schedule for the 2015-2016 NY Knicks season.

Currently, every teams link is hardcoded and all you need to do is run the scraper and it will make the current teams schedule.

# Scrappy
Everything you'll need to get started with Scrappy will be [here](http://scrapy.org/)