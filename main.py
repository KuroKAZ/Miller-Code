# Код Миллера (иногда называют трехчастотным) — один из способов линейного кодирования (физического кодирования, канального кодирования, импульсно-кодовая модуляция, манипуляция сигнала). Применяется для передачи информации, представленной в цифровом виде от передатчика к приемнику (например по последовательному интерфейсу, оптоволокну). Код формируемый согласно правилу кода Миллера: является двухуровневым (сигнала может принимать два потенциальных значения, например: высокий и низкий уровень напряжения) кодом, в котором каждый информационный бит кодируется комбинацией из двух значений потенциала, всего таких комбинаций 4 {00, 01, 10, 11}, а переходы из одного состояния в другое описываются графом. При непрерывном поступлении логических «нулей» или «единиц» на кодирующее устройство переключение полярности происходит с интервалом T, а переход от передачи «единиц» к передаче «нулей» с интервалом 1,5T. При поступлении на кодирующее устройство последовательности 101 возникает интервал 2Т, по этой причине данный метод кодирования называют трехчастотным. Переход с одного уровня на другой обеспечивает процесс синхронизации передатчика с приемником, в данном способе передачи осуществляется переключение с одного уровня на другой с минимальной частотой 2Т, что обеспечивает синхронизацию передатчика с приёмником.
# Входные данные: последовательность нулей и единиц
# Выходные данные: последовательность сигналов (00, 01, 10, 11)
# Пример:
# Вход: 0101000000011111100110
# Выход: 00 01 11 10 11 00 11 00 11 00 11 10 01 10 01 10 01 11 00 01 10 00

import sys
from typing import LiteralString
import matplotlib.pyplot as plt
import tkinter as tk


def miller_code(input) -> LiteralString:
    output = []
    # prev_bit = None
    for i, bit in enumerate(input, 0):
        if i == 0:  # first bit
            if bit == "0":
                output.append("00")
            else:
                output.append("11")
            # prev_bit = bit
        else:
            if bit == "0":
                if output[i - 1] == "00" or (
                    i > 3
                    and all(
                        [
                            input[i - 1] == "1",
                            input[i - 2] == "0",
                            input[i - 3] == "1",
                        ]
                    )
                ):
                    output.append("11")
                elif output[i - 1] == "11":
                    output.append("00")
                elif output[i - 1] == "01":
                    output.append("11")
                elif output[i - 1] == "10":
                    output.append("00")
                else:
                    sys.exit("Error")
            else:  # bit == "1"
                if output[i - 1] == "00":
                    output.append("01")
                elif output[i - 1] == "11":
                    output.append("10")
                elif output[i - 1] == "01":
                    output.append("10")
                elif output[i - 1] == "10":
                    output.append("01")
                else:
                    sys.exit("Error")
            # prev_bit = bit

    return " ".join(output)


def main(message: str, result: str) -> str:
    # Repeat every bit in the ori1nal message twice to match the Miller code
    original = []
    for bit in message:
        original.append(int(bit, base=2))
        original.append(int(bit, base=2))

    # Build a plot of the result to visualize the signal with matplotlib
    print(result)

    fig, axs = plt.subplots(2)
    if fig.canvas.manager:
        fig.canvas.manager.set_window_title("Код Миллера")

    # Convert the result string to a list of integers
    signal = [int(bit, base=2) for bit in result.replace(" ", "")]

    # Create x-axis values based on the length of the signal
    x = range(signal_len := len(signal))

    # Show the original message in the plot as well
    x = range(original_len := len(original))
    axs[0].set_xticks(x)
    axs[0].step(x, original)
    axs[0].set_xlabel("Время")
    axs[0].set_ylabel("Бит")
    axs[0].set_title("Оригинальное сообщение")

    for i in range(original_len):
        bit = original[i]
        if i < original_len - 1:
            bit = original[i + 1]
        axs[0].text(i, bit, str(bit))
    # Show value of each bit in the plot

    for i in range(signal_len):
        bit = signal[i]
        if i < signal_len - 1:
            bit = signal[i + 1]
        axs[1].text(i, bit, str(bit))

    # Create a subplot for the result using plt.subplots
    axs[1].set_xticks(x)
    axs[1].step(x, signal)
    axs[1].set_xlabel("Время")
    axs[1].set_ylabel("Бит")
    axs[1].set_title("Код Миллера")
    fig.tight_layout()

    return result


def run_code_with_input():
    # Get the input from the input field
    input = input_field.get()
    # Run the code with the input and update the output field
    try:
        result = main(input, miller_code(input))
    except Exception as e:
        # Check if e is ValueError
        if isinstance(e, ValueError):
            output_field_str.set("Ошибка: Введён недействительный сигнал")
        else:
            output_field_str.set(f"Ошибка: {e}")
    else:
        output_field_str.set(result)
        # Show the plot
        plt.show()


font = "Calibri 14"

# Create a new window
window = tk.Tk()
# Set the title of the window
window.title("Код Миллера")

# Use a dark theme for the window, but use activeBackground that does not match the background
window.tk_setPalette(
    background="#1e1e1e", foreground="#d4d4d4", activeBackground="#f3f3f3"
)

input_label = tk.Label(text="Входное сообщение:", font=font)
input_label.pack()

input_field_str = tk.StringVar()
input_field = tk.Entry(window, textvariable=input_field_str, font=font, width=50)
input_field.pack()

# Separate the input and output fields with a frame
frame = tk.Frame(window, height=20, bd=1, relief="sunken")
frame.pack()

output_label = tk.Label(text="Выходное сообщение:", font=font)
output_label.pack()

output_field_str = tk.StringVar()
output_field = tk.Entry(window, textvariable=output_field_str, font=font, width=50)
output_field.pack()

frame = tk.Frame(window, height=20, bd=1, relief="sunken")
frame.pack()

button = tk.Button(window, text="Запустить", command=run_code_with_input, font=font)
button.pack()

# When the button is clicked, run the code and update the output field
output_field_str.set(miller_code(input_field.get()))

# Run the window centered on the screen and expand its size
window.update()

# Center the window on the screen
x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
window.minsize(int(x), int(y))
window.geometry("+%d+%d" % (x, y))
window.mainloop()
