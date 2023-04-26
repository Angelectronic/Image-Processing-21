# https://www.youtube.com/watch?v=iZUcX4kYrSM

from tkinter import HORIZONTAL, filedialog, ttk, Tk, PhotoImage, RIDGE, Canvas, GROOVE
from PIL import Image, ImageTk
import cv2

CANVA_WIDTH = 400
CANVA_HEIGHT = 300

class FrontEnd:
    def __init__(self, master):
        self.master = master
        self.modified = False

        """
        self.frame_header = ttk.Frame(self.master)
        self.frame_header.pack()

        # logo
        self.logo = cv2.imread("icon.png")
        self.logo = cv2.cvtColor(self.logo, cv2.COLOR_BGR2RGB)
        self.logo = cv2.resize(self.logo, (50, 50))
        self.logo = Image.fromarray(self.logo)
        self.logo = ImageTk.PhotoImage(self.logo)


        # Header
        ttk.Label(self.frame_header, image=self.logo).grid(row=0, column=0, rowspan=2)
        ttk.Label(self.frame_header, text = "Photoshop", 
                  font=("Helvetica", 18)).grid(row=0, column=2, columnspan=1)
        ttk.Label(self.frame_header, text = "Version 1.0", 
                  font=("Helvetica", 10)).grid(row=1, column=1, columnspan=3)
        """
        

        # Menu
        self.frame_menu = ttk.Frame(self.master)
        self.frame_menu.pack()
        self.frame_menu.config(relief=RIDGE, padding=(50, 15))

        ttk.Button(self.frame_menu, text="Upload an image", 
                   command=self.upload_image).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        self.crop_button = ttk.Button(self.frame_menu, text="Crop Image",
                   command=self.crop_image)
        self.crop_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="sw")

        self.draw_button = ttk.Button(self.frame_menu, text="Draw on image",
                   command=self.draw_on_image)
        self.draw_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        
        self.filter_button = ttk.Button(self.frame_menu, text="Apply filter",
                   command=self.filter_action)
        self.filter_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="sw")

        self.save_button = ttk.Button(self.frame_menu, text="Save as",
                   command=self.save_as)
        self.save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        
        # Image
        self.canvas = Canvas(self.frame_menu, width=CANVA_WIDTH, height=CANVA_HEIGHT, bg="gray")
        self.canvas.grid(row=0, column=2, rowspan=10)
        
        
        # Footer
        self.apply_and_cancel = ttk.Frame(self.master)
        self.apply_and_cancel.pack()
        self.apply_button = ttk.Button(self.apply_and_cancel, text="Apply",
                                command=self.apply_action)
        self.apply_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="sw")
        
        self.revert_button = ttk.Button(self.apply_and_cancel, text="Revert All Changes",
                     command=self.revert_all_change)
        self.revert_button.grid(row=0, column=1, columnspan=1, padx=5, pady=5, sticky="sw")

        self.cancel_button = ttk.Button(self.apply_and_cancel, text="Cancel",
                   command=self.cancel)
        self.cancel_button.grid(row=0, column=2, columnspan=1, padx=5, pady=5, sticky="sw")
        
        # disable buttons
        self.crop_button.config(state="disabled")
        self.draw_button.config(state="disabled")
        self.filter_button.config(state="disabled")
        self.save_button.config(state="disabled")
        self.apply_button.config(state="disabled")
        self.revert_button.config(state="disabled")
        self.cancel_button.config(state="disabled")
        

        
    def upload_image(self):

        # clear canvas and reset all frames
        self.canvas.delete("all")
        
        self.filename = filedialog.askopenfilename()
        self.original_image = cv2.imread(self.filename)
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)

        # filter_image for processing
        self.filter_image = self.original_image.copy()

        # enable buttons
        self.crop_button.config(state="normal")
        self.draw_button.config(state="normal")
        self.filter_button.config(state="normal")
        self.save_button.config(state="normal")

        # reset all frames
        try:
            self.frame_menu.pack_forget()
            self.frame_menu.pack()
        except:
            pass

        try:
            self.apply_and_cancel.pack_forget()
            self.apply_and_cancel.pack()
        except:
            pass

        try:
            self.side_frame.pack_forget()
            self.side_frame.pack()
        except:
            pass

        self.display_action(self.filter_image)

    def display_action(self, image):
        if self.modified:
            self.apply_button.config(state="normal")
            self.revert_button.config(state="normal")
            self.cancel_button.config(state="normal")

        # resize image to fit the canvas
        new_width = CANVA_WIDTH
        new_height = int(image.shape[0] * (new_width / image.shape[1]))

        if new_height > CANVA_HEIGHT:
            new_height = CANVA_HEIGHT
            new_width = int(image.shape[1] * (new_height / image.shape[0]))
        self.display_image = cv2.resize(image, (new_width, new_height))


        self.display_image = Image.fromarray(self.display_image)
        self.display_image = ImageTk.PhotoImage(self.display_image)
        
        pos_x = int((CANVA_WIDTH - self.display_image.width()) / 2)
        pos_y = int((CANVA_HEIGHT - self.display_image.height()) / 2)

        self.canvas.create_image(pos_x, pos_y, image=self.display_image, anchor="nw")

    def crop_image(self):
        pass    

    def draw_on_image(self):
        pass

    def filter_action(self):
        self.refresh_side_frame()
        ttk.Button(self.side_frame, text="Grayscale", 
                   command=self.grayscale).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Blur",
                   command=self.blur_action).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Negative",
                   command=self.negative).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Sharpen",
                   command=self.sharpen).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Stylisation",
                   command=self.stylisation).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Sketch Effect",
                   command=self.sketch_effect).grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Emboss",
                   command=self.emboss).grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Sepia",
                   command=self.sepia).grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
    

    def grayscale(self):
        # check if the image is already grayscale
        if len(self.filter_image.shape) == 2:
            return

        self.editing_image = cv2.cvtColor(self.filter_image, cv2.COLOR_BGR2GRAY)

        self.modified = True
        self.display_action(self.editing_image)

    def blur_action(self):
        self.refresh_side_frame()

        ttk.Label(self.side_frame, text='Average Blur').grid(row=0, column=2, padx=5, sticky="sw")
        self.average_slider = ttk.Scale(self.side_frame, from_=1, to=100, orient=HORIZONTAL, 
                                        command=self.average_blur).grid(row=0, column=3, padx=5, sticky="sw")
        
        
    def average_blur(self, value):
        value = float(value)
        value = int(value)
        if value % 2 == 0:
            value += 1

        self.editing_image = self.filter_image.copy()
        self.editing_image = cv2.blur(self.editing_image, (value, value))

        self.modified = True
        self.display_action(self.editing_image)

    def negative(self):
        pass

    def sharpen(self):
        pass

    def stylisation(self):
        pass

    def sketch_effect(self):
        pass

    def emboss(self):
        pass

    def sepia(self):
        pass



    def save_as(self):
        pass

    def apply_action(self):
        self.filter_image = self.editing_image.copy()
        self.refresh_side_frame()

        self.display_action(self.filter_image)
        
    def cancel(self):
        pass

    def revert_all_change(self):
        pass

    def refresh_side_frame(self):
        try:
            self.side_frame.grid_forget()
        except:
            pass

        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")
        self.display_action(self.filter_image)
        self.side_frame = ttk.Frame(self.frame_menu)
        self.side_frame.grid(row=0, column=11, rowspan=10)
        self.side_frame.config(relief=GROOVE, padding=(50, 15))

if __name__ == "__main__":        
    mainWindow = Tk()
    mainWindow.title("Photoshop")
    mainWindow.iconphoto(False, PhotoImage(file='icon.png'))
    # mainWindow.geometry("1200x600")
    FrontEnd(mainWindow)
    mainWindow.mainloop()