from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from apikey import apikey
class YoutubeBot:
    CLIENT_SECRET_FILE = 'client_secret.json'
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_console()
    youtube = build('youtube', 'v3', credentials=credentials)

    def getVids(self):
        ids = [] #stores the video ids
        youtube = build('youtube', 'v3', developerKey=apikey)
        channelId = "UCdtYzLb2YIv97_NvMv2_OMQ"
        maxResults = 1
        request = youtube.search().list(part="snippet",channelId=channelId,maxResults=maxResults,order="date",type="video")
        response = request.execute()
        for item in response['items']:
            #print(item['snippet']['title'])
            ids.append((item['id']['videoId'], item['snippet']['channelId']))
        print(response)
        return ids
    def insert_comment(self, channel_id, video_id, text):
        self.youtube.commentThreads().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    channelId=channel_id,
                    videoId=video_id,
                    topLevelComment=dict(
                        snippet=dict(
                            textOriginal=text
                        )
                    )
                )
            )
        ).execute()	
			    
    def commentVids(self):
        print("---------------------------------------------")
        print("Startings CommentVideos")
        ids = self.getVids()
        message = "pythonでコメントを自動化"
        for id in ids:
            self.insert_comment(id[1], id[0], message)
        print("---------------------------------------------")
        print("End CommentVideos " + str(ids))
        print("---------------------------------------------")
        
bot = YoutubeBot()
bot.commentVids()
