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
        "test_add_course",
        "test_add_date",
        "test_add_training",
        "test_add_department",
        "test_add_town",
        "test_add_organism",
    ]

    test_instance = TestDatabaseFunctions()
    ordered_suite = unittest.TestSuite()

    for test_name in ordered_tests:
        ordered_suite.addTest(test_instance.findTest(test_instance, test_name))

    runner = unittest.TextTestRunner()
    runner.run(ordered_suite)
