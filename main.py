''' Program Name: Security snapper
module to install using pip
pip install opencv-python = webcam module
pip install mime = email module
pip install pynput = key press listener
pip install keyboard = key press controller
pip install pyttsx3 = Voice

First you must use the Email Setup menu to configure the email address used by the application.  To initiate the PC Monitor, enter a password in 
the field provided. The application will begin monitoring the keyboard and the window will then disappear.  To disable the application, 
depress the ESC key and reenter the password in the field provided. The application will then stop.'''

import os
import cv2
import threading
import time
import smtplib
import keyboard
import pyttsx3
import re
from os import path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key, Listener
from pynput import mouse
from tkinter import * 
from PIL import ImageTk, Image
from tkinter import messagebox

# Window
root = Tk()
root.title("Security snapper")
root.overrideredirect(False)
root.geometry("+300+300")
root.iconbitmap('Image-icon/1x/icon.ico')

# Voice bot: modules = (pyttsx3)
bot_security = pyttsx3.init()
bot_security.setProperty('rate', 123)

top_image = ImageTk.PhotoImage(Image.open('Image-icon/1x/top_image.png'))
my_image = Label(image=top_image)
my_image.pack(padx=15)

def send_email():
	''' <function send_email>

	This function is used to email the image when a keystroke is detected'''
	
	global file

	try:
		subject = "ALERT"
	    
	    # Email credential 
		msg = MIMEMultipart()
		msg['From'] = email
		msg['To'] = email
		msg['Subject'] = subject
		# Email body
		body = f"Hello,\nYour PC has been touched!!!"
		msg.attach(MIMEText (body, 'plein'))
		# Attachment
		file = 'image.png'
		attachment = open(file, 'rb')
		# Encode attachment
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename= ' + file)

	# Send email
	
		msg.attach(part)
		text = msg.as_string()
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(email, email_pass)
		server.sendmail(email, email, text)
		server.quit()
		bot_security.say("GET OUT MY LAPTOP" * 10)
		bot_security.runAndWait()
		
	except Exception as e:
		messagebox.showerror("email not send", f"{e}")


def cam():
	''' <function Webcam>

	Once the application has been activated by entry of a starting password, 
	this function starts the webcam and listener. For every key pressed, 
	a picture is taken and sent to the email address provided by the user.'''
	
	global key_
	# Check password is not empty
	if not len(enter_password.get()) <= 5:

		# Hide window
		root.overrideredirect(True)
		root.withdraw()
		

		# Variable password entered
		key_ = enter_password.get()

		# Disable options for security
		enter_password.delete(0, END)
		enter_password.config(state='disabled')
		start_application.config(state='disable')
		setup.entryconfig("Quit",state='disabled')
		setup.entryconfig("User Email",state='disabled')

		# Re able entry
		quit_application.config(state='normal')
		enter_password2.config(state="normal")
	
		listening_now = Label(root, text="Listening has started...", fg="red").pack(pady=5)	

	    # Instance of webcam
		webcam = cv2.VideoCapture(0)

		# Function when key press
		def key_press_detection(key):
			
			if key == Key.esc:
				root.deiconify()
			else:
				pass
			return_value, image = webcam.read()
			cv2.imwrite('image.png', image)
			
			time.sleep(10)
 
			threading.Thread(target=send_email())

		# Create listener
		while True:
			with Listener(on_press=key_press_detection) as listener:
				listener.join()
			

		del(webcam)
	else:
		messagebox.showerror("Password", "Password is empty or is less the 6 letters, please enter a Valid password to use for closing the application.")


def quit():
	''' <Function quit>

	Quits the program if re-entered passwrod matches the key, otherwise the program stays active '''

	try:
		if key_ == enter_password2.get():
			root.quit()
		else:
			messagebox.showerror("Password DENIED", "Password incorrect.")
	except Exception as error:
		messagebox.showerror("Password", f"{error}")


def threader():
	''' <Function thread>

	Starts the threading for webcam function and avoid freezing the application.'''

	global t
	t =threading.Thread(target=cam)
	t.setDaemon(True)
	t.start()


def submit_email():
	''' <function submit_email>

	defines user input in email_win as new variable email and email pass. '''
	
	global email
	global email_pass

	regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	if not re.search(regex_email, user_email_e.get()) or  len(user_pass_e.get()) == 0 :
		messagebox.showerror("Email / Password error.", "Email format incorrect. Please enter correct format. Example profilename@Domain.com or password box is empty.")
	else:
		email = user_email_e.get()
		email_pass = user_pass_e.get()
		email_win.destroy()
		email_alert.config(text='Email Configuration OK', fg='green')
		enter_password.config(state='normal')
		enter_password.delete(0, END)
		start_application.config(state='normal')
		

def email_setup():
	''' <function email_setup>

	This function allows the user to enter an email address for the application to use to receive images. '''

	global user_email_e
	global user_pass_e
	global email_win

	email_win = Toplevel()
	email_win.title("Setup user email")

	# Label
	instruction = Label(email_win, text="Enter your email and password. The Application will use this \ninfomation to send the email to some email address. ").pack(pady=15, padx=5)
	user_email = Label(email_win, text="Enter your email: ").pack(pady=(5,0))

	# Entry
	user_email_e = Entry(email_win, bd=2, width=25)
	user_email_e.pack()
	# Label
	user_pass = Label(email_win, text="Enter your password: ").pack(pady=(10, 0))
	# Entry
	user_pass_e = Entry(email_win, bd=2, width=25, show='*')
	user_pass_e.pack(pady=(0, 5))

	# Button
	submit = Button(email_win, text="Submit", command=submit_email)
	submit.pack(pady=5)



# Menu
my_menu = Menu(root)
root.config(menu=my_menu)

setup = Menu(my_menu)
setup = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Email setup', menu=setup)

# Submenu
setup.add_command(label="User Email", command=email_setup)
setup.add_command(label="Quit", command=root.quit)

# Fame
frame_discription = LabelFrame(root, text='Instruction :', pady=5, padx=5)
frame_discription.pack(pady=5, padx=15)

# Label
instruction = Label(frame_discription, text="""1: Configurate your Email in (Email setup) Email entered will serve as sender and reciver. 
2: Enter password to start watching. Application will Disappear \n3: Press (ECS) to reappear application once hidden. It may take 10seconds  
\tif any other key as been was hit. \n4: Re-enter password to stop application """, justify=LEFT).pack(pady=15, padx=5)

password = Label(root, text="Enter a Password : ")
password.pack(pady=(10,0))

# Entry
enter_password = Entry(root, bd=2, width=50)
enter_password.insert(0, "Email Not Configurated")
enter_password.config(state='disabled')
enter_password.pack(pady=2)

# Label
password = Label(root, text="Re-enter Password : ")
password.pack(pady=(10,0))

# Entry
enter_password2 = Entry(root, bd=2, width=50, state='disabled')

enter_password2.pack(pady=2)

# Button
start_application = Button(root, text="Start Watching", state='disabled', command=threader)
start_application.pack(pady=5)

quit_application = Button(root, text="Stop Watching", state='disabled', command=quit)
quit_application.pack(pady=5)

# Label
email_alert = Label(root, text="Email Not Configurated", fg='red')
email_alert.pack(pady=5, padx=10, side=LEFT, anchor=N)

root.mainloop()
if path.exists('image.png'):
	os.remove('image.png')
