from repository.generate import generate_journey_from_start_stop_coordinates, csv_start_stop_to_journeys, journeys_to_feature_collection, feature_collection_to_geojson
from data.model.point import Point

def test_generate_journey_from_start_stop_coordinates():          
    test = generate_journey_from_start_stop_coordinates( Point(59.93577, 10.69618), Point(59.91350, 10.72918) )
    print(test)

def test_csv_start_stop_to_journeys():
    filepath_to_csv = "./test/test_file.csv"
    
    print(csv_start_stop_to_journeys(filepath_to_csv))

def test_large_csv_start_stop_to_journeys():
    filepath_to_csv = "./test/1000_tilfeldige_punktpar_oslo.csv"
    
    print(csv_start_stop_to_journeys(filepath_to_csv, progress_bar = True))

def test_journeys_to_feature_collection():
    filepath_to_csv = "./test/test_file.csv"

    journeys = csv_start_stop_to_journeys(filepath_to_csv)

    feature_collection = journeys_to_feature_collection(journeys)

    print("Printing feature collection: ", feature_collection)

def test_feature_collection_to_geojson():
    # filepath_to_csv = "./test/test_file.csv"
    filepath_to_csv = "./test/1000_tilfeldige_punktpar_oslo.csv"

    journeys = csv_start_stop_to_journeys(filepath_to_csv, True)

    feature_collection = journeys_to_feature_collection(journeys)

    feature_collection_to_geojson(feature_collection, "./test/1000_punktpar_test.geojson")


def run_all_tests():
    test_generate_journey_from_start_stop_coordinates()
    test_csv_start_stop_to_journeys()
    test_journeys_to_feature_collection()
    test_feature_collection_to_geojson()

# run_all_tests()

# test_generate_journey_from_start_stop_coordinates
# test_large_csv_start_stop_to_journeys()
# test_journeys_to_feature_collection
test_feature_collection_to_geojson()