import customtkinter as ctk
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
from datetime import datetime
from sys import exit


try:
    session = WolframLanguageSession()
    session.evaluate('1')  # For some reason the first request takes a very long time. (then it is instant)
    print('The session has been successfully connected. Start')

except:
    root = ctk.CTk()
    root.title("Error")
    root.resizable(False, False)
    root.geometry('370x150')
    label = ctk.CTkLabel(root, text='Failed to connect to WolframKernel.\n'
                                    'Try again or if you don\'t have a default\n'
                                    'installation path specify the path to WolframKernel\n'
                                    '(if you have Windows, don\'t forget the .exe)', font=("Arial", 16))
    label.pack(pady=10, padx=10, fill='x')
    btn = ctk.CTkButton(root, text='Ok', font=("Arial", 16), height=50, command=root.destroy)
    btn.pack(pady=10, padx=10, fill='x')
    root.mainloop()
    exit()


root = ctk.CTk()
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
root.title("Wolfram Calculator")
root.geometry('640x210')
root.resizable(False, True)  # the user will not be able to change the size of the window

last_response = None  # 2-5+ -> error. To ensure that the user does not get an error during the input process, we save the last answer (2-5)

def on_key_release(event):  # function called each time the input field is updated
    current_text = text_var.get()  # get text
    global last_response
    start_time = datetime.now()
    try:
        wl_result = session.evaluate(wlexpr(current_text))
        pretty_wl_result = session.evaluate(wl.ToString(wl_result, wl.InputForm))
        if str(pretty_wl_result) == "$Failed":
            raise ValueError("Incomplete expression; more input is needed")
        else:
            last_response = pretty_wl_result
        print(pretty_wl_result)
    except:
        pretty_wl_result = last_response

    labels[0].configure(text=str(last_response))

    # for autofill
    index = entry.index("insert")  # we'll only take text up to the cursor
    auto_result = autocomplete(current_text[:index])
    labels[1].configure(text=", ".join(auto_result))


    print(f'{current_text} -> {pretty_wl_result}. Suggestions: {auto_result}. Time: {datetime.now()-start_time}')


def copy_to_clipboard(event):
    root.clipboard_clear()
    root.clipboard_append(labels[0].cget("text"))
    root.update()
    # root.iconify()


def on_close():  # need to terminate the session and had to tie this to the closing of the window
    session.terminate()
    root.destroy()


def last_uppercase(s):
    uppercase_letters = [c for c in s if c.isupper()]  # uppercase-only list
    if uppercase_letters:
        last_uppercase_letter = max(uppercase_letters, key=s.index)  # find the last uppercase letter by index
        return last_uppercase_letter
    else:
        return False


def autocomplete(text):
    global dictionary
    uppercase = last_uppercase(text)
    if uppercase:
        text = text[text.rfind(uppercase):]
        suggestions = [word for word in dictionary if word.startswith(text)]
        return suggestions
    else:
        return []


def select_autocomplete(event):
    suggestions = labels[1].cget("text").split(", ")
    if suggestions:
        index = entry.index("insert")
        text = text_var.get()
        last_uppercase_letter = last_uppercase(text[:index])
        first_index = text.rindex(last_uppercase_letter)
        entry.delete(first_index, index)
        entry.insert(entry.index("insert"), suggestions[0])
        labels[1].configure(text="")
        return 'break'


dictionary = ['AbsoluteTiming', 'Solve', 'Sqrt', 'Factor', 'N', 'NSolve', 'ScientificForm', 'Clear']

text_var = ctk.StringVar()

# Create a text field that will update StringVar when text is entered
entry = ctk.CTkEntry(root, textvariable=text_var, font=("Arial", 16), height=40)
entry.pack(pady=10, padx=10, fill='x')


labels = []
label_text = ['Write to ask Mathematica', 'This will be the autofill for Mathematica commands']
for i in range(2):
    label = ctk.CTkLabel(root, text=label_text[i], font=("Arial", 16), wraplength=600)
    label.pack(pady=10, padx=10, fill='x')
    labels.append(label)

btn = ctk.CTkButton(root, text='Ask WolframAlpha', font=("Arial", 16), height=35, corner_radius=16)
btn.pack(pady=10, padx=10, fill='x')


entry.bind('<KeyRelease>', on_key_release)  # any button in 'entry'
entry.bind('<Return>', copy_to_clipboard)
entry.bind('<Tab>', select_autocomplete)

labels[0].bind('<Button-1>', copy_to_clipboard)

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
