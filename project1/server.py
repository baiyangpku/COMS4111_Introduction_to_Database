
#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Project 1
author: Yang Bai & Jingying Zhou
"""

import os
import datetime
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, url_for, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
DATABASEURI = "postgresql://yb2356:GENXNR@w4111db.eastus.cloudapp.azure.com/yb2356"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)

userInfo = dict()
usrName = "?"


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request
  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  print request.args
  return render_template("front1.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
  render_template('login.html')
  try: 
    cursor = g.conn.execute("SELECT User_Name,User_Password FROM Usr")
  except Exception, e:
    pass  
  temp = cursor.fetchall()
  for row in temp:
    userInfo[row[0]] = row[1];
  cursor.close()
  error = None
  global usrName
  if request.method == 'POST':
    username = request.form['username'] 
    if username not in userInfo.keys():
      error = "Sorry, this user name does not exist!"
    elif request.form['password'] != userInfo.get(username): 
      error = "Sorry, incorrect password! Please try again."
    else:
      usrName = username
      return redirect('/front')
  return render_template('login.html', error=error)


@app.route('/front')
def front():
  return render_template("front2.html")


@app.route('/searchanimation',  methods=['GET', 'POST'])
def searchanimation():
  error = None
  global usrName
  try: 
    cursor = g.conn.execute("SELECT atitle FROM animation")
  except Exception, e:
    pass  
  ani_names = []
  for result in cursor:
    ani_names.append(result['atitle'])  
  cursor.close()
  
  if request.method == 'POST':
    query_ani_name = request.form['name']
    if query_ani_name not in ani_names:
      error = "Invalid animation name."
    else:
      rec = g.conn.execute("SELECT A.animation_id FROM animation A WHERE A.atitle = %s",(query_ani_name,))
      
      for res in rec:
        aniId=res['animation_id']
        
      return redirect(url_for('animation', aniId=aniId))
      
  return render_template("searchanimation.html", usr = usrName, animation = ani_names, error=error)


@app.route('/animation/<aniId>',  methods=['GET', 'POST'])
def animation(aniId):
  global usrName
  rec = g.conn.execute("SELECT *  FROM animation A WHERE A.animation_id = %s",(aniId,))
  for res in rec:
    aniName = res['atitle']
    aniLang = res['language']
    aniSeason = res['seasons']
    aniEpi = res['episodes']
    aniDate = res['released_date']
    aniComp = res['company_name']
    aniCid = res['comic_id']
  rec.close()
  temp = g.conn.execute("SELECT * FROM has H WHERE H.animation_id = %s", (aniId,))
  charac = []
  charac_dob = [] 
  actor = []
  actor_dob = []
  for t in temp:
    charac.append(t['character_name'])
    charac_dob.append(t['character_birthday'])
    actor.append(t['actor_name'])
    actor_dob.append(t['actor_birthday'])
  temp.close()
  comm = g.conn.execute("SELECT * FROM comment C, usr U WHERE C.animation_id = %s AND C.uid = U.uid", (aniId,))
  usr = []
  time = []
  content = []
  for c in comm:
    usr.append(c['user_name'])
    time.append(c['time_posted'])
    content.append(c['comment_content'])
  comm.close()

  return render_template("animation.html", aniId = aniId, aniName = aniName, aniLang = aniLang,aniDate = aniDate,
       aniSeason = aniSeason, aniEpi = aniEpi,  aniComp = aniComp, cid = aniCid, charac = charac,
       charac_dob = charac_dob, actor = actor, actor_dob = actor_dob, user = usr, timestamp = time, content = content)



@app.route('/compsearch', methods=['GET','POST'])
def compsearch():
  error = None
  try: 
    cursor = g.conn.execute("SELECT Company_Name FROM Company")
  except Exception, e:
    pass  
  comp_names = []
  for result in cursor:
    comp_names.append(result[0])  # can also be accessed using result[0]
  cursor.close()
  if request.method == "POST":
    query_comp_name = request.form['comp_name']
    if query_comp_name not in comp_names:
      error = "The company your searched for is not in the database"
    else:
      rec = g.conn.execute("SELECT Company_Name FROM Company WHERE Company_Name = %s",(query_comp_name,))
      # rec = g.conn.execute("SELECT * FROM Comic_Draw_Publish c, Magazine m, Cartoonists d WHERE c.Comic_Name = %s,(query_comi_name,) AND c.Cartoonist_ID = d.Cartoonist_ID AND c.ISSN = m.ISSN")
      for res in rec:
        compNam=res['company_name']
      rec.close()
      return redirect(url_for('company',compNam=compNam))
  return render_template("compsearch.html", comp_names=comp_names, error=error)


@app.route('/company/<compNam>')
def company(compNam):
  #global usrName
  rec = g.conn.execute("SELECT * FROM Company C WHERE C.company_name = %s",(compNam,))
  for res in rec:
    compName = res['company_name']
    compWeb = res['company_website']
    compCou = res['company_country']
    compDesc = res['company_description']
  rec.close()
  an = g.conn.execute("SELECT * FROM Company C, Animation A WHERE C.company_name = %s AND C.company_name = A.company_name",(compNam,))
  compAni =[]
  for ani in an:
      compAni.append(ani['atitle'])
  an.close()
  return render_template("company.html",compName=compName,compWeb=compWeb,compCou=compCou,compDesc=compDesc,compAni =compAni)
  
  
  
  
"""
By Comic Name
"""

@app.route('/comisearch', methods=['GET','POST'])
def comisearch():
  error = None
  try: 
    cursor = g.conn.execute("SELECT Comic_Name FROM Comic_Draw_Publish")
  except Exception, e:
    pass  
  comi_names = []
  for result in cursor:
    comi_names.append(result[0])  # can also be accessed using result[0]
  cursor.close()

  if request.method == 'POST':
    query_comi_name = request.form['comic_name'] #From comisearch.html
    if query_comi_name not in comi_names:
      error = "Invalid comic name."
    else:
      rec = g.conn.execute("SELECT Comic_ID FROM Comic_Draw_Publish C WHERE C.Comic_Name = %s",(query_comi_name,))
      for res in rec:
        comID=res['comic_id']
      return redirect(url_for('comics',comID=comID))
  return render_template("comisearch.html", comi = comi_names, error=error)

@app.route('/comics/<comID>', methods=['GET','POST'])
def comics(comID):
  rec = g.conn.execute("SELECT * FROM Comic_Draw_Publish C, Cartoonists R, Magazine M, Animation A WHERE C.comic_id = %s AND C.comic_id = A.comic_id AND C.Cartoonist_ID = R.Cartoonist_ID AND M.ISSN = C.ISSN",(comID,))
  for res in rec:
    comNam = res['comic_name']
    comDesc = res['comic_description']
    comIss = res['issn']
    carNam = res['cartoonist_name']
    carBir = res['date_of_birth']
    carSex = res['cartoonist_gender']
    carDesc = res['cartoonist_description']
    magNam = res['magazine_name']
    magLang = res['magazine_language']
    magDesc = res['magazine_description']
    aniName = res['atitle']
  return render_template("comics.html",comID=comID,comDesc=comDesc,comIss=comIss,comNam=comNam,carNam=carNam,carBir=carBir,carSex=carSex,carDesc=carDesc,magNam=magNam,magLang=magLang,magDesc=magDesc,aniName=aniName)



@app.route('/langsearch', methods=['GET','POST'])
def langsearch():
  error = None
  try: 
    cursor = g.conn.execute("SELECT DISTINCT language FROM Animation")
  except Exception, e:
    pass  
  ani_lang = []
  for result in cursor:
    ani_lang.append(result[0])  # can also be accessed using result[0]
  cursor.close()

  if request.method == 'POST':
    query_lang_name = request.form['langsearch'] #From comisearch.html
    if query_lang_name not in ani_lang:
      error = "Language Not Listed."
    else:
      rec = g.conn.execute("SELECT DISTINCT language FROM Animation WHERE language= %s",(query_lang_name,))
      for res in rec:
        langNam=res['language']
      return redirect(url_for('language',langNam=langNam))
  return render_template("langsearch.html", ani_lang = ani_lang, error=error)

@app.route('/language/<langNam>', methods=['GET','POST'])
def language(langNam):
  rec = g.conn.execute("SELECT * FROM Animation A WHERE A.language = %s",(langNam,))
  aniName = []
  for res in rec:
    aniName.append(res['atitle'])
  return render_template("language.html",aniName=aniName, langNam =langNam)


@app.route('/comment', methods= ['GET','POST'] )
def comment():
  error = None
  global usrName
  try: 
    cursor = g.conn.execute("SELECT atitle FROM animation")
  except Exception, e:
    pass  
  ani_names = []
  for result in cursor:
    ani_names.append(result['atitle'])  
  cursor.close()
  if usrName == '?':
    return redirect('/login')  
  if request.method == 'POST':
    content = request.form['content']
    aniName = request.form['aniName']
    if aniName not in ani_names:
      error = "Sorry, invalid animation name!"
    else:
      rec = g.conn.execute("SELECT A.animation_id FROM animation A WHERE A.atitle = %s", (aniName,))
      for res in rec:
        aniId = res['animation_id']
      st = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      usrTemp = g.conn.execute("SELECT U.uid FROM usr U WHERE U.user_name = %s", (usrName,))
      for t1 in usrTemp:
        uid = t1['uid']
      g.conn.execute("INSERT INTO comment(comment_content,time_posted, uid, animation_id) VALUES (%s, %s, %s, %s)", (str(content), str(st),uid, str(aniId)))
      return redirect(url_for('animation', aniId=aniId))
  return render_template("comment.html", cur_usr = usrName, animation= ani_names, error = error)

@app.route('/logout')
def logout():
  global usrName
  usrName = '?'
  return redirect('/')



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using
        python server.py
    Show the help text using
        python server.py --help
    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
