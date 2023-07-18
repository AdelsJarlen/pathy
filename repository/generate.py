import requests
import json
from data.model.point import Point
from data.model.journey import Journey
from geojson import LineString
from uuid import uuid4

def generate_journey_from_start_stop_coordinates(start_point: Point, end_point: Point):
    base = "http://localhost:8080"
    uri = "/otp/routers/default/transmodel/index/graphql"
    url = base + uri

    print(start_point.latitude, start_point.longitude)


    body = """
        {
            trip(
                from: {coordinates: {latitude: 59.92990, longitude: 10.71579}}
                to: {coordinates: {latitude: 59.92543, longitude: 10.78583}}
                modes: {directMode: bicycle}
                triangleFactors: {safety: 1.5, slope: 1.5, time: 1.5}
            ) {
                tripPatterns {
                legs {
                    mode
                    distance
                    duration
                    steps {
                    latitude
                    longitude
                    }
                }
                }
                debugOutput {
                totalTime
                }
            }
        }
    """

    response = requests.post(url=url, json={"query":body})

    print("reponse status code: ", response.status_code)

    list_with_coordinates = []

    # Parsing output if successfull
    if response.status_code == 200:
        parsed_respone = json.loads(response.content)
        legs = parsed_respone['data']['trip']['tripPatterns'][0]['legs'][0]
        properties = {"mode" : legs['mode'], "distance" : legs['distance'], "duration":legs['duration']}
        steps = legs['steps']

        for step in steps:
            latitude = step['latitude']
            longitude = step['longitude']

            list_with_coordinates.append([latitude,longitude])

    return Journey(uuid4(), start_point, end_point, LineString(list_with_coordinates))
            
            


        


test = generate_journey_from_start_stop_coordinates(Point(10.0,11.0),Point(12.0,13.0))

print(test)