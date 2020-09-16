from logging import log
from flask import Flask, request, render_template, Response
import flask_pymongo
from logger import logger
from randomStr import randomStr
import hashlib
import datetime
import configparser

""" Parser the config file """
config = configparser.ConfigParser()
config.read('config.ini')
mongoURL = config["database"]["mongoURL"]


app = Flask(__name__)

""" config the mongo DB """
app.config["MONGO_URI"] = mongoURL
mongo = flask_pymongo.PyMongo(app)

""" Define the function about Post log """


def postLog(username, URL, value):
    mongo.db.logs.insert_one({"USER": username,
                              "URL": URL,
                              "value": value,
                              "date": datetime.datetime.now()})


@app.errorhandler(404)
# Overwrite the default 404 page
def page_not_found(e):
    return(Response("Not Found!\r\n", mimetype="text/plain")), 404


@app.route("/", methods=["GET", "POST"])
# Index page
def index():
    if request.method == "GET":
        if "curl" in request.headers.get('User-Agent'):
            return(Response(render_template("index_curl.txt"), mimetype="text/plain"))
        else:
            return(Response(render_template("index_curl.txt"), mimetype="text/plain"))
            # return(render_template("index.html"))

    elif request.method == "POST":
        mystr = randomStr()
        URL = mystr.getRandomStr()
        for account in request.form:
            if account == ":":
                """ No username , anonymous update """
                postLog("anonymous", URL, value=request.form[account])
                logger.info("POST_DONE: User:{} , IP:{} , URL:{}".format(
                    account, request.remote_addr, URL))
                return("\r\n{}{}\r\n\r\n".format(request.url_root, URL))
            else:
                """ Post with username """
                try:
                    """ Split the username and password from post form. """
                    username = account.split(":")[0]
                    passwordplain = account.split(":")[1]

                    sha1 = hashlib.sha1()
                    sha1.update(passwordplain.encode('utf-8'))
                    password = sha1.hexdigest()
                except:
                    return(Response("\r\nSyntax error!\r\n\r\n", mimetype="text/plain"))
                logger.info("DUMP_USER:{} , IP:{} , URL:{}".format(
                    username, request.remote_addr, URL))
                dbUserName = mongo.db.username.find({"user": username})

                if dbUserName.count() == 0:
                    """ Customer post username and password, but no user in database, so create the NEW USERNAME """
                    mongo.db.username.insert_one({"user": username,
                                                  "pwd": password})
                    postLog(username, URL, value=request.form[account])
                    logger.info("POST_DONE: User:{} , IP:{} , URL:{}".format(
                        username, request.remote_addr, URL))
                    return(Response("\r\nUser: {} created, Have Fun!\r\n\r\n{}{}\r\n\r\n".format(username, request.url_root, URL), mimetype="text/plain"))

                elif dbUserName.count() == 1:
                    """ Customer post a username which existed in db, therefore Authencate the username && password """
                    for i in dbUserName:
                        if i["user"] == username and i["pwd"] == password:
                            """ AUTH passed, post the logs to db """
                            postLog(username, URL, value=request.form[account])
                            logger.info("POST_DONE: User:{} , IP:{} , URL:{}".format(
                                username, request.remote_addr, URL))
                            return(Response("\r\n{}{}\r\n\r\n".format(request.url_root, URL), mimetype="text/plain"))
                        else:
                            """ Auth failed, reject the logs. """
                            return(Response("\r\nIncorrect username/password\r\n\r\n", mimetype="text/plain"))


@ app.route("/<logid>", methods=["GET"])
def getLogid(logid):
    if request.method == "GET":
        """ Return the special url logs """
        try:
            logResult = mongo.db.logs.find_one({"URL": logid})["value"]
            return(Response(logResult, mimetype="text/plain"))
        except:
            logger.info("No Log for URL: {}".format(logid))
            return(Response("No Log for URL: {}\r\n\r\n".format(logid), mimetype="text/plain"), 404)


@ app.route("/<username>/", methods=["GET"])
def getUserLogList(username):
    userExist = mongo.db.username.find({"user": username}).count()
    if userExist == 0:
        return(Response("Username \"{}\" is available!\r\n\r\n".format(username), mimetype="text/plain"))

    if request.method == "GET":
        """ Return the special url logs """
        userLogList = mongo.db.logs.find({"USER": username}).sort(
            "date", flask_pymongo.DESCENDING)
        if "curl" in request.headers.get('User-Agent'):
            return(render_template("userLogList_curl.html", userLogList=userLogList))
        else:
            return(render_template("userLogList.html", userLogList=userLogList))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
