import tkinter as tk
from PIL import Image, ImageTk
from .common import Point


class Icon(tk.Widget):
    p_im: Image.Image | None
    im: ImageTk.PhotoImage | None
    info: str | None

    def __init__(self, master=None, **kw):
        self.p_im = kw.pop("pillow_image", None)
        if kw.pop("with_fix", None):
            kw["indicatoron"] = False
            tk.Widget.__init__(self, master, "checkbutton", kw)
        else:
            tk.Widget.__init__(self, master, "button", kw)
        self.im = None
        self.bind("<Configure>", self.__handle_configure)

    def __handle_configure(self, e: tk.Event):
        """auto change image size"""
        if self.p_im:
            h = self.winfo_height()
            """current button height"""
            self.im = ImageTk.PhotoImage(self.p_im.resize((h, h)))
            self.configure(image=self.im, width=h)


class StatusIcon:
    """Icon with status properties"""
    __c: tk.Canvas
    c_id: int
    __current: int
    __im: ImageTk
    __size = Point

    def __init__(self,
                 canvas: tk.Canvas,
                 images: dict[int, Image],
                 default: int = None):
        self.__c = canvas
        """ canvas for widget """
        self.__c_id = -1
        """ Image canvas ID. -1 if not place """
        self.__images = images
        self.__current = 0
        self.__size = Point(100, 100)
        """icon size"""
        self.set_status(tuple(self.__images.keys())[0] if default is None else self.__images[default])

    def get_status(self) -> int:
        """return current status"""
        return self.__current

    def set_status(self, value: int):
        """set status with change image"""
        self.__im = ImageTk.PhotoImage(self.__images[value].resize((self.__size.x, self.__size.y)))
        self.__current = value
        if self.__c_id != -1:
            self.__c.itemconfigure(self.__c_id, image=self.__im)

    def set_size(self, value: Point):
        self.__size = value

    @property
    def size(self):
        return self.__size

    def place(self, x: int, y: int):
        """ replace on canvas by (x, y). Old canvas id shall delete"""
        if self.__c_id != -1:
            self.__c.delete(self.__c_id)
        self.__c_id = self.__c.create_image(x, y,
                                            anchor=tk.NW,
                                            image=self.__im)
