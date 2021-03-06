# Import Statements
import csv
import plotly.graph_objects as go
import numpy as np
import os
from tkinter import *
from PIL import ImageTk, Image
import math

# Sum of Red, Black and static data rates
lists_red = []
lists_black = []

# GUI
root = Tk()
root.title('ניסוי הדרת המלך')
root.geometry('800x618')

# Background Image
img=ImageTk.PhotoImage(Image.open('./background.jpeg'))
bg_label = Label(root, image=img)
bg_label.place(x=0, y=0)

# 1st Heading
heading_frame = Frame(root, bg='#1a1a1a')
heading_frame.pack(pady=20, padx=60)
heading_Label = Label(heading_frame, bg='#1a1a1a', fg='white', font="Calibri 30", text='ניסוי הדרת המלך')
heading_Label.pack()

# Main Text
main_text_frame = Frame(root, bg='#1a1a1a')
main_text_frame.pack(pady=20, padx=60)
main_text_Label = Label(main_text_frame, anchor='w', font="Calibri 12", text=':בחר את הכלים אותם תרצה להפעיל', bg='#1a1a1a', fg='white')
main_text_Label.pack()

# list of 0 or 1 values indicating if the checkbox is checked
checkboxes_values = []
# An array containing the ship data files
ships_data_files = []

# Checkbuttons frame
check_buttons_frame = Frame(root, bg='#1a1a1a')

# Gets the ships data file names
global count
count=0
ships_data = os.listdir('./')
for file in ships_data:
    if file.endswith('.csv') and file != 'new.csv':
        checkbox_value = IntVar()
        checkbox = Checkbutton(check_buttons_frame, text=f'{file}', variable=checkbox_value, fg='white', bg='black', font='Calibri 11', selectcolor='grey')
        checkbox.pack(anchor='nw')
        # Appends to the data files array and to the checkboxes array to link to eachother
        ships_data_files.append(file)
        checkboxes_values.append(checkbox_value)
        count += 1

    check_buttons_frame.pack(pady=20, padx=60)      


def updateCheckboxes():
    # An array containing the chosen ship data files
    ships_chosen = []
    for value in checkboxes_values:
        if value.get():
            ships_chosen.append(ships_data_files[checkboxes_values.index(value)])
    
    if len(ships_chosen):
        # Levels
        levels = [250000, 1000000, 2500000, 4000000, 5500000, 7000000, 8500000, 10000000, 12000000]

        for ship_file_name in ships_chosen:
            temp_red = []
            # Reading the csv file
            with open(f'./{ship_file_name}', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        try:
                            # Appending the information into the arrays
                            temp_red.append(float(row[1]))
                        except:
                            print('Oops, didnt work')

            # Shifting temp_red before getting temp_black
            num_shift = np.random.randint(0, 1500)
            temp_red = np.roll(temp_red, num_shift)

            # Haderet Hamelech Code
            # Cycle the y values using y values indexes
            current_y_index = 0
            max_y_index = len(temp_red)
            jump_index = 0
            # Current level value
            current_level = levels[math.floor(len(levels) / 2)]

            # Final black y values
            temp_black = []

            while current_y_index < max_y_index:
                # If the y value is bigger than the current level
                if current_level < temp_red[current_y_index]:
                    # if it is not the last level and the y value is bigger than the next level
                    if current_level != levels[-1]:
                        if temp_red[current_y_index] < levels[levels.index(current_level) + 1]:
                            #         We jump to the next level

                            current_level = levels[levels.index(current_level) + 1]
                        else:
                            #         We jump to the higher level (last index)
                            current_level = levels[-1]
                    jump_index = 0
                # If the previous level is bigger than the y value and it is not the lowest level
                elif levels.index(current_level) >= 1:
                    if levels[levels.index(current_level) - 1] > temp_red[current_y_index]:
                        # if we haven't iterated 10 times and there wasn't a jump in the y value
                        if jump_index < 10:
                            if jump_index == 9:
                                current_level = levels[levels.index(current_level) - 1]
                                jump_index = 0
                            else:
                                jump_index += 1
                else:
                    jump_index = 0

                current_y_index += 1
                temp_black.append(current_level)

        #   Append to lists of red, black and static data
            lists_red.append(temp_red)
            lists_black.append(temp_black)

        # Accumulating all the red and black lists
        sum_red = [sum(x) for x in zip(*lists_red)]
        sum_black = [sum(x) for x in zip(*lists_black)]
        sum_static = [6000000 * len(ships_chosen)]

        avg_red = sum(sum_red) / len(sum_red)
        avg_black = sum(sum_black) / len(sum_black)

        x_axis = list(range(1, 2500))

        fig = go.Figure()
        # Static Data Rate Graph
        fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=sum_static * len(x_axis),
                name = "Static Data Rate",
                marker=dict(
                    color='blue'
                )
            ))

        # Red Data Rate Graph
        fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=sum_red,
                name = "Red Data Rate",
                marker=dict(
                    color='red'
                )
            ))

        # Red Data Average Rate Graph
        fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=[avg_red] * len(x_axis),
                name = "Red Data Average Rate",
                marker=dict(
                    color='purple'
                )
            ))

        # Black Data Rate Graph
        fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=sum_black,
                name = "Black Data Rate",
                marker=dict(
                    color='Black'
                )
            ))

        # Black Data Average Rate Graph
        fig.add_trace(
            go.Scatter(
                x=x_axis,
                y=[avg_black] * len(x_axis),
                name = "Black Data Average Rate"
            ))

        fig.show()

        # Exporting the data to csv file
        with open(f'./new.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for i in range(len(x_axis)):
                if i < len(sum_red) and i < len(sum_black):
                    writer.writerow([sum_red[i], sum_black[i], 6000000])
    else:
        Label(root, text='You must choose a .csv file').pack()


showGraphButton = Button(root, text='צור גרף', command=updateCheckboxes, bg='#1a1a1a', font='Calibri 11', fg='white')
showGraphButton.pack()

root.mainloop()
