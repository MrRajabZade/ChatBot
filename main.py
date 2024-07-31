import re
import tkinter as tk
from tkinter import scrolledtext
import random

memory = {}
history = []
reply = False
stopwords = []

def save_data(key, value):
    memory[key] = value

def stop_words(stopwords, text):
    for i in stopwords:
        text = str(text).replace(str(i), "")
    return text

def handle_data(data):
    for line in data.split("\n"):
        parts = line.split(" = ")
        if len(parts) == 2:
            if parts[0] == "stepwords":
                i = str(parts[1].split("[", 1)[1].split("]", 1)[0])
                i = i.split(",")
                for n in i:
                    stopwords.append(str(n))
            save_data(parts[0], parts[1])    

def replace_placeholders(response, memory):
    placeholders = set(re.findall(r'#\w+', response))
    for placeholder in placeholders:
        key = placeholder[1:]
        if key in memory:
            response = response.replace(placeholder, memory[key])
    
    return response    

def respond_to_user(input_text):
    global reply
    file = str(open("rulse.txt", "r", encoding="utf-8").read()).split("+")
    handle_data(file[0])
    ruls = file[1].split("\n")
    for ruls in ruls:
        if str(ruls) == "":
            continue
        pattern, response = ruls.split(" : ", 1)
        input_text = str(input_text).replace("ي", "ی")
        if reply:
            try:
                pattern, response = reply.split(" : ", 1)
            except:
                key, value = reply.split(" = ")
                save_data(key, value)
            else:
                if str(input_text) != str(pattern):
                    reply = False
                    pattern, response = ruls.split(" : ")

        if "[" in response:
            i = str(response.split("[", 1)[1].split("]", 1)[0])
            g = "["+str(i)+"]"
            i = i.split(",")
            response = response.replace(str(g), str(random.choice(i)))
        if "*" in pattern:
            regex_pattern = re.escape(pattern).replace(r'\*', '(.*)')
            match = re.match(regex_pattern, input_text)
            if match:
                for i in range(1, len(match.groups()) + 1):
                    response = response.replace('*', match.group(i), 1)
                if "(" in response:
                    reply = str(response.split("(", 1)[1].split(")")[0])
                    response = response.split("(")[0]
                return response
        if "{" in pattern:
            i = str(pattern.split("{", 1)[1].split("}", 1)[0])
            g = "{"+str(i)+"}"
            i = i.split("،")
            regex_pattern = pattern.split(str(g))
            for e in i:
                u = str(regex_pattern[0]+str(e)+regex_pattern[1])
                if str(regex_pattern[0]+str(e)+regex_pattern[1]) == input_text:
                    return response
        if input_text == pattern:
            if input_text == pattern:
                if "#" in response:
                    response = replace_placeholders(response, memory)
                    if "(" in response:
                        reply = str(response.split("(", 1)[1].split(")")[0])
                        response = response.split("(")[0]
                    return response
                else:
                    if "(" in response:
                        reply = str(response.split("(", 1)[1].split(")")[0])
                        response = response.split("(")[0]
                    return response
    return "متوجه نشدم."

def save_history(user_input, bot_response):
    history.append(f"شما: {user_input}\nبات: {bot_response}")

def send():
    user_input = entry.get()
    user_input = user_input.lower()
    if user_input in ['exit', 'quit', 'خداحافظ']:
        chat_area.insert(tk.END, "شما: " + user_input + "\n")
        chat_area.insert(tk.END, "بات: خداحافظ!\n")
        entry.delete(0, tk.END)
        root.quit()
        return

    chat_area.config(state='normal')
    chat_area.insert(tk.END, "شما: " + user_input + "\n")
    entry.delete(0, tk.END)
    
    user_input = stop_words(stopwords, user_input)
    response = respond_to_user(user_input)
    
    if response:
        history_response = response
        chat_area.insert(tk.END, "بات: " + history_response + "\n")
        save_history(user_input, history_response)
    
    chat_area.yview(tk.END)
    chat_area.config(state='disabled')

root = tk.Tk()
root.title("چت‌بات")

chat_area = scrolledtext.ScrolledText(root, state='disabled', height=20, width=70)
chat_area.grid(column=0, row=0)

entry = tk.Entry(root, width=50)
entry.grid(column=0, row=1)

send_button = tk.Button(root, text="ارسال", command=send)
send_button.grid(column=0, row=2)

root.mainloop()
