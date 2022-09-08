#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 13:18:44 2022

@author: FOWE FONKOU Christian B
@desc : Extraire les tableaux d'un fichier pdf donné
"""

import camelot
import os
import pandas as pd
from PyPDF2 import PdfFileWriter, PdfFileReader

def pdf_convertor (dir_path):
    '''
    Description : Cette fonction va prendre le chemin vers le dossier
     --------     qui contient toutes les pages splités du pdf et convertir
                  chaque page en dataframe puis faire une concatenation de
                  tous les dataframes
    Entrée : @dir_path représente le chemin vers le dossier 
     -----
     
    Sortie : @df Représente le dataframe qui contient toutes les tables concatenés
     ---
    '''
    df = pd.DataFrame()
    i = 1
    for r, d, f in os.walk(dir_path):
        for file in f:
            if file.endswith(".pdf"):
                print("début de conversion N°"+str(i)+" de "+file)
                data = camelot.read_pdf(dir_path+"/"+file, pages='all')
                frames = [df, data[0].df]
                df = pd.concat(frames)
                i = i + 1
    return df

def pdf_split(name):
    '''
    Description
    ----------
    Cette fonction prend un fichier pdf en paramètre créait un repertoire
    puis va spliter chaque page du pdf en un nouveau pdf

    Parameters
    ----------
    name : nom du fichier pdf (il doit être dans le repertoire ou s'éxécute la fonction)

    Returns
    -------
    Elle va retourner le dataframe contenant toutes les pages du pdf name.

    '''
    inputpdf = PdfFileReader(open(name, "rb"))
    filename = name.replace('.pdf', '')
    directory = filename
    # Path
    path = os.path.join(thisdir, directory)
    
    # Création du dossier qui va contenir toutes les pages du pdf
    os.mkdir(path)
    
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open(path+"/"+filename+"_%s.pdf" % i, "wb") as outputStream:
            output.write(outputStream)
    return(pdf_convertor(path))

"""
Début Main
"""
# Getting the current work directory (cwd)
thisdir = os.getcwd()

# r=root, d=directories, f = files
for r, d, f in os.walk(thisdir):
    for file in f:
        if file.endswith(".pdf"):
            print('Traitement du fichier '+file)
            data = pdf_split(file)
            csv_filename=file.replace('.pdf','.csv')
            data.to_csv("csv_filename")