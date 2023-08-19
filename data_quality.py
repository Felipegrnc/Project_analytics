import pandas as pd
import numpy as np
from global_variables import casos_ruta
from global_variables import edu_vial2018_ruta
from global_variables import encuesta_calidad_ruta
from global_variables import encuesta_cultura_ruta
from global_variables import hurto_tp_ruta
from global_variables import lesion_nf_ruta
from global_variables import mede_victimas_ruta
from global_variables import traffic_ruta
from global_variables import compar_ruta


def cargue_datasets():
    casos=pd.read_csv(casos_ruta, delimiter=";", encoding="utf-8")
    edu_vial2018=pd.read_csv(edu_vial2018_ruta, delimiter=";", encoding="utf-8")
    encuesta_calidad=pd.read_csv(encuesta_calidad_ruta, delimiter=";", encoding="utf-8")
    encuesta_cultura=pd.read_csv(encuesta_cultura_ruta, delimiter=";", encoding="utf-8")
    hurto_tp=pd.read_csv(hurto_tp_ruta, delimiter=";", encoding="utf-8")
    lesion_nf=pd.read_csv(lesion_nf_ruta, delimiter=";", encoding="utf-8")
    mede_victimas=pd.read_csv(mede_victimas_ruta, delimiter=";", encoding="utf-8")
    traffic=pd.read_csv(traffic_ruta, delimiter=";", encoding="utf-8")
    compar=pd.read_csv(compar_ruta, delimiter=";", encoding="utf-8")
    return casos, edu_vial2018, encuesta_calidad, encuesta_cultura, hurto_tp, lesion_nf, mede_victimas, traffic, compar

def casos_treatment(df):
    df.rename(columns={'Codigo_comuna': 'Comuna'}, inplace=True)
    df=df.drop(df[df["Comuna"]=="SIN DATO"].index)
    df["Comuna"]=df["Comuna"].astype(float)
    df["Comuna"]=df["Comuna"].astype(int)
    
    return df

def edu_vial2018_treatment(df):
    df = df.drop(df.columns[[0,2,3,5,7,8,10,11,31,32,33,34,35]], axis=1)
    df.rename(columns={'FECHA': 'Fecha', 'ACCIONES': 'Acciones', 'PUBLICO OBJETIVO': 'Publico', 'COD_COMUNA': 'Comuna'}, inplace=True)
    df.rename(columns={'TOTAL PERSONAS SENSIBILIZADAS': 'N_personas', 'TOTAL MUJER': 'N_mujeres', 'TOTAL HOMBRE': 'N_hombres'}, inplace=True)
    df.rename(columns={'MUJER NIÑO (6 a 13 años)': 'N_mujeres (6-13)', 'MUJER JOVEN (14 a 28 años)': 'N_mujeres (14-28)', 'MUJER ADULTO (29 a 59 años)': 'N_mujeres (29-59)'}, inplace=True)
    df.rename(columns={'MUJER PERSONA MAYOR (60  años y más)': 'N_mujeres (>60)', 'MUJER PEATÓN': 'N_mujeres_peaton', 'MUJER MOTOCICLISTA': 'N_mujeres_motoc'}, inplace=True)
    df.rename(columns={'MUJER CONDUCTOR': 'N_mujeres_cond', 'MUJER ACOMPAÑANTE Y/O PASAJERO': 'N_mujeres_ac/pas', 'HOMBRE_JOVEN_(14_A_28_ANOS)': 'N_hombres (14-28)'}, inplace=True)
    df.rename(columns={'HOMBRE ADULTO (29 A 59 ANOS)': 'N_hombres (29-59)', 'HOMBRE_PERSONA_MAYOR_(60_ANOS_Y_MÁS)': 'N_hombres (>60)', 'HOMBRE_PEATON': 'N_hombres_peaton'}, inplace=True)
    df.rename(columns={'HOMBRE_CICLISTA': 'N_hombres_cicl', 'HOMBRE_MOTOCICLISTA':'N_hombres_motoc','HOMBRE_CONDUCTOR':'N_hombres_cond','HOMBRE_ACOMPANANTE_ Y/O_ PASAJERO':'N_hombres_ac/pas'}, inplace=True)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Fecha'] = df['Fecha'].dt.strftime('%d/%m/%Y')   
    
    return df

def medevic_treatment():
    print(mede_victimas['Gravedad_victima'].value_counts())
    mede_victimas = mede_victimas.dropna()
    columns_to_check = ['Sexo', 'Edad']
    for column in columns_to_check:
        mede_victimas = mede_victimas[(mede_victimas[column] != 'Sin Inf') & (mede_victimas[column] != 'Sin inf')]
    import re
    def convert_age_to_int(age_str):
        
        if isinstance(age_str, str) and '-' in age_str:
            ages = re.findall(r'\d+', age_str)  # Extraer los números del rango
            return (int(ages[0]) + int(ages[1])) // 2  # Promedio de los valores del rango
        else:
            return int(age_str)  # Si es un valor único, simplemente conviértelo a entero
    # Eliminar filas con valores NaN en la columna 'Edad'
    mede_victimas['Edad'] = mede_victimas['Edad'].apply(convert_age_to_int)
    mede_victimas = mede_victimas.drop(mede_victimas[mede_victimas['Edad'] > 100].index)
    mede_victimas['Condicion'] = mede_victimas['Condicion'].replace({'Acompañante de Motocicleta': 'Acompañante de motocicleta'})
    