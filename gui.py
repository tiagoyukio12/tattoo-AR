import tkinter
import main
from os import path
from tkinter import filedialog


tattoo_file = path.join(path.dirname(__file__), "img", "tattoo.png")

def select_tattoo():
	img_dir = path.join(path.dirname(__file__), "img")
	global tattoo_file
	tattoo_file = filedialog.askopenfilename(initialdir=img_dir, filetypes = (("Image files","*.png"),("All files","*.*")))

	lbl.configure(text="Tattoo selecionada:")
	img = tkinter.PhotoImage(file=tattoo_file)
	scale = int(img.height() / 300)
	img = img.subsample(scale)
	lbl1.configure(image=img)
	lbl1.image = img  # Prevent garbage collection from deleting image

def start_test():
	main.main(tattoo_file)


if __name__ == "__main__":
	window = tkinter.Tk()
	window.grid_rowconfigure(0, weight=1)
	window.grid_rowconfigure(1, weight=1)
	window.grid_rowconfigure(2, weight=1)
	window.grid_rowconfigure(3, weight=1)
	window.grid_rowconfigure(4, weight=1)
	window.grid_columnconfigure(0, weight=1)
	window.title("Tattoo AR")
	window.state('zoomed')

	lbl = tkinter.Label(window, text="Tattoo AR", font=("Arial", 25))
	lbl.grid(column=0, row=0)

	lbl = tkinter.Label(window, text="Tattoo selecionada:")
	lbl.grid(column=0, row=1)
      
	img = tkinter.PhotoImage(file=tattoo_file)
	scale = int(img.height() / 300)
	img = img.subsample(scale)
	lbl1 = tkinter.Label(window, image=img)
	lbl1.grid(column=0, row=2)

	btn = tkinter.Button(window, text="Selecionar Tattoo", command=select_tattoo)
	btn.grid(column=0, row=3)	

	btn = tkinter.Button(window, text="Iniciar Teste", command=start_test)
	btn.grid(column=0, row=4)

	window.mainloop()
