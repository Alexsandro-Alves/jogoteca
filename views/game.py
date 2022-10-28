from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models.game import Games
from models.game_form import GameForm
from application import app, db
from utils import get_image


@app.route('/')
def index():
    games_list = Games.query.order_by(Games.id)
    return render_template('list.html', title='Jogos', games=games_list)


@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login', next=url_for('new')))
    form = GameForm()
    return render_template('new.html', title='Novo Jogo', form=form)


@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login', next=url_for('edit')))

    game = Games.query.filter_by(id=id).first()
    form = GameForm()
    form.name.data = game.name
    form.category.data = game.category
    form.console.data = game.console

    game_image = get_image(id)
    return render_template('edit.html', title='Editando Jogo', id=id, game_image=game_image, form=form)


@app.route('/create', methods=['POST', ])
def create():
    form = GameForm(request.form)

    if form.validate_on_submit():
        return redirect(url_for('novo'))

    name = form.name.data
    category = form.category.data
    console = form.console.data

    existing_game = Games.query.filter_by(name=name).first()
    if existing_game:
        flash(name + ' Já existe')
        return redirect(url_for('index'))

    new_game = Games(name=name, category=category, console=console)
    db.session.add(new_game)
    db.session.commit()

    file = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    file.save(f'{upload_path}/{new_game.id}.jpg')

    return redirect(url_for('index'))


@app.route('/update', methods=['POST', ])
def update():
    form = GameForm(request.form)

    if form.validate_on_submit():
        game = Games.query.filter_by(id=request.form['id']).first()
        game.name = form.name.data
        game.category = form.category.data
        game.console = form.console.data

        db.session.add(game)
        db.session.commit()

        file = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        file.save(f'{upload_path}/{game.id}.jpg')

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login'))

    Games.query.filter_by(id=id).delete()
    db.session.commit()

    flash('Jogo deletado com sucesso!')
    return redirect(url_for('index'))


@app.route('/uploads/<file_name>')
def upload_image(file_name):
    return send_from_directory('uploads', file_name)
