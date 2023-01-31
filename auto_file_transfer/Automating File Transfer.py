''' You work at a company that receives daily data files from external partners. These files need to be processed and analyzed, but first, they need to be transferred to the company's internal network.

The goal of this project is to automate the process of transferring the files from an external FTP server to the company's internal network.

Here are the steps you can take to automate this process:

    Use the ftplib library to connect to the external FTP server and list the files in the directory.

    Use the os library to check for the existence of a local directory where the files will be stored.

    Use a for loop to iterate through the files on the FTP server and download them to the local directory using the ftplib.retrbinary() method.

    Use the shutil library to move the files from the local directory to the internal network.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the files that have been transferred and any errors that may have occurred during the transfer process. '''

# importing required modules
import ftplib, socket, shutil, os, schedule, time
# custom logger import 
# import log
# default logging
import logging

"""
# default logging configurations
FORMAT = "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"
FILE_PATH = r"E:\Pavan Learnings\Braineest\week_01\auto_file_transfer\filelog.log"

logging.basicConfig(level=logging.DEBUG,filename=FILE_PATH,format=FORMAT)
"""

""" Inline custom logger that means the logger code also writing in the same file.
    the best way is to create separate file than import the file like (I done like line 22)"""
# inline custom logger
logger = logging.getLogger(__name__)

# set logger level
logger.setLevel(logging.DEBUG)

# create filehandler to store logs
f_handler = logging.FileHandler(r"E:\Pavan Learnings\Braineest\week_01\auto_file_transfer\filelog.log")

# create formatters and add it to handlers
f_format = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
f_handler.setFormatter(f_format)

# add handlers to the logger
logger.addHandler(f_handler)



running = True

# createing a server instance
remote_server = ftplib.FTP()


# FTP server connection
def ftp_server(hostname: str):
        
    # connection
    try:
        server_connection = remote_server.connect(hostname)
        # print(server_connection)
        # custom logger line
        # log.logger.info("server connection information:",server_connection)
        # Inline custom logger line
        logger.info(f"server connection information: {server_connection}")
    except socket.gaierror as connection_error:
        # print(connection_error)
        # custom logger line
        # log.logger.exception("Exception occured")
        # Inline custom logger line
        logger.exception("Exception occured")

    # login
    server_login = remote_server.login()
    # print(server_login)
    # custom logger line
    # log.logger.info("server login information:",server_login)
    # Inline custom logger line
    logger.info(f"server login information: {server_login}")


# check the preesent working directory
def current_directory():
    return remote_server.pwd()

# change working directory to Pub
def change_directory(path: str):
    try:
        remote_server.cwd(path)
    except ftplib.error_perm as path_error:
        # print(path_error)
        # custom logger line
        # log.logger.exception("exception occured")
        # Inline custom logger line
        logger.exception("exception occured")
    finally:
        return current_directory()    
    
# Use the shutil library to move the files from the local directory to the internal network.
def move_files(local_dir:str,file:str,remote_dir:str):
    print(remote_dir)
    try:
        moving_status = shutil.move(os.path.join(local_dir,file),remote_dir)
        # print(moving_status)
        # custom logger line
        # log.logger.info("files moving status:",moving_status)
        # Inline custom logger line
        logger.info(f"files moving status: {moving_status}")
    except shutil.Error as e:
        # print(e)
        # custom logger line
        # log.logger.exception("Exception occured")
        # Inline custom logger line
        logger.exception("Exception occured")

# download files from remote server
def download_to_local(working_dir,remote_dir):
    print(working_dir)
    for item in remote_server.nlst():
        with open(item,"wb") as file:
            try:
                download_status = remote_server.retrbinary(f"RETR {item}",file.write)
                # print(download_status)
                # custom logger line
                # log.logger.info(f"{download_status} file downloaded")
                # Inline custom logger line
                logger.info(f"{download_status} file downloaded")
            except ftplib.error_perm as e:
                # print(e)
                # custom logger line
                # log.logger.exception("exception occured")
                # Inline custom logger line
                logger.exception("exception occured")

        move_files(os.getcwd(),item,remote_dir)



# function for file transfer
def automate_file_trnasfer():
    # call ftp_server to make connection
    ftp_server("ftp.us.debian.org")

    # call current_directory function to know current working directory
    root_working_directory = current_directory()
    print("root_working_directory:",root_working_directory)

    # change working directory 
    new_working_directory = change_directory('debian')
    print("current working_directory:",new_working_directory)

    # checking the local directory existed or not. calling download_to_local function
    target_local_directory = "D:\\autocad"
    if os.path.exists(target_local_directory):
        if os.path.isdir(target_local_directory):
            if root_working_directory != new_working_directory:
                download_to_local(new_working_directory,target_local_directory)
            else:
                download_to_local(root_working_directory,target_local_directory)
        else:
            print(f"{target_local_directory} is not a directory")
    else:
        print(f"{target_local_directory} does not exist")

    # remote server quit
    remote_server.quit()

    global running
    running = False
    print("Stopped")
    return schedule.CancelJob

schedule.every(5).minutes.do(automate_file_trnasfer)

while running:
    schedule.run_pending()
    time.sleep(1)
