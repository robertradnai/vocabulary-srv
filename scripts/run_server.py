from vocabulary_srv import create_app
import os
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    os.chdir("..")
    create_app().run(debug=True)
