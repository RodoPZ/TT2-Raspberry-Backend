from fileinput import filename
from firebase_admin import initialize_app, storage
from firebase_admin import storage as admin_storage, credentials, firestore

cred = credentials.Certificate("tt2-database-31516e0b99db.json") #descargar de https://console.cloud.google.com/iam-admin/serviceaccounts/details/101070432244239069365/keys?project=tt2-database
initialize_app(cred, {'storageBucket': 'tt2-database.appspot.com'})

def checkModel(fileName):
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    fileExists = blob.exists()
    return fileExists

def uploadFile(fileName):
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    
def download(fileName): 
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.download_to_filename(fileName)

def delete(fileName):
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.delete()
