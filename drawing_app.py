import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        '''Метод инициализирует приложение для рисования'''
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.previous_color = tk.StringVar(value='black')  # Сохранение предыдущего цвета

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        '''Метод отвечает за создание и расположение виджетов управления.'''
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)
        '''Создание выпадающего списка.Выбор размера кисти из списка'''
        brush_sizes = [1, 2, 5, 10]
        self.brush_size = tk.IntVar()
        self.brush_size.set(5)  # Установка начального значения
        brush_size_option = tk.OptionMenu(self.root, self.brush_size, *brush_sizes)
        brush_size_option.pack(side=tk.LEFT)

        erase_button = tk.Button(control_frame, text="Ластик", command=self.erase)
        erase_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

    def paint(self, event):
        '''Метод для рисования на холсте при движени мыши.'''
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        '''Метод сбрасывает последние координаты кисти.'''
        self.last_x, self.last_y = None, None
        # Восстановливаем предыдущий цвет
        self.pen_color = self.previous_color.get()

    def clear_canvas(self):
        '''Метод очищает холст.'''
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        '''Метод для выбора цвета кисти.'''
        new_color = colorchooser.askcolor(color=self.pen_color)[1]
        if new_color:
            self.pen_color = new_color
            self.previous_color.set(new_color)

    def erase(self):
        '''Метод отвечает за действие ластика.'''
        self.pen_color = 'white'

    def save_image(self):
        '''Метод сохраняет изображение.'''
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