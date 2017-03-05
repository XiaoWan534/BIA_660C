import os
import json
import re
import requests
import time
from flask import Flask, request, Response
from textblob import TextBlob



application = Flask(__name__)

my_bot_name = 'xiao_bot'
my_slack_username = 'xiaowan'
my_ip_address = '35.166.3.154'

slack_inbound_url = 'https://hooks.slack.com/services/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'


# this handles POST requests sent to your server at SERVERIP:41953/slack
@application.route('/slack', methods=['POST'])
def inbound():
    print '========POST REQUEST @ /slack========='
    print 'FORM DATA RECEIVED IS:'
    print request.form

    #time.sleep(random.uniform(0, 20))
    response = {'username': my_bot_name, 'icon_emoji': ':bear:', 'text': ''}
    channel = request.form.get('channel_name')
    username = request.form.get('user_name')
    text = request.form.get('text')
    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message

    if botname != username and username in [my_slack_username, 'zac.wentzell', 'xiaowan']:

        # =========== Task 1 ============
        if re.findall(u'BOTS_RESPOND',text):
            response['text'] = 'Hello, my name is '+ my_bot_name +'. I belong to '+ \
                               my_slack_username +'. I live at '+ my_ip_address +'.'
            requests.post(slack_inbound_url, json=response)


        # =========== Task 2 & 3 ============
        if re.findall(u'I_NEED_HELP_WITH_CODING',text):

            question = text[32:]
            url = 'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=' + \
                  question + '&site=stackoverflow'
            answers = json.loads(requests.get(url).text)

            # if there are tags in question
            tags = re.findall('(?<=\[)\w+', text)
            if tags:
                for item  in answers['items']:
                    for tag in tags:
                        if not re.findall(tag, item['tags']):
                            answers['items'].remove(item)

            # selection of answers
            for item in answers['items']:
                if item["answer_count"] == '0':
                    answers['items'].remove(item)


            title = []
            title_link = []
            num_answers = []
            time_created = []
            attachments = []

            for item in answers['items'][0:5]:
                title.append(item["title"])
                title_link.append(item["link"])
                num_answers.append(item["answer_count"])
                time_created.append(item["creation_date"])

            for t, l, num, time in zip(title, title_link, num_answers, time_created):
                attachment_new = {
                'color': ['good'],
                'title': t,
                'title_link': l,
                'footer': num + 'responses.',
                'ts': time
                }
                attachments.append(attachment_new)

            response = {
                'username': 'xiao_bot',
                'icon_emoji': ':bear:',
                'text': 'Here are some solutions from StackOverflow.',
                'attachments': attachments
            }
            requests.post(slack_inbound_url, json=response)



        # =========== Task 4 ============
        if re.findall(u"WHAT'S_THE_WEATHER_LIKE_AT",text):
            location = text[35:]
            key_openWeatherMap = '7f02dd61c156ac1fc023ea7bcebe937c'
            key_google_geo = 'AIzaSyCdotFhwTFFqanF_fn4Q8dG1hDR906Ydj4'
            key_google_map = 'AIzaSyDOHstcVBCnU1oipen7DaAhh3HTyiD-eDc'


            # get location information
            url_googleMap = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ \
                            location +'&key='+ key_google_geo
            geo_info = json.loads(requests.get(url_googleMap).text)['results'][0]
            formatted_name = geo_info['formatted_address']
            geometry = geo_info['geometry']['location']
            lat = geometry['lat']
            lng = geometry['lng']


            # get map picture
            url_img = 'https://maps.googleapis.com/maps/api/staticmap?center=' + str(lat) + ',' + str(lng) + \
                      '&zoom=13&size=500x350&maptype=roadmap&path=weight:3%7Ccolor:blue%7Cenc:{coaHnetiVjM??_SkM??~R' \
                      '&key=' + key_google_map


            # get weather information
            url_weather = 'http://api.openweathermap.org/data/2.5/weather?lat='+ \
                                 str(lat) +'&lon='+ str(lng) +'&APPID='+ key_openWeatherMap
            weather_info = json.loads(requests.get(url_weather).text)

            now = weather_info['weather'][0]['main']
            temp = weather_info['main']['temp']
            hum = weather_info['main']['humidity']
            wind = weather_info['wind']['speed']

            # get forecast information
            url_forecast = 'http://api.openweathermap.org/data/2.5/forecast?lat='+ \
                                 str(lat) +'&lon='+ str(lng) +'&APPID='+ key_openWeatherMap
            forecast_info = json.loads(requests.get(url_forecast).text)

            forecast_main = forecast_info['list'][1]['weather'][0]['main']
            forecast_temp_min = forecast_info['list'][1]['main']['temp_min']
            forecast_temp_max = forecast_info['list'][1]['main']['temp_max']

            response = {
                'username': 'xiao_bot',
                'icon_emoji': ':bear:',
                'text': 'Here is the weather at '+ str(location),
                "attachments": [
                    {
                        "color": ['good'],
                        "pretext": "Weather Infomation",
                        "fields": [
                            {
                                "title": "Now",
                                "value": now,
                                "short": True
                            }, {
                                "title": "Current temperature",
                                "value": temp,
                                "short": True
                            }, {
                                "title": "Humidity",
                                "value": hum,
                                "short": True
                            }, {
                                "title": "wind",
                                "value": wind,
                                "short": True
                            }
                        ],
                        "image_url": url_img,
                        "footer": formatted_name
                    },{
                        "color": ['good'],
                        "pretext": "Weather Forecast",
                        "fields":[
                            {
                                "title": "Forecast",
                                "value": forecast_main,
                                "short": True
                            }, {
                                "title": "Lowest Temp",
                                "value": forecast_temp_min,
                                "short": True
                            },{
                                "title": "Highest Temp",
                                "value": forecast_temp_max,
                                "short": True
                            }
                        ]
                    }
                ]
            }

            requests.post(slack_inbound_url, json=response)




        if not response['text']:
            response['text'] = "I did not learn this yet.\nAsk me question begins with <BOTS_RESPOND>,"\
                               "\nor <I_NEED_HELP_WITH_CODING>, \nor <WHAT'S_THE_WEATHER_LIKE_AT>."
            requests.post(slack_inbound_url, json=response)

    print '========REQUEST HANDLING COMPLETE========\n\n'

    return Response(), 200


# this handles GET requests sent to your server at SERVERIP:41953/
@application.route('/', methods=['GET'])
def test():
    return Response('Your flask app is running!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)