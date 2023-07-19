from repository.generate import generate_journey_from_start_stop_coordinates, csv_start_stop_to_journeys, journeys_to_feature_collection
from data.model.point import Point

def test_generate_journey_from_start_stop_coordinates():          
    test = generate_journey_from_start_stop_coordinates( Point(59.93577, 10.69618), Point(59.91350, 10.72918) )
    print(test)

def test_csv_start_stop_to_journeys():
    filepath_to_csv = "./test/test_file.csv"

    print(csv_start_stop_to_journeys(filepath_to_csv))

def test_journeys_to_feature_collection():
    filepath_to_csv = "./test/test_file.csv"

    journeys = csv_start_stop_to_journeys(filepath_to_csv)

    feature_collection = journeys_to_feature_collection(journeys)

    print("Printing feature collection: ", feature_collection)


def run_all_tests():
    test_generate_journey_from_start_stop_coordinates()
    test_csv_start_stop_to_journeys()

# run_all_tests()

# test_csv_start_stop_to_journeys()

test_journeys_to_feature_collection()