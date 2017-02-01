FLASK NOTE

# Installation:

利用conda創虛擬環境

$ conda create -n InteractiveWeb_flask python=3.5

$ source activate InteractiveWeb_flask

安裝

$ conda install -n InteractiveWeb_flask flask

測試

$ flask: 顯示幫助文件

$ vim hello.py`

`from flask import Flask    
app = Flask(__name__) 

@app.route('/')      
def hello_world():
    return 'Hello World'`

$ export FLASK_APP=hello.py

$ export FLASK_DEBUG=1

$ flask run
