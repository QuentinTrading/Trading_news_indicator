# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import requests
from datetime import datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from flask import Flask, request

# Téléchargement des données nécessaires pour VADER
nltk.download('vader_lexicon')

# Initialisation de l'analyseur de sentiment VADER
sia = SentimentIntensityAnalyzer()

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data and 'ticker' in data:
        keyword = data['ticker']  # Utiliser le ticker d'action envoyé par TradingView
    else:
        return 'No ticker found in request', 400

    # Récupérer la clé API depuis les variables d'environnement
    api_key = os.getenv('API_KEY')
    
    # Dates pour la requête (articles d'aujourd'hui et d'hier)
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    today_date = datetime.now().strftime('%Y-%m-%d')

    # URL pour récupérer les articles liés au mot-clé (le ticker)
    url = (f'https://newsapi.org/v2/everything?q={keyword}&from={yesterday_date}'
           f'&to={today_date}&sortBy=publishedAt&language=en&apiKey={api_key}')

    # Effectuer la requête HTTP à l'API NewsAPI
    response = requests.get(url)

    # Vérifier le statut de la réponse
    if response.status_code == 200:
        news_data = response.json()

        # Vérifier s'il y a des articles dans la réponse
        if 'articles' in news_data and len(news_data['articles']) > 0:
            articles = news_data['articles']

            # Filtrer les articles dont le titre contient le mot-clé
            filtered_articles = [article for article in articles if article['title'] and keyword.lower() in article['title'].lower()]

            if filtered_articles:
                total_sentiment = 0
                for article in filtered_articles:
                    titre = article['title']
                    sentiment = sia.polarity_scores(titre)
                    score_sentiment = sentiment['compound']
                    total_sentiment += score_sentiment

                # Calcul de la moyenne du sentiment
                moyenne_sentiment = total_sentiment / len(filtered_articles)
                
                # Définir la tendance en fonction de la moyenne
                if moyenne_sentiment >= 0.05:
                    tendance = "Positive"
                elif moyenne_sentiment <= -0.05:
                    tendance = "Négative"
                else:
                    tendance = "Neutre"

                # Retourner la tendance au format attendu par TradingView
                return {
                    'tendance': tendance,
                    'moyenne_sentiment': moyenne_sentiment,
                    'articles_trouves': len(filtered_articles)
                }, 200
            else:
                return {'message': f'Aucun article trouvé pour {keyword}.'}, 200
        else:
            return {'message': f'Aucun article trouvé pour {keyword}.'}, 200
    else:
        return {'message': f'Erreur lors de la récupération des articles: {response.status_code}'}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
