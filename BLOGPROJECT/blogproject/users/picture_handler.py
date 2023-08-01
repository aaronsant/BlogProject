''' blogproject/users/picture_handlers 
This file provides the functionallity for uploading profile pictures
'''
import os
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload,username):
    #rename uploaded pic to 'username' . 'file extension'
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(username)+'.'+ext_type
    
    #send uploaded pic to static/profile_pics with the username labeled filename
    filepath = os.path.join(current_app.root_path,'static/profile_pics',storage_filename)
    
    output_size = (200,200) #picture size
    
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)
    
    return storage_filename