#encoding:utf8
from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO,emit, send, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.values.get('name', None):
        session['name'] = request.form['name']
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if session.get('name'):
        return render_template('chat.html')
    return redirect(url_for('index'))


@socketio.on('join1', namespace='/chat')
def join1(data):
    print 'data:'+str(data)
    room = data['room']
    session['room'] = room
    join_room(data['room'])
    emit('status',{'code':'200','msg':'welcome '+str(session['name'])+' join room!'}, room=room)


@socketio.on('message', namespace='/chat')
def message(data):
    room = data.get('room')
    msg = data.get('message')
    emit('status', {'code':'200','msg':msg}, room=room)

@socketio.on('left', namespace='/chat')
def left(data):
    room = session.pop('room', None)
    msg = '%s left room!!!'
    emit('status', {'code':'200', 'msg':msg}, room=room)



# @socketio.on('message')
# def handle_message(message):
#     print('received message: ' + message['data'])

if __name__ == '__main__':
    socketio.run(app,debug=True)
    # app.run(host='0.0.0.0', port=8000, debug=True)
