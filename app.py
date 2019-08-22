import time

import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, render_template
from flask_socketio import SocketIO


css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = app = Flask(__name__)
server.config['SECRET_KEY'] = 'secret!'
app = dash.Dash(__name__, server=server, external_stylesheets=css)
socketio = SocketIO(server)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js" integrity="sha256-yr4fRk/GU1ehYJPAs8P4JlTgu0Hdsp4ZKrx8bDEDC3I=" crossorigin="anonymous"></script>
        <script type="text/javascript" charset="utf-8">
            
            var socket = io();
            
            socket.on('connect', function() {
                socket.emit('hello', {data: 'connected'});
            });

            socket.on('update', function(data) {
                document.getElementById('finish').textContent=data+'/10';
            });
            
        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    'Hello!',
    html.Button('Click me', id='trigger'),
    html.H1('', id='finish')
])


@socketio.on('hello')
def handle_message(message):
    print(str(message))


@app.callback(
    Output('finish', 'children'),
    [Input('trigger', 'n_clicks')])
def countdown(click):
    
    if not click:
        raise PreventUpdate() 
    
    for i in range(10):
        socketio.emit('update', i)
        time.sleep(0.3)
    
    return click

if __name__ == '__main__':
    socketio.run(server)
    # app.run_server(debug=True)
