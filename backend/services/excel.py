import pandas as pd


def create_excel(volumes: {str: float}, density: float,
                 coeffs: {str: float}, gas_dict: {str: float},
                 lower_heat: float, energy_data: {str: {}}) -> None:
    df = pd.DataFrame()

    pollGasData = (density, gas_dict['nitrogen'], gas_dict['sulfur'], gas_dict['carbon'], *(None,) * 5)

    pollutants = [['Источники выбросов ЗВ',
                   'Объем сожженного газа (тыс*м3)',
                   'Тип топлива', 'Плотность газа (кг/м3)',
                   'Доля N в газе   (% масс)', 'Доля S в газе   (% масс)', 'Доля C в газе   (% масс)',
                   'Выбросы NO2 (тонн)', 'Выбросы NO (тонн)',
                   'Выбросы SO2 (тонн)', 'Выбросы CO (тонн)',
                   'Всего выбросов ЗВ (тонн)'],
                  ['ГТЭС', volumes['pp'], 'очищенный газ', *pollGasData],
                  ['Турбины по закачке газа', volumes['comp'], 'очищенный газ', *pollGasData],
                  ['Котлы высокого давления', volumes['boil'], 'очищенный газ', *pollGasData]]

    OFFSET_COL = 2
    OFFSET_ROW = 2

    writer = pd.ExcelWriter('report.xlsx', engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Sheet1', index=False)

    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        'bg_color': '#8FC1E7'
    })

    field_format = workbook.add_format({
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        'bg_color': '#F7F7F7'
    })

    field_format_polutants = workbook.add_format({
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        'bg_color': '#D6E9F8',
    })

    field_format_total = workbook.add_format({
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        'bg_color': '#F4EED1',
    })

    title_format = workbook.add_format({
        'bold': True,
        'font_size': 18,
    })

    arr = pollutants[0]
    for j in range(len(arr)):
        if j == 0:
            worksheet.set_column(OFFSET_ROW, j + OFFSET_COL, len(arr[j]) / 1.5)
        else:
            worksheet.set_column(OFFSET_ROW, j + OFFSET_COL, len(arr[j]) / 1.6)

    worksheet.set_row(OFFSET_ROW, 47)

    def worksheet_write(field_format):
        worksheet.write(row, j + OFFSET_COL, i[j], field_format)

    def worksheet_write_formula(formula, field_format):
        worksheet.write_formula(row, j + OFFSET_COL, formula, field_format)

    row = OFFSET_ROW

    for i in pollutants:
        for j in range(len(i)):
            if row == OFFSET_ROW:
                worksheet_write(header_format)

            elif (row != OFFSET_ROW) and (7 <= j < len(i) - 1):
                cells = ['G', 'G', 'H', 'I']  # клетки в которых записаны доли хим. элементов в газе
                coeffList = [coeffs['NO2coef'], coeffs['NOcoef'], coeffs['SO2coef'], coeffs['COcoef']]
                ci = j - 7
                rowNum: str = str(row + 1)
                formula = f'=ROUND({coeffList[ci]}*D{rowNum}*F{rowNum}*{cells[ci]}{rowNum}, 2)'
                worksheet_write_formula(formula, field_format_polutants)

            elif j == len(i) - 1:
                formula = f'=SUM(J{str(row + 1)}:M{str(row + 1)})'
                worksheet_write_formula(formula, field_format_total)

            else:
                worksheet_write(field_format)

        row += 1

    title1 = 'Расчет выбросов ЗВ'
    worksheet.write(OFFSET_ROW - 2, 5 + OFFSET_COL, title1, title_format)
    worksheet.set_column(OFFSET_ROW - 2, 5 + OFFSET_COL, len(title1) - 3)

    header_format_grhs = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        'bg_color': '#E4B3B3'
    })

    field_format_grhs = workbook.add_format({
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        'bg_color': '#FFE7E7',
    })

    grhsGasData = (density, lower_heat, gas_dict['CO2EmissionFactor'],
                   gas_dict['CH4SpecificFactor'], gas_dict['N2OSpecificFactor'], *(None,) * 4)

    grhsGases = [['Источники выбросов ПГ',
                  'Объем сожженного газа (тыс*м3)',
                  'Тип топлива', 'Плотность газа (кг/м3)',
                  'Низшая теплота сгорания Q (ГДж/т)',
                  'Фактор эмиссии CO2 (тCO2/TДж)',
                  'Удельный коэффициент CH4',
                  'Удельный коэффициент N2O',
                  'Выбросы CO2 (тонн)',
                  'Выбросы CH4 (тонн)',
                  'Выбросы N2O (тонн)',
                  'Всего выбросов ПГ (тонн)'],
                 ['ГТЭС', volumes['pp'], 'очищенный газ', *grhsGasData],
                 ['Турбины по закачке газа', volumes['comp'], 'очищенный газ', *grhsGasData],
                 ['Котлы высокого давления', volumes['boil'], 'очищенный газ', *grhsGasData]]

    row = OFFSET_ROW + 8

    worksheet.set_column(
        OFFSET_ROW + 8, len(grhsGases[0])
        + OFFSET_COL, len(grhsGases[0][-1]) / 2
    )

    for i in grhsGases:
        for j in range(len(i)):

            if row == OFFSET_ROW + 8:
                worksheet_write(header_format_grhs)

            elif (row != OFFSET_ROW + 8) and (8 <= j < len(i) - 1):
                cells = ['H', 'I', 'J']
                coeffList = [coeffs['CO2coef'], coeffs['CH4coef'], coeffs['N2Ocoef']]
                ci = j - 8
                rowNum: str = str(row + 1)
                formula = f'=ROUND({coeffList[ci]}*D{rowNum}*F{rowNum}*G{rowNum}*{cells[ci]}{rowNum}, 2)'
                worksheet_write_formula(formula, field_format_grhs)

            elif j == len(i) - 1:
                formula = f'=SUM(K{str(row + 1)}:M{str(row + 1)})'
                worksheet_write_formula(formula, field_format_total)

            else:
                worksheet_write(field_format)

        row += 1

    title2 = 'Расчет выбросов ПГ'
    worksheet.write(OFFSET_ROW + 6, 5 + OFFSET_COL, title2, title_format)
    worksheet.set_column(OFFSET_ROW + 6, 5 + OFFSET_COL, len(title2) - 3)

    energyPP = [['Источник потребления энергии', 'Время работы (часы)',
                 'Объем сожженного газа (тыс*м3)', 'Выработанная электроэнергия (МВт*ч)',
                 'Показатель энергоэффективности (м3 ТГ/МВт)'],
                ['ГТЭС', energy_data['pp']['hours'], volumes['pp'],
                 energy_data['pp']['generatedEnergy'], None]]

    energyComp = [['Источник потребления энергии', 'Время работы (часы)',
                   'Объем сожженного газа (тыс*м3)', 'Объем закаченного газа (тыс*м3)',
                   'Показатель энергоэффективности (м3 ТГ/м3 СГ)'],
                  ['Турбины по закачке газа', energy_data['comp']['hours'],
                   volumes['comp'], energy_data['comp']['volumeOfInjected'], None]]

    energyBoil = [['Источник потребления энергии', 'Время работы (часы)',
                   'Объем сожженного газа (тыс*м3)', 'Объем пара (тонн)',
                   'Показатель энергоэффективности (м3 ТГ/м3 тонна пара)'],
                  ['Котлы высокого давления', energy_data['boil']['hours'],
                   volumes['boil'], energy_data['boil']['volumeOfSteam'], None]]

    header_format_energy = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        'bg_color': '#DDDEC1'
    })

    field_format_grhs = workbook.add_format({
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        'bg_color': '#FFE7E7',
    })

    row = OFFSET_ROW + 16
    OFFSET_COL = 1

    for i in energyPP:
        for j in range(len(i)):

            if row == OFFSET_ROW + 16:
                worksheet_write(header_format_energy)

            elif j == len(i) - 1:
                rowNum: str = str(row + 1)
                formula = f'=ROUND(D{rowNum}*C{rowNum}/E{rowNum}, 2)'
                worksheet_write_formula(formula, field_format_total)

            else:
                worksheet_write(field_format)

        row += 1

    row = OFFSET_ROW + 16
    OFFSET_COL = 7

    for i in energyComp:
        for j in range(len(i)):

            if row == OFFSET_ROW + 16:
                worksheet_write(header_format_energy)

            elif j == len(i) - 1:
                rowNum: str = str(row + 1)
                formula = f'=ROUND(J{rowNum}/K{rowNum}, 2)'
                worksheet_write_formula(formula, field_format_total)

            else:
                worksheet_write(field_format)

        row += 1

    arr = energyBoil[0]
    for j in range(len(arr)):
        if j == len(arr) - 1:
            worksheet.set_column(OFFSET_ROW + 16, j + 13, len(arr[j]) / 3)

    row = OFFSET_ROW + 16
    OFFSET_COL = 13

    for i in energyBoil:
        for j in range(len(i)):

            if row == OFFSET_ROW + 16:
                worksheet_write(header_format_energy)

            elif j == len(i) - 1:
                rowNum: str = str(row + 1)
                formula = f'=ROUND(P{rowNum}/Q{rowNum}, 2)'
                worksheet_write_formula(formula, field_format_total)

            else:
                worksheet_write(field_format)

        row += 1

    title_format2 = workbook.add_format({
        'bold': True,
        'font_size': 18
    })

    title3 = 'Расчет энергоэффективности'
    worksheet.write(OFFSET_ROW + 14, 7, title3, title_format2)
    worksheet.set_column(OFFSET_ROW + 14, 7, len(title3) - 14)

    writer.save()

