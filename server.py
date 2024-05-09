import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>test</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.client_address[0], "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Программа длоя тестирования")
        window_height = 768
        window_width = 1024
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = int((screen_width/2) - (window_width/2))
        y_coordinate = int((screen_height/2) - (window_height/2))
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
        self.create_widgets()
        self.http = HTTPServer(('', 8088), HttpHandler)

    def create_widgets(self):
        frame = tk.Frame(self.master)
        frame.pack(fill=tk.X, padx=10, pady=10)
        self.select_files_button = tk.Button(frame, text="Выбрать файлы", command=self.select_files)
        self.select_files_button.grid(row=0, column=0)
        self.selected_files_label = tk.Label(frame, text="Файлы не выбраны")
        self.selected_files_label.grid(row=0, column=1)
        self.start_server_button = tk.Button(frame, text="Запустить сервер", state=tk.DISABLED, command=self.start_server)
        self.start_server_button.grid(row=1, column=0)
        self.stop_server_button = tk.Button(frame, text="Остановить сервер", state=tk.DISABLED, command=self.stop_server)
        self.stop_server_button.grid(row=1, column=1)
        self.tree = ttk.Treeview(self.master, columns=('id', 'ip', 'variant', 'count'), show='headings')
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.tree.heading("id", text='Номер')
        self.tree.heading("ip", text='IP адрес')
        self.tree.heading("variant", text='Вариант')
        self.tree.heading("count", text='Ответы')


    def select_files(self):
        files = filedialog.askopenfilenames()
        if len(files) > 0:
            self.selected_files_label.config(text=f"Выбрано {len(files)} файлов")
        else:
            self.selected_files_label.config(text="Файлы не выбраны")
        self.start_server_button.config(state=tk.NORMAL)

    def start_server(self):
        self.start_server_button.config(state=tk.DISABLED)
        self.stop_server_button.config(state=tk.NORMAL)
        self.select_files_button.config(state=tk.DISABLED)
        threading.Thread(target=self.http.serve_forever, daemon=True).start()

    def stop_server(self):
        self.start_server_button.config(state=tk.NORMAL)
        self.stop_server_button.config(state=tk.DISABLED)
        self.select_files_button.config(state=tk.NORMAL)
        self.http.server_close()

def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()