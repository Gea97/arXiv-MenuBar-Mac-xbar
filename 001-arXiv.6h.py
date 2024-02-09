#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# <xbar.title>arXiv</xbar.title>
# <xbar.version>v2.1.7-beta</xbar.version>
# <xbar.author>Gea</xbar.author>
# <xbar.author.github>Gea97</xbar.author.github>
# <xbar.desc>arXiv Feed</xbar.desc>
# <xbar.image>https://i.imgur.com/0tY2che.png</xbar.image>
# <xbar.dependencies>python2, urllib, feedparser, termcolor</xbar.dependencies>

# Plugin Version: v3.0
# Last Update: 2024-02-10
# Plugin Link: https://github.com/Gea97/arXiv-MenuBar-Mac-xbar

# You can change the default refresh time changing the plugin name with format "001-arXiv.<time>.py", for example "001-arXiv.5m.py" sets the refresh time to 5 minutes

# arXiv API User's Manual avaialable at:
# https://info.arxiv.org/help/api/user-manual.html#search_query_and_id_list

# The arXiv feed usually updates once per day, at 5 AM UTC, it's normal if you don't see resault from the last couple of hours

# IMPORTANT, THIS SCRIPT WORKS WITH PYTHON 2 (v2.7) AND NOT WITH PYTHON 3, SO IF YOU HAVE A RECENT COMPUTER YOU HAVE TO INSTALL PYTHON2
# And also install feedparser v5.2.1 and termcolor (in python 2 obviously)

"""
python2 -m pip install feedparser==5.2.1
python2 -m pip install termcolor
"""

import urllib
import feedparser
from termcolor import colored

# Set Keywords
# To search for phrases use the pattern "%22 Word1 + Word2 %22", without spaces, i.e. like "%22Black+Holes%22" will search for "Black Holes"
# do NOT put any spaces
# the first entry is for the number of result to skip for that Keyword
# the second one is the number of max result to show
# the third one is the sorting method, can be "relevance", "lastUpdatedDate", "submittedDate"
# the fourth one is the sorting orded, can be either "ascending" or "descending"
# from the fifth entry until the last one is for the keywords
# for each keyword you have to specify the prefix for the search field, the available ones are:
# ti for Title, au for Author, abs for Abstract, co for comment, jr for journal reference,
# cat for Category, rn for reporth number, id for Id, or you can use all for searching in each of the fields simultaneously.
# N.B. you can specify only 1 category
# so some examples would be "all:%22Black+Holes%22", "cat:gr-qc", "ti:electron"
# The second-last entry is a list for a string containing the boolen operators ("AND", "OR" or "NOT")
# And number that has to 1 if you want the boolean operators to be displayed but not for the first entry
# if you want that the boolean operator is displayed also for the fist entry pu it to -1
# Otherwise if you don't want to display boolean operators put it to any number that is not 1 or -1
# You have to specifity a boolean operator for each entry
# N.B. if you search for only one keyword you can use either "AND" or "OR", the function the same in this case
# If you put only 1 entry, or 1 entry + a category you can omit it
# The last entry is a list that has to be 1 if you want the corresponding (i.e. in the same position) word to be displayed


Keywords = [
    [0,  3,    "submittedDate",   "descending",  "all:%22Black+Holes%22", "all:%22Black+Hole%22",                                                     [0, "OR", "OR"],                [1 ,0]],
    [0,  3,    "submittedDate",   "descending",  "all:%22Black+Holes%22", "all:%22Black+Hole%22", "all:%22String+Theory%22",                  [1, "AND", "OR", "NOT"],             [1, 0, 1]],
    [0, 15,  "lastUpdatedDate",   "descending",  "all:Electron", "all:Proton", "all:Neutrino", "all:Ion",  "all:Jet",          [1, "AND", "AND", "NOT", "NOT", "NOT"],       [1, 1, 1, 0, 1]],
    [0,  4,  "lastUpdatedDate",   "descending",  "cat:gr-qc", "cat:hep-th",                                                                         [0, "AND", "AND"],                [1, 1]],
]

# List of NOT allowed characters
not_allowed_characters = "-"

# Set number of authors to display
AuthorsLenght = 6

# Website Adavance searc

# Put this equal to  1 if you want that links corresponding to Titles Result have "announced_date" has sorting method on arXiv (only on the website) when using submittedDate method.
# Put this equal to -1 if you want that links corresponding to Titles Result have "announced_date" has sorting method on arXiv (only on the website) when any sorting method (i.e. also for lastUpdatedDate)
# This will not display updated papers on arXiv, and will sort newstest paper using the announced date method instead of the submitted date or the lastUpdatedDate one
# otherwise if you want to use the submitted date method put this variable to anything that is not 0
Website_Title_AnnouncedSorting = 1

# Include cross list (1 if yoou want to do)
IncludeCrossList = 1

# Only in Physics Archive (!= 1 if you want for also other subjects like math, 1 if you want only the physics archive, N.B. if you speciify a category it become 1 automatically)
OnlyPhysicsArchive = 0

# Show Abstracts in results (put 1 if you want):
IncludeAbstracts = 1

# Result Size (number of result per page):
ResultsPerPage = 50

# Specify how to filter per dates
# DateFilterMethod can be "all_dates", "date_range", "past_12"
# DateYearFilter can be empty "" or a specifica year like "2023"
# DateStartFilter and DateEndFilter can be empty or in the format "YYYY-MM-DD"
DateFilterMethod = "all_dates"
DateYearFilter = ""
DateStartFilter = ""
DateEndFilter = ""

# Choose Display Order, N.B. Feed Last Updated has to be after the results:
DisplayOrder = ["Results", "FrontPage", "Legend", "Feed"]

# Choose if Display the Feed and the Legend, and the Warnings put 1 if you want, 0 otherwise
DisplayWarnings   =  0         # Put this to -1 if you want to display ony the first link of warning, to -2 if you also want the MenuBar Icon to be a warning, -3 for both things
DisplayLegend     =  1
DisplayFeed       =  1
DisplayNew        =  1          # You can set DisplayNew     to 0 if you want to change submittedDate   to lastUpdatedDate, otherwise use another number that isn't 1 or 0 if you don't want to change thant
DisplayUpdated    =  1          # You can set DisplayUpdated to 0 if you want to change lastUpdatedDate to   submittedDate, otherwise use another number that isn't 1 or 0 if you don't want to change thant

if (DisplayNew == 0):
    ColorUpdatedNotNew = 1  # You can put this to 1 if DisplayNew == 0 and you want to color all result in Days Range, and not only the updated ones
else:
    ColorUpdatedNotNew = 0

if ((DisplayUpdated == 0) and (DisplayNew == 1)):
     for Key in range(len(Keywords)):
        if (Keywords[Key][2] == "lastUpdatedDate"):
            Keywords[Key][2] = "submittedDate"
elif ((DisplayNew == 0) and (DisplayUpdated == 1)):
     for Key in range(len(Keywords)):
        if (Keywords[Key][2] == "submittedDate"):
            Keywords[Key][2] = "lastUpdatedDate"
elif ((DisplayNew != 1) and (DisplayUpdated != 1)):
    DisplayLegend = 0


# Set number of days considered new for colored icons
DaysNew          =  7
DaysWeekNew      = 15
DaysUpdatedWeek  =  7
DaysUpdatedMonth = 15

# If you want the icon put 1 in the first entry, 0 otherwise
# Then choose the color
# If you want the icon to be colored put the third value to 1, otherwise to 0
# Then choose the icon (put one anyway)
# For Links it's just choose if colored and the color
# For TitlesNewIconVar and TitlesWeekIconVar the first entry is the number of days to consider New
MenuBarIconVar            = [1,                  "grey",     0,   "⚛︎"]                               #MenuBar Icon Colored
KeywordIconVar            = [1,                  "blue",     1,   "⚡︎"]                               #Keyword Icon Colored
TitlesIconVar             = [1,                  "blue",     0,   "⚛︎"]                               #Title Icon Colored
TitlesNewestIconVar       = [1,                  "red",      1,   "⚛︎"]                               #Title Newest Icon Colored
TitlesNewIconVar          = [DaysNew,            "magenta",  1,   "⚛︎"]                               #Title New Icon Colored
TitlesWeekIconVar         = [DaysWeekNew,        "yellow",   1,   "⚛︎"]                               #Title Week Icon Colored
TitlesUpdatedWeekIconVar  = [DaysUpdatedWeek,    "green",    1,   "⚛︎"]                               #Title UpdatedWeek Icon Colored
TitlesUpdatedMonthIconVar = [DaysUpdatedMonth,   "cyan",     1,   "⚛︎"]                               #Title UpdatedMonth Icon Colored
FrontPageIconVar          = [1,                  "blue",     1,   "⚡︎"]                               #FrontPage Icon Colored
LegendIconVar             = [1,                  "yellow",   0,   "⚡︎"]                               #Legend Icon Colored
FeedIconVar               = [1,                  "yellow",   1,   "⚡︎"]                               #Feed Icon Colored
WarningIconVar            = [1,                  "yellow",   1,   "☢︎"]                               #Warning Icon Colored (Es. for no results)
LinkVar                   = [1,                  "cyan"]                                             #Link Colored

# Check if Display condition is satisfied
if (DisplayNew != 1):
    TitlesNewestIconVar[2] = 0
    TitlesNewIconVar[2] = 0
    TitlesWeekIconVar[2] = 0

if (DisplayUpdated != 1):
    TitlesUpdatedWeekIconVar[2] = 0
    TitlesUpdatedMonthIconVar[2] = 0

# Setting the Icons
if(MenuBarIconVar[0] == 1):
    if ( MenuBarIconVar[2] == 1 ):
        MenuBarIcon = colored(MenuBarIconVar[3], MenuBarIconVar[1], attrs=["bold"])
    else:
        MenuBarIcon = MenuBarIconVar[3]
else:
    MenuBarIcon = ""

if ( KeywordIconVar[0] == 1 ):
    if ( KeywordIconVar[2] == 1 ):
        KeywordIcon = colored(KeywordIconVar[3], KeywordIconVar[1], attrs=["bold"])
    else:
        KeywordIcon = KeywordIconVar[3]
else:
    KeywordIcon = ""

if ( TitlesIconVar[0] == 1 ):
    if ( TitlesIconVar[2] == 1 ):
        TitlesIcon = colored(TitlesIconVar[3], TitlesIconVar[1], attrs=["bold"])
    else:
        TitlesIcon = TitlesIconVar[3]
else:
    TitlesIcon = ""

if ( (TitlesNewestIconVar[2]) == 1 and (TitlesIcon != "") ):
    TitlesNewestIcon = colored(TitlesNewestIconVar[3], TitlesNewestIconVar[1], attrs=["bold"])
else:
    TitlesNewestIcon = TitlesIcon

if ( (TitlesNewIconVar[2]) == 1 and (TitlesIcon != "") ):
    TitlesNewIcon = colored(TitlesNewIconVar[3], TitlesNewIconVar[1], attrs=["bold"])
else:
    TitlesNewIcon = TitlesIcon

if ( (TitlesWeekIconVar[2] == 1) and (TitlesIcon != "") ):
    TitlesWeekIcon = colored(TitlesWeekIconVar[3], TitlesWeekIconVar[1], attrs=["bold"])
else:
    TitlesWeekIcon = TitlesIcon

if ( (TitlesUpdatedWeekIconVar[2] == 1) and (TitlesIcon != "") ):
    TitlesUpdatedWeekIcon = colored(TitlesUpdatedWeekIconVar[3], TitlesUpdatedWeekIconVar[1], attrs=["bold"])
else:
    TitlesUpdatedWeekIcon = TitlesIcon

if ( (TitlesUpdatedMonthIconVar[2] == 1) and (TitlesIcon != "") ):
    TitlesUpdatedMonthIcon = colored(TitlesUpdatedMonthIconVar[3], TitlesUpdatedMonthIconVar[1], attrs=["bold"])
else:
    TitlesUpdatedMonthIcon = TitlesIcon

if ( FrontPageIconVar[0] == 1 ):
    if ( FrontPageIconVar[2] == 1 ):
        FrontPageIcon = colored(FrontPageIconVar[3], FrontPageIconVar[1], attrs=["bold"])
    else:
        FrontPageIcon = FrontPageIconVar[3]
else:
    FrontPageIcon = ""

if ( LegendIconVar[0] == 1 ):
    if ( LegendIconVar[2] == 1 ):
        LegendIcon = colored(LegendIconVar[3], LegendIconVar[1], attrs=["bold"])
    else:
        LegendIcon = LegendIconVar[3]
else:
    LegendIcon = ""


if ( FeedIconVar[0] == 1 ):
    if ( FeedIconVar[2] == 1 ):
        FeedIcon = colored(FeedIconVar[3], FeedIconVar[1], attrs=["bold"])
    else:
        FeedIcon = FeedIconVar[3]
else:
    FeedIcon = ""

if ( WarningIconVar[0] == 1 ):
    if ( WarningIconVar[2] == 1 ):
        WarningIcon = colored(WarningIconVar[3], WarningIconVar[1], attrs=["bold"])
    else:
        WarningIcon = WarningIconVar[3]
else:
    WarningIcon = ""

if ( LinkVar[0] == 1 ):
    LinkColor="cyan"
    LinkAttributes=["bold", "underline"] #underline works only in terminal
else:
    LinkColor="white"
    LinkAttributes=["underline"]

# Set Correction rule for non-printable characters
Corrections = [
    ("|"," Abs "),
    ("\rm" , "\textrm",),
]

def Correct(string):
    for i in range(len(Corrections)):   
        string=string.replace(Corrections[i][0], Corrections[i][1])
    return string

# Clean

CleanAccents = [
    ("à","a"),
    ("è","e"),
    ("é","e"),
    ("ì","i"),
    ("ò","o"),
    ("ù","u"),
]

CleanSearchFields = [
    ("ti:",""),
    ("au:",""),
    ("abs:",""),
    ("co:"," "),
    ("jr:",""),
    ("cat:",""),
    ("rn:",""),
    ("id:",""),
    ("all:",""),
]

GetSearchFields = [
    ("ti:","title"),
    ("au:","author"),
    ("abs:","abstract"),
    ("co:","comments"),
    ("jr:","journal_ref"),
    ("cat:","cat"),
    ("rn:","report_num"),
    ("id:","paper_id"),
    ("all:","all"),
]

CleanBooleanOperators = [
    ("AND",""),
    ("OR",""),
    ("NOT",""),
    ("++","+"),
]

GetQueryBooleanOperators = [
    ("AND","AND"),
    ("OR","OR"),
    ("NOT","ANDNOT"),
]

CleanTitles = [
    ("\n",""),
    ("+"," "),
    ("%22",""),
    ("%28",""),
    ("%29",""),
]

def CleanAcc(string):
    for i in range(len(CleanAccents)):   
        string=string.replace(CleanAccents[i][0], CleanAccents[i][1])
    return string

def CleanFields(string):
    for i in range(len(CleanSearchFields)):   
        string=string.replace(CleanSearchFields[i][0], CleanSearchFields[i][1])
    return string

def GetFields(string):
    for i in range(len(GetSearchFields)):   
        if (GetSearchFields[i][0] in string):
            return GetSearchFields[i][1]

def CleanBoolean(string):
    for i in range(len(CleanBooleanOperators)):   
        string=string.replace(CleanBooleanOperators[i][0], CleanBooleanOperators[i][1])
    return string

def GetQueryBoolean(string):
    for i in range(len(GetQueryBooleanOperators)):
        if (string == GetQueryBooleanOperators[i][0]):
            return GetQueryBooleanOperators[i][1]

def CleanT(string):
    for i in range(len(CleanTitles)):   
        string=string.replace(CleanTitles[i][0], CleanTitles[i][1])
    return string

# Nesting Rules and Symbols
def Nesting(level):
    return "{}".format("-" * level)

def Indentation(level):
    if(level) == 1:
        return "-"
    elif(level) == 4:
        return " .        "    #Symbol for Abstract Text
    else:
        return Nesting(level-1)

# Function to determine the number of days in the current and previous month
DaysNotLeap = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
DaysLeap    = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

def NumberOfDays(Year, Month):
    if( (Year % 100 != 0) and (Year % 4 == 0) ):
        return DaysLeap[Month-1]
    elif( (Year % 400 == 0) ):
        return DaysLeap[Month-1]                
    else:
        return DaysNotLeap[Month-1]

# API query
base_API_url = 'http://export.arxiv.org/api/query?' #base API query url
arXiv_url = "https://arxiv.org/"

# Start main
def main():

    # breaker variable
    breaker = 0

    if(DaysNew == 1):
        print("⚠️")
        print(Nesting(3))
        print("⚠️⚠️⚠️ DaysNew can't be 1 ⚠️⚠️⚠️ | href={}".format("ERROR"))
        return
    
    if(DaysNew > 28):
        print("⚠️")
        print(Nesting(3))
        print("⚠️⚠️⚠️ DaysNew can't be more than 28 days ⚠️⚠️⚠️ | href={}".format("ERROR"))
        return
    
    if(DaysWeekNew > 28):
        print("⚠️")       
        print(Nesting(3))
        print("⚠️⚠️⚠️ DaysWeekNew can't be more than 28 days ⚠️⚠️⚠️ | href={}".format("ERROR"))
    
    if(DaysUpdatedWeek > 28):  
        print("⚠️")  
        print(Nesting(3))
        print("⚠️⚠️⚠️ DaysUpdatedWeek can't be more than 28 days ⚠️⚠️⚠️ | href={}".format("ERROR"))
        return

    if(DaysUpdatedMonth > 28):  
        print("⚠️")
        print(Nesting(3))  
        print("⚠️⚠️⚠️ DaysUpdatedMonth can't be more than 28 days ⚠️⚠️⚠️ | href={}".format("ERROR"))
        return
        
    if(DaysWeekNew <= DaysNew ):
        print("⚠️")
        print(Nesting(3))        
        print("⚠️⚠️⚠️ DaysWeekNew can't be more or equal than DaysNew ⚠️⚠️⚠️ | href={}".format("ERROR"))
        return
    
    if(DaysUpdatedMonth <= DaysUpdatedWeek ):
        print("⚠️")
        print(Nesting(3))        
        print("⚠️⚠️⚠️ DaysUpdatedWeek can't be more or equal than DaysUpdatedMonth ⚠️⚠️⚠️ | href={}".format("ERROR"))
        return

    # Set Advance search parameters
    if (OnlyPhysicsArchive == 1):                           # Search Only in the Physics Archive
        subject_archive = "&classification-physics=y"
    else:
        subject_archive = ""

    result_size = "&size="+str(ResultsPerPage)              # Number of results per page

    if (IncludeAbstracts == 1):                             # Include abstracts
        show_abstracts="&abstracts=show"
    else:
        show_abstracts=""

    if (IncludeCrossList == 1):                             # Include or not cross list
        cross_list="&classification-include_cross_list=include"
    else:
        cross_list="&classification-include_cross_list=exclude"
    
    date_filter = "&date-filter_by="+DateFilterMethod+"&date-year="+DateYearFilter+"&date-from_date="+DateStartFilter+"&date-to_date="+DateEndFilter  # date filte

    if (DisplayWarnings == -2):
        print(WarningIcon)
    elif (DisplayWarnings == -3):
        print(WarningIcon)    
    else:
        print(MenuBarIcon)

    for order in range (len(DisplayOrder)):

        if (DisplayOrder[order] == "Results"):
            for Key in range(len(Keywords)):

                print(Nesting(3))

                CategoryTrigger = 0

                PositionDisplayKeyword = len(Keywords[Key])-1
                PositionBoolean = len(Keywords[Key])-2

                if ( (len(Keywords[Key])-6) > len(Keywords[Key][PositionDisplayKeyword]) ):
                    KeywordTitleError = Keywords[Key][4]
                    for i in range (5, PositionBoolean):
                        KeywordTitleError = KeywordTitleError+", "+Keywords[Key][i]
                        KeywordTitleError = CleanT(CleanFields(KeywordTitleError))
                    print("{} arXiv - {}:| href={}".format(KeywordIcon, KeywordTitleError, "ERROR"))
                    print("⚠️⚠️⚠️ For this keyword there is a problem with the number that represents if each word should be displayed ⚠️⚠️⚠️ | href={}".format("ERROR"))
                    continue

                if ( (len(Keywords[Key])-6) > len(Keywords[Key][PositionBoolean])-1 ):
                    KeywordTitleError = Keywords[Key][4]
                    for i in range (5, PositionBoolean):
                        KeywordTitleError = KeywordTitleError+", "+Keywords[Key][i]
                        KeywordTitleError = CleanT(CleanFields(KeywordTitleError))
                    print("{} arXiv - {}:| href={}".format(KeywordIcon, KeywordTitleError, "ERROR"))
                    print("⚠️⚠️⚠️ For this keyword there is a problem with the boolean operators ⚠️⚠️⚠️ | href={}".format("ERROR"))
                    continue               

                for i in range (4, PositionBoolean):
                    if (" " in Keywords[Key][i]):
                        print( "{} arXiv - {}:| href={}".format(KeywordIcon, "\""+Keywords[Key][i]+"\"", "ERROR") )
                        print ( "{}| href={}".format("⚠️⚠️⚠️ Please don't use spaces in the keyword title, see documentation ⚠️⚠️⚠️ ", "ERROR") )
                        breaker = 1
                if (breaker == 1):
                    breaker = 0
                    continue

                # Search parameters

                skipped_index_query = 0

                if (Keywords[Key][PositionBoolean][1] == "NOT"):
                    for i in range (4, PositionBoolean):
                        if (Keywords[Key][PositionBoolean][i-3] != "NOT"):
                           search_query = "{}".format(Keywords[Key][i]) 
                           skipped_index_query = i
                else:
                    search_query = "{}".format(Keywords[Key][4])

                if (Keywords[Key][PositionDisplayKeyword][0] == 1):
                    if(Keywords[Key][PositionBoolean][0] == -1):
                        KeywordTitleClean = Keywords[Key][PositionBoolean][1]+" {}".format(Keywords[Key][4])
                    else:
                        KeywordTitleClean = "{}".format(Keywords[Key][4])

                for i in range (5, PositionBoolean):
                    if (i != skipped_index_query):
                        search_query = search_query+"+"+GetQueryBoolean(Keywords[Key][PositionBoolean][i-3])+"+{}".format(Keywords[Key][i])

                    if (Keywords[Key][PositionDisplayKeyword][i-4] == 1):
                        if(Keywords[Key][PositionBoolean][0] == 1):
                            KeywordTitleClean = KeywordTitleClean+" "+Keywords[Key][PositionBoolean][i-3]+" {}".format(Keywords[Key][i])
                        elif(Keywords[Key][PositionBoolean][0] == -1):
                            KeywordTitleClean = KeywordTitleClean+" "+Keywords[Key][PositionBoolean][i-3]+" {}".format(Keywords[Key][i])
                        else:
                            KeywordTitleClean = KeywordTitleClean+", {}".format(Keywords[Key][i])

                KeywordTitleClean = CleanT(CleanFields(KeywordTitleClean))
                search_query      = CleanAcc(search_query)
                #print(search_query)
                
                start = Keywords[Key][0]        # set how many results to skip
                max_results = Keywords[Key][1]  # set how many results to show
                sortBy = Keywords[Key][2]       # set sort method
                sortOrder = Keywords[Key][3]    # set sort order
                query = "search_query=%s&start=%i&max_results=%i&sortBy=%s&sortOrder=%s" % (search_query,
                                                                    start,
                                                                    max_results, sortBy, sortOrder)

                # Opensearch metadata such as totalResults, startIndex, 
                # and itemsPerPage live in the opensearch namespase.
                # Some entry metadata lives in the arXiv namespace.
                # This is a hack to expose both of these namespaces in
                # feedparser v4.1
                feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
                feedparser._FeedParserMixin.namespaces[arXiv_url+'/schemas/atom'] = 'arxiv'

                # Perform a GET request using the base_API_url and query
                response = urllib.urlopen(base_API_url+query).read()

                # Parse the response using feedparser
                feed = feedparser.parse(response)

                # Print out feed information
                # N.B.
                if(Keywords[Key][3] == "ascending"):
                    Website_SortOrder = "+"
                if(Keywords[Key][3] == "descending"):
                    Website_SortOrder = "-"
                else:
                    Website_SortOrder = ""

                if((Keywords[Key][2] == "lastUpdatedDate") and (Website_Title_AnnouncedSorting != -1)):
                    Website_Sort = "&date-date_type="+"submitted_date"+"&order="+Website_SortOrder+"submitted_date"
                elif((Keywords[Key][2] == "submittedDate") and (Website_Title_AnnouncedSorting == 0)):
                    Website_Sort = "&date-date_type="+"submitted_date_first"+"&order="+Website_SortOrder+"submitted_date"    
                elif((Keywords[Key][2] == "submittedDate") and (Website_Title_AnnouncedSorting != 0)):
                    Website_Sort = "&date-date_type="+"announced_date_first"+"&order="+Website_SortOrder+"announced_date_first"
                elif((Keywords[Key][2] == "lastUpdatedDate") and (Website_Title_AnnouncedSorting == -1)):
                    Website_Sort = "&date-date_type="+"announced_date_first"+"&order="+Website_SortOrder+"announced_date_first"                
                else:
                    Website_Sort = "&order="

                physics_archive = "&classification-physics_archives=all"
                subject_archive = ""
                KeywordTitle = ""

                for KeyNumber in range (4, PositionBoolean):

                    BooleanOpTerm = "&terms-"+str(KeyNumber-4)+"-operator="+Keywords[Key][PositionBoolean][KeyNumber-3]

                    if (GetFields(Keywords[Key][KeyNumber]) != "cat"):
                        FieldTerm = "&terms-"+str(KeyNumber-4)+"-field="+GetFields(Keywords[Key][KeyNumber])
                        TitleTerm = "&terms-"+str(KeyNumber-4)+"-term="+CleanBoolean(CleanAcc(CleanFields(Keywords[Key][KeyNumber])))  
                    elif ((GetFields(Keywords[Key][KeyNumber]) == "cat") and (CategoryTrigger == 0)):
                        FieldTerm = "&terms-"+str(KeyNumber-4)+"-field="+"all"
                        TitleTerm = "&terms-"+str(KeyNumber-4)+"-term="
                        physics_archive = "&classification-physics_archives="+CleanFields(Keywords[Key][KeyNumber])
                        subject_archive = "&classification-physics=y"
                        CategoryTrigger = CategoryTrigger + 1
                        category_disp = CleanFields(Keywords[Key][KeyNumber])      
                    elif ((GetFields(Keywords[Key][KeyNumber]) == "cat") and (CategoryTrigger != 0)):      
                        FieldTerm = "&terms-"+str(KeyNumber-4)+"-field="+"all"
                        TitleTerm = "&terms-"+str(KeyNumber-4)+"-term="+CleanBoolean(CleanAcc(CleanFields(Keywords[Key][KeyNumber])))    
                        CategoryTrigger = CategoryTrigger + 1

                    KeywordTitle = KeywordTitle+BooleanOpTerm+TitleTerm+FieldTerm    

                #Website_Search_Method="&searchtype=all&abstracts=show&size=50&order="+Website_SortOrder+Website_SortBy
                Website_Search_Method = subject_archive+physics_archive+cross_list+date_filter+show_abstracts+result_size+Website_Sort
                Website_Link = arXiv_url+"search/advanced?advanced="+KeywordTitle+Website_Search_Method

                print(
                #    "{} arXiv - {}:| href={}".format(KeywordIcon, KeywordTitleClean, "https://arxiv.org/search/?query="+KeywordTitle+Website_Search_Method.replace("\n",""))
                "{} arXiv - {}:| href={}".format(KeywordIcon, KeywordTitleClean, Website_Link)                    
                )

                print( "{}".format(Nesting(3)) )

                if (DisplayWarnings != 0):
                    if (CategoryTrigger > 1):
                        print ( "{} {}| href={}".format(WarningIcon, "The title link gives results \""+category_disp+"\""+"while the others are threated as normal keywords", Website_Link) )
                        if ((DisplayWarnings != -1) and (DisplayWarnings != -3)):
                            print ( "{} {}| href={}".format(WarningIcon, "This is because max 1 category can be specified on the website", Website_Link) )  
                            print ( "{} {}| href={}".format(WarningIcon, "Nonetheless the query still gives the correct results in the selected categories with the selected boolean operator:", Website_Link) )   

                CurrentYear=feed.feed.updated_parsed[0]
                CurrentMonth=feed.feed.updated_parsed[1]
                CurrentDay=feed.feed.updated_parsed[2]

                if (len(feed.entries) == 0):
                    print ( "{} {}| href={}".format(WarningIcon, "No Results Found", Website_Link) )
                    for i in range (4, PositionBoolean):
                        for c in not_allowed_characters:
                            if (c in Keywords[Key][i]):
                                print ( "{} {}| href={}".format(WarningIcon, "The Character "+c+" is sometimes NOT allowed for the query, but results may be available on arXiv ", Website_Link) )
                    continue

                # Run through each entry, and print out information
                for entry in feed.entries:

                    # Links for this e-print
                    for link in entry.links:
                        
                        if link.rel == 'alternate':
                            ABSurl = link.href
                            OriginalABSurl = link.href[:-2]

                        elif link.title == 'pdf':
                            PDFurl = link.href

                        elif link.title == 'doi':
                            DOIurl = link.href

                    #Is it from Today?
                    CheckNew=[CurrentYear - entry.published_parsed[0], CurrentMonth - entry.published_parsed[1], CurrentDay - entry.published_parsed[2]]

                    CheckUpdated=[CurrentYear - entry.updated_parsed[0], CurrentMonth - entry.updated_parsed[1], CurrentDay - entry.updated_parsed[2]]

                    EntryTitleIcon = TitlesIcon

                    if((TitlesWeekIconVar[2] == 1)):                                                                                  #Icon for articles in the previous DaysWeekNew days
                        if (CheckNew[0] == 0):                                                                                        #check if same year
                            if (CheckNew[1] == 0):                                                                                    #check if same month
                                if((CheckNew[2] >= 0) and (CheckNew[2] <= DaysWeekNew)):                                                              
                                    EntryTitleIcon = TitlesWeekIcon
                            elif (CheckNew[1] == 1):                                                                                  #check if previous month
                                if((CheckNew[2] <= 0) and (CheckNew[2] <= - NumberOfDays(CurrentYear, CurrentMonth-1) + DaysWeekNew)):                                                     
                                    EntryTitleIcon = TitlesWeekIcon
                        elif ((CheckNew[0] == 1) and (CurrentMonth == 1) and (CheckNew[1] == -11) and (CheckNew[2] >= CurrentDay - NumberOfDays(CurrentYear-1, CurrentMonth-1) + DaysWeekNew)):
                                    EntryTitleIcon = TitlesWeekIcon

                    if((TitlesNewIconVar[2] == 1)):                                                                                   #Icon for articles in the previous DaysNew days
                        if (CheckNew[0] == 0):                                                                                        #check if same year
                            if (CheckNew[1] == 0):                                                                                    #check if same month
                                if((CheckNew[2] >= 0) and (CheckNew[2] <= DaysNew)):                                                              
                                    EntryTitleIcon = TitlesNewIcon
                            elif (CheckNew[1] == 1):                                                                                  #check if previous month
                                if((CheckNew[2] <= 0) and (CheckNew[2] <= - NumberOfDays(CurrentYear, CurrentMonth-1) + DaysNew)):                                                     
                                    EntryTitleIcon = TitlesNewIcon
                        elif ((CheckNew[0] == 1) and (CurrentMonth == 1) and (CheckNew[1] == -11) and (CheckNew[2] >= CurrentDay - NumberOfDays(CurrentYear-1, CurrentMonth-1) + DaysNew)):
                                    EntryTitleIcon = TitlesNewIcon 

                    if((TitlesNewestIconVar[2] == 1)):
                        if (CheckNew == [0, 0, 0]):                                                                                     #same day
                            EntryTitleIcon = TitlesNewestIcon                                                                           #Icon for articles in the previous day
                        elif (CheckNew == [0, 0, 1]):                                                                                   #previous day same month
                            EntryTitleIcon = TitlesNewestIcon
                        elif (CurrentDay == 1):                                                                                         #check if it's the first day of the month
                            if (CheckNew == [1, -11, -30]):                                                                             #1st January and 31th December
                                EntryTitleIcon=TitlesNewestIcon
                            elif  (CheckNew == [0, -1, NumberOfDays(CurrentYear, CurrentMonth-1)]):                                     #1st of the Month and last of the previous
                                EntryTitleIcon = TitlesNewestIcon

                    if((TitlesWeekIconVar[2] == 1)):
                        if(EntryTitleIcon != TitlesWeekIcon):
                            ConditionWeek = 1
                        else:
                            ConditionWeek = 0
                    else:
                            ConditionWeek = 1
            
                    if((TitlesNewestIconVar[2] == 1)):
                        if(EntryTitleIcon != TitlesNewestIcon):
                            ConditionNewest = 1
                        else:
                            ConditionNewest = 0
                    else:
                            ConditionNewest = 1

                    if((TitlesNewIconVar[2] == 1)):
                        if(EntryTitleIcon != TitlesNewIcon):
                            ConditionNew = 1
                        else:
                            ConditionNew = 0
                    else:
                            ConditionNew = 1

                    if((DisplayNew == 0) and (ColorUpdatedNotNew == 1)):
                        ConditionCheck = 1
                    else:
                        if (CheckUpdated != CheckNew):
                            ConditionCheck = 1
                        else:
                            ConditionCheck = 0

                    if((TitlesUpdatedMonthIconVar[2] == 1) and (ConditionWeek == 1) and (ConditionNewest == 1) and (ConditionNew == 1) and (ConditionCheck == 1)):   #Icon for articles updated in the previous DaysUpdated days
                        if (CheckUpdated[0] == 0):                                                                                                                   #check if same year
                            if (CheckUpdated[1] == 0):                                                                                                               #check if same mont
                                if((CheckUpdated[2] >= 0) and (CheckUpdated[2] <= DaysUpdatedMonth)):                                                              
                                    EntryTitleIcon = TitlesUpdatedMonthIcon
                            elif (CheckUpdated[1] == 1):                                                                                                             #check if previous month
                                if((CheckUpdated[2] <= 0) and (CheckUpdated[2] <= - NumberOfDays(CurrentYear, CurrentMonth-1) + DaysUpdatedMonth)):                                                     
                                    EntryTitleIcon = TitlesUpdatedMonthIcon
                        elif ((CheckUpdated[0] == 1) and (CurrentMonth == 1) and (CheckUpdated[1] == -11) and (CheckUpdated[2] >= CurrentDay - NumberOfDays(CurrentYear-1, CurrentMonth-1) + DaysUpdatedMonth)):
                                    EntryTitleIcon = TitlesUpdatedMonthIcon   

                    if((TitlesUpdatedWeekIconVar[2] == 1) and (ConditionNewest == 1) and (ConditionNew == 1) and (ConditionCheck == 1)):         #Icon for articles updated in the previous DaysUpdated days
                        if (CheckUpdated[0] == 0):                                                                                               #check if same year
                            if (CheckUpdated[1] == 0):                                                                                           #check if same mont
                                if((CheckUpdated[2] >= 0) and (CheckUpdated[2] <= DaysUpdatedWeek)):                                                              
                                    EntryTitleIcon = TitlesUpdatedWeekIcon
                            elif (CheckUpdated[1] == 1):                                                                                         #check if previous month
                                if((CheckUpdated[2] <= 0) and (CheckUpdated[2] <= - NumberOfDays(CurrentYear, CurrentMonth-1) + DaysUpdatedWeek)):                                                     
                                    EntryTitleIcon = TitlesUpdatedWeekIcon
                        elif ((CheckUpdated[0] == 1) and (CurrentMonth == 1) and (CheckUpdated[1] == -11) and (CheckUpdated[2] >= CurrentDay - NumberOfDays(CurrentYear-1, CurrentMonth-1) + DaysUpdatedWeek)):
                                    EntryTitleIcon = TitlesUpdatedWeekIcon                
                    
                    #Title
                    try:
                        Title=Correct(entry.title).encode('utf-8').rsplit("\n ")
                        if len(Title) == 1:
                            print ( "{} {}| href={}".format(EntryTitleIcon, Title[0], PDFurl) )
                        elif len(Title) == 2:
                            print ( "{} {}{}| href={}".format(EntryTitleIcon, Title[0],Title[1], PDFurl) )
                        else:
                            print ( "{} {:.150} {}".format(EntryTitleIcon, Title[0]+Title[1], " ...") )
                    except AttributeError:
                        print ( "{} {} {}| href={}".format(Nesting(2), Indentation(2),'No Title Found'.replace("\n",""), ABSurl)
                        )
                    
                    if (DisplayNew != 1):
                        # Updated Date
                        try:
                            print ( "{} {} Updated: {}| href={}".format(Nesting(2), Indentation(2), entry.updated, ABSurl).replace("\n","") )
                        except AttributeError:
                            print ( "{} {} Updated: {}| href={}".format(Nesting(2), Indentation(2),'No Updated Date Found'.replace("\n",""), ABSurl)
                            )
                        # Published Date
                        try:
                            print ( "{} {} Published: {}| href={}".format(Nesting(2), Indentation(2), entry.published, OriginalABSurl).replace("\n","") )
                        except AttributeError:
                            print ( "{} {} Published: {}| href={}".format(Nesting(2), Indentation(2),'No Published Date Found'.replace("\n",""), ABSurl)
                            )
                    else:
                        # Published Date
                        try:
                            print ( "{} {} Published: {}| href={}".format(Nesting(2), Indentation(2), entry.published, OriginalABSurl).replace("\n","") )
                        except AttributeError:
                            print ( "{} {} Published: {}| href={}".format(Nesting(2), Indentation(2),'No Published Date Found'.replace("\n",""), ABSurl)
                            )
                        # Updated Date
                        try:
                            print ( "{} {} Updated: {}| href={}".format(Nesting(2), Indentation(2), entry.updated, ABSurl).replace("\n","") )
                        except AttributeError:
                            print ( "{} {} Updated: {}| href={}".format(Nesting(2), Indentation(2),'No Updated Date Found'.replace("\n",""), ABSurl)
                            )

                    # feedparser v5.0.1 correctly handles multiple authors, print them all
                    try:
                        Authors=', '.join(Correct(author.name) for author in entry.authors).encode('utf-8').replace("\n","").rsplit(', ')
                        if len(Authors) < AuthorsLenght :
                            print ( "{} {} Authors: {:.150}| href={}".format(Nesting(2), Indentation(2), ', '.join(Authors), ABSurl)
                            )
                        else :
                            AuthorsTemp=Authors[:AuthorsLenght]
                            print ( "{} {} Authors: {:.150}{}| href={}".format(Nesting(2), Indentation(2), ', '.join(AuthorsTemp),", ...", ABSurl)
                            )
                    except AttributeError:
                        print ( "{} {} Authors: {}| href={}".format(Nesting(2), Indentation(2),'No Authors Found'.replace("\n",""), ABSurl)
                        )

                    # Since the <arxiv:primary_category> element has no data, only
                    # attributes, feedparser does not store anything inside
                    # entry.arxiv_primary_category
                    # This is a dirty hack to get the primary_category, just take the
                    # first element in entry.tags.  If anyone knows a better way to do
                    # this, please email the list!
                        
                    # Primary Category, not activated, remove "#" to activate
                    #print ( "{} {} Primary Category: {}| href={}".format(Nesting(2), Indentation(2), entry.tags[0]['term'].encode('utf-8'), ABSurl)
                    #)
            
                    # All Categories
                    all_categories = [t['term'] for t in entry.tags]
                    try:
                        print ( "{} {} Categories: {:.150}| href={}".format(Nesting(2), Indentation(2), (', ').join(all_categories).replace("\n",""), ABSurl)
                        )      
                    except AttributeError:
                        print ( "{} {} Categories: {}| href={}".format(Nesting(2), Indentation(2),'No Categories Found'.replace("\n",""), ABSurl)
                        )          

                    # The abstract is in the <summary> element
                    Abstract=Correct(entry.summary).encode('utf-8').rsplit("\n")
                    try:
                        print ( "{} {} Abstract: | href={}".format(Nesting(2), Indentation(2), ABSurl)
                        )
                        for i in range(0, len(Abstract)):
                            while (Abstract[i][0] == " "):
                                Abstract[i] = Abstract[i][1:]
                            print ( "{} {}{}| href={}".format(Nesting(2), Indentation(4), Abstract[i], ABSurl)
                            )   
                    except AttributeError:
                        print ( "{} {} Abstract: {}| href={}".format(Nesting(2), Indentation(2),'No Abstract Found'.replace("\n",""), ABSurl)
                        )
                
                    # Print Comments
                    try:
                        print ( "{} {} Comments: {}| href={}".format(Nesting(2), Indentation(2), Correct(entry.arxiv_comment).encode('utf-8').replace("\n",""), ABSurl)
                        )
                    except AttributeError:
                        print ( "{} {} Comments: {}| href={}".format(Nesting(2), Indentation(2),'No Comments Found'.replace("\n",""), ABSurl)
                        )

                    # Print Affiliation
                    try:
                        print ( "{} {} Affiliation: {}| href={}".format(Nesting(2), Indentation(2), entry.arxiv_affiliation, ABSurl).replace("\n","") )
                    except AttributeError:
                        pass

                    # Print DOI Link and the journal reference, comments and primary_category sections live under the arxiv namespace
                    try:
                        print ( "{} {} Journal Reference: {}| href={}".format(Nesting(2), Indentation(2), Correct(entry.arxiv_journal_ref).encode('utf-8').replace("\n",""), DOIurl)
                        )    
                        print ( "{} {} Link DOI: {}| href={}".format(Nesting(2), Indentation(2), colored(DOIurl, LinkColor, attrs=LinkAttributes).encode('utf-8').replace("\n",""), DOIurl)
                        )                  
                    except AttributeError:
                        print ( "{} {} Journal Reference: {}| href={}".format(Nesting(2), Indentation(2), 'No Journal Refence Found'.replace("\n",""), ABSurl)
                        )
                        print ( "{} {} Link DOI: {}| href={}".format(Nesting(2), Indentation(2), 'Only arXiv DOI Found'.replace("\n",""), ABSurl)
                        )                              

                    # Print ABS Link
                    try:
                        print ( "{} {} Link ABS: {}| href={}".format(Nesting(2), Indentation(2), colored(ABSurl, LinkColor, attrs=LinkAttributes).encode('utf-8').replace("\n",""), ABSurl)
                        )
                    except AttributeError:
                        print ( "{} {} Link ABS: {}| href={}".format(Nesting(2), Indentation(2), 'No ABS Link Found'.replace("\n",""), PDFurl)
                        )            

                    # Print PDF Link
                    try:
                        print ( "{} {} Link PDF: {}| href={}".format(Nesting(2), Indentation(2), colored(PDFurl, LinkColor, attrs=LinkAttributes).encode('utf-8').replace("\n",""), PDFurl) 
                    )
                    except AttributeError:
                        print ( "{} {} Link PDF: {}| href={}".format(Nesting(2), Indentation(2), 'No PDF Found'.replace("\n",""), ABSurl)
                        )                      


        if (DisplayOrder[order] == "FrontPage"):
            # arXiv Front Page
            print(Nesting(3))
            print(
            "{} arXiv - Front Page | href={}".format(FrontPageIcon, arXiv_url)
            )

        if (DisplayOrder[order] == "Legend"):
            # Print out Legend Information
            print(Nesting(3))
            if ((DisplayLegend == 1) and (TitlesIcon != "")):
                TitlesIconLeg = TitlesIcon

                if (TitlesWeekIconVar[2] != 1):
                    TitlesWeekIconLeg = TitlesIconLeg
                else:
                    TitlesWeekIconLeg = TitlesWeekIcon

                if (TitlesNewIconVar[2] != 1):
                    TitlesNewIconLeg = TitlesWeekIconLeg
                else:
                    TitlesNewIconLeg = TitlesNewIcon

                if (TitlesNewestIconVar[2] != 1):
                    TitlesNewestIconLeg = TitlesNewIconLeg
                else:
                    TitlesNewestIconLeg = TitlesNewestIcon

                if (TitlesUpdatedMonthIconVar[2] != 1):
                    TitlesUpdatedMonthIconLeg = TitlesIconLeg
                else:
                    TitlesUpdatedMonthIconLeg = TitlesUpdatedMonthIcon

                if (TitlesUpdatedWeekIconVar[2] != 1):
                    TitlesUpdatedWeekIconLeg = TitlesUpdatedMonthIconLeg
                else:
                    TitlesUpdatedWeekIconLeg = TitlesUpdatedWeekIcon     

                print ("{} Legend: | href={}".format(LegendIcon, arXiv_url) )
                if (DisplayNew == 1):
                    print (".           Published:           {}   :   in 1 Day,           {}   :   in   {} Days,          {}   :   in {} Days,          {}   :   More than {} Days. | href={}".format(TitlesNewestIconLeg, TitlesNewIconLeg, DaysNew, TitlesWeekIconLeg, DaysWeekNew, TitlesIconLeg, DaysWeekNew, arXiv_url) )
                if (DisplayUpdated == 1):
                    print (".             Updated:           {}   :   in {} Days,         {}   :   in {} Days. | href={}".format(TitlesUpdatedWeekIconLeg, DaysUpdatedWeek, TitlesUpdatedMonthIconLeg, DaysUpdatedMonth, arXiv_url) )

        if (DisplayOrder[order] == "Feed"):
            # Print out Feed Last Updated Information
            print(Nesting(3))
            if (DisplayFeed == 1):
                response = urllib.urlopen(base_API_url).read()
                feed = feedparser.parse(response)
                print ("{} Feed Last Updated: {} | href={}".format(FeedIcon, feed.feed.updated, arXiv_url) )

main()