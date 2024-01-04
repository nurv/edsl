import unittest
from contextlib import redirect_stdout
from io import StringIO
from edsl.results.Results import Results, create_example_results


class TestResults(unittest.TestCase):
    def setUp(self):
        self.example_results = create_example_results(debug=True)

    def test_instance(self):
        self.assertIsInstance(self.example_results, Results)

    # def test_original_data_preserved(self):
    #     original_data = self.example_results.original_data
    #     self.example_results.append({"test": "data"})
    #     self.assertNotEqual(
    #         self.example_results.original_data, self.example_results.data
    #     )
    # self.assertEqual(set(original_data), set(self.example_results.original_data))

    def test_restore(self):
        self.example_results.append({"test": "data"})
        self.example_results.restore()
        self.assertEqual(self.example_results.original_data, self.example_results.data)

    def test_to_dict(self):
        results_dict = self.example_results.to_dict()

        self.assertIsInstance(results_dict, dict)
        self.assertIn("data", results_dict)
        self.assertIn("survey", results_dict)
        self.assertIsInstance(results_dict["data"], list)
        self.assertIsInstance(results_dict["survey"], dict)

    def test_from_dict(self):
        results_dict = self.example_results.to_dict()
        results_obj = Results.from_dict(results_dict)

        self.assertIsInstance(results_obj, Results)
        self.assertEqual(print(self.example_results), print(results_obj))

    def test_question_names(self):
        self.assertIsInstance(self.example_results.question_names, list)
        self.assertEqual(
            self.example_results.question_names, ["how_feeling", "elapsed"]
        )

    def test_filter(self):
        self.assertEqual(
            self.example_results.filter("how_feeling == 'Great'").select("how_feeling"),
            self.example_results.select("how_feeling").filter("how_feeling == 'Great'"),
        )

    def test_select(self):
        # results = self.example_results.select('how_feeling').first()
        self.assertIn(
            self.example_results.select("how_feeling").first(),
            ["Great", "Good", "OK", "Bad"],
        )

    def test_select_scenario(self):
        # breakpoint()
        # print(self.example_results.select('period'))
        self.assertIn(
            self.example_results.select("period").first(), ["morning", "afternoon"]
        )

    def flatten(self):
        self.assertEqual(
            self.example_results.select("how_feeling").flatten(),
            ["Great", "Great", "Good", "OK", "Bad", "Bad"],
        )

    def print(self):
        with StringIO() as buf, redirect_stdout(buf):
            self.example_results.print()
            output = buf.getvalue()
        self.assertIn("Great", output)
        self.assertIn("Bad", output)


if __name__ == "__main__":
    unittest.main()