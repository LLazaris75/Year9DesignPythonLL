 import sqlite3
    from sqlite3 import Error

    def create_connection(database):
        try:
            conn = sqlite3.connect(database, isolation_level=None, check_same_thread = False)
            conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))

            return conn
        except Error as e:
            print(e)

    def create_table(c,sql):
        c.execute(sql)

    def update_or_create_page(c,data):
        sql = "SELECT * FROM pages where name=? and session=?"
        c.execute(sql,data[:-1])
        result = c.fetchone()
        if result == None:
            create_pages(c,data)
        else:
            print(result)
            update_pages(c, result['id'])

    def create_pages(c, data):
        print(data)
        sql = ''' INSERT INTO pages(name,session,first_visited)
                  VALUES (?,?,?) '''
        c.execute(sql, data)

    def update_pages(c, pageId):
        print(pageId)
        sql = ''' UPDATE pages
                  SET visits = visits+1 
                  WHERE id = ?'''
        c.execute(sql, [pageId])

    def create_session(c, data):
        sql = ''' INSERT INTO sessions(ip, continent, country, city, os, browser, session, created_at)
                  VALUES (?,?,?,?,?,?,?,?) '''
        c.execute(sql, data)

    def select_all_sessions(c):
        sql = "SELECT * FROM sessions"
        c.execute(sql)
        rows = c.fetchall()
        return rows

    def select_all_pages(c):
        sql = "SELECT * FROM pages"
        c.execute(sql)
        rows = c.fetchall()
        return rows

    def select_all_user_visits(c, session_id):
        sql = "SELECT * FROM pages where session =?"
        c.execute(sql,[session_id])
        rows = c.fetchall()
        return rows

    def main():
        database = "./pythonsqlite.db"
        sql_create_pages = """ 
            CREATE TABLE IF NOT EXISTS pages (
                id integer PRIMARY KEY,
                name varchar(225) NOT NULL,
                session varchar(255) NOT NULL,
                first_visited datetime NOT NULL,
                visits integer NOT NULL Default 1
            ); 
        """
        sql_create_session = """ 
            CREATE TABLE IF NOT EXISTS sessions (
                id integer PRIMARY KEY,
                ip varchar(225) NOT NULL,
                continent varchar(225) NOT NULL, 
                country varchar(225) NOT NULL,
                city varchar(225) NOT NULL, 
                os varchar(225) NOT NULL, 
                browser varchar(225) NOT NULL, 
                session varchar(225) NOT NULL,
                created_at datetime NOT NULL
            ); 
        """

        # create a database connection
        conn = create_connection(database)
        if conn is not None:
            # create tables
            create_table(conn, sql_create_pages)
            create_table(conn, sql_create_session)
            print("Connection established!")
        else:
            print("Could not establish connection")

    if __name__ == '__main__':
        main()
Next, run the dbsetup.py file so that it creates a new SQLite database for us. We can run it with this command:

    $ python dbsetup.py
We should see this text logged to the terminal — ‘Connection established!’ — and there should be a new file — pythonsqlite.db — added to the project’s root directory.

Next, let’s open the app.py file and start writing the backend code that will handle incoming requests. We are going to register multiple routes here. Four of these routes will load a webpage each while the other routes will process submitted data and return a JSON response.

We will also create a Pusher instance and use it to broadcast data through two channels that we will shortly define — pageview and numbers — in the application. After that, we will import the database handler methods we defined in dbsetup.py so that we can use them in the app.py file. Open the app.py file and paste the following:

    from flask import Flask, render_template, request, session, jsonify
    import urllib.request
    from pusher import Pusher
    from datetime import datetime
    import httpagentparser
    import json
    import os
    import hashlib
    from dbsetup import create_connection, create_session, update_or_create_page, select_all_sessions, select_all_user_visits, select_all_pages

    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # configure pusher object
    pusher = Pusher(
    app_id='PUSHER_APP_ID',
    key='PUSHER_APP_KEY',
    secret='PUSHER_APP_SECRET',
    cluster='PUSHER_APP_CLUSTER',
    ssl=True)

    database = "./pythonsqlite.db"
    conn = create_connection(database)
    c = conn.cursor()

    userOS = None
    userIP = None
    userCity = None
    userBrowser = None
    userCountry = None
    userContinent = None
    sessionID = None

    def main():
        global conn, c

    def parseVisitor(data):
        update_or_create_page(c,data)
        pusher.trigger(u'pageview', u'new', {
            u'page': data[0],
            u'session': sessionID,
            u'ip': userIP
        })
        pusher.trigger(u'numbers', u'update', {
            u'page': data[0],
            u'session': sessionID,
            u'ip': userIP
        })

    @app.before_request
    def getAnalyticsData():
        global userOS, userBrowser, userIP, userContinent, userCity, userCountry,sessionID 
        userInfo = httpagentparser.detect(request.headers.get('User-Agent'))
        userOS = userInfo['platform']['name']
        userBrowser = userInfo['browser']['name']
        userIP = "72.229.28.185" if request.remote_addr == '127.0.0.1' else request.remote_addr
        api = "https://www.iplocate.io/api/lookup/" + userIP
        try:
            resp = urllib.request.urlopen(api)
            result = resp.read()
            result = json.loads(result.decode("utf-8"))                                                                                                     
            userCountry = result["country"]
            userContinent = result["continent"]
            userCity = result["city"]
        except:
            print("Could not find: ", userIP)
        getSession()

    def getSession():
        global sessionID
        time = datetime.now().replace(microsecond=0)
        if 'user' not in session:
            lines = (str(time)+userIP).encode('utf-8')
            session['user'] = hashlib.md5(lines).hexdigest()
            sessionID = session['user']
            pusher.trigger(u'session', u'new', {
                u'ip': userIP,
                u'continent': userContinent,
                u'country': userCountry,
                u'city': userCity,
                u'os': userOS,
                u'browser': userBrowser,
                u'session': sessionID,
                u'time': str(time),
            })
            data = [userIP, userContinent, userCountry, userCity, userOS, userBrowser, sessionID, time]
            create_session(c,data)
        else:
            sessionID = session['user']

    @app.route('/')
    def index():
        data = ['home', sessionID, str(datetime.now().replace(microsecond=0))]
        parseVisitor(data)
        return render_template('index.html')

    @app.route('/about')
    def about():
        data = ['about',sessionID, str(datetime.now().replace(microsecond=0))]
        parseVisitor(data)
        return render_template('about.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/dashboard/<session_id>', methods=['GET'])
    def sessionPages(session_id):
        result = select_all_user_visits(c,session_id)
        return render_template("dashboard-single.html",data=result)

    @app.route('/get-all-sessions')
    def get_all_sessions():
        data = []
        dbRows = select_all_sessions(c)
        for row in dbRows:
            data.append({
                'ip' : row['ip'],
                'continent' : row['continent'],
                'country' : row['country'], 
                'city' : row['city'], 
                'os' : row['os'], 
                'browser' : row['browser'], 
                'session' : row['session'],
                'time' : row['created_at']
            })
        return jsonify(data)

    if __name__ == '__main__':
        main()
        app.run(debug=True)
 const pusher = new Pusher('PUSHER_APP_KEY', {
      cluster: 'PUSHER_APP_CLUSTER',
      encrypted: true
    });

    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    $(document).ready(function(){
        var dataTable = $("#dataTable").DataTable()
        // var userSessions = $("#userSessions").DataTable()
        var pages = $("#pages").DataTable()

        axios.get('/get-all-sessions')
        .then(response => {
              response.data.forEach((data) => {
                  insertDatatable(data)
              })
          var d = new Date();
          var updatedAt = `${d.getFullYear()}/${months[d.getMonth()]}/${d.getDay()} ${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}`
          document.getElementById('session-update-time').innerText = updatedAt
        })

        var sessionChannel = pusher.subscribe('session');
        sessionChannel.bind('new', function(data) {
            insertDatatable(data)
        });

        var d = new Date();
        var updatedAt = `${d.getFullYear()}/${months[d.getMonth()]}/${d.getDay()} ${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}`
        document.getElementById('session-update-time').innerText = updatedAt
    });

    function insertDatatable(data){
        var dataTable = $("#dataTable").DataTable()
        dataTable.row.add([
            data.time,
            data.ip,
            data.continent,
            data.country,
            data.city,
            data.os,
            data.browser,
            `<a href=${"/dashboard/"+data.session}>View pages visited</a>`
          ]);
          dataTable.order([0, 'desc']).draw();
    }