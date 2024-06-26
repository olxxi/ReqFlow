from flask import Flask
import time

app = Flask(__name__)

@app.route('/delay/<int:delay_time>', methods=['GET', 'POST'])
def delay_response(delay_time):
    time.sleep(delay_time)
    return 'Delayed response', 200

if __name__ == '__main__':
    app.run(port=5000)