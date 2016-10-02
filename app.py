from flask import Flask, render_template, request
import csv, hashlib

app = Flask(__name__)

@app.route("/")
def main():
    print request.headers
    return render_template("login.html", message = "")

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
        row = hashlib.sha256(uname).hexdigest() + "," + hashlib.sha256(pword).digest()
        newacc.write(row)
        newacc.close()
        return render_template("login.html", message = "Account created, genie is waiting for you to login.")
    elif status == "Login":
        data = open("data/geniefriends.csv")
        accounts = csv.reader(data)
        for account in accounts:
            if account[0] == hashlib.sha256(uname).hexdigest():
                if account[1] == hashlib.sha256(pword).digest():
                    data.close()
                    return render_template("authenticate.html", login = True, message = "Genie is happy that you logged in.")
                else:
                    data.close()
                    return render_template("authenticate.html", login = False, message = "Genie is sad that you lied about your password.")
        data.close()
        return render_template("login.html", message = "Genie says you should sign up to be his friend.")

        
if __name__ == '__main__':
    app.debug = True
    app.run()
