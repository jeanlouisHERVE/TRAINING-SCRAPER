import unittest
import psycopg2
import subprocess
import time

from dotenv import load_dotenv
from modules.database_app import (
    create_tables,
    delete_tables,
    add_course,
    add_course_date_time,
    add_date,
    add_department,
    add_town,
    add_type,
    add_organism,
    get_courses,
    get_course_id,
    get_course_date_time,
    get_date,
    get_dates,
    get_departments,
    get_department_from_number,
    get_towns,
    get_town_from_name,
    get_types,
    get_type_from_name,
    get_organisms,
    get_organism_from_name,
    course_exists,
)

# TODO adapt to postgresql

# get data from .env file
load_dotenv()


class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.db = subprocess.Popen(["pg_tmp", "testdb"])
        time.sleep(2)

        self.conn = psycopg2.connect(
            dbname="testdb",
            user="test_user",
            password="test_password",
            host="localhost",
            port=self.db._kwargs['port']  # Get the port from pg_tmp
        )
        self.cur = self.conn.cursor()
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
            self.cur.close()
            self.conn.close()
            self.db.terminate()
            self.db.wait()
            print("------TEST END : ENSURE DATABASE IS CLEANED--------")
            courses = get_courses()
            dates = get_dates()
            course_date_time = get_course_date_time()
            departments = get_departments()
            towns = get_towns()
            types = get_types()
            organisms = get_organisms()
            print("get_courses", courses)
            print("get_dates", dates)
            print("get_course_date_time", course_date_time)
            print("get_departments", departments)
            print("get_towns", towns)
            print("get_types", types)
            print("get_organisms", organisms)
            print("-------------------------------------------------------")
            print("-------------------------------------------------------")

    def test_add_course(self):
        # Test with valid input
        result = add_course(10, 20, 100, 123456789.0, 1, 1, 1, 1)
        self.assertIsNotNone(result)

    def test_add_date(self):
        # Test with valid input
        result = add_date(123456789.0)
        self.assertIsNotNone(result)

    def test_add_course_date_time(self):
        # Test with valid input
        add_course(10, 20, 100, 123456789.0, 1, 1, 1, 1)
        result = add_course_date_time(1, 1, 9.0, 12.0)
        self.assertIsNone(result)

    def test_add_department(self):
        # Test with valid input
        result = add_department("123", "Department Name")
        self.assertIsNotNone(result)

    def test_add_town(self):
        # Test with valid input
        result = add_town("12345", "Town Name", 1)
        self.assertIsNotNone(result)

    def test_add_type(self):
        # Test with valid input
        result = add_type("Type Name", "Type Description")
        self.assertIsNotNone(result)

    def test_add_organism(self):
        # Test with valid input
        result = add_organism("Organism Name")
        self.assertIsNotNone(result)

    def test_get_courses(self):
        result = get_courses()
        self.assertIsNotNone(result)

    def test_get_course_id(self):
        # You may need to modify this test based on the actual data in your database
        result = get_course_id(1, 1, 1, 1)
        self.assertIsNotNone(result)

    def test_get_dates(self):
        result = get_dates()
        self.assertIsNotNone(result)

    def test_get_date(self):
        result = get_date(123456789.0)
        self.assertIsNotNone(result)

    def test_get_course_date_time(self):
        # You may need to modify this test based on the actual data in your database
        result = get_course_date_time(1)
        self.assertIsNotNone(result)

    def test_get_departments(self):
        result = get_departments()
        self.assertIsNotNone(result)

    def test_get_department_from_number(self):
        result = get_department_from_number("123")
        self.assertIsNotNone(result)

    def test_get_towns(self):
        result = get_towns()
        self.assertIsNotNone(result)

    def test_get_town_from_name(self):
        result = get_town_from_name("Town Name")
        self.assertIsNotNone(result)

    def test_get_types(self):
        result = get_types()
        self.assertIsNotNone(result)

    def test_get_type_from_name(self):
        result = get_type_from_name("Type Name")
        self.assertIsNotNone(result)

    def test_get_organisms(self):
        result = get_organisms()
        self.assertIsNotNone(result)

    def test_get_organism_from_name(self):
        result = get_organism_from_name("Organism Name")
        self.assertIsNotNone(result)

    def test_course_exists(self):
        # You may need to modify this test based on the actual data in your database
        result = course_exists(123456789.0, "Town Name", "Type Name")
        self.assertFalse(result)  # Assuming it should not exist in this case


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDatabaseFunctions)

    # Define the order of tests
    ordered_tests = [
            "test_add_course",
            "test_add_date",
            "test_add_course_date_time",
            "test_add_department",
            "test_add_town",
            "test_add_type",
            "test_add_organism",
            "test_get_courses",
            "test_get_course_id",
            "test_get_dates",
            "test_get_date",
            "test_get_course_date_time",
            "test_get_departments",
            "test_get_department_from_number",
            "test_get_towns",
            "test_get_town_from_name",
            "test_get_types",
            "test_get_type_from_name",
            "test_get_organisms",
            "test_get_organism_from_name",
            "test_course_exists",
            ]

    test_instance = TestDatabaseFunctions()
    ordered_suite = unittest.TestSuite()

    for test_name in ordered_tests:
        ordered_suite.addTest(test_instance.findTest(test_instance, test_name))

    runner = unittest.TextTestRunner()
    runner.run(ordered_suite)
