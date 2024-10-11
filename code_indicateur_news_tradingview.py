# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from datetime import datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Téléchargement des données nécessaires pour VADER
nltk.download('vader_lexicon')

# Initialisation de l'analyseur de sentiment VADER
sia = SentimentIntensityAnalyzer()

# Clé API fournie
api_key = 'cadbaa550b604aa0b674bfd03f80817a'
keyword = 'tesla'  # Mot-clé pour rechercher les articles
yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
today_date = datetime.now().strftime('%Y-%m-%d')  # Date actuelle formatée

# URL pour récupérer les articles du jour sur Tesla
url = (f'https://newsapi.org/v2/everything?q={keyword}&from=2024-10-01'
       f'&to={today_date}&sortBy=publishedAt&language=en&apiKey={api_key}')
#url = (f'https://newsapi.org/v2/everything?q={keyword}&from={today_date}'
#       f'&to={today_date}&sortBy=publishedAt&language=en&apiKey={api_key}')
#url = (f'https://newsapi.org/v2/everything?qInTitle={keyword}&from={today_date}'
#       f'&to={today_date}&sortBy=publishedAt&apiKey={api_key}')


# Effectuer la requête HTTP à l'API NewsAPI
response = requests.get(url)

# Vérifier le statut de la réponse
# if response.status_code == 200:
#     news_data = response.json()

#     # Vérifier s'il y a des articles dans la réponse
#     if 'articles' in news_data and len(news_data['articles']) > 0:
#         articles = news_data['articles']

#         # Filtrer manuellement les articles dont le titre contient "Tesla"
#         filtered_articles = [article for article in articles if article['title'] and 'tesla' in article['title'].lower()]

#         if filtered_articles:
#             print(f"Articles publiés depuis 3 jours avec '{keyword}' dans le titre (en anglais) :")
#             for article in filtered_articles:
#                 print(f"Titre: {article['title']}")
#                 print(f"Publié à: {article['publishedAt']}")
#                 print(f"Source: {article['source']['name']}")
#                 print(f"Lien: {article['url']}\n")
#         else:
#             print(f"Aucun article trouvé avec '{keyword}' dans le titre.")
#     else:
#         print(f"Aucun article trouvé pour '{keyword}'.")
# else:
#     print(f"Erreur lors de la récupération des articles : {response.status_code}")
    
    
# Vérifier le statut de la réponse
if response.status_code == 200:
    news_data = response.json()

    # Vérifier s'il y a des articles dans la réponse
    if 'articles' in news_data and len(news_data['articles']) > 0:
        articles = news_data['articles']

        # Filtrer manuellement les articles dont le titre contient "Tesla"
        filtered_articles = [article for article in articles if article['title'] and 'tesla' in article['title'].lower()]

        if filtered_articles:
            print(f"Articles publiés depuis 3 jours avec '{keyword}' dans le titre (en anglais) :")
            
            total_sentiment = 0
            for article in filtered_articles:
                titre = article['title']
                sentiment = sia.polarity_scores(titre)  # Analyse du sentiment du titre
                score_sentiment = sentiment['compound']  # Score global du sentiment (positif/négatif)
                total_sentiment += score_sentiment

                # Affichage des résultats d'analyse de sentiment
                if score_sentiment >= 0.05:
                    couleur = "Vert (bonne nouvelle)"
                elif score_sentiment <= -0.05:
                    couleur = "Rouge (mauvaise nouvelle)"
                else:
                    couleur = "Bleu (neutre)"

                print(f"Titre: {titre}")
                print(f"Sentiment: {couleur}")
                print(f"Score: {score_sentiment}")
                print(f"Publié à: {article['publishedAt']}")
                print(f"Source: {article['source']['name']}")
                print(f"Lien: {article['url']}\n")
                
            # Calcul de la moyenne du sentiment
            moyenne_sentiment = total_sentiment / len(filtered_articles)
            
            # Affichage de la tendance du jour
            if moyenne_sentiment >= 0.05:
                tendance = "Tendance générale : Positive"
            elif moyenne_sentiment <= -0.05:
                tendance = "Tendance générale : Négative"
            else:
                tendance = "Tendance générale : Neutre"
                
            print(tendance)
            print(f"Moyenne des scores de sentiment : {moyenne_sentiment}")
            
        else:
            print(f"Aucun article trouvé avec '{keyword}' dans le titre.")
    else:
        print(f"Aucun article trouvé pour '{keyword}'.")
else:
    print(f"Erreur lors de la récupération des articles : {response.status_code}")
