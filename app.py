from flask import Flask, render_template, request, session, url_for, redirect
import csv, hashlib, os

app = Flask(__name__)
app.secret_key = "c9_will_win_worlds"

@app.route("/")
@app.route("/login")
def main():
    if 'logged_in' in session.keys():
        if session['logged_in']:
            return redirect(url_for("homepage", message = "Genie says hi, " + session['username'] + "!"))
        else:
            return render_template("login.html", message = "")
    else:
        return render_template("login.html", message = "")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html", uname = session['username'])
    
@app.route("/authenticate", methods=['GET', 'POST'])
def authenticate():
    uname = request.form['username']
    pword = request.form['passwd']
    status = request.form['account']
    if status == 'Register':
        data = open("data/geniefriends.csv")
        accounts = csv.reader(data)
        for account in accounts:
            if account[0] == hashlib.sha256(uname).hexdigest():
                data.close()
                return render_template("login.html", message = "Genie says be more creative with usernames, that's taken already.")
        data.close()
        newacc = open("data/geniefriends.csv", "a")
        row = hashlib.sha256(uname).hexdigest() + "," + hashlib.sha256(pword).hexdigest() + "\n"
        newacc.write(row)
        newacc.close()
        return render_template("login.html", message = "Account created, genie is waiting for you to login.")
    elif status == "Login":
        data = open("data/geniefriends.csv")
        accounts = csv.reader(data)
        for account in accounts:
            if account[0] == hashlib.sha256(uname).hexdigest():
                if account[1] == hashlib.sha256(pword).hexdigest():
                    data.close()
                    session['logged_in'] = True
                    session['username'] = uname
                    return render_template("authenticate.html", login = True, message = "Genie says hi, " + uname + "!")
                else:
                    data.close()
                    return render_template("authenticate.html", login = False, message = "Genie is sad that you lied about your password.")
        data.close()
        return render_template("login.html", message = "Genie says you should sign up to be his friend.")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username')
    return render_template("login.html", message="")
    
if __name__ == '__main__':
    #app.debug = True
    app.run()
