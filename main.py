from flask import Flask, render_template, request, redirect

from EmailSending import EmailSending
from Weather import Weather

app = Flask(__name__, template_folder='WeatherApp/templates')



def TODO(message="Functionality not implemented"):
    raise NotImplementedError(message)


@app.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        city = request.form.get('city')
        email = request.form.get('email')

        # Get weather data

        weatherObj = Weather(city)
        message = weatherObj.weather()

        # Send email
        emailObj = EmailSending(message)
        emailObj.sending(email)

        return render_template('success.html', city=city, email=email)

    return render_template('index.html')


@app.route('/success')
def success():
    return render_template('success.html')





if __name__ == '__main__':
    app.add_url_rule('/<path:path>', endpoint='catch_all', view_func=submit)
    app.run(port=5002)

