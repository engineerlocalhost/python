from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
queue_number = 0

@app.route('/')
def index():
    return render_template('index.html', queue_number=str(queue_number))

@app.route('/next')
def next_queue():
    global queue_number
    queue_number += 1
    return redirect(url_for('index'))

@app.route('/reset')
def reset_queue():
    global queue_number
    queue_number = 0
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
