# TODO: deploy on heroku, add "undo" button, add minimax AI

from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.debug=True # added
Session(app)

@app.route('/')
def index():
    if 'board' not in session:
        session['board'] = [[None, None, None], [None, None, None], [None, None, None]]
        session['turn'] = 'X'
        session['winner'] = None

    return render_template('game.html', game=session['board'], turn=session['turn'], winner=session['winner'])

# X is 0, O is 1
def check_winner():
    for turn in ['X', 'O']:
        for i in range(3):
            if session['board'][i][0] == session['board'][i][1] == session['board'][i][2] == turn:
                return turn
            if session['board'][0][i] == session['board'][1][i] == session['board'][2][i] == turn:
                return turn
            if session['board'][0][0] == session['board'][1][1] == session['board'][2][2] == turn:
                return turn
            if session['board'][0][2] == session['board'][1][1] == session['board'][2][0] == turn:
                return turn
    return None

@app.route('/play/<int:row>/<int:col>')
def play(row, col):
    if session['turn'] == 'X':
        session['board'][row][col] = 'X'
        session['turn'] = 'O'
    elif session['turn'] == 'O':
        session['board'][row][col] = 'O'
        session['turn'] = 'X'
    else:
        raise Exception('undefined turn! %s' % session['turn'])
    session['winner'] = check_winner()
    return render_template('game.html', game=session['board'], turn=session['turn'], winner=session['winner'])

    # return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session['board'] = [[None, None, None], [None, None, None], [None, None, None]]
    session['turn'] = 'X'
    session['winner'] = None

    return render_template('game.html', game=session['board'], turn=session['turn'], winner=session['winner'])