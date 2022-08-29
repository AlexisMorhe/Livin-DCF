import random
import numpy as np
import pandas as pd
from numpy import cumsum
from babel.numbers import format_currency

years = [2023, 2024, 2025, 2026, 2027]

sup_crecimiento = np.array([1, 0.05, 0.05, 0, 0])
sup_contratos = 10
sup_impagos = 0.50
sup_valor = 1000000
sup_aprobacion = 0.75
sup_rentabilidad = 0.09
sup_enganche = 0.10
sup_plazo = 3

"""random.randint(1, 200)"""

comision_rentas = sup_rentabilidad * 0.5
comision_ventas = 0.01
porcentaje_devolucion_enganche = 0.4
porcentaje_compensacion = 0.5


contratos = sup_contratos * cumsum(sup_crecimiento)
contratos = np.rint(contratos)

eng = sup_enganche / sup_plazo
eng2 = eng * 2
eng3 = eng * 3
eng4 = eng * 4
eng5 = eng * 5

match sup_plazo:
    case 1:
        data_porcentajes = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]
        data_enganches = [[eng, eng, eng, eng, eng], [0, eng, eng, eng, eng], [0, 0,eng, eng, eng], [0, 0, 0,eng,eng], [0,0,0,0,eng]]

    case 2:
        data_porcentajes = [[.25, .75, 0, 0, 0], [0, .25, .75, 0, 0], [0, 0, .25, .75, 0], [0, 0, 0, .25, .75], [0, 0, 0, 0, .25]]
        data_enganches = [[eng, eng2, eng2, eng2, eng2], [0, eng, eng2, eng2, eng2], [0, 0,eng, eng2, eng2], [0, 0, 0,eng,eng2], [0, 0, 0, 0,eng]]
    case 3:
        data_porcentajes = [[.25, .25, .5, 0, 0], [0, .25, .25, .5, 0], [0, 0, .25, .25, .5], [0, 0, 0, .25, .25], [0, 0, 0, 0, .25]]
        data_enganches = [[eng, eng2, eng3, eng3, eng3], [0, eng, eng2, eng3, eng3], [0, 0, eng, eng2, eng3], [0, 0, 0, eng, eng2], [0, 0, 0, 0, eng]]
    case 4:
        data_porcentajes = [[.125, .125, .25, .5, 0], [0, .125, .125, .25, .5], [0, 0, .125, .125, .25], [0, 0, 0, .125, .125], [0, 0, 0, 0, .125]]
        data_enganches = [[eng, eng2, eng3, eng4, eng4], [0, eng, eng2, eng3, eng4], [0, 0, eng, eng2, eng3], [0, 0, 0, eng, eng2], [0, 0, 0, 0, eng]]

    case 5:
        data_porcentajes = [[.05, .1, .15, .2, .5], [0, .05, .1, .15, .2], [0, 0, .05, .1, .15], [0, 0, 0, .05, .1], [0, 0, 0, 0, .5]]
        data_enganches = [[eng, eng2, eng3, eng4, eng5], [0, eng, eng2, eng3, eng4], [0, 0, eng, eng2, eng3], [0, 0, 0, eng, eng2], [0, 0, 0, 0, eng]]


df_porcentajes = pd.DataFrame(data_porcentajes)
df_casas = df_porcentajes.mul(contratos, axis=0)
df_casas = df_casas.round(0)

df_casas_vendidas = df_casas * sup_aprobacion
df_casas_vendidas = df_casas_vendidas.round(0)
casas_vendidas_col = np.array(df_casas_vendidas.agg('sum'))

df_porcentajes_enganches = pd.DataFrame(data_enganches)
df_enganches = df_porcentajes_enganches.mul(df_casas_vendidas)
df_enganches *= sup_valor

enganches_utilizados = np.array(df_enganches.agg('sum'))
enganches_utilizados = np.round(enganches_utilizados, 0)

casas_col = np.array(df_casas.agg('sum'))
casas_vendidas_acum = np.array(cumsum(casas_col))
casas_vendidas_acum = np.insert(casas_vendidas_acum, 0, 0)
casas_vendidas_acum = np.delete(casas_vendidas_acum, casas_vendidas_acum.size - 1)

df_casas_no_vendidas = df_casas - df_casas_vendidas
casas_no_vendidas_col = np.array(df_casas_no_vendidas.agg('sum'))
df_enganches_no_utilizados = df_porcentajes_enganches.mul(df_casas_no_vendidas)
df_enganches_no_utilizados *= sup_valor

enganches_no_utilizados = np.array(df_enganches_no_utilizados.agg('sum'))
enganches_devueltos = enganches_no_utilizados * porcentaje_devolucion_enganche
compensaciones = enganches_no_utilizados * porcentaje_compensacion

casas_arrendadas = cumsum(contratos) - casas_vendidas_acum
rentas = sup_rentabilidad * casas_arrendadas * sup_valor
rentas_cobradas = rentas * (1 - sup_impagos)


comisiones_rentas = casas_arrendadas * comision_rentas * sup_valor
comisiones_ventas = casas_vendidas_col * comision_ventas * sup_valor
enganches_recibidos = casas_arrendadas * eng * sup_valor
enganches_recibidos = np.round(enganches_recibidos, 0)







empty = ['', '', '', '', '']

filas = ['Year', 'Contratos Realizados', 'Casas Arrendadas', 'Casas Vendidas', 'Casas No Vendidas', 'Ingresos', 'Comisiones Rentas', 'Comisiones Ventas', 'Rentas Cobradas', 'Enganches', 'Gastos', 'Rentas Pagadas', 'Compensaciones', 'Enganches Devueltos', 'Totales']

data = [years, contratos, casas_arrendadas, casas_vendidas_col, casas_no_vendidas_col, empty, comisiones_rentas, comisiones_ventas, rentas_cobradas, enganches_recibidos, empty, rentas, compensaciones, enganches_devueltos, empty]

df = pd.DataFrame(data=data, index = filas)

df_ingresos_totales = pd.DataFrame(df.loc[['Comisiones Rentas', 'Comisiones Ventas', 'Rentas Cobradas', 'Enganches']].sum(axis=0))
df_gastos_totales = pd.DataFrame(df.loc[['Rentas Pagadas', 'Compensaciones', 'Enganches Devueltos']].sum(axis=0))
df_total = df_ingresos_totales.sub(df_gastos_totales)

df_ingresos_totales = df_ingresos_totales.T
df_ingresos_totales = df_ingresos_totales.rename(index={0: 'Ingresos Totales'})
df_gastos_totales = df_gastos_totales.T
df_gastos_totales = df_gastos_totales.rename(index={0: 'Gastos Totales'})
df_total = df_total.T
df_total = df_total.rename(index={0: 'Total'})


totales = [df_ingresos_totales, df_gastos_totales, df_total]
df_totales = pd.concat(totales)
df = pd.concat([df, df_totales])
df = df.round(0)

# df = df.rename(index={0: 'Ingresos Totales', 'Gastos Totales', 'Total'})

print(df)

breakpoint()




