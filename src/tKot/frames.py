import tkinter as tk
from typing import Literal


class ScrollFrame(tk.Frame):
    """ scrolling use only grid, automatic"""
    first_viewable: int
    last_viewable: int
    yscrollcommand: ()
    # sticky: Literal[tk.W] | Literal[tk.E] | tk.N | tk.S | tk.E | tk.NW | tk.SW | tk.NE | tk.SE | tk.NS | tk.EW | tk.NSEW | tk.CENTER

    def __init__(self, **kwargs):
        super(ScrollFrame, self).__init__(**kwargs)
        self.first_viewable = self.last_viewable = 0  # first initialisation
        self.sticky = tk.W
        self.yscrollcommand = None  # need assigned after Scrollbar
        self.bind("<Configure>", lambda e: self.__handle_configure())

    def __handle_configure(self):
        if self.yscrollcommand:
            h = self.winfo_height()
            childs = self.winfo_children()
            sum = 0
            for c in childs[self.first_viewable:]:
                sum += c.winfo_reqheight()
                if sum > h:
                    self.last_viewable = childs.index(c)
                    break
            else:
                while sum < h and self.first_viewable > 0:
                    self.first_viewable -= 1
                    sum += childs[self.first_viewable].winfo_reqheight()
                self.last_viewable = len(childs)
            for i, c in enumerate(childs):
                if self.last_viewable < i or i < self.first_viewable:
                    if c.winfo_viewable():
                        c.grid_forget()
                    else:
                        pass
                else:
                    if not c.winfo_viewable():
                        c.grid(row=i, sticky=self.sticky)
                    else:
                        pass
            self.yscrollcommand(self.first_viewable / len(childs), self.last_viewable / len(childs))

    def yview(self, *args):
        """Query and change the vertical position of the view."""
        match args:
            case "scroll", offset, "units":
                self.first_viewable += int(offset)
            case "scroll", offset, "pages":
                page = self.last_viewable - self.first_viewable
                self.first_viewable += page * (int(offset))
            case "moveto", point:
                self.first_viewable = int(len(self.winfo_children()) * float(point))
            case err:
                raise ValueError(F"unknown scroll value: {err}")
        self.first_viewable = max(0, self.first_viewable)
        self.__handle_configure()
