import requests #http requests
from bs4 import BeautifulSoup #web scrapping
#send the mail
import smtplib
#email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#system date and time manipulation
import datetime
now= datetime.datetime.now() # to check that we dont recieve same mail everyday
#mail content placeholder
content='' #global variable
#extracting Hacker News stories
def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt=''#local variable
    cnt+=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response=requests.get(url)#sending reqeust to server
    content=response.content#storing contents of response in content
    soup=BeautifulSoup(content,'html.parser')
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+ '<a href"' + tag.a.get('href') + '">' + tag.text + '</a>' + "\n" + '<br>') if tag.text!='More' else'')
        #print(tag.prettify) #find_all("span",attrs={'class':'sitestr'})) #href=hu=yper reference kaha se link utha rahe hai #tag for href eg. a
    return(cnt)
cnt = extract_news('https://news.ycombinator.com/') #global variable
content += cnt 
content += ('<br>-------<br>')
content += ('<br><br>End if message')

#Sending the mail

print('Composing mail...')

#update your email details
#make sure to update the google low App Access setting before

SERVER = 'smtp.gmail.com' #your smtp server
PORT = 587 #entry point of a website the port number of smtp is 587
FROM = 'your mail' #your from email id
TO = 'receiver mail'
PASS = 'yourpassword'

# fp = open(file_name, 'rb')
#Create a text/plain message
# msg= MINEText('')
msg = MIMEMultipart()
 
# msg.add_header('Content-Disposition, 'attachment' , filename="empty.txt")
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
#fp.close()
#Kindly turn on less secure app acess
print('Initiating Server..')

server = smtplib.SMTP(SERVER, PORT)
#server = smtplip.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)# if u want to see error message then one and if u dont want then 0, seeing the error message helps u in debigging
server.ehlo() # connection establiishmnt
server.starttls() #start the process
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())
print('Email Sent..')
server.quit()