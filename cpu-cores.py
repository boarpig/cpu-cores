#!/usr/bin/env python

import multiprocessing
from random import randint
from math import sqrt, ceil

def generate_core(core_num, core_id):
    core = ""
    id = "[Face-{}]".format(core_id)
    core += id + "[Appearance]\n"
    core += "chartFace=org.kde.ksysguard.linechart\n"
    core += "showTitle=true\n"
    core += "title=Core {}\n\n".format(core_num)

    core += id + "[SensorColors]\n"
    core += "cpu/cpu{}/usage=233,224,61\n\n".format(core_num)

    core += id + "[Sensors]\n"
    core += "highPrioritySensorIds=[\"cpu/cpu{}/usage\"]\n\n".format(core_num)

    core += id + "[org.kde.ksysguard.linechart][General]\n"
    core += "showLegend=false\n"
    core += "showYAxisLabels=false\n\n"
    return core

def generate_column(row_num, column_num, core):
    column = ""
    column += "[page][row-{}][column-{}]\n".format(row_num, column_num)
    column += "name=column-{}\n".format(column_num)
    column += "showBackground=true\n\n"

    column += "[page][row-{}][column-{}][section-0]\n".format(row_num, column_num)
    column += "face=Face-{}\n".format(core)
    column += "isSeparator=false\n"
    column += "name=section-0\n\n"
    return column

def generate_row(row_num, columns, core_ids):
    row = ""
    row += "[page][row-{}]\n".format(row_num)
    row += "Title=\n"
    row += "isTitle=false\n"
    row += "name=row-{}\n\n".format(row_num)

    for column in range(columns):
        row += generate_column(row_num, column, core_ids[column])
    
    return row

def generate_page():
    core_count = multiprocessing.cpu_count()
    core_ids = [str(randint(90000000000000, 99999999999999)) for _ in range(core_count)]

    page = ""

    for core in range(len(core_ids)):
        page += generate_core(core, core_ids[core])

    page += "[page]\n"
    page += "Title=CPU cores\n"
    page += "actionsFace=\n"
    page += "icon=ksysguardd\n"
    page += "margin=1\n\n"

    column_count = ceil(sqrt(core_count))
    for row in range(ceil(core_count / column_count)):
        page += generate_row(row, column_count, core_ids[row * column_count: row * column_count + column_count])
    return page

# TODO: make it save automatically into ~/.local/share/plasma-systemmonitor/cpu-cores.page
# TODO: Check that said file doesn't exist already and prompt for override
# TODO: Add empty columns if core count doesn't line neatly into full rows       
print(generate_page())
