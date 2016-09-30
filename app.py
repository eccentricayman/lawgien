from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
    print request.headers
    return render_template("login.html")

@app.route("/authenticate", methods=['GET', 'POST'])
def authenticate():
    uname = "aladdin"
    pword = "opensesame"
    if request.form['username'] == uname and request.form['passwd'] == pword:
        return render_template("authenticate.html", login = True)
    else :
        return render_template("authenticate.html", login = False)

if __name__ == '__main__':
    app.debug = True
    app.run()
