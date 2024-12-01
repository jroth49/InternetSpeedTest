import speedtest
import sys
import datetime
import os
import socket
import smtplib
from email.mime.text import MIMEText

#functions
def check_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_048_576 # Convert to Mbps
    upload_speed = st.upload() / 1_048_576 # Convert to Mbps
    ping = st.results.ping
    return [download_speed, upload_speed, ping]

def get_timestamp():
    return datetime.datetime.now()

def get_date():
    return get_timestamp().strftime('%Y-%m-%d')

def get_connected_devices():
    return 1

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'sender' #replace with sender email
    msg['To'] = 'recipient' #replace with recipient email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login('user', 'password') #replace with gmail user/password
        smtp_server.sendmail('sender', 'recipient', msg.as_string()) #replace with sender/recipient emails
    
#main code
def main():

    timestamp = get_timestamp()
    day = get_date()
    file_path = f'reports/{day}.txt'

    file_exists = os.path.isfile(file_path) #check if the files been created yet

    if not file_exists: #create file if it hasn't been created yet
        with open(file_path, 'w') as f:
            f.write(str(timestamp) + ' : Creating Log...\n')
        f.close()

    try:
        if sys.argv[1] == '1': #run speed test then append to file

            results = check_speed()
            check_timestamp = get_timestamp()
            download_speed = results[0]
            upload_speed = results[1]
            ping = results[2]

            with open(file_path, 'a') as f:
                f.write(str(check_timestamp) + ' : ************* Running Speed Test *************\n')
                f.write(str(check_timestamp) + f' : Download Speed = {download_speed:.2f} Mbps\n')
                f.write(str(check_timestamp) + f' : Upload Speed = {upload_speed:.2f} Mbps\n')
                f.write(str(check_timestamp) + f' : Ping = {ping} ms\n')
                f.write(str(check_timestamp) + ' : ************* End Speed Test *************\n')
            f.close()
            
        elif sys.argv[1] == '2': # send email to email
            body = ''
            
            with open (file_path, 'r') as f:
                body = f.read()
            f.close()

            send_email(f'{day}_log_file', body)

        else:
            raise Exception 
    except Exception as e:
        print(str(e))


main()