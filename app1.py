from flask import Flask, render_template, url_for
import requests
from bs4 import BeautifulSoup as BS


# функция для получения элементов списка с помощью next
def list_generate(l):  # Создадим итератор при помощи генератора.
    for item in l:
        yield item

# деректива __name__  - передает название текущего файла в класс flask
# при  помощи app получаем доступ к функциям библиотеки flask

app1 = Flask(__name__)
# функции
# создаем декоратор для отслеживания url которые вводит пользователь в браузер
@app1.route("/")
def base():
    return render_template('base.html')


@app1.route("/cinema")
def cinema():
    # получаем содержимое
    r1 = requests.get("https://www.kinoafisha.info/rating/movies/sci-fi/")
    r2 = requests.get("https://www.kinonews.ru/top100-sci-fi/")
    r3 = requests.get("https://www.film.ru/a-z/movies/science_fiction")
    # результат отправляем в БС для поиска нужных тегов, парсер lxml
    html1 = BS(r1.content, 'html.parser')
    html2 = BS(r2.content, 'html.parser')
    html3 = BS(r3.content, 'html.parser')
    # Парсим блоки html с названием фильма и с рейтингом
    # Первые два сайта похожим способом
    nm1 = html1.find_all("a", class_="movieItem_title")
    rt1 = html1.find_all("span", class_="rating_num")
    nm2 = html2.find_all("a", class_="titlefilm")
    rt2 = html2.find_all("span", class_="rating-big")
    # Для третьего сайта глубина поиска немного сложнее
    nm3 = []
    rt3 = []
    nm_3 = html3.find_all("a", class_="film_list_link")
    cnt = 0
    for i in nm_3:
        cnt += 1
        nm3.append(i.find("strong"))
        rt3.append(i.find_all("span")[7].find("em"))
        if cnt == 10: break

    # функция для создания словаря где ключ nm - название фильма, значение rt - рейтинг
    def dct_cinema(nm, rt):
        d = dict()
        rate = list_generate(rt)
        cnt = 0
        for i in nm:
            cnt += 1
            d[i.text] = float(next(rate).text)
            if cnt == 10: break
        sorted_tuple = sorted(d.items(), key=lambda x: x[1], reverse=True) #сортирруем по убыванию рейтинга
        return dict(sorted_tuple)
    # получаем название фильма и его рейтинг в словаре
    get1 = dct_cinema(nm1, rt1)     # киноафиша
    get2 = dct_cinema(nm2, rt2)     # киноньюс
    get3 = dct_cinema(nm3, rt3)     # фильм

    # отправляем в шаблон наши словари в цикле выводим фильмы каждый в своем блоке
    return render_template('cinema.html', get3=get3, get2=get2, get1=get1)

@app1.route("/music")
def music():
    # результат отправляем в БС для поиска нужных тегов
    html1 = BS(requests.get("https://ruo.morsmusic.org/playlist/49").content, 'html.parser')
    u3 = "https://music.apple.com/ru/playlist/top-100-russia/pl.728bd30a9247487c80a483f4168a9dcd"
    html2 = BS(requests.get(u3).content, 'html.parser')
    html3 = BS(requests.get("https://music.yandex.ru/users/music-blog/playlists/1102").content, 'html.parser')
    # Парсим блоки html с названием трека и с именем исполнителя

    # парсим первый сайт
    nm1 = html1.find_all("a", class_="media-link media-name")
    ar1 = html1.find_all("div", class_="media-link media-artist")
    track_list1 = dict()
    nm11 = list_generate(nm1)       # используем генератор для перебора второго списка в цикле с помощью next
    cnt=0
    for i in ar1:
        cnt += 1
        q = i.find_all("a")
        art1 = ""
        for j in q:
            art1 += j.text + " "        # заносим в строку всех исполнителей
        track_list1[next(nm11).string.strip()] = art1       # с помощью next получаем очередное название трека
        if cnt == 10: break
    # парсим второй сайт
    nm2 = html2.find_all("div", class_="songs-list-row__song-name svelte-1yo4jst")
    ar2 = html2.find_all("span", class_="svelte-1yo4jst")
    nm22 = list_generate(nm2)
    track_list2 = dict()
    cnt = 0
    for i in ar2:
        cnt += 1
        q = i.find_all("a")
        art2 = ""
        for j in q:
            art2 += j.text + " "         # заносим в строку всех исполнителей
        if art2.strip() == "":           # бывают попадаются пустые элементы тогда шаг не засчитываем
            cnt -= 1
            continue                     # если попался пустой элемент без артиста пропустим пустой элемент
        track_list2[next(nm22).text] = art2
        if cnt == 10: break

    # парсим третий сайт
    nm3 = html3.find_all("a", class_="d-track__title deco-link deco-link_stronger")
    ar3 = html3.find_all("span", class_="d-track__artists")
    track_list3 = dict()
    nm33 = list_generate(nm3)
    cnt=0
    for i in ar3:
        cnt += 1
        q = i.find_all("a")
        art3 = ""
        for j in q:
            art3 += j.text + " "   # заносим в строку всех исполнителей
        track_list3[next(nm33).string.strip()] = art3
        if cnt == 10: break
    # отправляем в шаблон наши словари в цикле выводим фильмы каждый в своем блоке
    return render_template('music.html', track1=track_list1, track2=track_list2, track3=track_list3)


if __name__ == "__main__":
    app1.run(host ='0.0.0.0', port = 5005, debug = True)