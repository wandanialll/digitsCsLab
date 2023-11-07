import os.path
import tkinter
import copy
import customtkinter as ctk
import tkinter as tk
import random
from PIL import Image, ImageDraw, ImageFont
import tkinter.messagebox as messagebox

#initializations
operation = ["+","-","*","/"]
app = ctk.CTk()
operationHistory = []

#random numbers & target number generation
#wan danial
def generate_numbers():
    numbers = random.sample(range(1,16),6)
    operationHistory.append(numbers)
    return numbers

numbers = generate_numbers()
original_numbers = copy.deepcopy(numbers)

#cases for target number generation
#wan danial & christa tracy
def perform_case_1(numbers):
    num1, num2 = random.sample(numbers, 2)
    operators = ['+', '-', '*', '/']
    operations = []

    while True:
        print("Case 1:")
        print(numbers)
        operator = random.choice(operators)
        if operator == '/':
            if num2 != 0 and num1 % num2 == 0:
                target_num = num1 // num2
                operations.append(f'{num1} {operator} {num2} = {target_num}')
                print(target_num)
                print(operations)
                return target_num, operations
        else:
            result = eval(f'{num1}{operator}{num2}')
            if result > 0 and result % 1 == 0:
                target_num = int(result)
                operations.append(f'{num1} {operator} {num2} = {target_num}')
                print(target_num)
                print(operations)
                return target_num, operations

def perform_case_2(numbers):
    pairs = random.sample(numbers, 4)
    operators = ['+', '-', '*', '/']
    target_num = None
    operations = []

    while target_num is None:
        print("Case 2:")
        print(numbers)
        results = []
        for i in range(0, len(pairs), 2):
            num1, num2 = pairs[i], pairs[i + 1]
            operator = random.choice(operators)
            if operator == '/':
                if num2 != 0 and num1 % num2 == 0:
                    result = num1 // num2
                    results.append(result)
                    operations.append(f'{num1} {operator} {num2} = {result}')
                else:
                    break
            else:
                result = eval(f'{num1}{operator}{num2}')
                if result > 0 and result % 1 == 0:
                    results.append(int(result))
                    operations.append(f'{num1} {operator} {num2} = {int(result)}')
                else:
                    break

        if len(results) == 2:
            target_num, sub_operations = perform_case_1(results)
            operations.extend(sub_operations)
        elif len(results) == 1:
            target_num = results[0]

    return target_num, operations

def perform_case_3(numbers):
    operators = ['+', '-', '*', '/']
    target_num = None
    operations = []
    print("Case 3")

    while True:
        pairs = random.sample(numbers, 6)
        results = []
        for i in range(0, len(pairs), 2):
            num1, num2 = pairs[i], pairs[i + 1]
            operator = random.choice(operators)
            if operator == '/':
                if num2 != 0 and num1 % num2 == 0:
                    result = num1 // num2
                    results.append(result)
                    operations.append(f'{num1} {operator} {num2} = {result}')
                else:
                    break
            else:
                result = eval(f'{num1}{operator}{num2}')
                if result > 0 and result % 1 == 0:
                    results.append(int(result))
                    operations.append(f'{num1} {operator} {num2} = {int(result)}')
                else:
                    break
        if len(results) >= 3:
            target_num, sub_operations = perform_case_1(results[:2])
            operations.extend(sub_operations)
            target_num, sub_operations = perform_case_1([target_num, results[2]])
            operations.extend(sub_operations)
        elif len(results) == 2:
            target_num, sub_operations = perform_case_1(results)
            operations.extend(sub_operations)
        elif len(results) == 1:
            target_num = results[0]

        if target_num is None or target_num <= 0:
            target_num, sub_operations = perform_case_1(numbers[:2])
            operations.extend(sub_operations)

        if target_num is not None and target_num > 0:
            break

    return target_num, operations

def generate_target_number(numbers):
    while True:
        #numbers = generate_numbers()
        num_chosen = random.choice([2, 4, 6])

        if num_chosen == 2:
            target_num, operations = perform_case_1(numbers)
            return numbers, target_num, operations
        elif num_chosen == 4:
            target_num, operations = perform_case_2(numbers)
            return numbers, target_num, operations
        elif num_chosen == 6:
            target_num, operations = perform_case_3(numbers)
            return numbers, target_num, operations

numbers, target_num, operations = generate_target_number(numbers)

# Ensure target_num is not present in the generated numbers
while target_num in numbers:
    numbers, target_num, operations = generate_target_number(numbers)

print(target_num)

target_num_str = str(target_num)

#game mechanic
#wan danial & christa tracy
def perform_operation(numbers, num1, num2, op, target_num):
    global operationHistory
    result = None
    outputBox.delete(1.0, tk.END)
    userOperations = []

    if op == '+':
        result = num1 + num2
    elif op == '-':
        result = num1 - num2
        if  num2 > num1:
            print("Uh Oh You Can't Do That")
            opButton_minus.configure(image=minusButt_default)
            update_button_image()
            errorInvalidOperation()
            resetValue()
    elif op == '*':
        result = num1 * num2
    elif op == '/':
        if num2 != 0 and num1 % num2 == 0:
            result = num1 // num2
        else:
            print("Invalid Division Operation")
            errorInvalidOperation()
            opButton_division.configure(image=divisionButt_default)
            update_button_image()
            resetValue()

    if result is not None and result > 0:
        numbers.remove(num2)
        numbers[numbers.index(num1)] = 0
        numbers.append(result)
        generatePhoto()
        update_button_image()
        resetValue()
        checkWinner(numbers, target_num)
        print(numbers)
        print(target_num)
        operationHistory.append((num1,num2,op,result))
        opButton_add.configure(image=plusButt_default)
        opButton_minus.configure(image=minusButt_default)
        opButton_multiply.configure(image=multiplyButt_default)
        opButton_division.configure(image=divisionButt_default)
        return result
    else:
        return None

#izyann alish
def setValue(numButt):

    if setValue.num1 == numbers[numButt - 1]:
        setValue.num1 = None
        print("num1 deselected")
        outputBox.delete(1.0, tk.END)

        if  numButt == 1:
            button1_bg.configure(image=ring_default)
        elif numButt == 2:
            button2_bg.configure(image=ring_default)
        elif numButt == 3:
            button3_bg.configure(image=ring_default)
        elif numButt == 4:
            button4_bg.configure(image=ring_default)
        elif numButt == 5:
            button5_bg.configure(image=ring_default)
        elif numButt == 6:
            button6_bg.configure(image=ring_default)

    elif  not setValue.num1:
        setValue.num1 = numbers[numButt - 1]
        print("num1 = ", setValue.num1)
        outputBox.insert(tk.END, str(setValue.num1))

        if numButt == 1:
            button1_bg.configure(image=ring_clicked)
        elif numButt == 2:
            button2_bg.configure(image=ring_clicked)
        elif numButt == 3:
            button3_bg.configure(image=ring_clicked)
        elif numButt == 4:
            button4_bg.configure(image=ring_clicked)
        elif numButt == 5:
            button5_bg.configure(image=ring_clicked)
        elif numButt == 6:
            button6_bg.configure(image=ring_clicked)

    else:
        if setOpp.op is None:
            print("Select An Operation Value first")
            errorValueOpNull()

        else:
            setValue.num2 = numbers[numButt - 1]
            print("num2 = ", setValue.num2)
            outputBox.insert(tk.END, str(setValue.num2))

            if numButt == 1:
                button1_bg.configure(image=ring_clicked)
            elif numButt == 2:
                button2_bg.configure(image=ring_clicked)
            elif numButt == 3:
                button3_bg.configure(image=ring_clicked)
            elif numButt == 4:
                button4_bg.configure(image=ring_clicked)
            elif numButt == 5:
                button5_bg.configure(image=ring_clicked)
            elif numButt == 6:
                button6_bg.configure(image=ring_clicked)

            perform_operation(numbers, setValue.num1, setValue.num2, setOpp.op, target_num)

#izyann alish
def setOpp(opButt):
    if setOpp.op == operation[opButt - 1]:
        setOpp.op = None
        print("operation deselected")
        outputBox.delete('end-2c')

        if opButt == 1:
            opButton_add.configure(image=plusButt_default)
        elif opButt == 2:
            opButton_minus.configure(image=minusButt_default)
        elif opButt == 3:
            opButton_multiply.configure(image=multiplyButt_default)
        elif opButt == 4:
            opButton_division.configure(image=divisionButt_default)

    elif  not setOpp.op:
        if setValue.num1 is None:
            print("Select Num1 Value first")
            errorValue2Null()

        else:

            setOpp.op = operation[opButt - 1]
            print("operation =", setOpp.op)
            outputBox.insert(tk.END, str(setOpp.op))

            if  setOpp.op == "+":
                opButton_add.configure(image=plusButt_clicked)
            elif setOpp.op == "-":
                opButton_minus.configure(image=minusButt_clicked)
            elif setOpp.op == "*":
                opButton_multiply.configure(image=multiplyButt_clicked)
            elif setOpp.op == "/":
                opButton_division.configure(image=divisionButt_clicked)

setOpp.op = None
setValue.num1 = None
setValue.num2 = None

#christa tracy
def undoOperation():
    global numbers, operationHistory, original_numbers

    if operationHistory:
        last_operation = operationHistory.pop()
        num1, num2, op, result = last_operation

        if result is not None:
            numbers.remove(result)
            numbers[numbers.index(0)] = num1
            numbers.append(num2)

        generatePhoto()
        update_button_image()
        resetValue()
        outputBox.delete(1.0, tk.END)

        print("Undo successful")
        print(numbers)
        print(target_num)

        opButton_add.configure(image=plusButt_default)

        if not operationHistory:
            print("Nothing to undo")
        else:
            # Update UI elements to reflect the restored numbers
            for i, num in enumerate(numbers):

                button_text = str(numbers[i])
                button = buttons[i]
                button.place(x=button_pos[i][0], y=button_pos[i][1])  # Place the button at the specified position
                if button_text == "0":
                    button.place_forget()

        app.update()

    # Restore original numbers when all operations are undone
    if not operationHistory:
        numbers = original_numbers.copy()

#christa tracy
def startNewGame():
    global numbers, target_num, operations, original_numbers, target_num_str

    # Remove previous numbers and target number
    numbers.clear()
    original_numbers.clear()
    target_num = None
    operationHistory.clear()
    update_button_ring()

    # Generate new numbers and target number
    numbers = generate_numbers()
    original_numbers = copy.deepcopy(numbers)
    numbers, target_num, operations = generate_target_number(numbers)

    # Ensure target_num is not present in the generated numbers
    while target_num in numbers:
        numbers, target_num, operations = generate_target_number(numbers)

    print(target_num)

    announceTargetnum.configure(text=str(target_num))
    showAnswer.configure(text="")  # Clear the previous solution

    # Update UI elements
    outputBox.delete(1.0, tk.END)
    resetValue()
    generatePhoto()
    update_button_image()

    # Update the UI with the new numbers
    for i, num in enumerate(numbers):
        button = buttons[i]
        button.place(x=button_pos[i][0], y=button_pos[i][1])

    # Update the UI
    app.update()

    # Print the target number and numbers
    print("Starting a new game...")
    print("Target number:", target_num)
    print("Numbers:", numbers)

def printSolution(operations):
    operations_str = '\n'.join(operations)
    print("Here is our solution:")
    print(operations)
    showAnswer.configure(text=operations_str)
    app.update()

#checking & setting/updating
def resetValue():
    setOpp.op = None
    setValue.num1 = None
    setValue.num2 = None
    print("Resetting Values")

def checkWinner(numbers, target_num):
    if target_num in numbers:
        showNewGameMessageBox()
    if  numbers.count(0) == len(numbers) - 1:
        non_zero = next(item for item in numbers if item != 0)
        errorNoNumber()

def update_button_ring():

    button1_bg.configure(image=ring_default)
    button2_bg.configure(image=ring_default)
    button3_bg.configure(image=ring_default)
    button4_bg.configure(image=ring_default)
    button5_bg.configure(image=ring_default)
    button6_bg.configure(image=ring_default)

def update_button_image():
    global buttons, numbers, button_bg_list, button_pos
    buttons = [button1, button2, button3, button4, button5, button6]
    button_bg_list = [button1_bg, button2_bg, button3_bg, button4_bg, button5_bg, button6_bg]
    button_pos = [(142.5, 161), (207.5, 161), (272.5, 161), (142.5, 226), (207.5, 226), (272.5, 226)]  # Specify the button positions
    buttonBg_pos = [(130, 150), (195, 150), (260, 150), (130, 215), (195, 215), (260, 215)]
    i = 0
    for i, button in enumerate(buttons):
        button_text = str (numbers[i])
        button.configure(image=numButtPhoto[i])
        button_bg = button_bg_list[i]
        button_bg.configure(image=ring_default)
        print("Reset ring")
        button.place(x=button_pos[i][0], y=button_pos[i][1])  # Place the button at the specified position
        button_bg.place(x=buttonBg_pos[i][0], y=buttonBg_pos[i][1])
        if button_text == "0":
            button.place_forget()

#error & success
#wan danial and christa tracy
def showNewGameMessageBox():
    result = messagebox.askquestion("Target Achieved", "Congratulations! You have achieved the target number.\n\nDo you want to start a new game?")
    if result == "yes":
        startNewGame()
def errorNoNumber():
    result = messagebox.askquestion("Uh Oh", "Oh No, You Ran out of Numbers. \n\n Give it another try?")
    if result == "yes":
        startNewGame()
def errorValue2Null():
    messagebox.showinfo("Uh Oh", "Can't Do That! Choose a Number First")

def errorValueOpNull():
    messagebox.showinfo("Uh Oh", "Can't Do That! Choose an Operation First")

def errorInvalidOperation():
    messagebox.showinfo("Uh Oh", "Can't Do That! Try Another Operation")

#media generation
text = "15"
font_size = 400

# Create a transparent image with text
font = ImageFont.truetype("fonts\\Poppins-Regular.ttf", font_size)
text_width, text_height = font.getsize(text)

image_width = text_width # Add some padding for the text
image_height = text_height

buttonPhoto_generate = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
image_pil = ImageDraw.Draw(buttonPhoto_generate)
text_x = (image_width - text_width) // 2  # Calculate the x-coordinate for centering the text
text_y = (image_height - text_height) // 2  # Calculate the y-coordinate for centering the text
image_pil.text((text_x, text_y), text, fill=(0, 0, 0, 0), font=font)

buttonPhoto = ctk.CTkImage(buttonPhoto_generate)

# generate images for the 6 numbers

font_size = 24

numButtPhoto={}

#wan danial
def generatePhoto():

    for index, number in enumerate(numbers):
        text = str(number)
        font = ImageFont.truetype("fonts\\Poppins-Regular.ttf", font_size)
        image_width = 30
        image_height = 30

        numButtPhoto_generate = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
        image_pil = ImageDraw.Draw(numButtPhoto_generate)
        text_width, text_height = image_pil.textsize(text, font=font)
        text_x = (image_width - text_width) // 2
        text_y = (image_height - text_height) // 2
        image_pil.text((text_x, text_y), text, fill=(0, 0, 0, 255), font=font)

        numButtPhoto[index] = ctk.CTkImage(numButtPhoto_generate)
        file_path = f"ButtNumPhoto\\numButt_{index}.png"
        numButtPhoto_generate.save(file_path, "PNG")

pics=generatePhoto()

#media import
ring_default = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\ring_default.png")), size=(50,50))
ring_clicked = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\ring_clicked.png")), size=(50,50))

plusButt_default = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\plus_default.png")), size=(50,50))
plusButt_clicked = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\plus_clicked.png")), size=(50,50))

minusButt_default = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\minus_default.png")), size=(50,50))
minusButt_clicked = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\minus_clicked.png")), size=(50,50))

multiplyButt_default = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\multiply_default.png")), size=(50,50))
multiplyButt_clicked = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\multiply_clicked.png")), size=(50,50))

divisionButt_default = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\division_default.png")), size=(50,50))
divisionButt_clicked = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\division_clicked.png")), size=(50,50))

equalButt_default = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\equal_default.png")), size=(50,50))
equalButt_clicked = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\equal_clicked.png")), size=(50,50))

undoButt_default = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\undo_default.png")), size=(50,50))
undoButt_clicked = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\undo_default.png")), size=(50,50))

showButt_default = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\show_default.png")), size=(50,50))
showButt_clicked = ctk.CTkImage(dark_image=Image.open(os.path.join("media\\show_clicked.png")), size=(50,50))

font_path = ("fonts\\Poppins-Regular.ttf")

#operation buttons & output box
#wan danial & izyann alish
opButton_add = ctk.CTkButton(master=app, text="", image=plusButt_default, fg_color="transparent", hover="false",border_width=0, corner_radius=0, width=0, command= lambda : setOpp(1))
opButton_add.place(x=90, y=280)

opButton_minus = ctk.CTkButton(master=app, text="", image=minusButt_default, fg_color="transparent", hover="false",border_width=0, corner_radius=0, width=0, command= lambda : setOpp(2))
opButton_minus.place(x=155, y=280)

opButton_multiply = ctk.CTkButton(master=app, text="", image=multiplyButt_default, fg_color="transparent", hover="false",border_width=0, corner_radius=0, width=0, command= lambda : setOpp(3))
opButton_multiply.place(x=225, y=280)

opButton_division = ctk.CTkButton(master=app, text="", image=divisionButt_default, fg_color="transparent", hover="false",border_width=0, corner_radius=0, width=0, command= lambda : setOpp(4))
opButton_division.place(x=294, y=280)

solveButton = ctk.CTkButton(master=app, text="", image=showButt_default, fg_color="transparent", hover="false",border_width=0, corner_radius=0, width=0, command= lambda : printSolution(operations))
solveButton.place(x= 355, y=90)

undoButton = ctk.CTkButton(master=app, text="", image=undoButt_default , fg_color="transparent", hover="false",border_width=0, corner_radius=0,width=1, command= lambda : undoOperation())
undoButton.place(x=35,y=90)

outputBox = ctk.CTkTextbox(app, height=40, width=180, fg_color="white", text_color="black", font=(font_path,18))
outputBox.place(x=130, y=95)

showAnswer = ctk.CTkLabel(master=app, text="", text_color="black", font=(font_path,12))
showAnswer.place(x=355, y=155)

announceTargetnum = ctk.CTkLabel(master=app, text=str(target_num_str), font=(font_path,24), text_color="black")
announceTargetnum.place(x=213, y=58)

announceTargetnumLabel = ctk.CTkLabel(master=app, text="Target Number:", text_color="black", font=(font_path,16))
announceTargetnumLabel.place(x=170, y=33)

#number buttons
button1_bg = ctk.CTkLabel(app, text="",image=ring_default)
button1_bg.place(x=130, y=150)
button1 = ctk.CTkButton(master=app, hover="false",text="",image=numButtPhoto[0], corner_radius=0,border_width=0, width=0,border_spacing=0, fg_color="transparent", command= lambda : setValue(1))
button1.place(x=142.5, y=161)

button2_bg = ctk.CTkLabel(app, text="",image=ring_default)
button2_bg.place(x=195, y=150)
button2 = ctk.CTkButton(master=app, hover="false", text="",image=numButtPhoto[1], corner_radius=0,border_width=0, width=0,border_spacing=0, fg_color="transparent", command= lambda : setValue(2))
button2.place(x=207.5, y=161)

button3_bg = ctk.CTkLabel(app, text="",image=ring_default)
button3_bg.place(x=260, y=150)
button3 = ctk.CTkButton(master=app, hover="false", text="",image=numButtPhoto[2], corner_radius=0,border_width=0, width=0,border_spacing=0, fg_color="transparent", command= lambda : setValue(3))
button3.place(x=272.5, y=161)

button4_bg = ctk.CTkLabel(app, text="",image=ring_default)
button4_bg.place(x=130, y=215)
button4 = ctk.CTkButton(master=app, hover="false", text="",image=numButtPhoto[3], corner_radius=0,border_width=0, width=0,border_spacing=0, fg_color="transparent", command= lambda : setValue(4))
button4.place(x=142.5, y=226)

button5_bg = ctk.CTkLabel(app, text="",image=ring_default)
button5_bg.place(x=195, y=215)
button5 = ctk.CTkButton(master=app, hover="false", text="",image=numButtPhoto[4], corner_radius=0,border_width=0, width=0,border_spacing=0, fg_color="transparent", command= lambda : setValue(5))
button5.place(x=207.5, y=226)

button6_bg = ctk.CTkLabel(app, text="",image=ring_default)
button6_bg.place(x=260, y=215)
button6 = ctk.CTkButton(master=app, hover="false", text="",image=numButtPhoto[5], corner_radius=0,border_width=0, width=0,border_spacing=0, fg_color="transparent", command= lambda : setValue(6))
button6.place(x=272.5, y=226)

#app initialization
app.geometry("450x440")
app.resizable("False","False")
app.title("Digits Ripoff")
app.configure(fg_color="#bad7f2")
app.mainloop()