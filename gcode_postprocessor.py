import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def transform_gcode(input_file, output_file, angle_deg=0, scale_x=1.0, scale_y=1.0, scale_z=1.0, translate_x=0.0, translate_y=0.0):
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    try:
        with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
            for line in f_in:
                if line.startswith(("G0", "G1")) and ("X" in line or "Y" in line or "Z" in line):
                    parts = line.split()
                    x = y = z = None
                    for p in parts:
                        if p.startswith("X"):
                            try:
                                x = float(p[1:])
                            except ValueError:
                                pass
                        elif p.startswith("Y"):
                            try:
                                y = float(p[1:])
                            except ValueError:
                                pass
                        elif p.startswith("Z"):
                            try:
                                z = float(p[1:])
                            except ValueError:
                                pass

                    if x is not None or y is not None or z is not None:
                        new_parts = [parts[0]]
                        for p in parts[1:]:
                            if not (p.startswith("X") or p.startswith("Y") or p.startswith("Z")):
                                new_parts.append(p)
                        
                        if x is None:
                            x = 0.0
                        if y is None:
                            y = 0.0
                        if z is None:
                            z = 0.0
                        
                        x_scaled = x * scale_x
                        y_scaled = y * scale_y
                        z_scaled = z * scale_z
                        
                        new_x = x_scaled * cos_a - y_scaled * sin_a
                        new_y = x_scaled * sin_a + y_scaled * cos_a
                        
                        new_x += translate_x
                        new_y += translate_y
                        
                        new_parts.insert(1, f"X{new_x:.3f}")
                        new_parts.insert(2, f"Y{new_y:.3f}")
                        
                        if "Z" in line or z_scaled != z:
                            new_parts.append(f"Z{z_scaled:.3f}")
                            
                        f_out.write(" ".join(new_parts) + "\n")
                    else:
                        f_out.write(line)
                else:
                    f_out.write(line)
        
        return True, f"Transformed {input_file} and saved as {output_file}"
    except Exception as e:
        return False, f"Error: {str(e)}"

class GCodeTransformerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("G-Code Transformer")
        self.root.geometry("500x650")
        
        self.rotation_var = tk.DoubleVar(value=0.0)
        self.scale_x_var = tk.DoubleVar(value=1.0)
        self.scale_y_var = tk.DoubleVar(value=1.0)
        self.scale_z_var = tk.DoubleVar(value=1.0)
        self.translate_x_var = tk.DoubleVar(value=0.0)
        self.translate_y_var = tk.DoubleVar(value=0.0)
        
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        file_frame = ttk.LabelFrame(self.root, text="File Selection", padding=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(file_frame, text="Input File:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(file_frame, textvariable=self.input_file, width=40).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_input_file).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(file_frame, text="Output File:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(file_frame, textvariable=self.output_file, width=40).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_output_file).grid(row=1, column=2, padx=5, pady=5)
        
        transform_frame = ttk.LabelFrame(self.root, text="Transformations", padding=10)
        transform_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        rotation_frame = ttk.Frame(transform_frame)
        rotation_frame.pack(fill="x", pady=5)
        
        ttk.Label(rotation_frame, text="Rotation (degrees):").pack(side="left")
        rotation_value = ttk.Label(rotation_frame, textvariable=self.rotation_var, width=6)
        rotation_value.pack(side="right")
        
        rotation_scale = ttk.Scale(
            rotation_frame, 
            from_=-180, 
            to=180, 
            variable=self.rotation_var,
            orient="horizontal",
            command=lambda v: self.rotation_var.set(round(float(v), 1))
        )
        rotation_scale.pack(fill="x", padx=5)
        
        scale_frame = ttk.Frame(transform_frame)
        scale_frame.pack(fill="x", pady=5)
        
        ttk.Label(scale_frame, text="Scale X:").grid(row=0, column=0, sticky="w")
        scale_x_value = ttk.Label(scale_frame, textvariable=self.scale_x_var, width=6)
        scale_x_value.grid(row=0, column=1, padx=5)
        
        scale_x_scale = ttk.Scale(
            scale_frame, 
            from_=0.1, 
            to=3.0, 
            variable=self.scale_x_var,
            orient="horizontal",
            command=lambda v: self.scale_x_var.set(round(float(v), 2))
        )
        scale_x_scale.grid(row=0, column=2, sticky="ew", padx=5)
        
        ttk.Label(scale_frame, text="Scale Y:").grid(row=1, column=0, sticky="w", pady=5)
        scale_y_value = ttk.Label(scale_frame, textvariable=self.scale_y_var, width=6)
        scale_y_value.grid(row=1, column=1, padx=5, pady=5)
        
        scale_y_scale = ttk.Scale(
            scale_frame, 
            from_=0.1, 
            to=3.0, 
            variable=self.scale_y_var,
            orient="horizontal",
            command=lambda v: self.scale_y_var.set(round(float(v), 2))
        )
        scale_y_scale.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        
        ttk.Label(scale_frame, text="Scale Z:").grid(row=2, column=0, sticky="w", pady=5)
        scale_z_value = ttk.Label(scale_frame, textvariable=self.scale_z_var, width=6)
        scale_z_value.grid(row=2, column=1, padx=5, pady=5)
        
        scale_z_scale = ttk.Scale(
            scale_frame, 
            from_=0.1, 
            to=3.0, 
            variable=self.scale_z_var,
            orient="horizontal",
            command=lambda v: self.scale_z_var.set(round(float(v), 2))
        )
        scale_z_scale.grid(row=2, column=2, sticky="ew", padx=5, pady=5)
        
        scale_frame.columnconfigure(2, weight=1)
        
        translate_frame = ttk.Frame(transform_frame)
        translate_frame.pack(fill="x", pady=5)
        
        ttk.Label(translate_frame, text="Translate X (mm):").grid(row=0, column=0, sticky="w")
        translate_x_value = ttk.Label(translate_frame, textvariable=self.translate_x_var, width=6)
        translate_x_value.grid(row=0, column=1, padx=5)
        
        translate_x_scale = ttk.Scale(
            translate_frame, 
            from_=-50, 
            to=50, 
            variable=self.translate_x_var,
            orient="horizontal",
            command=lambda v: self.translate_x_var.set(round(float(v), 1))
        )
        translate_x_scale.grid(row=0, column=2, sticky="ew", padx=5)
        
        ttk.Label(translate_frame, text="Translate Y (mm):").grid(row=1, column=0, sticky="w", pady=5)
        translate_y_value = ttk.Label(translate_frame, textvariable=self.translate_y_var, width=6)
        translate_y_value.grid(row=1, column=1, padx=5, pady=5)
        
        translate_y_scale = ttk.Scale(
            translate_frame, 
            from_=-50, 
            to=50, 
            variable=self.translate_y_var,
            orient="horizontal",
            command=lambda v: self.translate_y_var.set(round(float(v), 1))
        )
        translate_y_scale.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        
        translate_frame.columnconfigure(2, weight=1)
        
        reset_button = ttk.Button(transform_frame, text="Reset All", command=self.reset_values)
        reset_button.pack(pady=10)
        
        transform_button = ttk.Button(self.root, text="Transform G-Code", command=self.transform_gcode)
        transform_button.pack(pady=10)
    
    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select Input G-Code File",
            filetypes=[("G-Code files", "*.gcode *.nc"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Suggest output filename
            if not self.output_file.get():
                base_name = filename.rsplit('.', 1)[0]
                self.output_file.set(f"{base_name}_transformed.gcode")
    
    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save Output G-Code File As",
            defaultextension=".gcode",
            filetypes=[("G-Code files", "*.gcode"), ("All files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
    
    def reset_values(self):
        self.rotation_var.set(0.0)
        self.scale_x_var.set(1.0)
        self.scale_y_var.set(1.0)
        self.scale_z_var.set(1.0)
        self.translate_x_var.set(0.0)
        self.translate_y_var.set(0.0)
    
    def transform_gcode(self):
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file")
            return
        
        if not self.output_file.get():
            messagebox.showerror("Error", "Please select an output file")
            return
        
        try:
            success, message = transform_gcode(
                self.input_file.get(),
                self.output_file.get(),
                self.rotation_var.get(),
                self.scale_x_var.get(),
                self.scale_y_var.get(),
                self.scale_z_var.get(),
                self.translate_x_var.get(),
                self.translate_y_var.get()
            )
            
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GCodeTransformerApp(root)
    root.mainloop()