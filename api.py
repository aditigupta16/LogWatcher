from flask import Flask, Response, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/initial-data")
def initial_data():
    file = open('log.csv')
    content = file.read().split(',')
    file.close()
    output = "{}".format(content[-10:])
    return Response(output, mimetype="application/json")


@app.route("/stream")
def stream():
    def eventStream():
        # will run only once for storing the initial index
        file=open('log.csv')
        file.read()
        initial_content_index = file.tell()
        file.close()
        while True:
            file=open('log.csv')
            # to avoid reading the complete file again start from last updated index
            file.seek(initial_content_index)
            content = file.read()
            file.close()
            new_data_length = len(content) if content else 0
            if new_data_length > 0:
                initial_content_index += new_data_length
                yield "data: {}\n\n".format(content.strip(',').split(','))
    return Response(eventStream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0')
