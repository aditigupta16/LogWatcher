from flask import Flask, Response, render_template
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/initial-data")
def initial_stream():
    file = open('log.csv')
    content = file.read().split(',')
    file.close()
    output = "data: {}".format(content[-10:])
    content = content[-10:]
    return Response(output, mimetype="application/json")


@app.route("/stream")
def stream():
    def eventStream():
        file=open('log.csv')
        initial_content=file.read().split(',')
        file.close()
        while True:
            content = []
            file=open('log.csv')
            content=file.read().split(',')
            file.close()
            new_data_length = len(content) - len(initial_content)
            if new_data_length > 0:
                initial_content = content
                yield "data: {}\n\n".format(content[-new_data_length:])

    return Response(eventStream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0')
