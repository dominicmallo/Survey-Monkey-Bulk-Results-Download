# Survey-Monkey-Bulk-Results-Download
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
