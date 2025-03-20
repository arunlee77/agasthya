import tkinter as tk
from tkinter import ttk
import subprocess
from threading import Thread
from tkinter import ttk
from tkinter import messagebox
from tkinter import Label
import os
import time
import re

process = None
is_running = False
machine_option=""

def close_window():
    import os, signal
    global process
    if process is None:
        os.killpg(os.getpid(), signal.SIGTERM)
    else:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)

def clean_script():
    prefix="rm -rf "
    command=prefix+os.getcwd()+"/yocto/build/conf"
    print(command)
    os.system(command)
    command=prefix+os.getcwd()+"/yocto/rasp_pi_build/conf"
    print(command)
    os.system(command)
    command=prefix+os.getcwd()+"/yocto/rock_pi_build/conf"
    print(command)
    os.system(command)
    command=prefix+os.getcwd()+"/yocto/qemux86_64_build/conf"
    print(command)
    os.system(command)
    command=prefix+os.getcwd()+"/yocto/qemuarm64_build/conf"
    print(command)
    os.system(command)

def stop_script():
    import os, signal
    global process
    global is_running
    global stop_button
    global run_button
    is_running = False
    process.kill()
    process.wait()
    process=None
    print("Process killed")
    stop_button.config(bg='grey', state="disabled")
    run_button.config(bg='grey', state="active")
    textbox.delete('1.0', tk.END)

def run_script():
    global process
    global is_running
    global machine_option
    stop_button.config(bg='red', state="active")
    is_running = True
    board_option = board_dropdown.get()
    build_option = build_dropdown.get()
    machine_option = machine_dropdown.get()
    print("board_option: " + board_option)
    print("build_option: " + build_option)
    print("machine_option: " + machine_option)

    print(os.getcwd())
    # Example shell script execution with arguments from dropdowns
    #command = f"./build.sh -c {board_option} -b {build_option} -M {machine_option}"

    command = ['bash', os.getcwd()+'/build.sh', '-c', board_option, '-b', build_option ,'-M', machine_option]
    print(command)

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
        reader_thread = Thread(target=update_output)
        reader_thread.start()
    except Exception as e:
        messagebox.showinfo("Error", str(e))

def update_output():
    global process
    global is_running
    global run_button
    global textbox

    run_button.config(bg='grey', state="disabled")
    is_running = True
    while is_running:
        output=""
        try:
            output = process.stdout.readline()
            if process is not None and output == '' and process.poll() is not None:
                is_running = False
                stop_script()
                break
        except Exception as e:
            #messagebox.showinfo("FullFlash", "CANNOT FLASH")
            is_running = False
            messagebox.showinfo("Error", str(e))
            return
        #Todo search the output and decide the progress of the script
        textbox.insert(tk.END, output)
        textbox.see(tk.END)  # Scroll to the end of the textbox
        if output.find("BuildSuccess") != -1:
            is_running = False
            stop_script()
            break
        if output.find("BuildFailed") != -1:
            is_running = False
            stop_script()
            messagebox.showinfo("Error", "Build Failed")
            break

# Create the main window
root = tk.Tk()
root.title("Agasthya Image Builder")
root.geometry("")
root.resizable(True, True)
root.protocol("WM_DELETE_WINDOW", close_window)

#Dropdowm text
text_frame = tk.Frame(root)
text_frame.pack(pady=10)

group_dropdown_text = tk.Frame(text_frame)
tk.Label(group_dropdown_text, text="Select Board, build folder and machine",font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
group_dropdown_text.pack(side=tk.LEFT, padx=10)


# Frame for dropdowns
frame = tk.Frame(root)
frame.pack(pady=10)

# Dropdown options
boardoptions = ["qemux86_64", "qemuarm64", "x86_64", "rasp_pi", "rock_pi"]
builddiroptions = ["build", "rasp_pi_build", "rock_pi_build", "qemux86_64_buid", "qemuarm64_build"]
machineoptions = ["qemux86-64", "qemuarm64", "x86_64", "raspberrypi4-64", "rockpi-4b-rk3399"]

group_dropdown1 = tk.Frame(frame)
tk.Label(group_dropdown1, text="Board:").pack(side=tk.LEFT, padx=5)
board_dropdown = ttk.Combobox(group_dropdown1, values=boardoptions)
board_dropdown.pack(side=tk.LEFT, padx=5)
board_dropdown.current(0)
group_dropdown1.pack(side=tk.LEFT, padx=5)

group_dropdown2 = tk.Frame(frame)
tk.Label(group_dropdown2, text="Build Directory:").pack(side=tk.LEFT, padx=5)
build_dropdown = ttk.Combobox(group_dropdown2, values=builddiroptions)
build_dropdown.pack(side=tk.LEFT, padx=5)
build_dropdown.current(0)
group_dropdown2.pack(side=tk.LEFT, padx=5)

group_dropdown3 = tk.Frame(frame)
heading4=Label(group_dropdown3, text="Machine:").pack(side=tk.LEFT, padx=5)
machine_dropdown = ttk.Combobox(group_dropdown3, values=machineoptions)
machine_dropdown.pack(side=tk.LEFT, padx=5)
machine_dropdown.current(0)
group_dropdown3.pack(side=tk.LEFT, padx=5)

# Buttons to run and stop the script
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Button to run shell script
run_button = tk.Button(button_frame, text="Build", command=run_script)
run_button.pack(side=tk.LEFT, padx=5)
#run_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_script)
stop_button.pack(side=tk.LEFT, padx=5)
#stop_button.pack(side=tk.LEFT, padx=5)

stop_button.config(bg='grey', state="disabled")
run_button.config(bg='grey', state="active")

# Button to run shell script
clean_button = tk.Button(button_frame, text="Clean", command=clean_script)
clean_button.pack(side=tk.LEFT, padx=5)


# Output display
textbox = tk.Text(root, height=20, width=50)
textbox.pack(side=tk.BOTTOM, fill='both', expand=True)

os.chdir(os.getcwd())
root.mainloop()
