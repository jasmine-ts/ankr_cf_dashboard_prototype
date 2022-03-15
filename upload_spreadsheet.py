import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def main():
    args = sys.argv[1:]

    upload_file = str(args[0])

    gfile = drive.CreateFile({'parents': [{'id': '1UQ2cMXzcTsy5Zgw08k415RrDdCH_JJP7'}]})
    gfile.SetContentFile(upload_file)
    gfile.Upload() # Upload the file.

if __name__ == "__main__":
    main()