#!/usr/bin/python
#! -*-coding:utf-8 -*-
'''
File: main.py
Author: Hervé Beraud
Email: herveberaud.pro<at>gmail<dot>com
Description: Déterminer le nombre d'évènements possibles
en fonction de dates fournits en entrée
'''
from datetime import date
from datetime import timedelta
import re

def main():
    '''
    main() -> None
    Initialiser les données d'entrée à partir de saisies utilisateur.
    '''
    # Récupérer le nombre d'évènements
    good = False
    while(not good):
        try:
            events = int(raw_input())
            if events <= 100 and events >= 1:
                good = True
        except ValueError:
            print('''/!\ Données non conforme /!\ (type = entier min 1/max 100)
            '''
            )
    # Récupérer les infos des evenements
    count = 0
    data = []
    while(count is not events):
        valide_day = False
        # Demander tant que l'info n'est pas valide
        while(not valide_day):
            event_day = raw_input()
            valide = re.match(r'\d{4}-\d{1,2}-\d{2};\d{1,2}', event_day)
            if not valide:
                print("/!\ Mauvais format pour l'evenement {0} /!\\" . \
                    format((count + 1)))
                continue
            try:
                data.append({'day' : format_date(event_day.split(';')[0]), \
                    'end_day' : event_day.split(';')[1]})
                count += 1
                valide_day = True
            except ValueError:
                # Prendre en compte les années bisextile,
                # les formats de date valide ou la date n'existe pas
                print("\n/!\ La date de l'évènement n'existe pas /!\ \n")
    print(compute(sorted(data)))

def compute(sorted_data):
    '''
    compute(sorted_data) -> int
    Retourne le nombre de rendez-vous possibles
    en fonction des dates fournits en entrée
    data = list de données au format '["2013-06-15;14", "2013-06-16;2"]'

    Valeurs de l'exemple
    >>> data = []
    >>> data.append({'day' : date(2013, 01, 12), 'end_day' : 5})
    >>> data.append({'day' : date(2013, 01, 1), 'end_day' : 13})
    >>> data.append({'day' : date(2013, 01, 16), 'end_day' : 20})
    >>> compute(data)
    2

    Cas plus complexe
    >>> data = []
    >>> data.append({'day' : date(2014, 04, 28), 'end_day' : 4})
    >>> data.append({'day' : date(2014, 05, 1), 'end_day' : 7})
    >>> data.append({'day' : date(2014, 05, 3), 'end_day' : 7})
    >>> data.append({'day' : date(2014, 05, 9), 'end_day' : 5})
    >>> data.append({'day' : date(2014, 05, 11), 'end_day' : 11})
    >>> data.append({'day' : date(2014, 05, 16), 'end_day' : 3})
    >>> data.append({'day' : date(2014, 05, 20), 'end_day' : 1})
    >>> compute(data)
    4

    Année bissextile
    >>> data = []
    >>> data.append({'day' : date(2012, 02, 20), 'end_day' : 10})
    >>> data.append({'day' : date(2012, 03, 1), 'end_day' : 2})
    >>> data.append({'day' : date(2012, 03, 12), 'end_day' : 2})
    >>> data.append({'day' : date(2012, 03, 14), 'end_day' : 2})
    >>> data.append({'day' : date(2012, 03, 15), 'end_day' : 2})
    >>> data.append({'day' : date(2012, 03, 20), 'end_day' : 13})
    >>> compute(data)
    5
    '''
    # Prevenir le cas des données non ordonnées au préalable
    # (utilisatio direct)
    if sorted(sorted_data) is not sorted_data:
        sorted_data = sorted(sorted_data)

    optimum = 0
    # Parcourir toutes les combinaisons possibles en fonction
    # du nombre d'évènements fournis
    for possibility in range(pow(2, len(sorted_data))):
        current_event = None
        result = 0
        for index, event in enumerate(sorted_data):
            position = pow(2, index)
            # Comparer les dates uniquement si l'évènement fait partie
            # de la combinaison courante
            if (possibility & position):
                if not current_event:
                    current_event = event
                    result = 1
                else:
                    compare = sorted_data[index]
                    current_event_end = futur(
                        current_event['day'],
                        current_event['end_day']
                    )
                    # Remplacer l'évènement courrant si celui-ci
                    # ne possède pas d'intervale en commun
                    # avec l'évènement à tester
                    if current_event_end <= compare['day']:
                        current_event = compare
                        result += 1
        if result > optimum:
            optimum = result
    return optimum

def format_date(day_date):
    '''
    format_date(day_date) -> datetime
    Retourne un objet à partir d'une chaine au format "AAAA-MM-DD"
    day_date = date au format "AAAA-MM-DD"
    >>> format_date('2013-06-15')
    datetime.date(2013, 6, 15)
    '''
    day_date = day_date.split('-')
    end = date(
        year=int(day_date[0]),
        month=int(day_date[1]),
        day=int(day_date[2]))
    return end

def futur(day_date, nb_days):
    '''
    futur(day_date, nb_days) -> datetime
    Retourne la date de fin de l'évenement
    day_date = date de début de l'évènement
    nb_days = durée de l'évènement
    >>> futur(format_date("2013-06-15"), 4)
    datetime.date(2013, 6, 19)
    '''
    end = day_date + timedelta(days=int(nb_days))
    return end

if __name__ == "__main__":
    # Lancer la fonction de saisie
    main()
