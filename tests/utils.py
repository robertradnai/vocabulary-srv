import os
import shutil

def reset_test_env():
    # Delete and re-create test data folder so that the app can't accidentally
    #  overwrite the original test data.
    test_data = 'testdata'
    temp_folder = 'testdata_temp'
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    shutil.copytree(test_data, temp_folder)
