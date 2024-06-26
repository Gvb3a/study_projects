import customtkinter as ctk
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
from datetime import datetime
from sys import exit
from CTkMessagebox import CTkMessagebox
from random import randint

try:
    session = WolframLanguageSession('D:\\Wolfram\\Mathematica\\WolframKernel.exe')
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
root.geometry('640x280')
root.resizable(False, False)

last_response = None
last_request = ''
answer_label = None


def resize_window_to_fit():
    root.update_idletasks()  # Update all "idle" tasks in the GUI
    width = 640
    height = entry.winfo_reqheight() + math_label.winfo_reqheight() + btn.winfo_reqheight() + answer_window_btn.winfo_reqheight() + 40

    # Ensure minimum height for autofill_label
    autofill_label_height = autofill_label.winfo_reqheight() + 40 if autofill_label.cget("text") else 40
    height += autofill_label_height

    if answer_label:
        height += answer_label.winfo_reqheight() + 20  # Add padding for the answer label

    root.geometry(f"{width}x{height}")


def on_key_release(event):  # Function called each time the input field is updated
    current_text = text_var.get()
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
            wl_result = last_response
            pretty_wl_result = last_response

        if pretty_wl_result.startswith('Graphics'):
            name = 'plot.png'
            try:
                a = wl.Export(name, wl_result, "PNG")
                print(f'Graphics: {name}')
                session.evaluate(a)
            except Exception as e:
                print(f'Graphics: {e}')
            pretty_wl_result = 'Graphics'
            last_response = pretty_wl_result  # what kind of incomprehensible code I've created
    else:
        pretty_wl_result = last_response


    math_label.configure(text=pretty_wl_result)
    resize_window_to_fit()  # Resize window

    # For autofill
    index = entry.index("insert")  # We'll only take text up to the cursor
    auto_result = autocomplete(current_text[:index])
    autofill_label.configure(text=", ".join(auto_result))
    resize_window_to_fit()  # Resize window

    print(f'{current_text} >>> {pretty_wl_result}. Suggestions: {auto_result}. Time: {datetime.now()-start_time}')



def copy_to_clipboard(event):
    root.clipboard_clear()
    root.clipboard_append(math_label.cget("text"))
    root.update()
    root.iconify()


def on_close():  # Need to terminate the session and tie this to the closing of the window
    session.terminate()
    root.destroy()


def last_uppercase(s):
    uppercase_letters = [c for c in s if c.isupper()]  # Uppercase-only list
    if uppercase_letters:
        last_uppercase_letter = max(uppercase_letters, key=s.index)  # Find the last uppercase letter by index
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
        resize_window_to_fit()
        return 'break'


first_query = True  # The first query takes a very long time (4-5 seconds)

def warning(request):
    global first_query
    if request.strip() == '':
        CTkMessagebox(title="Empty enquiry",
                      icon="warning",
                      message="Enter your enquiry!!!")
        return True
    elif first_query:
        msg = CTkMessagebox(title="Info",
                            message="The first Wolfram Alpha query and the opening of the response window will take "
                                    "much longer than the following queries (the programme may hang)",
                            options=['OK', 'Cancel'])
        if msg.get() == 'OK':
            first_query = False
    return first_query


def ask_wolfram_alpha():
    global first_query, answer_label
    request = text_var.get()

    if warning(request):
        return

    a = datetime.now()
    result = session.evaluate(wl.WolframAlpha(request))

    for rule in result:
        if rule[0][0] == ('Result', 1) and rule[0][1] == 'Plaintext':
            answer = rule[1]
            break

    else:
        try:
            answer = result[1][1]
        except:
            answer = 'None'

    if not answer_label:
        answer_label = ctk.CTkLabel(root, text=answer, font=("Arial", 16), wraplength=600, height=40)
        answer_label.pack(pady=10, padx=10, fill='x', before=answer_window_btn)
    else:
        answer_label.configure(text=answer)
    resize_window_to_fit()

    print(f'WolframAlpha: {request} >>> {answer}. Time: {datetime.now()-a}')


def answer_window():
    request = text_var.get()
    if warning(request):
        return

dictionary = ['AbsoluteTiming', 'Solve', 'Sqrt', 'Factor', 'N', 'NSolve', 'ScientificForm', 'Clear', 'Plot']

text_var = ctk.StringVar()

# Create a text field that will update StringVar when text is entered
entry = ctk.CTkEntry(root, textvariable=text_var, font=("Arial", 16), height=40)
entry.pack(pady=10, padx=10, fill='x')

math_label = ctk.CTkLabel(root, text='Write to ask Mathematica', font=("Arial", 16), wraplength=600)
math_label.pack(pady=10, padx=10, fill='x')

btn = ctk.CTkButton(root, text='Ask WolframAlpha', font=("Arial", 16), height=40, corner_radius=16,
                    command=ask_wolfram_alpha)
btn.pack(pady=10, padx=10, fill='x')

answer_window_btn = ctk.CTkButton(root, text='Create a reply window', font=("Arial", 16), height=40, corner_radius=16,
                                  command=answer_window)
answer_window_btn.pack(pady=10, padx=10, fill='x')

autofill_label = ctk.CTkLabel(root, text='Autofill for Mathematica commands', font=("Arial", 16), height=40, wraplength=600)
autofill_label.pack(pady=10, padx=10, fill='x')

entry.bind('<KeyRelease>', on_key_release)  # Any button in 'entry'
entry.bind('<Return>', copy_to_clipboard)
entry.bind('<Tab>', select_autocomplete)

math_label.bind('<Button-1>', copy_to_clipboard)

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
