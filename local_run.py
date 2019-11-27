import main
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def local_main():
    return main.entry_point(request=request)
