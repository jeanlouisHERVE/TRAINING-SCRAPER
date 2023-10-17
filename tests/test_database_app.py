import unittest
import psycopg2

from dotenv import load_dotenv
from modules.database_app import (
    create_tables,
    delete_tables
)
# TODO add functions to test
# TODO adapt to postgresql

# get data from .env file
load_dotenv()


class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.database_connection = psycopg2.connect(":memory:")

        self.cursor = self.database_connection.cursor()

        # Create the database tables before running tests
        create_tables()

    def tearDown(self):
        try:
            # Reset the database before closing the connection
            print("Resetting database")
            delete_tables()
        except Exception as e:
            print(f"Error resetting the database: {e}")
        finally:
            # Close the database connection
            print("Closing database")
            self.database_connection.close()
            print("------TEST END : ENSURE DATABASE IS CLEANED--------")
            # properties = get_properties()
            # agencies = get_agencies()
            # descriptions = get_properties_descriptions()
            # prices = get_prices()
            # old_properties = get_old_properties()
            # old_properties_descriptions = get_old_properties_descriptions()
            # old_prices = get_old_prices()
            # print("get_properties", properties)
            # print("get_agencies", agencies)
            # print("get_descriptions", descriptions)
            # print("get_prices", prices)
            # print("get_old_properties", old_properties)
            # print("get_old_properties_descriptions", old_properties_descriptions)
            # print("get_old_prices", old_prices)
            print("-------------------------------------------------------")
            print("-------------------------------------------------------")


# TODO add functions to test


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDatabaseFunctions)

    # Define the order of tests
    ordered_tests = [
        # "test_add_property",
        # "test_add_old_property",
        # "test_add_description",
        # "test_add_agency",
        # "test_add_price_to_property",
        # "test_get_property_by_url",
        # "test_get_property_by_id",
        # "test_get_id_url_from_properties",
        # "test_get_id_url_dateofmodification_from_properties",
        # "test_get_properties",
        # "test_get_properties_number",
        # "test_get_properties_from_adding_date",
        # "test_get_property_description_by_id",
        # "test_get_agency",
        # "test_get_agencies",
        # "test_get_agency_id_from_name",
        # "test_update_description",
        # "test_update_agency",
        # "test_delete_property",
    ]

    test_instance = TestDatabaseFunctions()
    ordered_suite = unittest.TestSuite()

    for test_name in ordered_tests:
        ordered_suite.addTest(test_instance.findTest(test_instance, test_name))

    runner = unittest.TextTestRunner()
    runner.run(ordered_suite)
