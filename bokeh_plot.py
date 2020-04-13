import pandas as pd
import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, show, output_notebook
from bokeh.models import CustomJS
from bokeh.models.widgets import CheckboxGroup
from bokeh.layouts import row, column
from bokeh.palettes import Category20
from bokeh.models.annotations import Title, Legend
from bokeh.models import LinearAxis, Range1d
Category10 = Category20[14]
from bokeh.plotting import reset_output
reset_output()
output_notebook()

# bv1 = pd.read_csv('datasets/bv1_sensors_rus_v3.csv')
bv2 = pd.read_csv('datasets/bv2_sensors_rus_v4.csv')

#bv1['время формирования точки на БВ'] = pd.to_datetime(bv1['время формирования точки на БВ'])
#bv1['время прихода точки на сервере'] = pd.to_datetime(bv1['время прихода точки на сервере'])

bv2['время формирования точки на БВ'] = pd.to_datetime(bv2['время формирования точки на БВ'])
bv2['время прихода точки на сервере'] = pd.to_datetime(bv2['время прихода точки на сервере'])

# df = bv1
df = bv2

df['время формирования точки на БВ'] = pd.to_datetime(df['время формирования точки на БВ'], format='%d/%m/%Y')

p1 = figure(x_axis_type='datetime', plot_width=2500)
p1.extra_y_ranges = {"binary": Range1d(start=-2, end=2)}
aline = p1.circle(df['время формирования точки на БВ'], df['Cекция №1 Заливная горловина'], line_width=2, color=Category10[0],
                 y_range_name="binary")
bline = p1.circle(df['время формирования точки на БВ'], df['Секция №1 Датчик на дне отсека'], line_width=2, color=Category10[1],
                 y_range_name="binary")
cline = p1.circle(df['время формирования точки на БВ'], df['Секция №1 Датчик в сливной магистрали'], line_width=2, color=Category10[2],
                 y_range_name="binary")
dline = p1.circle(df['время формирования точки на БВ'], df[df['Cекция №1 Уровень НП'] < df['Cекция №1 Уровень НП'].quantile(.95)]['Cекция №1 Уровень НП'], line_width=2, color=Category10[3])

eline = p1.circle(df['время формирования точки на БВ'], df['Cекция №3 Заливная горловина'], line_width=2, color=Category10[4],
                 y_range_name="binary")
fline = p1.circle(df['время формирования точки на БВ'], df['Секция №3 Датчик на дне отсека'], line_width=2, color=Category10[5],
                 y_range_name="binary")
gline = p1.circle(df['время формирования точки на БВ'], df['Секция №3 Датчик в сливной магистрали'], line_width=2, color=Category10[6],
                 y_range_name="binary")
hline = p1.circle(df['время формирования точки на БВ'], df[df['Cекция №2 Уровень НП'] < df['Cекция №2 Уровень НП'].quantile(.95)]['Cекция №2 Уровень НП'], line_width=2, color=Category10[7])
iline = p1.circle(df['время формирования точки на БВ'], df['Cекция №4 Заливная горловина'], line_width=2, color=Category10[8],
                 y_range_name="binary")
jline = p1.circle(df['время формирования точки на БВ'], df['Cекция №4 Датчик на дне отсека'], line_width=2, color=Category10[9],
                 y_range_name="binary")
kline = p1.circle(df['время формирования точки на БВ'], df['Секция №4 Датчик в сливной магистрали'], line_width=2, color=Category10[10])
# p2 = figure(x_axis_type='datetime', plot_width=10000)
# eline = p1.circle(df['время прихода точки на сервере'], df['Скорость'], line_width=2, color=Viridis6[5])

p1.yaxis.axis_label = 'Открытие/Закрытие/Уровень НП'
p1.xaxis.axis_label = 'время формирования точки на БВ'
# p2.yaxis.axis_label = 'Скорость'
# p2.xaxis.axis_label = 'время формирования точки на БВ'

legend = Legend(items=[
    ("Секция №1 Заливная горловина", [aline]),
    ("Секция №1 Датчик на дне отсека", [bline]),
    ("Секция №1 Датчик в сливной магистрали", [cline]),
    ("Секция №1 Уровень НП", [dline]),
    ("Cекция №3 Заливная горловина", [eline]),
    ("Секция №3 Датчик на дне отсека", [fline]),
    ("Секция №3 Датчик в сливной магистрали", [gline]),
    ("Секция №3 Уровень НП", [hline]),
    ("Cекция №4 Заливная горловина", [iline]),
    ("Секция №4 Датчик на дне отсека", [jline]),
    ("Секция №4 Датчик в сливной магистрали", [kline]),
], location=(0, 250))

t = Title()
t.text = 'BV2_DUT_sensors'
p1.title = t
# p2.title = t
p1.add_layout(legend, 'left')
p1.add_layout(LinearAxis(y_range_name="binary"), 'right')
# p2.add_layout(legend, 'left')
checkboxes = CheckboxGroup(labels=list(['Секция №1 Заливная горловина', 'Секция №1 Датчик на дне отсека',
                                        'Секция №1 Датчик в сливной магистрали', 'Секция №1 Уровень НП',
                                        'Cекция №3 Заливная горловина', 'Секция №3 Датчик на дне отсека',
                                        'Секция №3 Датчик в сливной магистрали', 'Секция №3 Уровень НП',
                                        'Cекция №4 Заливная горловина', 'Секция №4 Датчик на дне отсека',
                                        'Секция №4 Датчик в сливной магистрали',]),
                           active=[0])
callback = CustomJS(code="""aline.visible = false; // aline and etc.. are 
                            bline.visible = false; // passed in from args
                            cline.visible = false; 
                            dline.visible = false;
                            eline.visible = false;
                            fline.visible = false; 
                            gline.visible = false;
                            hline.visible = false;
                            iline.visible = false; 
                            jline.visible = false;
                            kline.visible = false;
                            // cb_obj is injected in thanks to the callback
                            if (cb_obj.active.includes(0)){aline.visible = true;} 
                                // 0 index box is aline
                            if (cb_obj.active.includes(1)){bline.visible = true;} 
                                // 1 index box is bline
                            if (cb_obj.active.includes(2)){cline.visible = true;} 
                                // 1 index box is bline
                            if (cb_obj.active.includes(3)){dline.visible = true;} 
                                // 1 index box is bline
                            if (cb_obj.active.includes(4)){eline.visible = true;} 
                                // 1 index box is bline
                            if (cb_obj.active.includes(5)){fline.visible = true;} 
                                // 1 index box is bline
                            if (cb_obj.active.includes(6)){gline.visible = true;} 
                                // 1 index box is bline
                            if (cb_obj.active.includes(7)){hline.visible = true;} 
                                // 1 index box is bline
                            if (cb_obj.active.includes(8)){iline.visible = true;} 
                                // 1 index box is bline
                            if (cb_obj.active.includes(9)){jline.visible = true;} 
                                // 1 index box is bline
                            if (cb_obj.active.includes(10)){kline.visible = true;} 
                                // 1 index box is bline
                            """,
                            args={'aline': aline, 'bline': bline, 'cline': cline, 'dline': dline,
                                  'eline': eline, 'fline': fline, 'gline': gline, 'hline': hline,
                                  'iline': iline, 'jline': jline, 'kline': kline})
checkboxes.js_on_click(callback)
layout = row(p1, checkboxes)
# output_file('BV2_DUT_sensors_134_sections.html')
# show(column(p1, p2, checkboxes))
curdoc().add_root(layout)
curdoc().title="BV2"

show(layout)