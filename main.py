from flask import Flask, request , redirect
import random

nextid = 4
topics = [
    {'id':1,'title':'a','body':'aaaaaaaa'},
    {'id':2,'title':'b','body':'bbbbbbbb'},
    {'id':3,'title':'c','body':'cccccccc'}
]

def template(contents,content,id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
            <ul><a href="/update/{id}/">update</a></li>
        '''
    return f'''<!doctype>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
                {content}
            <ul>
                <li><a href="/create/">create</a></li>
                <li><a href="/update/1/">update</a></li>
                <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
            </ul> 
        </body>
    </html>
    '''

def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags

app = Flask(__name__)

@app.route('/')
def index():
    return template(getContents(),'<h2>Welcome</h2>Hello, World!')

@app.route('/create/', methods=['GET',"POST"])
def create():
    if request.method == "GET":
        content = '''
        <form action='/create/' method='POST'> 
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea placeholder='body' name="body"></textarea></p>
            <p><input type="submit" value="create"></p>
        '''
        return template(getContents(),content)
    else:
        global nextid
        title = request.form['title']
        body = request.form['body']
        newtopic = {'id':nextid,'title':title,'body':body}
        topics.append(newtopic)
        url = '/read/' + str(nextid) + '/'
        nextid += 1
        return redirect(url)
    
@app.route('/update/<int:id>/', methods=['GET',"POST"])
def update(id):
    if request.method == "GET":

        title = ''
        body = ''
        for topic in topics:
            if id== topic['id']:
                title = topic['title']
                body = topic['body']
                break

        content = f'''
        <form action='/update/{id}/' method='POST'> 
            <p><input type="text" name="title" placeholder="title" value="{title}"></p>
            <p><textarea placeholder='body' name="body">{body}</textarea></p>
            <p><input type="submit" value="update"></p>
        '''
        return template(getContents(),content)
    else:
        global nextid
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/' + str(nextid) + '/'
        return redirect(url)

@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id== topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(getContents(),f'<h2>{title}</h2>{body}',id=id)

@app.route('/delete/<int:id>/',methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')

app.run(debug=True)
