#2020 Dominic Mallo

print(r"""

                        _
                    ,.-" "-.,
                   /   ===   \
                  /  =======  \
               __|  (o)   (0)  |__      
              / _|    .---.    |_ \         ____________________________________________________________________________________________________
             | /.----/ O O \----.\ |       /                                                                                                    \
              \/     |     |     \/        |Manually downloading Survey Monkey results as a pdf SUCKS because they do not have a native method! |
              |                   |        |So I, Dominic Mallo, created this Windows Python script to bulk que and log the download links      |
              |                   |        |You must have a directory called C:\1IT\SurveyMonkey\Day201902 or modify line 40                    |
              |                   |        |The download links are saved to downloadLinks.txt in the specified directory                        |
              _\   -.,_____,.-   /_        |As the script runs, you will see stats on which survey is being queued for download                 | 
          ,.-"  "-.,_________,.-"  "-.,    |Once the Survey Monkey servers have all the PDFs ready, you can download them with the logged link  |
         /          |       |          \   |                                                                                                    |
        |           l.     .l           |  |Before running...                                                                                   | 
        |            |     |            |  |Modify the cookies.env file with your Survey Monkey 'ep203' (line 1) and 'auth' (line 2) VALUES     |
        l.           |     |           .l  |Modify the surveyStartLinks.txt file with the Survey Monkey management URLs you want the results for| 
         |           l.   .l           | \,|See the included screenshots for additional help                                                    |
         l.           |   |           .l   \,___________________________________________________________________________________________________/
          |           |   |           |      \,
          l.          |   |          .l        |
           |          |   |          |         |
           |          |---|          |         |
           |          |   |          |         |
           /"-.,__,.-"\   /"-.,__,.-"\"-.,_,.-"\
          |            \ /            |         |
          |             |             |         |
           \__|__|__|__/ \__|__|__|__/ \_|__|__/

""")

input("Press enter to run...")

import requests,json,os,time,re,subprocess,sys

os.chdir(r"C:\1IT\SurveyMonkey\Day201902") # run directory

downloadLinks = []

try: #define cookies from cookies.env
        authCookieVars = open("cookies.env", "r")
        authCookieVars = authCookieVars.read().split('\n')

        authCookie = ('''ep203={};
                        auth={};
                        ''').replace('\n',' ').format(authCookieVars[0],authCookieVars[1])
except:
        print("[ERROR] There was an error parsing cookies.env or declaring your cookies. Ensure the values are valid and you have followed all the instructions.")
        sys.exit()


#define surveyStartLinks from surveyStartLinks.txt
surveyStartLinks = open("surveyStartLinks.txt", "r")
surveyStartLinks = surveyStartLinks.read().split('\n')

#survey progress counter
totalSurveys= len(surveyStartLinks)
thisSurvey = 0

#header table row
print("-------------------------------------------------------------------------------------------------------------------------------------------------")
print("[x/y] |  surveyID |  viewID   | surveyName")
print("-------------------------------------------------------------------------------------------------------------------------------------------------")

#main execution
for surveyURL in surveyStartLinks:
        try:
                if (surveyURL[0:37] == "https://www.surveymonkey.com/summary/") and ((surveyURL[-26:-1] + 't') == "?ut_source=my_surveys_list"): # ensure link is a survey monkey form link

                        #get survey metadata
                        url = (surveyURL.replace('/summary/','/analyze/summary/')).replace('?ut_source=my_surveys_list','/data.js?utc_offset=-14400000&_=1595644595665')
                        headers = {
                            'cookie': authCookie
                        }

                        response = requests.get(url, headers=headers)
                        response = response.text
                        response = json.loads(response)

                        #parse survey metadata
                        surveyID = response["data"]["survey_id"]
                        viewID = response["data"]["current_view_id"]
                        surveyName = response["data"]["survey_data"]["title"]
                        fileName = surveyName + ".pdf"
                        fileName = re.sub(r'[\\/*?:"<>|]',"",fileName)

                        thisSurvey = thisSurvey + 1
                        print("[" + str(thisSurvey) + "/" + str(totalSurveys) + "] | " + surveyID + " | " + viewID + " | " + surveyName) #show what survey we are on
                        print("-------------------------------------------------------------------------------------------------------------------------------------------------")
                        
                        #que a PDF generation

                        headers = {
                            'content-type': 'application/json',
                            'cookie': authCookie
                        }

                        data = '''{"survey_id":"!surveyIDHere!","view_id":"!viewIDHere!","exportjob":{"custom_filename":"!fileNameHere!","format":"pdf",
                                        "email":"null@example.com","export_data":{"orientation":"portrait","include_openended":false,
                                        "show_word_cloud":false,"dimension":"letter","zoomFactor":".95","forced_page_break":true,"marginTop":"15mm",
                                        "marginBottom":"15mm","headerSpacing":"3","footerSpacing":"2","phantomjs_pdf_enabled":false,"hide_branding":true,
                                        "multilingual":false,"use_cassandra":false,"respondent_count":17,"isCSVOnly":false,"package_type":"ADVANTAGE",
                                        "timezone_offset":14400000,"iana_tz":"America/New_York"},"export_type":"summary",
                                        "job_info":{"view_name":"Original View","pages":"All","questions":"All"},"type":"summary"}}'''
                        data = data.replace("!fileNameHere!", fileName) #include the desired fileName in the payload
                        data = data.replace("!surveyIDHere!", surveyID) #include the survey's surveyID in the payload
                        data = data.replace("!viewIDHere!", viewID) #include the survey's viewID in the payload

                        
                        response = requests.post('https://www.surveymonkey.com/analyze/ajax/export/create', headers=headers, data=data)
                        response = json.loads(response.text)

                        exportJobID = response["data"]["export_job"]["exportjob_id"] #parse exportJobID

                        #create download link and append to array for further use
                        downloadLink = ("https://www.surveymonkey.com/analyze/export/download/?survey_id={}&export_job_id={}").format(surveyID,exportJobID)
                        downloadLinks.append(downloadLink)
        except:
                thisSurvey = thisSurvey + 1
                errorMessage = "[ERROR] There was an error with " + surveyURL + ". Ensure the link is valid and you have follwed all the instructions"
                print("An error occured downloading this survey, logging surveyURL.")
                print("-------------------------------------------------------------------------------------------------------------------------------------------------")
                with open('errorLog.txt', 'w') as errorLog:
                        errorLog.write(errorMessage)

#write file download links to downloadLinks.txt     
with open('downloadLinks.txt', 'w') as downloadLinksFile:
        for downloadLink in downloadLinks:
                downloadLinksFile.write(downloadLink + "\n")
                

print("Next steps...")
print(("[1] {} survey PDF download links in file downloadLinks.txt").format(len(downloadLinks)))
print("[2] Ensure you are logged into Survey Monkey (must have an authentication cookie)")
print("[3] Copy the download links from downloadLinks.txt into a tool like openmultipleurl.com to bulk download all the PDFs. ")
input("Press enter to close...")
