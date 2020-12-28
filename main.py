from tkinter import *
import sounddevice as sd
import soundfile as sf
from datetime import datetime
import queue
import time
from threading import Thread

class Record:
	def __init__(self, can_record):
		self.can_record = can_record
		self.queue = queue.Queue()

class TempLabel:
	def __init__(self, label):
		self.label = label

l = TempLabel(None)
r = Record(True)

def recordStart():
	with sf.SoundFile(str(datetime.now()).replace(":", "-")+".wav", mode='x', samplerate=16000, channels=2) as file:
		with sd.InputStream(samplerate=16000, channels=2, callback=callback):
			while r.can_record:
				file.write(r.queue.get())

def callback(indata, frames, time, status):
    r.queue.put(indata.copy())

def record():
	l.label = Label(tk, text="Recording...", font=("Comic Sans MS", 10))
	l.label.pack()
	l.label.place(x=150, y=160)
	l2.configure(text="Stop")
	l2.configure(command=stop)
	t = Thread(target=recordStart).start()


def stop():
	r.can_record = not r.can_record
	l.label.destroy()
	l2.configure(text="Record")
	l2.configure(command=record)

tk = Tk()
tk.geometry("400x200")
tk.resizable(False, False)

l = Label(tk, text="Sound Recorder", font=("Comic Sans MS", 22))
l.pack()

l2 = Button(tk, text="Record", font=("Arial", 16), command=record)
l2.pack()
l2.place(x=185, y=100, anchor="center")

tk.mainloop()