from flask import Flask,render_template,url_for,request
import pickle
import requests
import pandas as pd
from patsy import dmatrices

movies = pickle.load(open('model/movie.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

def fetch_poster(movies_id):
    url = "https://api.themoviedb.org/3/movie/550?api_key=f26f00586aa6ba538f35f141093402c4".format(movies_id)
    data =   requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/kqjL17yufvn9OVLyXYpvtyrFfak.jpg"+poster_path
    return full_path
 
def recommend(movie):
    for j in movies['title']:
        index = movies[movies['title'].values() == movies].index[0]
    print(index)
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommend_movies_name = []
    recommend_movies_poster = []
    for i in distances[1:6]:
        movies_id = movies.iloc[i[0]].movies_id
        recommend_movies_poster.append(fetch_poster(movies_id))
        print(movies.iloc[i[0]].title)
        recommend_movies_name.append(movies.iloc[i[0]].title)
    print(recommend_movies_name)
    return recommend_movies_name, recommend_movies_poster


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/recommendation', methods = ['GET', 'POST'])
def recommendation():
    movies_list = movies['title'].values()
    status = False
    print(">>>>>>",request.method)
    if request.method == "POST":
        try:
            if request.form:
                movies_name = request.form['movies']
                print(movies_name)
                print(recommend_movies_poster)
                recommend_movies_name,recommend_movies_poster = recommend(movies_name)
                print(recommend_movies_name)
                status = True
                return render_template("prediction.html", movies_names = recommend_movies_name, poster = recommend_movies_poster, movies_list = movies_list, status = status)

        except Exception as e:
            error = {'error':e}      
            return render_template("prediction.html", error = error, movies_list = movies_list, status = status)
    else:
        return render_template("prediction.html", movies_list = movies_list, status = status)

if __name__ == '__main__':
    app.debug = True
    app.run() 