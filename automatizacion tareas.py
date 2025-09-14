import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import shutil
import hashlib
import threading
import subprocess
import sys
from datetime import datetime
import json
import webbrowser

class TaskAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoTask - Sistema de Automatización de Tareas")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        # Configuración de estilos
        self.setup_styles()
        
        # Variables
        self.selected_folder = tk.StringVar()
        self.task_in_progress = False
        self.config_file = "autotask_config.json"
        self.saved_scripts = []
        
        # Cargar configuración
        self.load_config()
        
        # Crear interfaz
        self.create_widgets()
        
        # Actualizar log
        self.update_log("AutoTask iniciado. Seleccione una carpeta y una tarea.")
        self.update_log(f"Carpeta predefinida: {self.selected_folder.get()}")
    
    def setup_styles(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('TFrame', background='#f0f0f0')
        style.configure('Title.TLabel', background='#f0f0f0', font=('Arial', 18, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', background='#f0f0f0', font=('Arial', 11, 'bold'), foreground='#34495e')
        style.configure('TButton', font=('Arial', 10), padding=6)
        style.configure('Action.TButton', font=('Arial', 10, 'bold'), background='#3498db', foreground='white')
        style.configure('Success.TButton', background='#2ecc71', foreground='white')
        style.configure('Danger.TButton', background='#e74c3c', foreground='white')
        
        style.map('Action.TButton', background=[('active', '#2980b9')])
        style.map('Success.TButton', background=[('active', '#27ae60')])
        style.map('Danger.TButton', background=[('active', '#c0392b')])
    
    def load_config(self):
        """Carga la configuración desde el archivo JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.selected_folder.set(config.get('last_folder', ''))
                    self.saved_scripts = config.get('saved_scripts', [])
            except:
                # Si hay error, usar valores por defecto
                self.selected_folder.set(os.path.expanduser("~/Documents"))
                self.saved_scripts = []
        else:
            self.selected_folder.set(os.path.expanduser("~/Documents"))
    
    def save_config(self):
        """Guarda la configuración en el archivo JSON"""
        config = {
            'last_folder': self.selected_folder.get(),
            'saved_scripts': self.saved_scripts
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid para expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="AutoTask", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Selección de carpeta
        ttk.Label(main_frame, text="Carpeta de trabajo:", style="Subtitle.TLabel").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        folder_frame.columnconfigure(0, weight=1)
        
        folder_entry = ttk.Entry(folder_frame, textvariable=self.selected_folder, font=('Arial', 10))
        folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(folder_frame, text="Examinar", command=self.browse_folder, style="Action.TButton").grid(
            row=0, column=1, padx=(5, 0))
        
        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        
        # Opciones de tareas
        ttk.Label(main_frame, text="Tareas de Automatización:", style="Subtitle.TLabel").grid(
            row=3, column=0, sticky=tk.W, pady=(0, 10))
        
        # Botones de tareas
        task_frame = ttk.Frame(main_frame)
        task_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Primera fila de botones
        ttk.Button(task_frame, text="Renombrar Archivos", command=self.rename_files, 
                  style="Action.TButton").grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(task_frame, text="Organizar por Tipo", command=self.organize_by_type, 
                  style="Action.TButton").grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(task_frame, text="Eliminar Duplicados", command=self.remove_duplicates, 
                  style="Action.TButton").grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Segunda fila de botones
        ttk.Button(task_frame, text="Limpiar Temporales", command=self.clean_temporals, 
                  style="Action.TButton").grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(task_frame, text="Ejecutar Script Python", command=self.run_python_script, 
                  style="Action.TButton").grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(task_frame, text="Ejecutar Script AHK", command=self.run_ahk_script, 
                  style="Action.TButton").grid(row=1, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Configurar expansión uniforme de columnas
        for i in range(3):
            task_frame.columnconfigure(i, weight=1)
        
        # Separador
        separator2 = ttk.Separator(main_frame, orient='horizontal')
        separator2.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        
        # Área de log
        ttk.Label(main_frame, text="Registro de Actividades:", style="Subtitle.TLabel").grid(
            row=6, column=0, sticky=tk.W, pady=(0, 10))
        
        # Área de texto con scrollbar
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, wrap=tk.WORD, width=85, height=15, 
            font=('Consolas', 10), bg='#2c3e50', fg='#ecf0f1', insertbackground='white'
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones de control
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=8, column=0, columnspan=3, pady=(15, 0))
        
        ttk.Button(control_frame, text="Abrir Carpeta", command=self.open_folder, 
                  style="Success.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Limpiar Log", command=self.clear_log, 
                  style="Action.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Guardar Log", command=self.save_log, 
                  style="Action.TButton").grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="GitHub", command=self.open_github, 
                  style="Action.TButton").grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Salir", command=self.quit_app, 
                  style="Danger.TButton").grid(row=0, column=4, padx=5)
    
    def update_log(self, message, message_type="info"):
        """Agrega un mensaje al registro con formato de colores"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Asignar color según el tipo de mensaje
        if message_type == "error":
            tag = "error"
            self.log_text.tag_config(tag, foreground="#e74c3c")
        elif message_type == "success":
            tag = "success"
            self.log_text.tag_config(tag, foreground="#2ecc71")
        elif message_type == "warning":
            tag = "warning"
            self.log_text.tag_config(tag, foreground="#f39c12")
        else:
            tag = "info"
            self.log_text.tag_config(tag, foreground="#3498db")
        
        # Insertar mensaje
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{message}\n", tag)
        
        # Auto-scroll al final
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Limpia el área de registro"""
        self.log_text.delete(1.0, tk.END)
        self.update_log("Log limpiado.")
    
    def save_log(self):
        """Guarda el registro en un archivo"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Archivos de log", "*.log"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.update_log(f"Log guardado en: {file_path}", "success")
            except Exception as e:
                self.update_log(f"Error guardando log: {str(e)}", "error")
    
    def browse_folder(self):
        """Abre un diálogo para seleccionar carpeta"""
        folder_path = filedialog.askdirectory(title="Seleccione una carpeta", initialdir=self.selected_folder.get())
        if folder_path:
            self.selected_folder.set(folder_path)
            self.update_log(f"Carpeta seleccionada: {folder_path}")
            self.save_config()
    
    def open_folder(self):
        """Abre la carpeta seleccionada en el explorador de archivos"""
        if self.selected_folder.get() and os.path.exists(self.selected_folder.get()):
            os.startfile(self.selected_folder.get())
            self.update_log("Carpeta abierta en el explorador")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una carpeta válida primero.")
            self.update_log("Intento de abrir carpeta fallido: carpeta no válida", "warning")
    
    def open_github(self):
        """Abre el perfil de GitHub en el navegador"""
        webbrowser.open("https://github.com")
        self.update_log("Navegador abierto hacia GitHub")
    
    def quit_app(self):
        """Cierra la aplicación guardando la configuración"""
        self.save_config()
        self.update_log("AutoTask finalizado. Configuración guardada.")
        self.root.quit()
    
    def validate_folder(self):
        """Valida que se haya seleccionado una carpeta válida"""
        if not self.selected_folder.get():
            messagebox.showwarning("Advertencia", "Por favor, seleccione una carpeta primero.")
            return False
        if not os.path.exists(self.selected_folder.get()):
            messagebox.showerror("Error", "La carpeta seleccionada no existe.")
            return False
        return True
    
    def rename_files(self):
        """Renombra archivos en la carpeta seleccionada"""
        if not self.validate_folder():
            return
        
        def rename_task():
            self.task_in_progress = True
            self.update_log("Iniciando renombrado de archivos...")
            
            try:
                folder = self.selected_folder.get()
                files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
                
                if not files:
                    self.update_log("No se encontraron archivos para renombrar", "warning")
                    return
                
                for i, filename in enumerate(files, 1):
                    name, ext = os.path.splitext(filename)
                    new_name = f"documento_{i:03d}{ext}"
                    old_path = os.path.join(folder, filename)
                    new_path = os.path.join(folder, new_name)
                    
                    # Evitar sobreescribir archivos existentes
                    counter = 1
                    while os.path.exists(new_path):
                        new_name = f"documento_{i:03d}_{counter}{ext}"
                        new_path = os.path.join(folder, new_name)
                        counter += 1
                    
                    os.rename(old_path, new_path)
                    self.update_log(f"Renombrado: {filename} -> {new_name}")
                
                self.update_log("Renombrado completado exitosamente.", "success")
            except Exception as e:
                self.update_log(f"Error durante el renombrado: {str(e)}", "error")
            finally:
                self.task_in_progress = False
        
        # Ejecutar en un hilo separado para no bloquear la interfaz
        threading.Thread(target=rename_task, daemon=True).start()
    
    def organize_by_type(self):
        """Organiza archivos por su extensión en subcarpetas"""
        if not self.validate_folder():
            return
        
        def organize_task():
            self.task_in_progress = True
            self.update_log("Organizando archivos por tipo...")
            
            try:
                folder = self.selected_folder.get()
                files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
                
                if not files:
                    self.update_log("No se encontraron archivos para organizar", "warning")
                    return
                
                for filename in files:
                    file_ext = os.path.splitext(filename)[1].lower()
                    if not file_ext:
                        file_ext = "sin_extension"
                    else:
                        file_ext = file_ext[1:]  # Quitar el punto
                    
                    # Crear carpeta si no existe
                    type_folder = os.path.join(folder, file_ext)
                    if not os.path.exists(type_folder):
                        os.makedirs(type_folder)
                        self.update_log(f"Creada carpeta: {file_ext}")
                    
                    # Mover archivo
                    old_path = os.path.join(folder, filename)
                    new_path = os.path.join(type_folder, filename)
                    
                    shutil.move(old_path, new_path)
                    self.update_log(f"Movido: {filename} -> {file_ext}/")
                
                self.update_log("Organización completada exitosamente.", "success")
            except Exception as e:
                self.update_log(f"Error durante la organización: {str(e)}", "error")
            finally:
                self.task_in_progress = False
        
        threading.Thread(target=organize_task, daemon=True).start()
    
    def remove_duplicates(self):
        """Elimina archivos duplicados basándose en su hash MD5"""
        if not self.validate_folder():
            return
        
        def remove_duplicates_task():
            self.task_in_progress = True
            self.update_log("Buscando y eliminando archivos duplicados...")
            
            try:
                folder = self.selected_folder.get()
                files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
                
                if not files:
                    self.update_log("No se encontraron archivos para analizar", "warning")
                    return
                
                hashes = {}
                duplicates_count = 0
                
                for filename in files:
                    file_path = os.path.join(folder, filename)
                    
                    # Calcular hash MD5
                    try:
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                    except:
                        self.update_log(f"No se pudo leer el archivo: {filename}", "warning")
                        continue
                    
                    # Si el hash ya existe, es un duplicado
                    if file_hash in hashes:
                        os.remove(file_path)
                        self.update_log(f"Eliminado duplicado: {filename}")
                        duplicates_count += 1
                    else:
                        hashes[file_hash] = filename
                
                self.update_log(
                    f"Eliminación de duplicados completada. Se eliminaron {duplicates_count} archivos.", 
                    "success" if duplicates_count > 0 else "info"
                )
            except Exception as e:
                self.update_log(f"Error durante la eliminación de duplicados: {str(e)}", "error")
            finally:
                self.task_in_progress = False
        
        threading.Thread(target=remove_duplicates_task, daemon=True).start()
    
    def clean_temporals(self):
        """Limpia archivos temporales en la carpeta seleccionada"""
        if not self.validate_folder():
            return
        
        def clean_temporals_task():
            self.task_in_progress = True
            self.update_log("Limpiando archivos temporales...")
            
            try:
                folder = self.selected_folder.get()
                temp_extensions = ['.tmp', '.temp', '.bak', '.backup', '.old']
                deleted_count = 0
                
                for root, dirs, files in os.walk(folder):
                    for filename in files:
                        if any(filename.lower().endswith(ext) for ext in temp_extensions):
                            file_path = os.path.join(root, filename)
                            try:
                                os.remove(file_path)
                                self.update_log(f"Eliminado temporal: {filename}")
                                deleted_count += 1
                            except:
                                self.update_log(f"No se pudo eliminar: {filename}", "warning")
                
                self.update_log(
                    f"Limpieza completada. Se eliminaron {deleted_count} archivos temporales.", 
                    "success" if deleted_count > 0 else "info"
                )
            except Exception as e:
                self.update_log(f"Error durante la limpieza: {str(e)}", "error")
            finally:
                self.task_in_progress = False
        
        threading.Thread(target=clean_temporals_task, daemon=True).start()
    
    def run_python_script(self):
        """Ejecuta un script Python seleccionado por el usuario"""
        script_path = filedialog.askopenfilename(
            title="Seleccione un script Python",
            filetypes=[("Python scripts", "*.py"), ("All files", "*.*")],
            initialdir=self.selected_folder.get()
        )
        
        if not script_path:
            return
        
        def run_python_task():
            self.task_in_progress = True
            self.update_log(f"Ejecutando script Python: {os.path.basename(script_path)}")
            
            try:
                # Ejecutar el script en un proceso separado
                working_dir = self.selected_folder.get() if self.selected_folder.get() else os.path.dirname(script_path)
                
                result = subprocess.run(
                    [sys.executable, script_path],
                    cwd=working_dir,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutos de timeout
                )
                
                if result.stdout:
                    self.update_log("Salida del script:", "info")
                    for line in result.stdout.splitlines():
                        self.update_log(f"  {line}", "info")
                
                if result.stderr:
                    self.update_log("Errores del script:", "error")
                    for line in result.stderr.splitlines():
                        self.update_log(f"  {line}", "error")
                
                exit_code = result.returncode
                if exit_code == 0:
                    self.update_log(f"Script ejecutado exitosamente. Código de salida: {exit_code}", "success")
                else:
                    self.update_log(f"Script finalizado con errores. Código de salida: {exit_code}", "error")
                    
            except subprocess.TimeoutExpired:
                self.update_log("El script excedió el tiempo máximo de ejecución (5 minutos).", "error")
            except Exception as e:
                self.update_log(f"Error ejecutando el script: {str(e)}", "error")
            finally:
                self.task_in_progress = False
        
        threading.Thread(target=run_python_task, daemon=True).start()
    
    def run_ahk_script(self):
        """Ejecuta un script de AutoHotkey seleccionado por el usuario"""
        script_path = filedialog.askopenfilename(
            title="Seleccione un script de AutoHotkey",
            filetypes=[("AHK scripts", "*.ahk"), ("All files", "*.*")],
            initialdir=self.selected_folder.get()
        )
        
        if not script_path:
            return
        
        # Verificar si AutoHotkey está instalado
        ahk_path = None
        possible_paths = [
            "C:\\Program Files\\AutoHotkey\\AutoHotkey.exe",
            "C:\\Program Files (x86)\\AutoHotkey\\AutoHotkey.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                ahk_path = path
                break
        
        if not ahk_path:
            messagebox.showerror("Error", "AutoHotkey no está instalado o no se pudo encontrar.")
            self.update_log("Error: AutoHotkey no está instalado", "error")
            return
        
        def run_ahk_task():
            self.task_in_progress = True
            self.update_log(f"Ejecutando script AHK: {os.path.basename(script_path)}")
            
            try:
                # Ejecutar el script de AutoHotkey
                working_dir = self.selected_folder.get() if self.selected_folder.get() else os.path.dirname(script_path)
                
                result = subprocess.run(
                    [ahk_path, script_path],
                    cwd=working_dir,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutos de timeout
                )
                
                if result.stdout:
                    self.update_log("Salida del script:", "info")
                    for line in result.stdout.splitlines():
                        self.update_log(f"  {line}", "info")
                
                if result.stderr:
                    self.update_log("Errores del script:", "error")
                    for line in result.stderr.splitlines():
                        self.update_log(f"  {line}", "error")
                
                exit_code = result.returncode
                if exit_code == 0:
                    self.update_log(f"Script ejecutado exitosamente. Código de salida: {exit_code}", "success")
                else:
                    self.update_log(f"Script finalizado con errores. Código de salida: {exit_code}", "error")
                    
            except subprocess.TimeoutExpired:
                self.update_log("El script excedió el tiempo máximo de ejecución (5 minutos).", "error")
            except Exception as e:
                self.update_log(f"Error ejecutando el script: {str(e)}", "error")
            finally:
                self.task_in_progress = False
        
        threading.Thread(target=run_ahk_task, daemon=True).start()

def main():
    """Función principal"""
    root = tk.Tk()
    app = TaskAutomationApp(root)
    
    # Configurar cierre seguro
    def on_closing():
        app.quit_app()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()