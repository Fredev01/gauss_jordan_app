import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class MatrixInputFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.entries = []
        self._create_widgets()
    
    def _create_widgets(self):
        # Título principal
        ttk.Label(self, text="Ingresar los datos matriz de 4×4", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=9, pady=20)
        
        # Crear etiquetas para variables
        variables = ["x", "y", "z", "w"]
        
        # Crear entradas para la matriz
        for row in range(4):
            row_entries = []
            for col in range(4):
                entry = ttk.Entry(self, width=5)
                entry.grid(row=row+1, column=col*2, padx=5, pady=10)
                # Asignar un nombre al widget para facilitar la navegación con Tab
                entry.name = f"coef_{row}_{col}"
                row_entries.append(entry)
                
                # Agregar el símbolo de la variable después de cada entrada (excepto la última)
                if col < 3:
                    ttk.Label(self, text=variables[col], font=("Arial", 12)).grid(row=row+1, column=col*2+1)
            
            # Agregar el símbolo de la última variable
            ttk.Label(self, text=variables[3], font=("Arial", 12)).grid(row=row+1, column=7)
            
            # Agregar el signo igual
            ttk.Label(self, text="=", font=("Arial", 12)).grid(row=row+1, column=8)
            
            # Agregar la entrada para el término independiente
            result_entry = ttk.Entry(self, width=5)
            result_entry.grid(row=row+1, column=9, padx=5)
            result_entry.name = f"result_{row}"
            row_entries.append(result_entry)
            
            self.entries.append(row_entries)
        
        # Asignar eventos de teclado para mejorar la navegación
        self._setup_keyboard_navigation()
    
    def _setup_keyboard_navigation(self):
        # Vincular la tecla Enter para moverse al siguiente campo
        for row in self.entries:
            for entry in row:
                entry.bind("<Return>", lambda event, widget=entry: self._focus_next_widget(widget))
                entry.bind("<KP_Enter>", lambda event, widget=entry: self._focus_next_widget(widget))
    
    def _focus_next_widget(self, widget):
        # Función para pasar al siguiente widget cuando se presiona Enter
        widget.tk_focusNext().focus_set()
        return "break"  # Evita que el evento se propague
    
    def get_matrix(self):
        coef_matrix = np.zeros((4, 4))
        result_vector = np.zeros(4)
        
        for i in range(4):
            for j in range(4):
                try:
                    value = self.entries[i][j].get().strip()
                    # Si está vacío, asumir cero
                    if value == "":
                        coef_matrix[i, j] = 0.0
                    else:
                        coef_matrix[i, j] = float(value)
                except ValueError:
                    messagebox.showerror("Error", f"Valor inválido en fila {i+1}, columna {j+1}")
                    return None, None
            try:
                value = self.entries[i][4].get().strip()
                # Si está vacío, asumir cero
                if value == "":
                    result_vector[i] = 0.0
                else:
                    result_vector[i] = float(value)
            except ValueError:
                messagebox.showerror("Error", f"Valor inválido en el resultado de la fila {i+1}")
                return None, None
                
        return coef_matrix, result_vector
    
    def clear_all(self):
        # Limpiar todas las entradas
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
        
        # Colocar el foco en la primera entrada
        if self.entries and self.entries[0]:
            self.entries[0][0].focus_set()

class GaussJordanSolver:
    def solve(self, A, b):
        try:
            # Verificar si la matriz es singular antes de intentar resolver
            if np.linalg.det(A) == 0:
                messagebox.showerror("Error", "La matriz es singular, el sistema no tiene solución única.")
                return None
                
            # Crear matriz aumentada [A|b]
            n = len(A)
            augmented = np.column_stack((A, b))
            
            # Aplicar eliminación de Gauss-Jordan
            for i in range(n):
                # Pivoteo parcial
                max_row = i + np.argmax(np.abs(augmented[i:, i]))
                if max_row != i:
                    augmented[[i, max_row]] = augmented[[max_row, i]]
                
                # Verificar si el pivote es cero
                if abs(augmented[i, i]) < 1e-10:
                    return None
                
                # Normalizar la fila del pivote
                augmented[i] = augmented[i] / augmented[i, i]
                
                # Eliminar en todas las demás filas
                for j in range(n):
                    if i != j:
                        factor = augmented[j, i]
                        augmented[j] = augmented[j] - factor * augmented[i]
            
            # Extraer la solución
            solution = augmented[:, n]
            return solution
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver: {str(e)}")
            return None

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema 4x4 Gauss-Jordan")
        self.geometry("800x600")
        
        # Configurar estilo
        self._setup_style()
        
        # Crear widgets
        self._create_widgets()
        
        # Centrar la ventana en la pantalla
        self.center_window()
    
    def _setup_style(self):
        # Crear un estilo personalizado
        style = ttk.Style()
        
        # Configurar el estilo para los botones
        style.configure("TButton", font=("Arial", 11), padding=5)
        style.configure("Action.TButton", background="#4CAF50", foreground="white")
        style.configure("Clear.TButton", background="#f44336", foreground="white")
        
        # Configurar el estilo para las etiquetas
        style.configure("TLabel", font=("Arial", 11))
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        
        # Configurar el estilo para los frames
        style.configure("TFrame", background="#f5f5f5")
    
    def _create_widgets(self):
        # Frame principal con fondo
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Panel izquierdo para entrada
        self.matrix_frame = MatrixInputFrame(main_frame)
        self.matrix_frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)
        
        # Botón de resolver
        solve_btn = ttk.Button(button_frame, text="Resolver", command=self.solve, style="Action.TButton")
        solve_btn.pack(side=tk.LEFT, padx=10)
        
        # Botón de limpiar
        clear_btn = ttk.Button(button_frame, text="Limpiar", command=self.clear_all, style="Clear.TButton")
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Panel derecho para resultados
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=0, column=1, padx=20, pady=20, sticky='n')
        
        ttk.Label(results_frame, text="Resultados", style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=10)
        
        self.result_entries = []
        variables = ["x", "y", "z", "w"]
        
        for i, var in enumerate(variables):
            ttk.Label(results_frame, text=f"{var} =", font=("Arial", 12)).grid(row=i+1, column=0, padx=5, pady=10, sticky='e')
            result_entry = ttk.Entry(results_frame, width=10, state="readonly")
            result_entry.grid(row=i+1, column=1, padx=5, pady=10)
            self.result_entries.append(result_entry)
        
        # Agregar un mensaje de estado
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 10, "italic"))
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Agregar atajos de teclado
        self.bind("<Control-r>", lambda event: self.solve())
        self.bind("<Control-c>", lambda event: self.clear_all())
        self.bind("<F5>", lambda event: self.solve())
    
    def center_window(self):
        # Centrar la ventana en la pantalla
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def solve(self):
        # Limpiar el estado anterior
        self.status_var.set("")
        
        # Obtener matriz de coeficientes y vector de términos independientes
        A, b = self.matrix_frame.get_matrix()
        if A is None or b is None:
            return
        
        # Resolver el sistema
        solver = GaussJordanSolver()
        solution = solver.solve(A, b)
        
        if solution is None:
            return
        
        # Mostrar resultados
        for i, entry in enumerate(self.result_entries):
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, f"{solution[i]:.4f}")
            entry.config(state="readonly")
        
        # Actualizar mensaje de estado
        self.status_var.set("Sistema resuelto exitosamente")
    
    def clear_all(self):
        # Limpiar todas las entradas de la matriz
        self.matrix_frame.clear_all()
        
        # Limpiar resultados
        for entry in self.result_entries:
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="readonly")
        
        # Actualizar mensaje de estado
        self.status_var.set("Campos limpiados")

if __name__ == "__main__":
    app = Application()
    app.mainloop()