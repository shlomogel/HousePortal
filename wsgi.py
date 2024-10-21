from portal import app
from waitress import serve
import webbrowser
import threading
import time


def open_browser():
    time.sleep(1)
    webbrowser.open("http://localhost:9999")


if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    serve(app, host="0.0.0.0", port=8080)
