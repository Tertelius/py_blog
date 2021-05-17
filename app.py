from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    print('Ghbdtn')
    return render_template("about.html")


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html")


@app.route('/posts')
def posts ():
    articles = Article.query.order_by(Article.date.desc()).all()
    # articles = Article.query.first()
    return render_template("posts.html", articles=articles) #Передаем в шаблон постс данные через переменную артиклс
    # в принципе ее можно было бы назвать как угодно, однако, принято использовать такое же обозначение, для меньшей
    # путаницы.


@app.route('/posts/<int:id>')
def posts_detail (id):
    article = Article.query.get(id)
    return render_template("posts_detail.html", article=article)


if __name__ == "__main__":
    app.run(debug=True)
