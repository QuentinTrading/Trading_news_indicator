# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Initialisation de Flask
app = Flask(__name__)

# Téléchargement des données nécessaires pour VADER
nltk.download('vader_lexicon')

# Initialisation de l'analyseur de sentiment VADER
sia = SentimentIntensityAnalyzer()

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        # Extraire les données pertinentes (par ex. le symbole de l'action comme 'TSLA')
        keyword = data.get('ticker', 'tesla').lower()
        
        # Récupérer les articles pour ce symbole
        api_key = 'ta_cle_newsapi'
        today_date = datetime.now().strftime('%Y-%m-%d')
        yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # URL pour récupérer les articles du jour
        url = (f'https://newsapi.org/v2/everything?q={keyword}&from={yesterday_date}'
               f'&to={today_date}&sortBy=publishedAt&language=en&apiKey={api_key}')
        
        response = requests.get(url)
        
        if response.status_code == 200:
            news_data = response.json()
            
            if 'articles' in news_data and len(news_data['articles']) > 0:
                articles = news_data['articles']
                filtered_articles = [article for article in articles if 'title' in article and keyword in article['title'].lower()]
                
                if filtered_articles:
                    total_sentiment = 0
                    for article in filtered_articles:
                        titre = article['title']
                        sentiment = sia.polarity_scores(titre)  # Analyse du sentiment du titre
                        score_sentiment = sentiment['compound']
                        total_sentiment += score_sentiment
                    
                    # Calcul de la moyenne du sentiment
                    moyenne_sentiment = total_sentiment / len(filtered_articles)
                    
                    # Déterminer la tendance
                    if moyenne_sentiment >= 0.05:
                        tendance = "positive"
                    elif moyenne_sentiment <= -0.05:
                        tendance = "negative"
                    else:
                        tendance = "neutre"
                    
                    # Retourner la tendance comme réponse
                    return jsonify({"status": "success", "tendance": tendance, "score": moyenne_sentiment}), 200
                
                else:
                    return jsonify({"status": "no_articles", "message": "Aucun article pertinent trouvé"}), 200
            else:
                return jsonify({"status": "no_articles", "message": "Aucun article trouvé pour la période donnée"}), 200
        else:
            return jsonify({"status": "error", "message": f"Erreur API: {response.status_code}"}), 500
    else:
        return jsonify({"status": "error", "message": "Données invalides reçues"}), 400

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
