from flask import Flask, render_template

app = Flask(__name__)

IpAddressen = [
    'kaka',
    'pipi',
    'stront'
]

@app.route('/printTesten')
def printTesten():
    for i in range(4):
        print('samen eten we m&m')
    return 'dit is mijn statement'

@app.route('/')
def index():
    print('Thomas is aan het koken  ' )

    return render_template('index.html', adressen=[IpAddressen])

if __name__ == "__main__":
    app.run(debug=True)

# def addIpAddres():

