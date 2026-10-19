"""Video Studio: interfaz local para las skills audiovisuales del repositorio."""
import io
import ctypes
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
from worker import ROOT, PYTHON, tool

if sys.platform == 'win32':
    ctypes.windll.user32.SetProcessDPIAware()
# El Python portátil anterior perdió su alias de Tcl; resolver el recurso real.
for tcl in sorted((ROOT / 'tmp/python').glob('*/tcl/tcl8.6/init.tcl')):
    os.environ['TCL_LIBRARY'] = str(tcl.parent)
    os.environ['TK_LIBRARY'] = str(tcl.parent.parent / 'tk8.6')
    break


class Studio:
    def __init__(self, root):
        self.root = root
        root.tk.call('tk', 'scaling', 1.0)
        root.title('Video Studio · Agent Lab')
        root.geometry(f'{min(1200, root.winfo_screenwidth()-60)}x{min(850, root.winfo_screenheight()-100)}+20+20')
        root.minsize(1050, 700)
        root.configure(bg='#E8EEF4')
        self.events = queue.Queue()
        self.files = []
        self.masks = {}
        self.current = None
        self.frame = self.mask = None
        self.process = None
        self.busy = False
        self.last_output = None
        self.request = 0
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', font=('Segoe UI', 10), background='#E8EEF4', foreground='#172C43')
        style.configure('TButton', padding=(12, 8))
        style.configure('Accent.TButton', background='#067D87', foreground='white')
        style.configure('Title.TLabel', font=('Segoe UI Semibold', 23))
        top = ttk.Frame(root, padding=20)
        top.pack(fill='x')
        ttk.Label(top, text='VIDEO STUDIO', style='Title.TLabel').pack(side='left')
        ttk.Label(top, text='Herramientas locales / originales protegidos').pack(side='right')
        body = ttk.Frame(root, padding=(20, 0, 20, 10))
        body.pack(fill='both', expand=True)
        left = ttk.Frame(body, width=230)
        left.pack(side='left', fill='y', padx=(0, 16))
        ttk.Label(left, text='TUS VIDEOS', font=('Segoe UI Semibold', 11)).pack(anchor='w', pady=8)
        ttk.Button(left, text='+ Añadir videos', command=self.add).pack(fill='x')
        self.list = tk.Listbox(left, width=28, bg='white', fg='#172C43', selectbackground='#067D87', borderwidth=0, font=('Segoe UI', 10), exportselection=False)
        self.list.pack(fill='both', expand=True, pady=10)
        self.list.bind('<<ListboxSelect>>', self.select)
        ttk.Button(left, text='Quitar de la lista', command=self.remove).pack(fill='x')
        right = ttk.Frame(body, width=285)
        right.pack(side='right', fill='y', padx=(16, 0))
        self.restore = tk.BooleanVar(value=False)
        self.upscale = tk.BooleanVar(value=True)
        self.metadata = tk.BooleanVar(value=True)
        self.erase = tk.BooleanVar(value=False)
        self.mode = tk.StringVar(value='fast')
        self.sharpness = tk.StringVar(value='0')
        ttk.Label(right, text='PROCESAMIENTO', font=('Segoe UI Semibold', 11)).pack(anchor='w', pady=8)
        ttk.Checkbutton(right, text='1. Quitar marca de agua', variable=self.restore).pack(anchor='w', pady=8)
        ttk.Label(right, text='Pintá únicamente las marcas visibles.\nLa máscara pertenece al video seleccionado.').pack(anchor='w')
        ttk.Checkbutton(right, text='Borrador de máscara', variable=self.erase).pack(anchor='w', pady=5)
        for title, callback in [('Importar máscara PNG', self.import_mask), ('Guardar máscara', self.save_mask), ('Limpiar máscara', self.clear_mask)]:
            ttk.Button(right, text=title, command=callback).pack(fill='x', pady=2)
        ttk.Separator(right).pack(fill='x', pady=12)
        ttk.Checkbutton(right, text='2. Exportar a 1080p', variable=self.upscale).pack(anchor='w')
        ttk.Radiobutton(right, text='Rápido · Lanczos', value='fast', variable=self.mode).pack(anchor='w', pady=5)
        ttk.Radiobutton(right, text='Calidad · Real-ESRGAN', value='quality', variable=self.mode).pack(anchor='w')
        ttk.Label(right, text='Nitidez adicional (0 a 1)').pack(anchor='w', pady=(8, 2))
        ttk.Spinbox(right, from_=0, to=1, increment=.1, textvariable=self.sharpness, width=8).pack(anchor='w')
        ttk.Separator(right).pack(fill='x', pady=12)
        ttk.Checkbutton(right, text='3. Eliminar metadatos personales', variable=self.metadata).pack(anchor='w')
        ttk.Label(right, text='Se aplica después de la exportación.').pack(anchor='w', pady=6)
        ttk.Button(right, text='Comparar Lanczos / IA · 2 s', command=lambda: self.start(True, True)).pack(fill='x', pady=12)
        center = ttk.Frame(body)
        center.pack(fill='both', expand=True)
        self.info = ttk.Label(center, text='Seleccioná un video para comenzar', wraplength=430)
        self.info.pack(anchor='w', pady=8)
        self.canvas = tk.Canvas(center, bg='#172C43', highlightthickness=0, width=360, height=320)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', lambda e: self.render())
        self.canvas.bind('<Button-1>', self.paint)
        self.canvas.bind('<B1-Motion>', self.paint)
        ttk.Label(center, text='Vista del primer fotograma · pintá la máscara sobre la imagen').pack(anchor='w', pady=5)
        footer = ttk.Frame(root, padding=(20, 0, 20, 16))
        footer.pack(fill='x')
        self.output = tk.StringVar(value=str(ROOT / 'outputs/video-studio'))
        ttk.Label(footer, text='Guardar en').grid(row=0, column=0, sticky='w')
        ttk.Entry(footer, textvariable=self.output).grid(row=0, column=1, columnspan=3, sticky='ew', padx=8)
        ttk.Button(footer, text='Elegir carpeta', command=self.choose_output).grid(row=0, column=4)
        ttk.Button(footer, text='Probar 2 segundos', command=lambda: self.start(True)).grid(row=1, column=0, pady=10)
        ttk.Button(footer, text='Procesar lote', style='Accent.TButton', command=self.start).grid(row=1, column=1, sticky='w', padx=8)
        ttk.Button(footer, text='Cancelar', command=self.cancel).grid(row=1, column=2)
        ttk.Button(footer, text='Abrir resultados', command=self.open_output).grid(row=1, column=4)
        footer.columnconfigure(1, weight=1)
        self.status = tk.StringVar(value='Listo. Probá un fragmento antes de procesar el video completo.')
        ttk.Label(footer, textvariable=self.status).grid(row=2, column=0, columnspan=5, sticky='w')
        self.progress = ttk.Progressbar(footer, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=5, sticky='ew', pady=5)
        self.log = tk.Text(footer, height=5, bg='white', fg='#172C43', font=('Consolas', 9), state='disabled')
        self.log.grid(row=4, column=0, columnspan=5, sticky='ew')
        root.after(100, self.poll)
        root.protocol('WM_DELETE_WINDOW', self.close)

    def add(self):
        for name in filedialog.askopenfilenames(filetypes=[('Videos', '*.mp4 *.mov *.mkv *.webm'), ('Todos', '*.*')]):
            if name not in self.files:
                self.files.append(name)
                self.list.insert('end', Path(name).name)
        if self.files and not self.list.curselection():
            self.list.selection_set(0)
            self.select()

    def remove(self):
        if self.list.curselection():
            i = self.list.curselection()[0]
            self.list.delete(i)
            self.files.pop(i)
            self.current = None
            self.frame = self.mask = None
            self.render()

    def select(self, event=None):
        if not self.list.curselection():
            return
        self.current = self.files[self.list.curselection()[0]]
        source = self.current
        self.request += 1
        token = self.request
        self.frame = self.mask = None
        self.info.configure(text='Leyendo fotograma…')
        def load():
            try:
                raw = subprocess.run([tool('ffmpeg'), '-v', 'error', '-i', source, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                frame = Image.open(io.BytesIO(raw.stdout)).convert('RGB')
                data = json.loads(subprocess.check_output([tool('ffprobe'), '-v', 'error', '-show_streams', '-of', 'json', source], creationflags=subprocess.CREATE_NO_WINDOW))
                video = next(s for s in data['streams'] if s['codec_type'] == 'video')
                self.events.put(('frame', (token, frame, video)))
            except Exception as exc:
                self.events.put(('error', str(exc)))
        threading.Thread(target=load, daemon=True).start()

    def render(self):
        self.canvas.delete('all')
        if self.frame is None:
            self.canvas.create_text(max(100, self.canvas.winfo_width()/2), 160, text='VISTA PREVIA', fill='#FFFFFF', font=('Segoe UI', 14))
            return
        image = self.frame.copy()
        if self.mask:
            overlay = Image.new('RGB', image.size, '#D98B27')
            image = Image.composite(overlay, image, self.mask.point(lambda p: int(p*.55)))
        image.thumbnail((max(1, self.canvas.winfo_width()-16), max(1, self.canvas.winfo_height()-16)))
        self.scale = image.width/self.frame.width
        self.offset = ((self.canvas.winfo_width()-image.width)/2, (self.canvas.winfo_height()-image.height)/2)
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(*self.offset, image=self.photo, anchor='nw')

    def paint(self, event):
        if self.frame is None:
            return
        x, y = [(v-o)/self.scale for v, o in zip((event.x, event.y), self.offset)]
        if not (0 <= x < self.frame.width and 0 <= y < self.frame.height):
            return
        radius = 12/self.scale
        ImageDraw.Draw(self.mask).ellipse((x-radius, y-radius, x+radius, y+radius), fill=0 if self.erase.get() else 255)
        self.masks[self.current] = self.mask
        self.render()

    def clear_mask(self):
        if self.frame:
            self.mask = Image.new('L', self.frame.size)
            self.masks[self.current] = self.mask
            self.render()

    def import_mask(self):
        if self.frame is None:
            return
        name = filedialog.askopenfilename(filetypes=[('Máscara PNG', '*.png')])
        if name:
            try:
                mask = Image.open(name).convert('L')
                if mask.size != self.frame.size:
                    raise ValueError(f'La máscara debe medir {self.frame.width} × {self.frame.height}.')
                self.mask = mask
                self.masks[self.current] = mask
                self.render()
            except Exception as exc:
                messagebox.showerror('Máscara', str(exc))

    def save_mask(self):
        if self.mask:
            name = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG', '*.png')])
            if name:
                self.mask.save(name)

    def choose_output(self):
        name = filedialog.askdirectory()
        if name:
            self.output.set(name)

    def start(self, sample=False, compare=False):
        if self.busy:
            return
        try:
            if not self.files:
                raise ValueError('Añadí al menos un video.')
            sharpness = float(self.sharpness.get())
            if not 0 <= sharpness <= 1:
                raise ValueError('La nitidez debe estar entre 0 y 1.')
            selected = [self.current] if sample and self.current else list(self.files)
            if not any([self.restore.get(), self.upscale.get(), self.metadata.get(), compare]):
                raise ValueError('Seleccioná una operación.')
            if self.restore.get() and any(not self.masks.get(p) or not self.masks[p].getbbox() for p in selected):
                raise ValueError('Falta pintar o importar una máscara para cada video del lote.')
            base = Path(self.output.get()).expanduser().resolve()
            base.mkdir(parents=True, exist_ok=True)
            config = base / ('trabajo-' + str(time.time_ns()) + '.json')
            destination = base / ('prueba-' if sample else 'lote-') / str(time.time_ns())
            items = []
            for i, path in enumerate(selected):
                item = {'path': path}
                if self.restore.get():
                    mask = config.with_name(config.stem + f'-mask-{i}.png')
                    self.masks[path].save(mask)
                    item['mask'] = str(mask)
                items.append(item)
            job = dict(inputs=items, output=str(destination), sample=sample, compare=compare, restore=self.restore.get(), upscale=self.upscale.get(), metadata=self.metadata.get(), mode=self.mode.get(), sharpness=str(sharpness))
            config.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding='utf-8')
            self.last_output = destination
            self.busy = True
            self.status.set('Procesando… IA puede tardar varios minutos. El registro indica la etapa actual.')
            self.progress.start()
            def work():
                try:
                    self.process = subprocess.Popen([str(PYTHON), '-u', str(Path(__file__).with_name('worker.py')), str(config)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace', creationflags=subprocess.CREATE_NO_WINDOW)
                    with config.with_suffix('.log').open('w', encoding='utf-8') as log:
                        for line in self.process.stdout:
                            log.write(line)
                            log.flush()
                            self.events.put(('log', line))
                    code = self.process.wait()
                    self.events.put(('done', code))
                except Exception as exc:
                    self.events.put(('error', str(exc)))
                    self.events.put(('done', 1))
            threading.Thread(target=work, daemon=True).start()
        except Exception as exc:
            messagebox.showerror('No se puede iniciar', str(exc))

    def cancel(self):
        if self.process and self.process.poll() is None:
            subprocess.run(['taskkill', '/PID', str(self.process.pid), '/T', '/F'], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.status.set('Cancelando. Los parciales y el registro se conservan.')

    def open_output(self):
        path = self.last_output or Path(self.output.get())
        if path.exists():
            os.startfile(path)

    def poll(self):
        try:
            while True:
                kind, data = self.events.get_nowait()
                if kind == 'frame':
                    token, frame, info = data
                    if token == self.request:
                        self.frame = frame
                        self.mask = self.masks.get(self.current, Image.new('L', frame.size))
                        self.info.configure(text=f'{frame.width} × {frame.height}  /  {info["avg_frame_rate"]} FPS  /  {info["codec_name"]}')
                        self.render()
                elif kind == 'log':
                    self.log.configure(state='normal')
                    self.log.insert('end', data)
                    self.log.see('end')
                    self.log.configure(state='disabled')
                elif kind == 'done':
                    self.busy = False
                    self.progress.stop()
                    self.status.set('Terminado. Abrí resultados y revisá el video o la comparación.' if data == 0 else 'Trabajo interrumpido o con errores. Revisá el registro y resumen.json.')
                elif kind == 'error':
                    self.status.set('Error: ' + data)
        except queue.Empty:
            pass
        self.root.after(100, self.poll)

    def close(self):
        if self.busy and not messagebox.askyesno('Cerrar Video Studio', 'Hay un trabajo activo. ¿Cancelar y cerrar?'):
            return
        self.cancel()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = Studio(root)
    root.mainloop()
