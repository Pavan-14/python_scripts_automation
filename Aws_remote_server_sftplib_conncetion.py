import ftplib
from ftplib import FTP
import os

# remote server details
HOSTNAME = "ec2-100-24-54-101.compute-1.amazonaws.com"
USER = "Administrator"
PASSWORD = "es63-BN7kf1p2TUsqhVN5PGVYJ9TZnZC"

# server connection test
with FTP(host=HOSTNAME) as ftp:
    ftp.encoding = "utf-8"
    try:
        login = ftp.login(user=USER,passwd=PASSWORD)
        print(login)
    except ftplib.error_perm as usererror:
        print(usererror)
    
    # getwelcome
    print(ftp.getwelcome())

    # retrieve files and directories ASCII transfer mode
    ftp.retrlines('LIST')

    # checking current working directory
    print(ftp.pwd())

    # list of directoris and file in current working directory
    ftp.dir()

    # create a directory
    try:
        ftp.mkd('clientdir')
    except ftplib.error_perm as resp:
        print(resp)

    # changing the working directory
    try:
        ftp.cwd('clientdir')
    except ftplib.error_perm as filenot:
        print(filenot)

    # the working directory changed to /clientdir
    print(ftp.pwd())
    

    # read file in binary mode 
    # trying to upload file from local server --> remote server

    if os.path.isfile(r"C:\Users\Adapala\Desktop\sample_text.txt"):
        with open(r'C:\Users\Adapala\Desktop\sample_text.txt','rb') as file:
            try:
                ftp.storbinary('STOR remote_sample_text.txt', file)
            except ftp.error_perm as presented:
                print(presented)
    else:
        print("sample_text.txt does not exist")

    ftp.dir()

    '''
    # delete file from the remote server

    response = ftp.delete('remote_sample_text.txt')
    print(response)

    ftp.dir()
    '''

    print(ftp.pwd())
    # download the file from remote server to local
    filename = 'remote_sample_text.txt'

    # directiory existed or not
    if os.path.isdir(r"D:\autocad"):
        local_file = os.path.join(r"D:\autocad",filename)
        with open(local_file, "wb") as new_file:
        # Command for Downloading the file "RETR filename"
            try:
                ftp.retrbinary(f"RETR {filename}", new_file.write)
            except ftplib.error_perm as e:
                print(e)
    else:
        print("autocad directory not existed")

    # Display the content of downloaded file
    file = open(filename, "r")
    print('File Content:', file.read())

# created a new directory
    try:
        ftp.mkd('newdir')
    except ftplib.error_perm as res:
        print(res)

# check the nlst giving only files or files and directories
    print(ftp.nlst())
