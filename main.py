import requests
import calendar

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

check = None
@app.route("/", methods=["GET"])
def static_file():
    if request.method == "GET":
        street = request.args.get("street")
        city = request.args.get("city")
        state = request.args.get("state")
        ipinfo = request.args.get("ip")
        global check
        check = request.args.get("auto")

        print(street, city, state)
        if street is not None and city is not None and state is not None:
            location = street + " " + city + " " + state
            print(location)

            # using geo api to get the lat lng
            key = "AIzaSyCeGPfA4Mjfni116otUYj6QOaJB1T3fJXY"
            params = {"address": location, "key": key}
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            response = requests.get(url, params=params).json()
            if response["status"] == "OK":
                lat = response["results"][0]["geometry"]["location"]["lat"]
                lng = response["results"][0]["geometry"]["location"]["lng"]
                loc = response["results"][0]["formatted_address"]
                print(loc)
                loc_arr = loc.split(", ")
                for index in range(len(loc_arr)):
                    print(index, loc_arr[index])

                # call tomorrow api
                num = str(lat) + ", " + str(lng)
                # print(num)
                url = "https://api.tomorrow.io/v4/timelines"
                querystring = {"location": num,
                               "fields": ["temperature", "humidity", "temperatureApparent", "temperatureMin", "temperatureMax",
                                          "windSpeed", "windDirection", "humidity", "pressureSeaLevel", "uvIndex",
                                          "weatherCode", "precipitationProbability", "precipitationType", "sunriseTime",
                                          "sunsetTime", "visibility", "moonPhase", "cloudCover"],
                               "units": "imperial",
                               "timesteps": ["1h", "1d", "current"],
                               "timezone": "America/Los_Angeles",
                               #"apikey": "U5JkcDUxTYiySxKNrIX58vd1kX9EuqVS"
                               "apikey": "U5JkcDUxTYiySxKNrIX58vd1kX9EuqVS"
                               }
                headers = {"Accept": "application/json"}
                response = requests.request("GET", url, headers=headers, params=querystring).json()

                # response = {"data":{"timelines":[{"timestep":"1d","startTime":"2021-10-05T13:00:00Z","endTime":"2021-10-20T13:00:00Z","intervals":[{"startTime":"2021-10-05T13:00:00Z","values":{"temperature":81.5,"weatherCode":1000,"temperatureMax":81.5,"temperatureMin":62.04,"windSpeed":10.92,"precipitationType":0,"precipitationProbability":0,"humidity":95,"visibility":9.94,"sunriseTime":"2021-10-05T13:50:00Z","sunsetTime":"2021-10-06T01:31:40Z"}},{"startTime":"2021-10-06T13:00:00Z","values":{"temperature":74.19,"weatherCode":1001,"temperatureMax":74.19,"temperatureMin":60.26,"windSpeed":7.83,"precipitationType":0,"precipitationProbability":0,"humidity":98.66,"visibility":9.94,"sunriseTime":"2021-10-06T13:51:40Z","sunsetTime":"2021-10-07T01:30:00Z"}},{"startTime":"2021-10-07T13:00:00Z","values":{"temperature":70.72,"weatherCode":1001,"temperatureMax":70.72,"temperatureMin":60.08,"windSpeed":7.9,"precipitationType":1,"precipitationProbability":10,"humidity":98.93,"visibility":9.94,"sunriseTime":"2021-10-07T13:51:40Z","sunsetTime":"2021-10-08T01:30:00Z"}},{"startTime":"2021-10-08T13:00:00Z","values":{"temperature":68.56,"weatherCode":1001,"temperatureMax":68.56,"temperatureMin":55.27,"windSpeed":15.21,"precipitationType":1,"precipitationProbability":15,"humidity":88.41,"visibility":12.05,"sunriseTime":"2021-10-08T13:51:40Z","sunsetTime":"2021-10-09T01:26:40Z"}},{"startTime":"2021-10-09T13:00:00Z","values":{"temperature":72.93,"weatherCode":1000,"temperatureMax":72.93,"temperatureMin":57.24,"windSpeed":11.77,"precipitationType":0,"precipitationProbability":0,"humidity":73.24,"visibility":15,"sunriseTime":"2021-10-09T13:53:20Z","sunsetTime":"2021-10-10T01:26:40Z"}},{"startTime":"2021-10-10T13:00:00Z","values":{"temperature":80.04,"weatherCode":1000,"temperatureMax":80.04,"temperatureMin":66.07,"windSpeed":12.24,"precipitationType":0,"precipitationProbability":0,"humidity":63.82,"visibility":15,"sunriseTime":"2021-10-10T13:53:20Z","sunsetTime":"2021-10-11T01:25:00Z"}},{"startTime":"2021-10-11T13:00:00Z","values":{"temperature":74.35,"weatherCode":1000,"temperatureMax":74.35,"temperatureMin":60.53,"windSpeed":18.5,"precipitationType":1,"precipitationProbability":0,"humidity":67.39,"visibility":15,"sunriseTime":"2021-10-11T13:53:20Z","sunsetTime":"2021-10-12T01:23:20Z"}},{"startTime":"2021-10-12T13:00:00Z","values":{"temperature":70.68,"weatherCode":1000,"temperatureMax":70.68,"temperatureMin":60.28,"windSpeed":12.42,"precipitationType":0,"precipitationProbability":0,"humidity":31.1,"visibility":15,"sunriseTime":"2021-10-12T13:56:40Z","sunsetTime":"2021-10-13T01:23:20Z"}},{"startTime":"2021-10-13T13:00:00Z","values":{"temperature":72.05,"weatherCode":1000,"temperatureMax":72.05,"temperatureMin":62.56,"windSpeed":13.8,"precipitationType":0,"precipitationProbability":0,"humidity":41.02,"visibility":15,"sunriseTime":"2021-10-13T13:56:40Z","sunsetTime":"2021-10-14T01:21:40Z"}},{"startTime":"2021-10-14T13:00:00Z","values":{"temperature":76.39,"weatherCode":1000,"temperatureMax":76.39,"temperatureMin":64.47,"windSpeed":10.07,"precipitationType":0,"precipitationProbability":0,"humidity":40.08,"visibility":15,"sunriseTime":"2021-10-14T13:58:20Z","sunsetTime":"2021-10-15T01:21:40Z"}},{"startTime":"2021-10-15T13:00:00Z","values":{"temperature":79.72,"weatherCode":1000,"temperatureMax":79.72,"temperatureMin":66.69,"windSpeed":8.81,"precipitationType":0,"precipitationProbability":0,"humidity":41.33,"visibility":15,"sunriseTime":"2021-10-15T13:58:20Z","sunsetTime":"2021-10-16T01:18:20Z"}},{"startTime":"2021-10-16T13:00:00Z","values":{"temperature":80.85,"weatherCode":1001,"temperatureMax":80.85,"temperatureMin":68.41,"windSpeed":8.52,"precipitationType":0,"precipitationProbability":0,"humidity":41.31,"visibility":15,"sunriseTime":"2021-10-16T13:58:20Z","sunsetTime":"2021-10-17T01:16:40Z"}},{"startTime":"2021-10-17T13:00:00Z","values":{"temperature":78.76,"weatherCode":1001,"temperatureMax":78.76,"temperatureMin":65.19,"windSpeed":8.86,"precipitationType":0,"precipitationProbability":0,"humidity":67.12,"visibility":15,"sunriseTime":"2021-10-17T14:00:00Z","sunsetTime":"2021-10-18T01:16:40Z"}},{"startTime":"2021-10-18T13:00:00Z","values":{"temperature":74.26,"weatherCode":1001,"temperatureMax":74.26,"temperatureMin":64.9,"windSpeed":10.47,"precipitationType":0,"precipitationProbability":0,"humidity":69.02,"visibility":15,"sunriseTime":"2021-10-18T14:00:00Z","sunsetTime":"2021-10-19T01:15:00Z"}},{"startTime":"2021-10-19T13:00:00Z","values":{"temperature":74.41,"weatherCode":1100,"temperatureMax":74.41,"temperatureMin":63.52,"windSpeed":10.72,"precipitationType":0,"precipitationProbability":0,"humidity":52.89,"visibility":15,"sunriseTime":"2021-10-19T14:00:00Z","sunsetTime":"2021-10-20T01:15:00Z"}},{"startTime":"2021-10-20T13:00:00Z","values":{"temperature":73.9,"weatherCode":1100,"temperatureMax":73.9,"temperatureMin":64.22,"windSpeed":9.33,"precipitationType":0,"precipitationProbability":0,"humidity":54.94,"visibility":15,"sunriseTime":"2021-10-20T14:03:20Z","sunsetTime":"2021-10-21T01:13:20Z"}}]}]}}
                # print(response)
                # return redirect(url_for("current", location=num, content=response))
                weekdays = (
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                )
                mon = (
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                )
                arr = []
                for dic in response["data"]["timelines"][1]["intervals"]:
                    date = dic["startTime"].split("-")
                    year = date[0]
                    month = date[1]
                    mon_string = mon[int(date[1]) - 1]
                    temp = date[2]
                    day = temp[0:2]
                    index = calendar.weekday(int(year), int(month), int(day))
                    weeknum = weekdays[index]
                    arr.append(
                        str(weeknum)
                        + ","
                        + str(day)
                        + " "
                        + str(mon_string)
                        + " "
                        + str(year)
                    )
                return render_template(
                    "current.html",
                    location=loc,
                    content=response,
                    day=arr,
                    format_location=num,
                    city=city,
                    street=street,
                    state=state,
                    check=check
                )

    #     if ipinfo is not None:
    #         # call tomorrow api
    #         num = ipinfo
    #         # return current(num, response)
    #         # print(num)
    #         # url = "https://api.tomorrow.io/v4/timelines"
    #         # querystring = {"location": num,
    #         #                "fields": ["temperature", "humidity", "temperatureApparent", "temperatureMin", "temperatureMax",
    #         #                           "windSpeed", "windDirection", "humidity", "pressureSeaLevel", "uvIndex",
    #         #                           "weatherCode", "precipitationProbability", "precipitationType", "sunriseTime",
    #         #                           "sunsetTime", "visibility", "moonPhase", "cloudCover"],
    #         #                "units": "imperial",
    #         #                "timesteps": ["1h", "1d", "current"],
    #         #                "timezone": "America/Los_Angeles",
    #         #                "apikey": "U5JkcDUxTYiySxKNrIX58vd1kX9EuqVS"}
    #         # headers = {"Accept": "application/json"}
    #         # response = requests.request("GET", url, headers=headers, params=querystring).json()
    #
    #
    #         # print(response)
    #         # return redirect(url_for("current", location=num, content=response))
    #         weekdays = (
    #             "Monday",
    #             "Tuesday",
    #             "Wednesday",
    #             "Thursday",
    #             "Friday",
    #             "Saturday",
    #             "Sunday",
    #         )
    #         mon = (
    #             "Jan",
    #             "Feb",
    #             "Mar",
    #             "Apr",
    #             "May",
    #             "Jun",
    #             "Jul",
    #             "Aug",
    #             "Sep",
    #             "Oct",
    #             "Nov",
    #             "Dec",
    #         )
    #         arr = []
    #         for dic in response["data"]["timelines"][1]["intervals"]:
    #             date = dic["startTime"].split("-")
    #             year = date[0]
    #             month = date[1]
    #             mon_string = mon[int(date[1]) - 1]
    #             temp = date[2]
    #             day = temp[0:2]
    #             index = calendar.weekday(int(year), int(month), int(day))
    #             weeknum = weekdays[index]
    #             arr.append(
    #                 str(weeknum)
    #                 + ","
    #                 + str(day)
    #                 + " "
    #                 + str(mon_string)
    #                 + " "
    #                 + str(year)
    #             )
    #             print("check")
    #         # return render_template('current.html', location="xxx", content=response, day=arr, format_location=num)
    #         # return render_template('current.html', location=response['results'][0]['formatted_address'], content=response, day=arr, format_location=num)
    #         # render_template('current.html', location="xxx", content=response, day=arr, format_location=num)
    #         return "hello"
    #
    #     #     return render_template('getmethod.html')
    # # http://127.0.0.1:8080/weather?street=770+S+Grand+Ave&city=Los+Angeles&state=California
    # print("here")
    return render_template("base.html")


@app.route("/current<location>")
def current(location, content):
    return render_template("current.html", location=location, content=content)



@app.route("/detail<info>")
def detail(info):
    print("hereeeeeee")
    print(check)

    arr = info.split("+")
    url = "https://api.tomorrow.io/v4/timelines"
    querystring = {"location": arr[1],
                   "fields": ["temperature", "humidity", "temperatureApparent", "temperatureMin", "temperatureMax",
                              "windSpeed", "windDirection", "humidity", "pressureSeaLevel", "uvIndex",
                              "weatherCode", "precipitationProbability", "precipitationType", "sunriseTime",
                              "sunsetTime", "visibility", "moonPhase", "cloudCover"],
                   "units": "imperial",
                   "timesteps": ["1h", "1d", "current"],
                   "timezone": "America/Los_Angeles",
                   #"apikey": "U5JkcDUxTYiySxKNrIX58vd1kX9EuqVS"
                   "apikey": "U5JkcDUxTYiySxKNrIX58vd1kX9EuqVS"
                   }
    # mlKq38WsS2gQpTXtHtucSDc4D5zZhpaJ
    # U5JkcDUxTYiySxKNrIX58vd1kX9EuqVS
    headers = {"Accept": "application/json"}
    resp = requests.request("GET", url, headers=headers, params=querystring).json()
    # resp = {"data":{"timelines":[{"timestep":"1d","startTime":"2021-10-05T13:00:00Z","endTime":"2021-10-20T13:00:00Z","intervals":[{"startTime":"2021-10-05T13:00:00Z","values":{"temperature":81.5,"weatherCode":1000,"temperatureMax":81.5,"temperatureMin":62.04,"windSpeed":10.92,"precipitationType":0,"precipitationProbability":0,"humidity":95,"visibility":9.94,"sunriseTime":"2021-10-05T13:50:00Z","sunsetTime":"2021-10-06T01:31:40Z"}},{"startTime":"2021-10-06T13:00:00Z","values":{"temperature":74.19,"weatherCode":1001,"temperatureMax":74.19,"temperatureMin":60.26,"windSpeed":7.83,"precipitationType":0,"precipitationProbability":0,"humidity":98.66,"visibility":9.94,"sunriseTime":"2021-10-06T13:51:40Z","sunsetTime":"2021-10-07T01:30:00Z"}},{"startTime":"2021-10-07T13:00:00Z","values":{"temperature":70.72,"weatherCode":1001,"temperatureMax":70.72,"temperatureMin":60.08,"windSpeed":7.9,"precipitationType":1,"precipitationProbability":10,"humidity":98.93,"visibility":9.94,"sunriseTime":"2021-10-07T13:51:40Z","sunsetTime":"2021-10-08T01:30:00Z"}},{"startTime":"2021-10-08T13:00:00Z","values":{"temperature":68.56,"weatherCode":1001,"temperatureMax":68.56,"temperatureMin":55.27,"windSpeed":15.21,"precipitationType":1,"precipitationProbability":15,"humidity":88.41,"visibility":12.05,"sunriseTime":"2021-10-08T13:51:40Z","sunsetTime":"2021-10-09T01:26:40Z"}},{"startTime":"2021-10-09T13:00:00Z","values":{"temperature":72.93,"weatherCode":1000,"temperatureMax":72.93,"temperatureMin":57.24,"windSpeed":11.77,"precipitationType":0,"precipitationProbability":0,"humidity":73.24,"visibility":15,"sunriseTime":"2021-10-09T13:53:20Z","sunsetTime":"2021-10-10T01:26:40Z"}},{"startTime":"2021-10-10T13:00:00Z","values":{"temperature":80.04,"weatherCode":1000,"temperatureMax":80.04,"temperatureMin":66.07,"windSpeed":12.24,"precipitationType":0,"precipitationProbability":0,"humidity":63.82,"visibility":15,"sunriseTime":"2021-10-10T13:53:20Z","sunsetTime":"2021-10-11T01:25:00Z"}},{"startTime":"2021-10-11T13:00:00Z","values":{"temperature":74.35,"weatherCode":1000,"temperatureMax":74.35,"temperatureMin":60.53,"windSpeed":18.5,"precipitationType":1,"precipitationProbability":0,"humidity":67.39,"visibility":15,"sunriseTime":"2021-10-11T13:53:20Z","sunsetTime":"2021-10-12T01:23:20Z"}},{"startTime":"2021-10-12T13:00:00Z","values":{"temperature":70.68,"weatherCode":1000,"temperatureMax":70.68,"temperatureMin":60.28,"windSpeed":12.42,"precipitationType":0,"precipitationProbability":0,"humidity":31.1,"visibility":15,"sunriseTime":"2021-10-12T13:56:40Z","sunsetTime":"2021-10-13T01:23:20Z"}},{"startTime":"2021-10-13T13:00:00Z","values":{"temperature":72.05,"weatherCode":1000,"temperatureMax":72.05,"temperatureMin":62.56,"windSpeed":13.8,"precipitationType":0,"precipitationProbability":0,"humidity":41.02,"visibility":15,"sunriseTime":"2021-10-13T13:56:40Z","sunsetTime":"2021-10-14T01:21:40Z"}},{"startTime":"2021-10-14T13:00:00Z","values":{"temperature":76.39,"weatherCode":1000,"temperatureMax":76.39,"temperatureMin":64.47,"windSpeed":10.07,"precipitationType":0,"precipitationProbability":0,"humidity":40.08,"visibility":15,"sunriseTime":"2021-10-14T13:58:20Z","sunsetTime":"2021-10-15T01:21:40Z"}},{"startTime":"2021-10-15T13:00:00Z","values":{"temperature":79.72,"weatherCode":1000,"temperatureMax":79.72,"temperatureMin":66.69,"windSpeed":8.81,"precipitationType":0,"precipitationProbability":0,"humidity":41.33,"visibility":15,"sunriseTime":"2021-10-15T13:58:20Z","sunsetTime":"2021-10-16T01:18:20Z"}},{"startTime":"2021-10-16T13:00:00Z","values":{"temperature":80.85,"weatherCode":1001,"temperatureMax":80.85,"temperatureMin":68.41,"windSpeed":8.52,"precipitationType":0,"precipitationProbability":0,"humidity":41.31,"visibility":15,"sunriseTime":"2021-10-16T13:58:20Z","sunsetTime":"2021-10-17T01:16:40Z"}},{"startTime":"2021-10-17T13:00:00Z","values":{"temperature":78.76,"weatherCode":1001,"temperatureMax":78.76,"temperatureMin":65.19,"windSpeed":8.86,"precipitationType":0,"precipitationProbability":0,"humidity":67.12,"visibility":15,"sunriseTime":"2021-10-17T14:00:00Z","sunsetTime":"2021-10-18T01:16:40Z"}},{"startTime":"2021-10-18T13:00:00Z","values":{"temperature":74.26,"weatherCode":1001,"temperatureMax":74.26,"temperatureMin":64.9,"windSpeed":10.47,"precipitationType":0,"precipitationProbability":0,"humidity":69.02,"visibility":15,"sunriseTime":"2021-10-18T14:00:00Z","sunsetTime":"2021-10-19T01:15:00Z"}},{"startTime":"2021-10-19T13:00:00Z","values":{"temperature":74.41,"weatherCode":1100,"temperatureMax":74.41,"temperatureMin":63.52,"windSpeed":10.72,"precipitationType":0,"precipitationProbability":0,"humidity":52.89,"visibility":15,"sunriseTime":"2021-10-19T14:00:00Z","sunsetTime":"2021-10-20T01:15:00Z"}},{"startTime":"2021-10-20T13:00:00Z","values":{"temperature":73.9,"weatherCode":1100,"temperatureMax":73.9,"temperatureMin":64.22,"windSpeed":9.33,"precipitationType":0,"precipitationProbability":0,"humidity":54.94,"visibility":15,"sunriseTime":"2021-10-20T14:03:20Z","sunsetTime":"2021-10-21T01:13:20Z"}}]}]}}

    # print(response)
    sunset = resp["data"]["timelines"][1]["intervals"][int(arr[0])]["values"][
        "sunsetTime"
    ].split("T")
    sunrise = resp["data"]["timelines"][1]["intervals"][int(arr[0])]["values"][
        "sunriseTime"
    ].split("T")

    print(sunrise, sunset)
    time = {
        "00": "12AM",
        "01": "1AM",
        "02": "2AM",
        "03": "3AM",
        "04": "4AM",
        "05": "5AM",
        "06": "6AM",
        "07": "7AM",
        "08": "8AM",
        "09": "9AM",
        "10": "10AM",
        "11": "11AM",
        "12": "12PM",
        "13": "1PM",
        "14": "2PM",
        "15": "3PM",
        "16": "4PM",
        "17": "5PM",
        "18": "6PM",
        "19": "7PM",
        "20": "8PM",
        "21": "9PM",
        "22": "10PM",
        "23": "11PM",
    }
    print(arr[3], arr[4], arr[5])
    sunsetTime = time[sunset[1][0:2]]
    sumriseTime = time[sunrise[1][0:2]]

    return render_template(
        "detail.html",
        content=resp["data"]["timelines"][1]["intervals"][int(arr[0])]["values"],
        date=arr[2],
        sunsetTime=sunsetTime,
        sumriseTime=sumriseTime,
        date_content=resp["data"]["timelines"][1]["intervals"],
        hour_data=resp["data"]["timelines"][0]["intervals"],
        city=arr[3],
        street=arr[4].strip(),
        state=arr[5].strip(),
        check=check
    )

@app.route("/getapi<info>")
def getapi(info):
    print(info)
    lat = info.split("+")[0]
    lng = info.split("+")[1]
    print(lat)
    print(lng)
    num = str(lat) + ", " + str(lng)
    # print(num)
    url = "https://api.tomorrow.io/v4/timelines"
    querystring = {"location": num,
                   "fields": ["temperature", "humidity", "temperatureApparent", "temperatureMin", "temperatureMax",
                              "windSpeed", "windDirection", "humidity", "pressureSeaLevel", "uvIndex",
                              "weatherCode", "precipitationProbability", "precipitationType", "sunriseTime",
                              "sunsetTime", "visibility", "moonPhase", "cloudCover"],
                   "units": "imperial",
                   "timesteps": ["1h", "1d", "current"],
                   "timezone": "America/Los_Angeles",
                   #"apikey": "U5JkcDUxTYiySxKNrIX58vd1kX9EuqVS"
                   "apikey": "U5JkcDUxTYiySxKNrIX58vd1kX9EuqVS"
                   }
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
