import requests
import json
from data.model.point import Point
from data.model.journey import Journey
from geojson import LineString
from uuid import uuid4
import polyline

def generate_journey_from_start_stop_coordinates(start_point: Point, end_point: Point) -> Journey:
    base = "http://localhost:8080"
    uri = "/otp/routers/default/transmodel/index/graphql"
    url = base + uri

    print(start_point.latitude, start_point.longitude)

    start_pos_lat = start_point.latitude
    start_pos_long = start_point.longitude

    end_pos_lat = end_point.latitude
    end_pos_long = end_point.longitude

    body = f"""
        {{
            trip(
                from: {{
                    coordinates: {{
                        latitude: {start_pos_lat}, 
                        longitude: {start_pos_long}
                        }}
                        }}
                to: {{
                    coordinates: {{
                        latitude: {end_pos_lat}, 
                        longitude: {end_pos_long}
                        }}
                    }}
                modes: {{directMode: bicycle}}
                bicycleOptimisationMethod: triangle
                triangleFactors: {{safety: 1.5, slope: 1.5, time: 1.5}}
            ) {{
            tripPatterns {{
                legs {{
                    mode
                    distance
                    duration
                    pointsOnLink {{
                        points
                    }}
                }}
            }}
            debugOutput {{
                totalTime
                }}
            }}
        }}
    """

    response = requests.post(url=url, json={"query":body})

    print("reponse status code: ", response.status_code)

    list_with_coordinates = []

    # Parsing output if successfull
    if response.status_code == 200:
        parsed_respone = json.loads(response.content)

        points = parsed_respone['data']['trip']['tripPatterns'][0]['legs'][0]['pointsOnLink']['points']
    
        decodedListOfPoints = polyline.decode(points)

        for item in decodedListOfPoints:
            list_with_coordinates.append([item[1],item[0]])


    return Journey(uuid4(), start_point, end_point, LineString(list_with_coordinates))


def test_generate_journey_from_start_stop_coordinates():          
    test = generate_journey_from_start_stop_coordinates(Point(59.93577, 10.69618),Point(59.91350, 10.72918))
    print(test)