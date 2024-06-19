import os
import tkinter as tk
from tkinter import filedialog, messagebox
# from zipfile import ZipFile
import htmltemplate_dist as ht



def get_cwd():
    '''
    Work-around to get working directory because os.getcwd() points to wrong
    directory. TODO Investigate why.
    '''
    return '.'


def get_memory_view(filepath):
    with open(filepath, 'rb') as file:
        mem_view = memoryview(file.read())
    return mem_view



class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master, placeholder: str):
        super().__init__(master)

        self.placeholder_text = placeholder
        self.bind("<FocusOut>", self.autofill_empty)


    def autofill_empty(self, event):
        '''
        Makes sure that input text entry is never empty. If empty, it autofills
        with placeholder text.
        '''
        if not self.get():
            self.insert(0, self.placeholder_text)



class FileBrowser(tk.Button):
    def __init__(self, master, path_label: tk.Label, get_file_data=True,
                 filetypes=[('All files', '*')]):
        super().__init__(master, text='Browse', bg='#FFFFFF', 
                         command=self.get_file)

        self.dialog_title = 'Load file'
        self.intial_dir = '.'

        self.path_label = path_label
        self.get_file_data = get_file_data
        self.filetypes = filetypes

        self.content = None
        self.path = None


    def get_file(self):
        '''
        Get the file path and data. Also update the file path label widget with 
        the loaded file path.
        '''
        path = filedialog.askopenfilename(filetypes=self.filetypes, 
                                            title=self.dialog_title, 
                                            initialdir=self.intial_dir)
        if path:
            self.path = path
            self.path_label.config(text=path)
            self.content = get_memory_view(path) if self.get_file_data else None


    def get(self):
        return self.content, self.path



class Tooltip():
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()



def convert():
    # Get parameters
    NAME = projectname.get()
    KMZ_content, KMZ_path = kmz_browser.get()
    SplashImage_content, SplashImage_path = splash_browser.get() 


    # Deal with missing parameters
    if not all((NAME, KMZ_content, KMZ_path)):
        return fail_msgbox.show()
    
    if not all((SplashImage_content, SplashImage_path)):
        SplashImage_path = os.path.join(get_cwd(), 'resources\\loading.gif')
        SplashImage_content = get_memory_view(SplashImage_path)

    # Convert fullpaths to filenames
    KMZ_filename = os.path.split(KMZ_path)[1]
    SplashImage_filename = os.path.split(SplashImage_path)[1]

    # print(NAME)
    # print(KMZ_filename)
    # print(SplashImage_filename)

    # Create main folder and save file inside it
    project_folder = os.path.join(get_cwd(), NAME)
    os.makedirs(project_folder, exist_ok=True)

    with open(os.path.join(project_folder, KMZ_filename), 'wb') as f:
        f.write(KMZ_content)
        f.close()

    with open(os.path.join(project_folder, SplashImage_filename), 'wb') as f:
        f.write(SplashImage_content)
        f.close()

    #prepare folder and files
    ht.KMZ_THREEJS_ADDONS_FILES_ADD_TO_PROJECT(project_folder)

    html_filename = os.path.join(project_folder, f'{NAME}.html')
    with open(html_filename, 'w', encoding="utf-8") as out_file:
        out_file.write(ht.KMZ_HTMLHEAD)
        out_file.write(ht.KMZ_IMPORTLIBS)
        out_file.write(ht.KMZ_OPENINGSCRIPT)
        out_file.write(ht.KMZ_LOADINGIMAGE(SplashImage_filename))
        out_file.write(ht.KMZ_THREEJS_script(KMZ_filename))
        out_file.write(ht.KMZ_CLOSINGSCRIPT)
        out_file.write(ht.KMZ_STYLE)
        out_file.write(ht.KMZ_HTMLFOOT)

    # Send message to user
    return success_msgbox.show()




# Main Window
window = tk.Tk()
window_geometry='800x500'
window_title = 'KMZ to HTML'
window.geometry(window_geometry)
window.title(window_title)
window.columnconfigure(0, weight=1)

# Message boxes
success_msgbox = messagebox.Message(window,
                                    title=window_title, 
                                    type=messagebox.OK, 
                                    icon=messagebox.INFO,
                                    message='Conversion completed.')
fail_msgbox = messagebox.Message(window, 
                                title=window_title,
                                type=messagebox.OK, 
                                icon=messagebox.ERROR,
                                message='Missing required parameters.')

# Frames bakcground color
FRAME_BG = '#dadfe1'


# REQUIRED INPUTS -------------------------------------------------------------

required_frame = tk.LabelFrame(window, 
                               text='Required parameters', 
                               pady=10,
                               font=('Segoe UI', 11, 'bold'),
                               background=FRAME_BG)
required_frame.grid(row=0, column=0, sticky='EW', pady=15)
required_frame.columnconfigure(1, minsize=150)

# KMZ file description label
label_kmz = tk.Label(required_frame, text='KMZ file', background=FRAME_BG)
label_kmz.grid(row=0, column=0, sticky='W', pady=5)

# KMZ file path label
kmz_path_label = tk.Label(required_frame, text='<No file loaded>', 
                          background=FRAME_BG)
kmz_path_label.grid(row=0, column=2, sticky='W', padx=10, pady=5)

# KMZ browser
kmz_browser = FileBrowser(required_frame, kmz_path_label,
                          filetypes=[('KMZ files', ['*.kmz', '*.KMZ'])])
kmz_browser.grid(row=0, column=1, sticky='EW', padx=10, pady=5)
Tooltip(kmz_browser, 'Select the model file (please do not exceed 20MB)')

# Project name input description
label_name = tk.Label(required_frame, text='Project name', background=FRAME_BG)
label_name.grid(row=1, column=0, sticky='W', pady=5)

# Project name text entry
projectname = EntryWithPlaceholder(required_frame, 'NAME')
projectname.insert(0, 'NAME')
projectname.grid(row=1, column=1, sticky='EW', padx=10, pady=5)
Tooltip(projectname, 'Select the project name')

# END OF REQUIRED INPUTS ------------------------------------------------------


# OPTIONAL INPUTS -------------------------------------------------------------

optional_frame = tk.LabelFrame(window,
                               text='Optional parameters',
                               pady=10,
                               font=('Segoe UI', 11, 'bold'),
                               background=FRAME_BG)
optional_frame.grid(row=1, column=0, sticky='EW', pady=10)
optional_frame.columnconfigure(1, minsize=150)

# Splash image description label
label_splash = tk.Label(optional_frame, text='Splash screen', 
                        background=FRAME_BG)
label_splash.grid(row=0, column=0, sticky='W', pady=5)

# Splash image file path label
splash_path_label = tk.Label(optional_frame, text='<No file loaded>', 
                             background=FRAME_BG)
splash_path_label.grid(row=0, column=2, sticky='W', padx=10, pady=5)

# Splash image browser
splash_browser = FileBrowser(optional_frame, splash_path_label, 
                             filetypes=[('GIF files', ['*.gif', '*.GIF'])])
splash_browser.grid(row=0, column=1, sticky='EW', padx=10, pady=5)
Tooltip(splash_browser, 'Select a custom splashscreen GIF animation (please do not ecceed 5MB)')

# Placeholder parameters TODO
for x in range(1, 4):
    lbl = tk.Label(optional_frame, text=f'Extra param.{x}', background=FRAME_BG)
    lbl.grid(row=x, column=0, sticky='W', pady=5)
    entry = tk.Entry(optional_frame)
    entry.grid(row=x, column=1, sticky='EW', padx=10, pady=5)
    Tooltip(entry, 'Example extra optional parameter')

# END OF OPTIONAL INPUTS ------------------------------------------------------


# OK button
ok_frame = tk.Frame(window, highlightbackground="#00A300", highlightthickness=2)
ok_frame.grid(row=2, column=0, sticky='W', pady=20, padx=5)
ok_button = tk.Button(ok_frame, text='Convert now', bg='#FFFFFF', height=2, 
                      width=15, command=convert)
ok_button.grid(sticky='NESW')


# Execute main loop
if __name__ == "__main__":
    window.mainloop()
    