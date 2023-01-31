''' You work at a company that sends daily reports to clients via email. The goal of this project is to automate the process of sending these reports via email.

Here are the steps you can take to automate this process:

    Use the smtplib library to connect to the email server and send the emails.

    Use the email library to compose the email, including the recipient's email address, the subject, and the body of the email.

    Use the os library to access the report files that need to be sent.

    Use a for loop to iterate through the list of recipients and send the email and attachment.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the emails that have been sent and any errors that may have occurred during the email sending process. '''


# import modules 
import smtplib, os, schedule, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date
import email_log


running = True

# multipart instance for email
message = MIMEMultipart()

# credentials
sender_email = "adapalapavan5@gmail.com"
receiver_email = ["pavankumar.biw@gmail.com","pavankumaradapala.deu@gmail.com"]
# use your own password value
password = os.environ.get('EMAIL_PASSWORD_CODE')
body_txt = f"Hello, here are {date.today()} daily reports."

# message preparattion
def message_preparation():
    message['From'] = sender_email
    if len(receiver_email) > 1:
        message['To'] = ",".join(receiver_email)
    else:
        message['To'] = receiver_email
    message['Subject'] = f"{date.today()} daily reports."
    body = body_txt
    message.attach(MIMEText(body,'plain'))

# attach files to email
def attach_files(report_files):
    for file in report_files:
        part = MIMEBase('application','octet-stream')
        # attaching files
        try:
            with open(file,'rb') as attachment:
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',"attachment; filename= "+file)
                message.attach(part)
                email_log.logger.info(f"{file} attached to email")
        except FileNotFoundError as e:
            email_log.logger.exception("Exception Occured")
        except FileExistsError as err:
            email_log.logger.exception("Exception Occured")


# To get report files
def reportfiles_list(path:str):
    files_list = []
    if os.path.exists(path):
        for file in os.listdir(path):
            files_list.append(os.path.join(path,file))
            email_log.logger.info(f"{file} appended")
    else:
        print(f"{path} not exist")
    return files_list




def main_function():

    message_preparation()

    # calling the reportfiles function
    path = "C:\\Users\\Adapala\\Desktop\\Scholarship_app_Adapala\\"
    report_files = reportfiles_list(path)

    if len(report_files) != 0:
        attach_files(report_files)
    else:
        print(f"No files presented in {path}")

    text = message.as_string()


    # SMTP server instance
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        if password == None:
            print("email password not available")
        else:          
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        server.quit()
    except smtplib.SMTPException as e:
        email_log.logger.exception("Exception Occured")



    global running
    running = False
    print("stopped")
    return schedule.CancelJob

schedule.every(5).minutes.do(main_function)

# schedule.every().day.at("06:00").do(main_function)


while running:
    schedule.run_pending()
    time.sleep(1)
