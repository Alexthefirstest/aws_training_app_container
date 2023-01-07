import os
import shutil

base_path = r'../deploy/'

# if os.path.exists(r'%s' % base_path): #remove if created
#     shutil.rmtree(base_path)

os.makedirs(base_path)

shutil.copytree('../extra_files', base_path+'/extra_files')
shutil.copytree('../app', base_path+'/app')