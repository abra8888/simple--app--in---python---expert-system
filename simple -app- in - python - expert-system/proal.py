import PySimpleGUI as psg
import PySimpleGUI as sg

import os
from PIL import Image, ImageTk
import io
sg.theme('SandyBeach')
layout = [
    [sg.Text('Please enter your Name')],
    [sg.Text('Name', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Simple data entry window', layout)
event, values = window.read()
print(event, values[0])
folder = sg.popup_get_folder('Image folder to open', default_path='')
if not folder:
    sg.popup_cancel('Cancelling')
    raise SystemExit()
img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp",".jfif")


flist0 = os.listdir(folder)


fnames = [f for f in flist0 if os.path.isfile(
    os.path.join(folder, f)) and f.lower().endswith(img_types)]

num_files = len(fnames)
if num_files == 0:
    sg.popup('No files in folder')
    raise SystemExit()

del flist0

def get_img_data(f, maxsize=(1200, 850), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)
# ------------------------------------------------------------------------------


filename = os.path.join(folder, fnames[0])
image_elem = sg.Image(data=get_img_data(filename, first=True))
filename_display_elem = sg.Text(filename, size=(80, 3))
file_num_display_elem = sg.Text('File 1 of {}'.format(num_files), size=(15, 1))

# define layout, show and read the form
col = [[filename_display_elem],
       [image_elem]]

col_files = [[sg.Listbox(values=fnames, change_submits=True, size=(60, 30), key='listbox')],
             [sg.Button('Next', size=(8, 2)), sg.Button('Prev', size=(8, 2)), file_num_display_elem]]

layout = [[sg.Column(col_files), sg.Column(col)]]

window = sg.Window('Image Browser', layout, return_keyboard_events=True,
                   location=(0, 0), use_default_focus=False)


i = 0
while True:

    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED:
        break
    elif event in ('Next', 'MouseWheel:Down', 'Down:40', 'Next:34'):
        i += 1
        if i >= num_files:
            i -= num_files
        filename = os.path.join(folder, fnames[i])
    elif event in ('Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33'):
        i -= 1
        if i < 0:
            i = num_files + i
        filename = os.path.join(folder, fnames[i])
    elif event == 'listbox':            # something from the listbox
        f = values["listbox"][0]            # selected filename
        filename = os.path.join(folder, f)  # read this file
        i = fnames.index(f)                 # update running index
    else:
        filename = os.path.join(folder, fnames[i])
    image_elem.update(data=get_img_data(filename, first=True))
    # update window with filename
    filename_display_elem.update(filename)

    file_num_display_elem.update('File {} of {}'.format(i+1, num_files))


# define layout
layout = [[psg.Text('Choose a design for the bedroom ', size=(20, 1), font='Lucida', justification='left')],
          [psg.Combo(['Bedroom1', 'Bedroom2', 'Bedroom3'],
                     default_value='Choose', key='disb')],
          [psg.Text('Choose a kitchen design ', size=(30, 1), font='Lucida', justification='left')],
          [psg.Combo(['kitchen1', 'kitchen2', 'kitchen3'],
                     key='desk')],
          [psg.Text('Choose a bathroom design', size=(30, 1), font='Lucida', justification='left')],
          [psg.Listbox(values=['bathroom1', 'bathroom2', 'bathroom3'],
                       select_mode='extended', key='desibt', size=(30, 6))],
          [psg.Button('SAVE', font=('Times New Roman', 12)), psg.Button('CANCEL', font=('Times New Roman', 12))]]

win = psg.Window('Customise your Home', layout)

e, v = win.read()
sg.popup('The result ','all your choice',v)
win.close()

