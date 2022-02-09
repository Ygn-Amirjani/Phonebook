from flask import Flask, json

app = Flask(__name__)

@app.route('/')
def check():
    return json.dumps({"Hello": "World"})

if __name__ == '__main__':
    app.run()
