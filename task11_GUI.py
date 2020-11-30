import task11_num as ln
import PySimpleGUI as sg

sg.theme('DarkPurple3')  # Add a touch of color

# All the stuff inside your window.
def make_table(data):
    #col_widths = [5, 5, 5, 5, 5, 5, 5, 5]
    headers = [' № ', 'x', 'v', 'v2', "v'", "v2'",'ОЛП', ' h ', ' C1 ', ' C2 ']
    col_map = [1 for i in range(len(headers))]
    table_data = [[0 for col in range(len(headers))] for row in range(len(data[0])-1)]
    for row in range(1, len(data[0])):
        table_data[row-1][0] = '{:d}'.format(row)  # step number
        table_data[row-1][1] = '{:.5f}'.format(data[0][row])  # x
        table_data[row-1][2] = '{:.5f}'.format(data[1][row])  # v
        table_data[row-1][3] = '{:.5f}'.format(data[2][row])  # v2
        table_data[row-1][4] = '{:.5f}'.format(data[7][row])  # v'
        table_data[row-1][5] = '{:.5f}'.format(data[8][row])  # v'2
        table_data[row-1][6] = '{:.2E}'.format(data[3][row])  # LE
        table_data[row-1][7] = '{:.2E}'.format(data[4][row])  # h
        table_data[row-1][8] = '{:d}'.format(data[5][row])  # C1
        table_data[row-1][9] = '{:d}'.format(data[6][row])  # C2


    layout = [
        [
            sg.Table(values=table_data, headings=headers, auto_size_columns=True,
                     col_widths=None, num_rows=15, vertical_scroll_only=True, font='Georgia 15',
                     visible_column_map=col_map)
        ],
        [sg.Text("Начальные условия: (x₀, v₀, v₀') = ({:.2f},{:.2f},{:.2f}), h₀ = {:.2E}".format(data[0][0],data[1][0],data[7][0], data[4][0]),
                 font='Georgia 14', text_color="#ADFF2F")],
        [sg.Text("(x, v) – точка численной траектории v(x), вычисленная методом Рунге-Кутта IV с «текущим» шагом,",
            font='Georgia 12')],
        [sg.Text("(x, v2) – точка численной траектории v(x), вычисленная методом Рунге-Кутта IV двойным счетом с половинным шагом,",
                 font='Georgia 12')],
        [sg.Text("(x, v') – точка численной траектории v'(x), вычисленная методом Рунге-Кутта IV с «текущим» шагом,",
                 font='Georgia 12')],
        [sg.Text("(x, v2') – точка численной траектории v'(x), вычисленная методом Рунге-Кутта IV двойным счетом с половинным шагом,",
                 font='Georgia 12')],
        [sg.Text("ОЛП – оценка локальной погрешности, h - текущий шаг, на котором «взяли» точку,",
                 font='Georgia 12')],
        [sg.Text("C1 – счетчик деления шага, С2 – счетчик удвоения шага",
                 font='Georgia 12')],
        [
            sg.Button('Закрыть', size=(7, 1), font='Georgia 15')
        ]
    ]
    return layout


input_frame_layout = [

    [
        sg.Text('u(0):', tooltip="Начальное отклонение груза", font='Georgia 15', text_color="#fff3a3"),
        sg.InputText('10', font='Georgia 15', tooltip="Начальное отклонение груза (см)", size=(3, 1), key='input_y0'),
        sg.Text("u'(0):", tooltip="Начальная скорость груза", font='Georgia 15', text_color="#fff3a3"),
        sg.InputText('0', tooltip="Начальная скорость груза (см/с)", size=(3, 1), font='Georgia 15', key='input_u20',
                     disabled_readonly_background_color=sg.theme_background_color()),
        sg.Text('0 ≤ X ≤', tooltip="Время", font='Georgia 15', text_color="#fff3a3"),
        sg.InputText('20', size=(4, 1), tooltip="Время (с)", font='Georgia 15', key='input_rb'),
        sg.Text('Нач. шаг:', font='Georgia 15', text_color="#fff3a3"),
        sg.InputText('0.05', size=(4, 1), font='Georgia 15', key='input_h'),
    ],

    [
        sg.Text('Параметр контроля погрешности:', font='Georgia 15'), sg.InputText('10e-4', size=(8, 1), font='Georgia 15',
                                          disabled_readonly_background_color=sg.theme_background_color(),
                                          key='input_e')
    ],
    [
        sg.Text('Макс. число шагов:', font='Georgia 15'), sg.InputText('10000', size=(8, 1), font='Georgia 15',
                                                                 disabled_readonly_background_color=sg.theme_background_color(),
                                                                 key='input_N')
    ],


    #   [
    # sg.Text('x0:'), sg.InputText('0', size = (7,1), key = 'input_x0'),
    #   ],

    [
            sg.Text("Контроль выхода на правую границу:", font='Georgia 15'), sg.InputText('0.01', font='Georgia 15', size=(8, 1), key='input_r')
    ],


    [sg.Image("12.png", pad=(5,5))],
    [sg.Text("Параметры задачи:", font='Georgia 15')],
    [
        sg.Text('', size=(1, 1)),
        sg.Text("m:", font='Georgia 15', tooltip="Масса груза"), sg.InputText('0.1', size=(6, 1), key='input_m', font='Georgia 15',
                                                       tooltip="Масса груза (кг)",
                                    disabled_readonly_background_color=sg.theme_background_color()),
        sg.Text("c:", font='Georgia 15', tooltip="Коэффициент демпфирования"), sg.InputText('0.4', size=(6, 1), key='input_c', font='Georgia 15',
                                                        tooltip="Коэффициент демпфирования (Н*с/см^2)",
                                                        disabled_readonly_background_color=sg.theme_background_color()),
        sg.Text('k:', font='Georgia 15', tooltip="Постоянная жесткость первой пружины"), sg.InputText('0.2', size=(6, 1), font='Georgia 15', key='input_k',
                                                       tooltip="Постоянная жесткость первой пружины (Н/см)",
                                    disabled_readonly_background_color=sg.theme_background_color()),
        sg.Text('k*:' , font='Georgia 15', tooltip="Нелинейная характеристика второй пружины"), sg.InputText('0.2', size=(6, 1), font='Georgia 15', key='input_k*',
                                                         tooltip="Нелинейная характеристика второй пружины (Н/см^3)",
                                    disabled_readonly_background_color=sg.theme_background_color()),
    ],
]


output_frame_layout = [[sg.Text(text="", size=(43, 5), font='Georgia 15', key='main_out')]]

layout_main = [
    [
        sg.Frame(layout=input_frame_layout, title='', border_width=0)
    ],

    [
        sg.Frame('Выходные данные:', output_frame_layout, font='Georgia 15', border_width=2)
    ],

    [
        sg.Button('Выход', size=(6, 2), font='Georgia 15'),
        sg.Text('', size=(1, 2)),
        sg.Button(' Условия \nзадачи', size=(7, 2), font='Georgia 15'),
        sg.Button('Таблица', size=(7, 2), font='Georgia 15', disabled=True),
        # sg.Button('Clear', size = (6,1), font=('Avenir 15'), disabled = True),
        sg.Button('Графики', size=(7, 2), font='Georgia 15', disabled=True),
        sg.Button('Вычислить', size=(9, 2), font='Georgia 15', bind_return_key=True)
    ]
]

def show_task():
    picture_frame = [
        [sg.Image('123.png')],
        [sg.Button('Закрыть', size=(7, 1), font='Georgia 15')]
    ]
    return picture_frame


# Create main window
window_main = sg.Window('Задача №11', layout_main, font='Georgia 15')
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window_main.read()
    if event == sg.WIN_CLOSED or event == 'Выход':  # if user closes window or clicks cancel
        break

    # if event == 'Clear':
    #     ln.clear()

    if event == 'Таблица':
        window_table = sg.Window('Таблица', make_table(data))
        while True:
            event_t, values_t = window_table.read()
            if event_t == sg.WIN_CLOSED or event_t == 'Закрыть':
                break
        window_table.close()

    if event == ' Условия \nзадачи':
        window_task = sg.Window(' Условия \nзадачи', show_task())
        while True:
            event_u, values_u = window_task.read()
            if event_u == sg.WIN_CLOSED or event_u == 'Закрыть':
                break
        window_task.close()

    if event == 'Вычислить':
        # window_main.FindElement('Clear').Update(disabled = False)
        # user input
        # x0 = float(values['input_x0'])
        x0 = 0
        try:
            u0 = float(values['input_y0'])
            x_max = float(values['input_rb'])
            h = float(values['input_h'])
            Nmax = float(values['input_N'])  # максимальное кол-во итераций
            e = float(values['input_e'])
            e_rb = float(values['input_r'])
            u20 = float(values['input_u20'])
            k = float(values['input_k'])
            k1 = float(values['input_k*'])
            c = float(values['input_c'])
            m = float(values['input_m'])
        except ValueError:
            sg.Popup('\n  Заполните все поля  \n', title='Ошибка!', font='Georgia 15')

        else:
            window_main.FindElement('Таблица').Update(disabled=True)
            window_main.FindElement('Графики').Update(disabled=True)
            window_main.FindElement('Выход').Update(disabled=True)

            data = ln.num_sol_3_task(k, k1, m, c, Nmax, ln.f_1, ln.f_2, x0, u0, u20, x_max, h, e, e_rb)

            n = data[9]
            rem = '{:.2f}'.format(x_max - data[0][len(data[0])-1])
            maxLE = '{:.2E}'.format(abs(max(data[3], key=abs)))
            main_out = "Кол-во точек численной траектории: n = {} \nX - x_n = {}".format(n, rem)

            # Adding error control output
            maxH = max(data[4])
            minH = min(data[4])
            ind_maxH = data[4].index(maxH)
            x_maxH = '{:.2f}'.format(data[0][ind_maxH])
            ind_minH = data[4].index(minH)
            x_minH = '{:.2f}'.format(data[0][ind_minH])
            maxH = '{:.2E}'.format(maxH)
            minH = '{:.2E}'.format(minH)
            main_out += "\nmax |ОЛП| = {} \nmax h = {} при x = {}\nmin h = {} при x = {}".format(maxLE, maxH, x_maxH, minH, x_minH)
            # Adding test finc output

            window_main.FindElement('main_out').Update(value=main_out)

            window_main.FindElement('Таблица').Update(disabled=False)
            window_main.FindElement('Графики').Update(disabled=False)
            window_main.FindElement('Выход').Update(disabled=False)

    if event == 'Графики':
        ln.draw(data)


window_main.close()
