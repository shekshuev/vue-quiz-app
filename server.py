import tkinter as tk
from flask import Flask
from flask_cors import CORS, cross_origin
from werkzeug.serving import make_server
import threading

webapp = Flask(__name__)
CORS(webapp)

@webapp.route('/', defaults={'path': ''})
@webapp.route('/<path:path>')
def catch_all(path):
    return webapp.send_static_file("index.html")

@webapp.get('/categories')
@cross_origin()
def get_category():
    return webapp.send_static_file("categories.json")

@webapp.get('/questions')
@cross_origin()
def get_questions():
    return webapp.send_static_file("questions.json")

def flask_main():
    webapp.run(port=8088)

class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('0.0.0.0', 8088, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Программа для тестирования")
        window_height = 100
        window_width = 300
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = int((screen_width/2) - (window_width/2))
        y_coordinate = int((screen_height/2) - (window_height/2))
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
        self.create_widgets()
        self.server = None

    def create_widgets(self):
        self.start_server_button = tk.Button(self.master, text="Запустить сервер", state=tk.NORMAL, command=self.start_server)
        self.start_server_button.pack(fill=tk.X, padx=10, pady=10)
        self.stop_server_button = tk.Button(self.master, text="Остановить сервер", state=tk.DISABLED, command=self.stop_server)
        self.stop_server_button.pack(fill=tk.X, padx=10)


    def start_server(self):
        self.start_server_button.config(state=tk.DISABLED)
        self.stop_server_button.config(state=tk.NORMAL)
        self.server = ServerThread(webapp)
        self.server.start()
        

    def stop_server(self):
        self.start_server_button.config(state=tk.NORMAL)
        self.stop_server_button.config(state=tk.DISABLED)
        self.server.shutdown()

def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()