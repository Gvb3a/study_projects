import customtkinter as ctk
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

# Start a Wolfram Language session
session = WolframLanguageSession('D:\\Wolfram\\Mathematica\\MathKernel.exe')
session.evaluate('1')  # For some reason the first request takes a very long time. (then it is instant)

root = ctk.CTk()
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
root.title("Wolfram Calculator")
root.geometry('640x165')
root.resizable(False, False)  # the user will not be able to change the size of the window

last_response = None  # 2-5+ -> error. To ensure that the user does not get an error during the input process, we save the last answer (2-5)

def on_key_release(event):  # function called each time the input field is updated
    current_text = text_var.get()  # get text
    global last_response
    try:
        wl_result = session.evaluate(wlexpr(current_text))
        pretty_wl_result = session.evaluate(wl.ToString(wl_result, wl.InputForm))
        if str(pretty_wl_result) == "$Failed":
            raise ValueError("Incomplete expression; more input is needed")
        else:
            last_response = pretty_wl_result
            label.configure(text=pretty_wl_result)
    except:
        label.configure(text=str(last_response))

    # for autofill
    index = entry.index("insert")  # we'll only take text up to the cursor
    auto_result = autocomplete(current_text[:index])
    label_autofill.configure(text=", ".join(auto_result))

    if auto_result:  # I'll definitely make a proper window change, but not today...
        root.geometry('640x165')
    else:
        root.geometry('640x125')


def copy_to_clipboard(event):
    root.clipboard_clear()
    root.clipboard_append(label.cget("text"))
    root.update()
    # root.iconify()


def on_close():
    session.terminate()
    root.destroy()

def check_uppercase(s):
    uppercase_letters = [c for c in s if c.isupper()]
    if uppercase_letters:
        last_uppercase_letter = max(uppercase_letters, key=s.index)
        return True, last_uppercase_letter
    else:
        return False, None


def autocomplete(text):
    global dictionary
    has_uppercase, last_uppercase = check_uppercase(text)
    if has_uppercase:
        suggestions = [word for word in dictionary if word.startswith(text[text.rfind(last_uppercase):])]
        return suggestions
    else:
        return []


def select_autocomplete(event):
    suggestions = label_autofill.cget("text").split(", ")
    if suggestions:
        entry.delete(0, 'end')
        entry.insert(0, suggestions[0])
        label_autofill.configure(text="")
        entry.icursor(ctk.END)  # Putting the cursor at the end of a line
        return 'break'

dictionary = ['AbsoluteTiming', 'Solve', 'Sqrt', 'Factor', 'N', 'NSolve', 'ScientificForm', 'Clear']

text_var = ctk.StringVar()

# Create a text field that will update StringVar when text is entered
entry = ctk.CTkEntry(root, textvariable=text_var, font=("Arial", 16), height=40)
entry.pack(pady=10, padx=10, fill='x')


label = ctk.CTkLabel(root, text='Hello', font=("Arial", 16), height=40, wraplength=600)
label.pack(pady=10, padx=10, fill='x')


label_autofill = ctk.CTkLabel(root, text='Autofill', font=("Arial", 16), height=40, wraplength=600)
label_autofill.pack(pady=10, padx=10, fill='x')


entry.bind('<KeyRelease>', on_key_release)  # any button in 'entry'
entry.bind('<Return>', copy_to_clipboard)
entry.bind('<Tab>', select_autocomplete)

label.bind('<Button-1>', copy_to_clipboard)

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
