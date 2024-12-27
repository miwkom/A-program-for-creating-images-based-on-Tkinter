import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw

class DrawingApp:
    def __init__(self, root):
        """
        Инициализирует приложение для рисования с указанным корневым окном и настраивает начальное состояние.
        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (500, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white', bd=0, highlightthickness=0)
        self.canvas.pack()

        self.pen_color = 'black'
        self.eraser_color = self.pen_color

        self.setup_ui()

        self.setup_menu()

        self.last_x, self.last_y = None, None

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.canvas.bind('<Button-3>', self.pick_color)

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс с инструментами.
        """
        control_frame = tk.Frame(self.root, bg='lightgray')
        control_frame.pack(fill=tk.X, side=tk.BOTTOM)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=1)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT, padx=1)

        self.selected_color = tk.Label(control_frame, width=2, bg=self.pen_color)
        self.selected_color.pack(side=tk.LEFT, padx=1)

        brush_button = tk.Button(control_frame, text="Кисть", command=self.use_brush)
        brush_button.pack(side=tk.LEFT, padx=1)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT, padx=1)

        sizes = range(1,11)
        self.brush_size_var = tk.StringVar()
        self.brush_size_var.set(sizes[0])
        self.brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *sizes,
                                             command=self.update_brush_size)
        self.brush_size_menu.pack(side=tk.LEFT, padx=1)

    def setup_menu(self):
        """
        Настраивает верхнее меню приложения
        """
        self.main_menu = tk.Menu(self.root)
        self.root.config(menu=self.main_menu, bg='lightgray')

        file_menu = tk.Menu(self.main_menu, tearoff=0)

        self.main_menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Создать новое изображение", command=self.new_image)
        file_menu.add_separator()
        file_menu.add_command(label="Сохранить", command=self.save_image)

    def bind_shortcuts(self):
        """
        Настраивает горячие клавиши для приложения.
        """
        self.root.bind('<Control-s>', lambda event: self.save_image(event))
        self.root.bind('<Control-c>', lambda event: self.choose_color(event))

    def paint(self, event):
        """
        Рисует линию на холсте и обновляет изображение с новой линией.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=int(self.brush_size_var.get()), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=int(self.brush_size_var.get()))

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        Сбрасывает последние координаты для рисования.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """
        Очищает холст и сбрасывает изображение до белого цвета.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        """
        Открывает диалоговое окно выбора цвета и обновляет цвет кисти.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.selected_color.config(bg=self.pen_color)

    def update_brush_size(self, event):
        """
        Обновляет размер кисти на основе выбранного значения из выпадающего меню.
        """
        self.brush_size = int(self.brush_size_var.get())

    def use_eraser(self):
        """
        Устанавливает цвет кисти в цвет фона ("white") и сохраняет используемый цвет.
        """
        if self.pen_color != 'white':
            self.eraser_color = self.pen_color

        self.pen_color = 'white'

    def use_brush(self):
        """
        Восстанавливает исходный цвет пера при переключении обратно на инструмент «Кисть».
        """
        self.pen_color = self.eraser_color
        self.selected_color.config(bg=self.pen_color)

    def pick_color(self, event):
        """
        Выбирает цвет пипеткой на основе цвета пикселя под курсором мыши.
        """
        x, y = event.x, event.y
        color = self.image.getpixel((x, y))
        self.pen_color = '#{:02x}{:02x}{:02x}'.format(*color)
        self.selected_color.config(bg=self.pen_color)

    def new_image(self):
        """
        Создает новое изображение и настраивает размеры приложения под его размер.
        """
        x = tk.simpledialog.askinteger("Создать новое изображение", "Введите целое число для обозначения ширины:",
                                       initialvalue=600, minvalue=100, maxvalue=1500, parent=self.root)
        if x is None:
            return

        y = tk.simpledialog.askinteger("Создать новое изображение", "Введите целое число для обозначения высоты:",
                                       initialvalue=400, minvalue=100, maxvalue=800, parent=self.root)
        if y is None:
            return

        if x and y:
            self.image = Image.new("RGB", (x, y), "white")
            self.draw = ImageDraw.Draw(self.image)
            self.canvas.config(width=x, height=y)
            self.clear_canvas()


    def save_image(self, event=None):
        """
        Открывает диалоговое окно сохранения файла для сохранения изображения в формате PNG.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    app.bind_shortcuts()
    root.mainloop()


if __name__ == "__main__":
    main()