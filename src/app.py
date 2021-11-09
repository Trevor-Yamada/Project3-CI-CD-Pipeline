

from flask import Flask,render_template
        
app = Flask(__name__)

@app.route("/")
def index():
    user = {'username' : 'Trevor'}
    return render_template("base.html",title="home",user=user)
if __name__ == "__main__":
    app.run()
