import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import customtkinter as ctk
import cv2
import numpy as np

from edit.blur import BlurMode
from edit.crop import *
from edit.draw import DrawMode
from edit.gamma import GammaMode

CANVAS_WIDTH, CANVAS_HEIGHT = 1040, 720

class Memory:
    def __init__(self):
        self.cur = -1
        self.arr = []

    def append(self, object):
        while self.cur < len(self.arr) - 1:
            self.arr.pop()

        self.cur += 1
        self.arr.append(object)

    def back(self):
        return self.arr[-1]

    def current(self):
        return self.arr[self.cur]

    def undo(self):
        if self.cur > 0:
            self.cur -= 1

        return self.arr[self.cur]

    def redo(self):
        if self.cur < len(self.arr) - 1:
            self.cur += 1

        return self.arr[self.cur]

class Window:
    def __init__(self, app):
        self.app = app
        self.modify = False

        # ##############################################################################################################
        self.filename = None
        self.original_image = None
        self.edit_image = Memory()

        self.img = None
        self.display_image = None

        self.mode = []

        # ##############################################################################################################
        # ############################################# Appearance #####################################################

        # ################# Button Frame ###############

        self.button_frame = ctk.CTkFrame(app, width=40, height=720, fg_color="gray12")
        self.button_frame.pack(side='left', fill="y")

        self.draw_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12", hover_color="black",
                                         image=ctk.CTkImage(dark_image=Image.open("assets/drawing.png"))
                                         , command=self.draw_mode)
        self.draw_button.pack(pady=20)

        self.erase_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12", hover_color="black",
                                          image=ctk.CTkImage(dark_image=Image.open("assets/eraser.png")))
        self.erase_button.pack()

        self.crop_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12", hover_color="black",
                                         image=ctk.CTkImage(dark_image=Image.open("assets/crop-tool.png")))
        self.crop_button.pack(pady=20)

        self.blur_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12", hover_color="black",
                                         image=ctk.CTkImage(dark_image=Image.open("assets/blur.png")),
                                         command=self.blur)
        self.blur_button.pack()

        self.gray_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12", hover_color="black",
                                         image=ctk.CTkImage(dark_image=Image.open("assets/greyscale.png")),
                                         command=self.grayscale)
        self.gray_button.pack(pady=20)

        self.sepia_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12", hover_color="black",
                                          image=ctk.CTkImage(dark_image=Image.open("assets/sepia.png")),
                                          command=self.sepia)
        self.sepia_button.pack()

        self.neg_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12", hover_color="black",
                                        image=ctk.CTkImage(dark_image=Image.open("assets/minus.png")),
                                        command=self.neg)
        self.neg_button.pack(pady=20)

        self.gamma_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12", hover_color="black",
                                          image=ctk.CTkImage(dark_image=Image.open("assets/gamma.png")),
                                          command=self.gamma)
        self.gamma_button.pack()

        self.emboss_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12", hover_color="black",
                                           image=ctk.CTkImage(dark_image=Image.open("assets/emboss.png")))
        self.emboss_button.pack(pady=20)

        self.sharpen_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12",
                                            hover_color="black",
                                            image=ctk.CTkImage(dark_image=Image.open("assets/sharpen.png")))
        self.sharpen_button.pack()

        self.sketch_button = ctk.CTkButton(self.button_frame, width=20, text="", fg_color="gray12", hover_color="black",
                                           image=ctk.CTkImage(dark_image=Image.open("assets/sketch.png")))
        self.sketch_button.pack(pady=20)

        # ################# Canvas Frame ###############

        self.canvas_frame = ctk.CTkFrame(app, width=1040, height=720, fg_color="#2d2d2d")
        self.canvas_frame.pack(side='left', fill="y")

        self.canvas = ctk.CTkCanvas(master=self.canvas_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#595959")
        self.canvas.pack()
        self.canvas.place(anchor='center', relx=0.5, rely=0.5)

        self.load_image_button = ctk.CTkButton(master=self.canvas_frame, text="Upload new image", width=200, height=40
                                               , bg_color="#595959", command=self.load_image)
        self.load_image_button.pack()
        self.load_image_button.place(anchor='center', relx=0.5, rely=0.5)

        # ################# Properties Frame ###############
        self.property_frame = ctk.CTkFrame(app, width=200, height=720)
        self.property_frame.pack(side='right', fill='y')

        self.button_frame2 = ctk.CTkFrame(self.property_frame, width=180, height=40)
        self.button_frame2.pack(pady=20)
        self.undo_button = ctk.CTkButton(master=self.button_frame2, width=80, text="Undo", command=self.undo)
        self.redo_button = ctk.CTkButton(master=self.button_frame2, width=80, text="Redo", command=self.redo)
        self.undo_button.pack(side='left', padx=5)
        self.redo_button.pack(side='right', padx=5)

        self.property_view = ctk.CTkTabview(master=self.property_frame, height=300,
                                            segmented_button_selected_color="gray30")
        self.property_view.pack(padx=10)
        self.property_view.add("Properties")  # add tab at the end
        self.property_view.set("Properties")  # set currently visible tab

        layer_view = ctk.CTkTabview(master=self.property_frame, height=300, segmented_button_selected_color="gray30")
        layer_view.pack(padx=10, pady=10)
        layer_view.add("Layers")  # add tab at the end
        layer_view.set("Layers")  # set currently visible tab

        self.df_property = ctk.CTkLabel(master=self.property_view.tab("Properties"), text="No properties")
        self.df_property.pack()

        self.draw_mode = DrawMode(self.property_view.tab("Properties"), self.canvas, self.canvas_frame, self)
        self.draw_mode.hide()
        self.mode.append(self.draw_mode)

        self.gamma_mode = GammaMode(self.property_view.tab("Properties"), self)
        self.gamma_mode.hide()
        self.mode.append(self.gamma_mode)

        self.blur_mode = BlurMode(self.property_view.tab("Properties"), self)
        self.blur_mode.hide()
        self.mode.append(self.blur_mode)

    def show_image(self, image):
        if image is None:
            return

        # resize image to fit the canvas
        new_width = CANVAS_WIDTH
        new_height = int(image.shape[0] * (new_width / image.shape[1]))

        if new_height > CANVAS_HEIGHT:
            new_height = CANVAS_HEIGHT
            new_width = int(image.shape[1] * (new_height / image.shape[0]))
        self.display_image = cv2.resize(image, (new_width, new_height))

        self.display_image = Image.fromarray(self.display_image)
        self.display_image = ImageTk.PhotoImage(self.display_image)

        pos_x = int((CANVAS_WIDTH - self.display_image.width()) / 2)
        pos_y = int((CANVAS_HEIGHT - self.display_image.height()) / 2)

        self.canvas.create_image(pos_x, pos_y, image=self.display_image, anchor="nw")

    def load_image(self):
        self.canvas.delete("all")

        self.filename = filedialog.askopenfilename()
        self.original_image = cv2.imread(self.filename)
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)

        self.edit_image.append(self.original_image.copy())
        self.img = self.edit_image.back()

        self.modify = True
        self.load_image_button.pack_forget()
        self.load_image_button.place_forget()

        self.show_image(self.img)

    def save_png(self):
        self.filename = filedialog.asksaveasfilename(
            filetypes=(
                ("PNG Image", "*.png"),
                ("All File", "*.*")
            )
        )

        self.display_image = ImageGrab.grab(bbox=(
            self.canvas.winfo_rootx() + self.app.winfo_rootx(),
            self.canvas.winfo_rooty() + self.app.winfo_rooty(),
            self.canvas.winfo_rootx() + self.canvas.winfo_width(),
            self.canvas.winfo_rooty() + self.canvas.winfo_height()
        ))

        self.display_image.save(self.filename + ".png")

    def save_jpg(self):
        self.filename = filedialog.asksaveasfilename(
            filetypes=(
                ("JPG Image", "*.jpg"),
                ("All File", "*.*")
            )
        )

        self.display_image = ImageGrab.grab(bbox=(
            self.canvas.winfo_rootx() + self.app.winfo_rootx(),
            self.canvas.winfo_rooty() + self.app.winfo_rooty(),
            self.canvas.winfo_rootx() + self.canvas.winfo_width(),
            self.canvas.winfo_rooty() + self.canvas.winfo_height()
        ))
        self.display_image.save(self.filename + ".jpg")

    def draw_mode(self):
        for x in self.mode:
            x.hide()

        self.df_property.pack_forget()
        self.draw_mode.pack()
        self.draw_mode.can_draw()
        self.show_image(self.img)

    def grayscale(self):
        self.reset_property()
        if len(self.img.shape) == 2:
            return

        self.edit_image.append(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY))
        self.img = self.edit_image.back()
        self.show_image(self.img)

    def sepia(self):
        self.reset_property()
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) if len(self.img.shape) != 2 else self.img

        normalized_gray = np.array(gray, np.float32) / 255
        # solid color
        sepia = np.ones((self.img.shape[0], self.img.shape[1], 3))
        sepia[:, :, 0] *= 153  # B
        sepia[:, :, 1] *= 204  # G
        sepia[:, :, 2] *= 255  # R
        # hadamard
        sepia[:, :, 0] *= normalized_gray  # B
        sepia[:, :, 1] *= normalized_gray  # G
        sepia[:, :, 2] *= normalized_gray  # R

        self.edit_image.append(np.array(sepia, np.uint8))
        self.img = self.edit_image.back()
        self.show_image(self.img)

    def neg(self):
        self.reset_property()
        self.edit_image.append(255 - self.img)
        self.img = self.edit_image.back()
        self.show_image(self.img)

    def gamma(self):
        for x in self.mode:
            x.hide()

        self.df_property.pack_forget()
        self.gamma_mode.pack()

    def blur(self):
        for x in self.mode:
            x.hide()

        self.df_property.pack_forget()
        self.blur_mode.pack()

    def undo(self):
        self.img = self.edit_image.undo()
        self.show_image(self.img)

    def redo(self):
        self.img = self.edit_image.redo()
        self.show_image(self.img)

    def reset_property(self):
        for x in self.mode:
            x.hide()

        self.df_property.pack()
