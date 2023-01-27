from flask import Flask, render_template, request, url_for
from bs4 import BeautifulSoup as BS
import requests
import json

app2 = Flask(__name__)

# рандомный поиск
@app2.route("/")
def base():
    # получаем рандомное имя животного
    r = requests.post("https://randomall.ru/api/custom/gens/1490")
    jd = json.loads(r.text)
    # вставляем в название животного поисковой запрос bing
    url = f'https://www.bing.com/images/search?q={jd["msg"]}&qs=SC&pq=rjym&sc=10-4&cvid=31C2237795E84E6D901AB92A4FE093E1&form=QBLH&sp=1&first=1&cw=1177&ch=647'
    r1 = requests.get(url)
    html = BS(r1.content, 'html.parser')
    # получаем ссылку на картинку
    src = html.find("div", class_="img_cont hoff").select('img')[0]['src']
    # отправляем картинку на сайт
    return render_template('index.html', src=src, name=jd['msg'], hd="Рандомное животное")


# поиск по данным введенным пользователем
@app2.route('/user', methods=['POST'])
def user():
    q = request.form["field"]       # получаем текст который ввел пользовательна сайте вставляем в ссылку:
    url = f'https://www.bing.com/images/search?q={q}&qs=SC&pq=rjym&sc=10-4&cvid=31C2237795E84E6D901AB92A4FE093E1&form=QBLH&sp=1&first=1&cw=1177&ch=647'
    # находим картинку по введенному запросу
    r1 = requests.get(url)
    html = BS(r1.content, 'html.parser')
    src = html.find("div", class_="img_cont hoff").select('img')[0]['src']
    # отправляем данные на сайт
    return render_template('index.html', src=src, name=q, hd="Поисковой запрос пользователя")


if __name__ == "__main__":
    app2.run(host ='0.0.0.0', port = 5008, debug = True)
