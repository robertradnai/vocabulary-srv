Introduction


# User guide
## Installation
- You can install the application from source, 
  after cloning the repository
```shell script
git clone https://github.com/robertradnai/vocabulary-srv.git
cd vocabulary-srv
pip install -e
```

## Configuration and example run
  - The app looks for `config.py` in the current working directory. 
    For an example configuration, see **this file ###**.
```shell script
FLASK_APP="vocabulary_srv:create_app()"
flask run
```







## Developer guide
### Setting up the development environment
Installing a specific Python version
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10
sudo apt install python3.10-venv
sudo apt install python3.10-dev
```


### Testing
### Building the Docker image: `make build`
