import customtkinter as ctk
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
from datetime import datetime
from sys import exit
from CTkMessagebox import CTkMessagebox


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
root.geometry('640x220')
root.resizable(False, True)  # the user will not be able to change the size of the window

last_response = None  # 2-5+ -> error. To ensure that the user does not get an error during the input process, we save the last answer (2-5)
last_request = ''


def resize_window_to_fit():
    root.update_idletasks()  # Обновить все задачи интерфейса
    width = max(entry.winfo_width(), math_label.winfo_width(), btn.winfo_width(), autofill_label.winfo_width())
    height = entry.winfo_height() + math_label.winfo_height() + btn.winfo_height() + autofill_label.winfo_height() + 60  # добавьте отступы
    root.geometry(f"{width}x{height}")


def on_key_release(event):  # function called each time the input field is updated
    current_text = text_var.get()  # get text
    global last_response, last_request

    start_time = datetime.now()
    if last_request != current_text.strip():
        last_request = current_text.strip()
        try:
            wl_result = session.evaluate(wlexpr(current_text))
            pretty_wl_result = session.evaluate(wl.ToString(wl_result, wl.InputForm))
            if str(pretty_wl_result) == "$Failed":
                raise ValueError("Incomplete expression; more input is needed")
            else:
                last_response = pretty_wl_result
        except:
            pretty_wl_result = last_response
    else:
        pretty_wl_result = last_response

    math_label.configure(text=pretty_wl_result)

    # for autofill
    index = entry.index("insert")  # we'll only take text up to the cursor
    auto_result = autocomplete(current_text[:index])
    autofill_label.configure(text=", ".join(auto_result))


    print(f'{current_text} >>> {pretty_wl_result}. Suggestions: {auto_result}. Time: {datetime.now()-start_time}')


def copy_to_clipboard(event):
    root.clipboard_clear()
    root.clipboard_append(math_label.cget("text"))
    root.update()
    root.iconify()


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
    suggestions = autofill_label.cget("text").split(", ")
    if suggestions:
        index = entry.index("insert")
        text = text_var.get()
        last_uppercase_letter = last_uppercase(text[:index])
        first_index = text.rindex(last_uppercase_letter)
        entry.delete(first_index, index)
        entry.insert(entry.index("insert"), suggestions[0])
        autofill_label.configure(text="")
        return 'break'


first_wolfram_alpha = True  # It's even worse here. The first query takes a very long time (4-5 seconds)
def ask_wolfram_alpha():
    global first_wolfram_alpha
    if first_wolfram_alpha:
        msg = CTkMessagebox(title="Info", message="The first request will be longer than the next. Please wait.",
                            options=['Cancel', 'OK'])
        if msg.get() == 'OK':
            first_wolfram_alpha = False
        else:
            return


    answer_label = ctk.CTkLabel(root, text='answer', font=("Arial", 16), wraplength=600)
    answer_label.pack(pady=10, padx=10, fill='x')

    resize_window_to_fit()
    autofill_label.pack_forget()
    autofill_label.pack(pady=10, padx=10, fill='x')


dictionary = ['AbsoluteTiming', 'Solve', 'Sqrt', 'Factor', 'N', 'NSolve', 'ScientificForm', 'Clear']

text_var = ctk.StringVar()

# Create a text field that will update StringVar when text is entered
entry = ctk.CTkEntry(root, textvariable=text_var, font=("Arial", 16), height=40)
entry.pack(pady=10, padx=10, fill='x')

math_label = ctk.CTkLabel(root, text='Write to ask Mathematica', font=("Arial", 16), wraplength=600)
math_label.pack(pady=10, padx=10, fill='x')

btn = ctk.CTkButton(root, text='Ask WolframAlpha', font=("Arial", 16), height=40, corner_radius=16, command=ask_wolfram_alpha)
btn.pack(pady=10, padx=10, fill='x')

autofill_label = ctk.CTkLabel(root, text='Autofill for Mathematica commands', font=("Arial", 16), wraplength=600)
autofill_label.pack(pady=10, padx=10, fill='x')


entry.bind('<KeyRelease>', on_key_release)  # any button in 'entry'
entry.bind('<Return>', copy_to_clipboard)
entry.bind('<Tab>', select_autocomplete)

math_label.bind('<Button-1>', copy_to_clipboard)

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
