import threading
import subprocess
import tkinter as tk
from tkinter import ttk


class PingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("DosGUI")

        # Estilos personalizados
        self.root.configure(bg="#F0F0F0")
        self.root.option_add("*TCombobox*Listbox*Background", "#FFFFFF")
        self.root.option_add("*TCombobox*Listbox*Foreground", "#000000")

        style = ttk.Style()
        style.configure("TFrame", background="#F0F0F0")
        style.configure("TLabel", background="#F0F0F0")
        style.configure("TButton", background="#007ACC", foreground="white")

        # Frame principal
        main_frame = ttk.Frame(self.root, padding=10, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Cuadro de entrada de IP/URL, tamaño de paquete y número de hilos
        input_frame = ttk.Frame(main_frame, style="TFrame")
        input_frame.pack(fill=tk.X, pady=10)

        target_label = ttk.Label(input_frame, text="IP/URL:", style="TLabel")
        target_label.pack(side=tk.LEFT, padx=5)

        self.target_entry = ttk.Entry(input_frame)
        self.target_entry.pack(side=tk.LEFT, padx=5)

        packet_size_label = ttk.Label(input_frame, text="Tamaño de paquete:", style="TLabel")
        packet_size_label.pack(side=tk.LEFT, padx=5)

        self.packet_size_entry = ttk.Entry(input_frame, width=10)
        self.packet_size_entry.insert(tk.END, "64")
        self.packet_size_entry.pack(side=tk.LEFT, padx=5)

        packet_count_label = ttk.Label(input_frame, text="Número de paquetes:", style="TLabel")
        packet_count_label.pack(side=tk.LEFT, padx=5)

        self.packet_count_entry = ttk.Entry(input_frame, width=10)
        self.packet_count_entry.insert(tk.END, "4")
        self.packet_count_entry.pack(side=tk.LEFT, padx=5)

        protocol_label = ttk.Label(input_frame, text="Protocolo:", style="TLabel")
        protocol_label.pack(side=tk.LEFT, padx=5)

        self.protocol_combo = ttk.Combobox(input_frame, values=["IP", "HTTP", "HTTPS"])
        self.protocol_combo.current(0)
        self.protocol_combo.pack(side=tk.LEFT, padx=5)

        threads_label = ttk.Label(input_frame, text="Número de threads:", style="TLabel")
        threads_label.pack(side=tk.LEFT, padx=5)

        self.threads_entry = ttk.Entry(input_frame, width=10)
        self.threads_entry.insert(tk.END, "1")
        self.threads_entry.pack(side=tk.LEFT, padx=5)

        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=10)

        ping_button = ttk.Button(button_frame, text="Iniciar Pings", command=self.start_ping, style="TButton")
        ping_button.pack(side=tk.LEFT, padx=10)

        # Cuadro de resultados
        results_frame = ttk.Frame(main_frame, style="TFrame")
        results_frame.pack(fill=tk.BOTH, expand=True)

        self.results_text = tk.Text(results_frame, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        self.ping_threads = []  # Lista de threads de ping
        self.ping_running = False  #  controlar la ejecución de los pings

    def start_ping(self):
        if self.ping_running:
            return

        target = self.target_entry.get()
        packet_size = self.packet_size_entry.get()
        packet_count = self.packet_count_entry.get()
        protocol = self.protocol_combo.get()
        threads = self.threads_entry.get()

        if not target:
            return

        self.ping_running = True

        # Iniciar pings en threads separados
        for _ in range(int(threads)):
            ping_thread = threading.Thread(target=self.run_ping, args=(target, packet_size, packet_count, protocol))
            ping_thread.start()
            self.ping_threads.append(ping_thread)

    def stop_ping(self):
        self.ping_running = False

    def run_ping(self, target, packet_size, packet_count, protocol):
        if protocol == "IP":
            command = ["ping", "-c", packet_count, "-s", packet_size, target]
        elif protocol == "HTTP":
            command = ["curl", "-I", target]
        elif protocol == "HTTPS":
            command = ["curl", "-I", "-k", target]
        else:
            return

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        # Mostrar resultados en tiempo real
        for line in process.stdout:
            self.results_text.insert(tk.END, line)
            self.results_text.see(tk.END)

        process.kill()


if __name__ == "__main__":
    root = tk.Tk()
    PingTool(root)
    root.mainloop()
