from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template()

@app.route("/hello")
def hello():
    return "만나서 반갑습니다."

@app.route("/user/<userId>")
def profile(userId):
    return f"{userId}\'s profile"

if __name__ == '__main__':
    app.run()