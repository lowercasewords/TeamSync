from flask import Flask, render_template

app = Flask(__name__)

# Debugging 
@app.route("/login", methods=["GET", 'POST'])
def login():
    return render_template("login.html")

# Debugging 
@app.route("/logout", methods=['POST'])
def logout():
    return render_template("login.html")

# Debugging 
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Debugging 
@app.route('/create_event', methods=['GET'])
def create_event():
    return render_template('create_event.html')

# Debugging 
@app.route('/new_user', methods=['GET'])
def new_user():
    return render_template('new_user.html')

if __name__ == '__main__':
    app.run(debug=True) # debug=True enables reloader and debugger for development