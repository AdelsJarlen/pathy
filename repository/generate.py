from requests import Response, post
import json
from data.model.point import Point
from data.model.journey import Journey
from geojson import LineString, FeatureCollection, Feature, dump
from uuid import uuid4
import polyline
import csv

def generate_journey_from_start_stop_coordinates(start_point: Point, end_point: Point) -> Journey:
    
    response = bicycle_graphQl_query(start_point, end_point)

    list_with_coordinates = []

    # Parsing output if successfull response
    if response.status_code == 200:
        parsed_respone = json.loads(response.content)

        points = parsed_respone['data']['trip']['tripPatterns'][0]['legs'][0]['pointsOnLink']['points']
    
        decodedListOfPoints = polyline.decode(points)

        for item in decodedListOfPoints:
            list_with_coordinates.append([item[1],item[0]])


    return Journey(uuid4(), start_point, end_point, LineString(list_with_coordinates))

def bicycle_graphQl_query(start_point, end_point) -> Response:
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

    response = post(url=url, json={"query":body})

    print("reponse status code: ", response.status_code)

    return response

def csv_start_stop_to_journeys(file_path) -> list[Journey]:
    '''
    The CSV should have a coordinates for a start location and stop location on a single line following lat, long, lat, long.
    For several start and stop locations seperate with a new line
    '''
    journeys = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)

        if reader != float: next(reader)

        for row in reader:
            start_point = Point(float(row[0]), float(row[1]))
            end_point = Point(float(row[2]), float(row[3]))

            journey = generate_journey_from_start_stop_coordinates(start_point, end_point)

            journeys.append(journey)
            
    return journeys

def journeys_to_feature_collection(journeys: list[Journey]) -> FeatureCollection:
    # Create a list of features from the LineString objects
    line_strings = [journey.path for journey in journeys]

    features = [Feature(geometry=line_string) for line_string in line_strings]
    
    # Create a FeatureCollection from the features
    feature_collection = FeatureCollection(features)
    
    return feature_collection


def feature_collection_to_geojson(featureCollection: FeatureCollection, filename: str):
    with open(filename, 'w') as f:
        dump(featureCollection, f)

        