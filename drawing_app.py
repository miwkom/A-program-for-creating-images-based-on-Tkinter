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

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.eraser_color = self.pen_color

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.canvas.bind('<Button-3>', self.pick_color)

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс с инструментами.
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        brush_button = tk.Button(control_frame, text="Кисть", command=self.use_brush)
        brush_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        sizes = range(1,11)
        self.brush_size_var = tk.StringVar()
        self.brush_size_var.set(sizes[0])
        self.brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *sizes,
                                             command=self.update_brush_size)
        self.brush_size_menu.pack(side=tk.LEFT)

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

    def choose_color(self):
        """
        Открывает диалоговое окно выбора цвета и обновляет цвет кисти.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

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

    def pick_color(self, event):
        """
        Выбирает цвет пипеткой на основе цвета пикселя под курсором мыши.
        """
        x, y = event.x, event.y
        color = self.image.getpixel((x, y))
        self.pen_color = '#{:02x}{:02x}{:02x}'.format(*color)

    def save_image(self):
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
    root.mainloop()


if __name__ == "__main__":
    main()