import requests
import json
from flask import Flask, render_template, request, url_for
from flask_cors import CORS, cross_origin


API_Key = 'edf10c245991eb326456f5b7f2b1b3a8'
API_Read_Access_Token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZGYxMGMyNDU5OTFlYjMyNjQ1NmY1YjdmMmIxYjNhOCIsInN1YiI6IjU5NjE2MmMxOTI1MTQxMjI1MTBhNjhkZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.diqM-wMrIoLAb72gF4dWjRwDHtH-pp1Rr0UxHflkKIE'
REQUEST_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE0OTk1NTU3MzAsImV4cCI6MTQ5OTU1NjYzMCwic2NvcGVzIjpbInBlbmRpbmdfcmVxdWVzdF90b2tlbiJdLCJhdWQiOiJlZGYxMGMyNDU5OTFlYjMyNjQ1NmY1YjdmMmIxYjNhOCIsImp0aSI6MzIxOTU2LCJyZWRpcmVjdF90byI6Imh0dHA6XC9cL3d3dy50aGVtb3ZpZWRiLm9yZ1wvIiwidmVyc2lvbiI6MX0.KvfFMXgtRP1NH-4rzc7L2vi9DERMTre2EFb-oTOFsew'

GENRE_LIST = ['action', 'adventure', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'family',
              'fantasy', 'history', 'horror', 'music', 'mystery', 'romance', 'science', 'thriller', 'war', 'western', 'tv']
GENRE_NAME_TO_ID = {'action': 28, 'adventure': 12, 'animation': 16, 'comedy': 35, 'crime': 80, 'documentary': 99, 'drama': 18,
                    'family': 10751, 'fantasy': 14, 'history': 36, 'horror': 27, 'music': 10402, 'mystery': 9648, 'romance': 10749,
                    'science': 878, 'tv': 10770, 'thriller': 53, 'war': 10752, 'western': 37}

app = Flask(__name__)
CORS(app)

@app.route('/search/<movie_name>', methods=['GET'])
def search_movie(movie_name):
    data = search_movie(movie_name)
    print(data)
    data = json.loads(data)
    data_id = ''
    data_title = ''
    data_overview = ''
    data_img_link = ''

    for idx in data['results']:
        data_id = idx['id']
        data_title = idx['title']
        data_overview = idx['overview']
        data_img_link = "http://i1.wp.com/image.tmdb.org/t/p/w600" + idx['poster_path']
        break
    data_trailer_link = get_trailer(data_id)

    print(data_id)
    print(data_title)
    print(data_img_link)

    data_trailer_link = json.loads(data_trailer_link)
    data_trailer_link = data_trailer_link['results'][0]['key']
    print(data_trailer_link)
    d = dict()
    d['id'] = data_id
    d['title'] = data_title
    d['overview'] = data_overview
    d['img_link'] = data_img_link
    d['trailer_link'] = data_trailer_link
    return json.dumps(d)

@app.route('/genre/<sentence>/<howmany>', methods=['GET'])
def recognize_genre(sentence, howmany):
    genre = ''
    for word in sentence.lower().split():
        if word in GENRE_LIST:
            genre = word
    if len(genre):
        l = list()
        for each in json.loads(discover_movie(GENRE_NAME_TO_ID[genre]))['results'][:int(howmany)]:
            print(each)
            d = dict()
            d['id'] = each['id']
            d['title'] = each['title']
            d['overview'] = each['overview']
            d['img_link'] = "http://i1.wp.com/image.tmdb.org/t/p/w600" + each['poster_path']
            data_trailer_link = get_trailer(d['id'])
            data_trailer_link = json.loads(data_trailer_link)
            data_trailer_link = data_trailer_link['results'][0]['key']
            d['trailer_link'] = data_trailer_link
            l.append(d)
        return json.dumps(l)
    return ''

@app.route('/now_playing/<howmany>', methods=['GET'])
def now_playing(howmany):
    l = list()
    for each in json.loads(get_now_playing())['results'][:int(howmany)]:
        print(each)
        d = dict()
        d['id'] = each['id']
        d['title'] = each['title']
        d['overview'] = each['overview']
        d['img_link'] = "http://i1.wp.com/image.tmdb.org/t/p/w600" + each['poster_path']
        data_trailer_link = get_trailer(d['id'])
        data_trailer_link = json.loads(data_trailer_link)
        data_trailer_link = data_trailer_link['results'][0]['key']
        d['trailer_link'] = data_trailer_link
        l.append(d)
    return json.dumps(l)

@app.route('/popular/<howmany>', methods=['GET'])
def popular(howmany):
    l = list()
    for each in json.loads(get_popular())['results'][:int(howmany)]:
        print(each)
        d = dict()
        d['id'] = each['id']
        d['title'] = each['title']
        d['overview'] = each['overview']
        d['img_link'] = "http://i1.wp.com/image.tmdb.org/t/p/w600" + each['poster_path']
        data_trailer_link = get_trailer(d['id'])
        data_trailer_link = json.loads(data_trailer_link)
        data_trailer_link = data_trailer_link['results'][0]['key']
        d['trailer_link'] = data_trailer_link
        l.append(d)
    return json.dumps(l)

@app.route('/top_rated/<howmany>', methods=['GET'])
def top_rated(howmany):
    l = list()
    for each in json.loads(get_top_rated())['results'][:int(howmany)]:
        print(each)
        d = dict()
        d['id'] = each['id']
        d['title'] = each['title']
        d['overview'] = each['overview']
        d['img_link'] = "http://i1.wp.com/image.tmdb.org/t/p/w600" + each['poster_path']
        data_trailer_link = get_trailer(d['id'])
        data_trailer_link = json.loads(data_trailer_link)
        data_trailer_link = data_trailer_link['results'][0]['key']
        d['trailer_link'] = data_trailer_link
        l.append(d)
    return json.dumps(l)


@app.route('/recommendation/<movie_name>/<howmany>', methods=['GET'])
def recommendation(movie_name, howmany):
    data = search_movie(movie_name)
    print(data)
    movie_id = json.loads(data)['results'][0]['id']

    l = list()

    for each in json.loads(get_similar(movie_id))['results'][:int(howmany)]:
        print(each)
        d = dict()
        d['id'] = each['id']
        d['title'] = each['title']
        d['overview'] = each['overview']
        d['img_link'] = "http://i1.wp.com/image.tmdb.org/t/p/w600" + each['poster_path']
        data_trailer_link = get_trailer(d['id'])
        print(data_trailer_link)
        data_trailer_link = json.loads(data_trailer_link)
        data_trailer_link = data_trailer_link['results'][0]['key']
        d['trailer_link'] = data_trailer_link
        l.append(d)
    return json.dumps(l)


def request_token():
    url = "https://api.themoviedb.org/4/auth/request_token"

    payload = "{\"redirect_to\":\"http://www.themoviedb.org/\"}"
    headers = {
        'authorization': "Bearer {}".format(API_Read_Access_Token),
        'content-type': "application/json;charset=utf-8"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text


def get_genre_lists(page=1):
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key={}&language=en-US".format(API_Key, page)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text


def get_latest(page=1):
    url = "https://api.themoviedb.org/3/movie/latest?api_key={}&language=en-US".format(API_Key, page)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text


def get_now_playing(page=1):
    url = "https://api.themoviedb.org/3/movie/now_playing?api_key={}&language=en-US".format(API_Key, page)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text


def get_popular(page=1):
    url = "https://api.themoviedb.org/3/movie/popular?api_key={}&language=en-US".format(API_Key, page)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text


def get_top_rated(page=1):
    url = "https://api.themoviedb.org/3/movie/top_rated?api_key={}&language=en-US".format(API_Key, page)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text


def get_upcoming(page=1):
    url = "https://api.themoviedb.org/3/movie/upcoming?api_key={}&language=en-US&page={}".format(API_Key, page)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text


def get_similar(id, page=1):
    url = "https://api.themoviedb.org/3/movie/{}/similar?api_key={}&language=en-US&page={}".format(id, API_Key, page)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text


def get_recommendations(id, page=1):
    url = "https://api.themoviedb.org/3/movie/{}/similar?api_key={}&language=en-US&page={}".format(id, API_Key, page)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text


def search_movie(query):
    url = "https://api.themoviedb.org/3/search/movie?api_key={}&language=en-US&query={}&page=1&include_adult=true".format(API_Key, query)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text


def get_trailer(id):
    url = "http://api.themoviedb.org/3/movie/{}/videos?api_key={}".format(id, API_Key)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text


def discover_movie(genre):
    url = "https://api.themoviedb.org/3/discover/movie?api_key={}&language=en-US&sort_by" \
          "=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={}".format(API_Key, str(genre))

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    return response.text

if __name__ == "__main__":
    # json_data = get_genre_lists()
    # data = json.loads(json_data)
    #
    # # print(data)
    # # print(data['genres'])
    #
    # # get genre lists
    # for idx in data['genres']:
    #     print(idx['name'])
    #
    # # print(get_latest())
    # # print(get_now_playing())
    # # print(get_popular())
    # # print(get_top_rated())
    # # print(get_upcoming())
    # # print(get_similar(123))
    # print(json.loads(discover_movie(28))['results'])
    #
    # print(get_trailer('234'))
    # print(get_trailer('342'))
    # print(get_trailer('355216'))
    # print(get_trailer('284052'))


    app.run(
        host="0.0.0.0",
        port=int("8888")
    )
