import telebot
import numpy as np
import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Import Movie Dataset, taken from Kaggle
#Note: IDs in the data are taken from IMDB
metadata = pd.read_csv("D:\\assets\\temp\\studies\\tru\\ai_bot_telegram\\movie_dataset\\movies_metadata.csv")
credits = pd.read_csv("D:\\assets\\temp\\studies\\tru\\ai_bot_telegram\\movie_dataset\\credits.csv")
keywords = pd.read_csv("D:\\assets\\temp\\studies\\tru\\ai_bot_telegram\\movie_dataset\\keywords.csv")


metadata = pd.read_csv("D:\\assets\\temp\\studies\\tru\\ai_bot_telegram\\movie_dataset\\movies_metadata.csv")
metadata = metadata.iloc[0:10000,:]


#Set ID type to int in order to use pandas .merge

metadata['id'] = metadata['id'].astype('int')
credits['id'] = credits['id'].astype('int')
keywords['id'] = keywords['id'].astype('int')

#Merge all Datasets into 1 based on ID

metadata = metadata.merge(credits, on='id')
metadata = metadata.merge(keywords, on='id')

#Changing Datatypes to Python relavant

features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
	metadata[feature] = metadata[feature].apply(literal_eval)

#Function to get director's information if there is, otherwise teruns NaN

def get_director_info(dataset):
	for i in dataset:
		if(i['job'] == 'Director'):
			return i['name']
	return np.nan

#Function to get all actors, keywords and genres

def get_all(dataset):
	if(isinstance(dataset, list)):
		names = [i['name'] for i in dataset]
		if (len(names) > 3):
			names = names[:3]
		return names
	#Return empty list
	return []

metadata['director'] = metadata['crew'].apply(get_director_info)

features = ['cast', 'keywords', 'genres']
for i in features:
	metadata[i] = metadata[i].apply(get_all)

#Edit data from dataset for readibility

def clean_data(dataset):
    if isinstance(dataset, list):
        return [str.lower(i.replace(" ", "")) for i in dataset]
    else:
        if isinstance(dataset, str):
            return str.lower(dataset.replace(" ", ""))
        else:
            return ''

features = ['cast', 'keywords', 'director', 'genres']
for i in features:
	metadata[i] = metadata[i].apply(clean_data)

#Create a rec

def create_rec(dataset):
	return ' '.join(dataset['keywords']) + ' ' + ' '.join(dataset['cast']) + ' ' + dataset['director'] + ' ' + ' '.join(dataset['genres'])

metadata['rec'] = metadata.apply(create_rec, axis=1)

#Function to combine all search options
def combine_search(genres, actors, keywords):
	search_options = []
	if(genres != 'SKIP'):
		search_options.append(genres)
	if(actors != 'SKIP'):
		search_options.append(actors)
	if(keywords != 'SKIP'):
		search_options.append(keywords)
	return search_options


#################################################################################
#Bot Deployment

#Create and assign Bot Token from Telegram
bot = telebot.TeleBot('6208295004:AAF94s1vV1Mk91GvOLX4w2Z4B1_M4gFZCeM');

#Starting message
@bot.message_handler(commands=['start'])
def start(message):
	greeting_message = f'Hello, <b>{message.from_user.first_name}</b>\nI am Movie Recommendation Bot. I will need you to provide me Genres, Actors and Keywords'
	bot.send_message(message.chat.id, greeting_message, parse_mode='html');
	bot.send_message(message.chat.id, 'Provide them to me in this format:\n*Genre*,*Genre*...\n*Actor*,*Actor*...\n*Keyword*,*Keyword*...\nPlease note you can provide SKIP to skip respective option', parse_mode='html');


@bot.message_handler()
def input_genre(message):
	temp_msg = message.text.lower().split('\n')
	tg_genres = " ".join(["".join(n.split()) for n in temp_msg[0].split(',')])
	tg_actors = " ".join(["".join(n.split()) for n in temp_msg[1].split(',')])
	tg_keywords = " ".join(["".join(n.split()) for n in temp_msg[2].split(',')])
	recommend(message, tg_genres, tg_actors, tg_keywords)

def recommend(message, genres, actors, keywords, metadata=metadata):
	temp_row = metadata.iloc[-1,:].copy()

	search_options = combine_search(genres, actors, keywords)
	temp_row.iloc[-1] = " ".join(search_options)

	metadata = metadata.append(temp_row)

	count = CountVectorizer(stop_words='english')
	count_matrix = count.fit_transform(metadata['rec'])

	cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
	sim_scores = list(enumerate(cosine_sim2[-1,:]))
	sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

	ranked_titles = []
	for i in range(1, 4):
		index = sim_scores[i][0]
		ranked_titles.append([metadata['title'].iloc[index], metadata['imdb_id'].iloc[index]])

	for z in ranked_titles:
		bot.send_message(message.chat.id, z)


bot.polling(none_stop=True);
