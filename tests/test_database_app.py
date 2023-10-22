# import unittest
# import psycopg2
# import subprocess
# import time

# from dotenv import load_dotenv
# from modules.database_app import (
#     create_tables,
#     delete_tables,
#     add_course,
#     add_date,
#     add_training,
#     add_department,
#     add_town,
#     add_organism,
#     get_courses,
#     get_dates,
#     get_trainings,
#     get_departments,
#     get_towns,
#     get_organisms
# )

# # TODO adapt to postgresql

# # get data from .env file
# load_dotenv()


# class TestDatabaseFunctions(unittest.TestCase):
#     def setUp(self):
#         # Create an in-memory SQLite database for testing
#         self.db = subprocess.Popen(["pg_tmp", "testdb"])
#         time.sleep(2)

#         self.conn = psycopg2.connect(
#             dbname="testdb",
#             user="test_user",
#             password="test_password",
#             host="localhost",
#             port=self.db._kwargs['port']  # Get the port from pg_tmp
#         )
#         self.cur = self.conn.cursor()
#         create_tables()

#     def tearDown(self):
#         try:
#             # Reset the database before closing the connection
#             print("Resetting database")
#             delete_tables()
#         except Exception as e:
#             print(f"Error resetting the database: {e}")
#         finally:
#             # Close the database connection
#             print("Closing database")
#             self.cur.close()
#             self.conn.close()
#             self.db.terminate()
#             self.db.wait()
#             print("------TEST END : ENSURE DATABASE IS CLEANED--------")
#             courses = get_courses()
#             dates = get_dates()
#             trainings = get_trainings()
#             departments = get_departments()
#             towns = get_towns()
#             organisms = get_organisms()
#             print("get_courses", courses)
#             print("get_dates", dates)
#             print("get_trainings", trainings)
#             print("get_departments", departments)
#             print("get_towns", towns)
#             print("get_organisms", organisms)
#             print("-------------------------------------------------------")
#             print("-------------------------------------------------------")

#     def test_add_course(self):
#         places_available = 10
#         places_total = 20
#         price = 100
#         date_add_to_db = 1634520000
#         town_id = 1
#         type_id = 2
#         organism_id = 3
#         department_id = 4
#         date_id = 5

#         last_inserted_id = add_course(
#             places_available,
#             places_total,
#             price,
#             date_add_to_db,
#             town_id,
#             type_id,
#             organism_id,
#             department_id,
#             date_id,
#         )

#         self.assertIsNotNone(last_inserted_id)
#         self.cur.execute("SELECT * FROM courses WHERE id = %s", (last_inserted_id,))
#         result = self.cur.fetchone()
#         self.assertIsNotNone(result)
#         self.assertEqual(result[1], places_available)
#         self.assertEqual(result[2], places_total)
#         self.assertEqual(result[3], price)
#         self.assertEqual(result[4], date_add_to_db)
#         self.assertEqual(result[5], town_id)
#         self.assertEqual(result[6], type_id)
#         self.assertEqual(result[7], organism_id)
#         self.assertEqual(result[8], department_id)
#         self.assertEqual(result[9], date_id)

#     def test_add_date(self):
#         hour_start = "08:00 AM"
#         hour_end = "04:00 PM"
#         date = 1634606400

#         last_inserted_id = add_date(hour_start, hour_end, date)

#         self.assertIsNotNone(last_inserted_id)

#         self.cur.execute("SELECT * FROM dates WHERE id = %s", (last_inserted_id,))
#         result = self.cur.fetchone()
#         self.assertIsNotNone(result)
#         self.assertEqual(result[1], hour_start)
#         self.assertEqual(result[2], hour_end)
#         self.assertEqual(result[3], date)

#     def test_add_training(self):
#         name = "Test Training"
#         description = "A training description"

#         last_inserted_id = add_training(name, description)

#         self.assertIsNotNone(last_inserted_id)

#         self.cur.execute("SELECT * FROM training WHERE id = %s", (last_inserted_id,))
#         result = self.cur.fetchone()
#         self.assertIsNotNone(result)
#         self.assertEqual(result[1], name)
#         self.assertEqual(result[2], description)

#     def test_add_department(self):
#         number = "123"
#         name = "Test Department"

#         last_inserted_id = add_department(number, name)

#         self.assertIsNotNone(last_inserted_id)

#         self.cur.execute("SELECT * FROM department WHERE id = %s", (last_inserted_id,))
#         result = self.cur.fetchone()
#         self.assertIsNotNone(result)
#         self.assertEqual(result[1], number)
#         self.assertEqual(result[2], name)

#     def test_add_town(self):
#         name = "Test Town"

#         last_inserted_id = add_town(name)

#         self.assertIsNotNone(last_inserted_id)

#         self.cur.execute("SELECT * FROM town WHERE id = %s", (last_inserted_id,))
#         result = self.cur.fetchone()
#         self.assertIsNotNone(result)
#         self.assertEqual(result[1], name)

#     def test_add_organism(self):
#         name = "Test Organism"

#         last_inserted_id = add_organism(name)

#         self.assertIsNotNone(last_inserted_id)

#         self.cur.execute("SELECT * FROM organism WHERE id = %s", (last_inserted_id,))
#         result = self.cur.fetchone()
#         self.assertIsNotNone(result)
#         self.assertEqual(result[1], name)


# if __name__ == '__main__':
#     loader = unittest.TestLoader()
#     suite = loader.loadTestsFromTestCase(TestDatabaseFunctions)

#     # Define the order of tests
#     ordered_tests = [
#         "test_add_course",
#         "test_add_date",
#         "test_add_training",
#         "test_add_department",
#         "test_add_town",
#         "test_add_organism",
#     ]

#     test_instance = TestDatabaseFunctions()
#     ordered_suite = unittest.TestSuite()

#     for test_name in ordered_tests:
#         ordered_suite.addTest(test_instance.findTest(test_instance, test_name))

#     runner = unittest.TextTestRunner()
#     runner.run(ordered_suite)
