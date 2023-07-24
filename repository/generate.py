from requests import Response, post
import json
from data.model.point import Point
from data.model.journey import Journey
from geojson import LineString, FeatureCollection, Feature, dump
from uuid import uuid4
import polyline
from math import ceil
import csv
from util import terminal_progress_bar
from threading import Thread, Condition
import time

def generate_journey_from_start_stop_coordinates(start_point: Point, end_point: Point, print=False) -> Journey:
    
    response = bicycle_graphQl_query(start_point, end_point)

    list_with_coordinates = []

    # Parsing output if successfull response
    if response.status_code == 200:
        parsed_respone = json.loads(response.content)
        
        if print: print(parsed_respone)

        if len(parsed_respone['data']['plan']['itineraries']) == 0 : return None

        travel_time_seconds = parsed_respone['data']['plan']['itineraries'][0]['legs'][0]['duration']
        points = parsed_respone['data']['plan']['itineraries'][0]['legs'][0]['legGeometry']['points']
    
        decodedListOfPoints = polyline.decode(points)

        for item in decodedListOfPoints:
            list_with_coordinates.append([item[1],item[0]])


        return Journey(uuid4(), start_point, end_point, LineString(list_with_coordinates), duration_seconds = travel_time_seconds)
    
    return None

def bicycle_graphQl_query(start_point, end_point, print = False) -> Response:
    base = "http://localhost:8080"
    uri = "/otp/routers/default/index/graphql"
    url = base + uri

    if print: 
        print(start_point.latitude, start_point.longitude)
        print(end_point.latitude, end_point.longitude)

    start_pos_lat = start_point.latitude
    start_pos_long = start_point.longitude

    end_pos_lat = end_point.latitude
    end_pos_long = end_point.longitude

    body = f"""
        query {{
            plan(
                from: {{
                    lat: {start_pos_lat}, 
                    lon: {start_pos_long}
                }}
                to: {{
                    lat: {end_pos_lat}, 
                    lon: {end_pos_long}
                }}
                transportModes: {{
                    mode: BICYCLE
                }}
                optimize: TRIANGLE
                triangle: {{
                    safetyFactor: 1.5, 
                    slopeFactor: 1.5, 
                    timeFactor: 1.5
                }}
            ) {{
                itineraries {{
                    legs {{
                        to {{
                            lat
                            lon
                        }}
                        from {{
                            lat
                            lon
                        }}
                        distance
                        duration
                        walkingBike
                        generalizedCost
                        legGeometry {{
                            length
                            points
                        }}
                    }}
                }}
            }}
        }}
    """

    response = post(url=url, json={"query":body})

    if print: print("reponse status code: ", response.status_code)

    return response

def csv_start_stop_to_journeys(file_path, progress_bar = False) -> list[Journey]:
    '''
    The CSV should have a coordinates for a start location and stop location on a single line following lat, long, lat, long.
    For several start and stop locations seperate with a new line
    '''

    print("Starting CSV to Journey conversion")
    cv = Condition()
    global current_line
    current_line = 1
    start_time = time.perf_counter()

    if progress_bar:
        global line_count

        line_count = 0
        with open(file_path, 'r') as file:
            print("Counting number of lines")
            for line in file:
                print("\rNumber of lines ",line_count, end='')
                line_count += 1
        file.close
        s = f"\nDone in {ceil(time.perf_counter() - start_time)} seconds." 
        print(s)

        def progress_bar():
            start_time = time.perf_counter()
            with cv:
                global current_line
                print("Starting progress bar")
                while True:
                    if current_line % 10^(len(str(line_count)) - 1) == 0:
                        
                        time_seconds = ceil((time.perf_counter() - start_time)/current_line * line_count)
                        time_string = ("seconds", time_seconds)
                        if time_seconds > 60:
                            time_minutes = ceil(time_seconds / 60)
                            if time_minutes > 60:
                                time_hours = ceil(time_minutes/60)
                                if time_hours/24 > 24:
                                    print("WARNING. estimated time more than 24 hours")
                                else: time_string = ("hours", time_hours)
                            else: time_string = ("minutes", time_minutes)
                            

                        s = terminal_progress_bar.create_progress_bar(message = "Processing CSV: ", progress = current_line, count = line_count) + " Time remaining " + str(time_string[1]) + " " + time_string[0]
                        print(s, end='')
                    cv.wait()
                
        progress_bar_thread = Thread(target = progress_bar, daemon=True)


    journeys = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file,delimiter=",")

        if reader != float: next(reader)
        if progress_bar: progress_bar_thread.start()

        for row_index, row_value in enumerate(reader):
            current_line = row_index
            start_point = Point(float(row_value[0]), float(row_value[1]))
            end_point = Point(float(row_value[2]), float(row_value[3]))

            journey = generate_journey_from_start_stop_coordinates(start_point, end_point)
            if journey != None: journeys.append(journey)
            with cv:
                cv.notify_all()
            
    return journeys

def journeys_to_feature_collection(journeys: list[Journey]) -> FeatureCollection:
    # Create a list of features from the LineString objects

    features = [Feature(geometry=journey.path, properties = {"duration_seconds" : journey.duration_seconds}) for journey in journeys]
    
    # Create a FeatureCollection from the features
    feature_collection = FeatureCollection(features)
    
    return feature_collection


def feature_collection_to_geojson(featureCollection: FeatureCollection, filename: str):
    with open(filename, 'w') as f:
        dump(featureCollection, f)

        