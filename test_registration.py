"""Registration Planning Test Suite"""

import unittest
import sys
from registration import Graph


class TestGetRegistrationPlan(unittest.TestCase):
    """get_registration_plan Test Suite"""

    def check_registration_plan(self, graph, student_output):
        """
        Validate if the given registration plan is valid.
        """
        n = len(graph.adjacency_matrix)

        position = {}
        flattened_registration_plan = []
        for group in student_output:
            flattened_registration_plan.extend(group)
        for i, course in enumerate(flattened_registration_plan):
            position[course] = i

        # Stores information about which semester
        semesters = {}
        for i, semester in enumerate(student_output):
            if len(semester) > 4:
                self.fail(f"Length of semester {i} exceeded 4: {semester}")
            if len(semester) == 0:
                self.fail(f"Length of semester {i} should not be 0.")
            for course in semester:
                semesters[course] = i

        labels = [graph.vertices[i].label for i in range(n)]

        actual, expected = set(flattened_registration_plan), set(labels)
        if len(actual) != len(expected):
            self.fail(
                "Length of registration plan does not match expected result. "
                f"actual: {len(actual)}, expected: {len(expected)}"
            )

        if actual != expected:
            self.fail(
                "Registration plan courses do not match expected result. "
                f"actual: {sorted(actual)}, expected: {sorted(expected)}"
            )

        for u in range(n):
            for v in range(n):
                if graph.adjacency_matrix[u][v] == 1:  # Edge u -> v exists
                    if semesters[labels[u]] == semesters[labels[v]]:
                        self.fail(
                            f"Prerequisite course {labels[u]} cannot be "
                            f"taken in the same semester as {labels[v]}"
                        )
                    if (
                        position[labels[u]] > position[labels[v]]
                    ):  # u must appear before v
                        self.fail(
                            f"Prerequisite course {labels[u]} was not "
                            f"taken before course {labels[v]}"
                        )

    def test_get_registration_plan_1(self):
        """Test get_registration_plan with 3 vertices"""
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge(0, 1)  # A -> B
        graph.add_edge(1, 2)  # B -> C
        result = graph.get_registration_plan()
        self.check_registration_plan(graph, result)

    def test_get_registration_plan_2(self):
        """Test get_registration_plan with 3 vertices."""
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        result = graph.get_registration_plan()
        self.check_registration_plan(graph, result)

    def test_get_registration_plan_3(self):
        """Test get_registration_plan with 4 vertices."""
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_vertex("D")
        graph.add_edge(0, 1)  # A -> B
        graph.add_edge(0, 2)  # A -> C
        graph.add_edge(1, 3)  # B -> D
        graph.add_edge(2, 3)  # C -> D
        result = graph.get_registration_plan()
        self.check_registration_plan(graph, result)

    def test_get_registration_plan_4(self):
        """Test get_registration_plan with 4 vertices."""
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_vertex("D")
        graph.add_edge(0, 1)  # A -> B
        graph.add_edge(0, 2)  # A -> C
        graph.add_edge(0, 3)  # A -> D
        result = graph.get_registration_plan()
        self.check_registration_plan(graph, result)

    def test_get_registration_plan_5(self):
        """Test get_registration_plan with 4 vertices."""
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_vertex("D")
        graph.add_edge(0, 1)  # A -> B
        graph.add_edge(2, 3)  # C -> D
        result = graph.get_registration_plan()
        self.check_registration_plan(graph, result)

    def test_get_registration_plan_6(self):
        """Test get_registration_plan with 10 vertices."""
        graph = Graph()
        for i in range(10):
            graph.add_vertex(str(i))
        for i in range(9):
            graph.add_edge(i, i + 1)  # 0 -> 1 -> 2 -> ... -> 9
        result = graph.get_registration_plan()
        self.check_registration_plan(graph, result)


class TestHasCycle(unittest.TestCase):
    """has_cycle Test Suite"""

    def test_has_cycle_1(self):
        """Test has_cycle with 3 vertex and 2 edges, expecting a return of False."""
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge(0, 1)  # A -> B
        graph.add_edge(1, 2)  # B -> C
        self.assertFalse(graph.has_cycle())

    def test_has_cycle_2(self):
        """Test has_cycle with 2 vertex and 2 edges, expecting a return of True."""
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_edge(0, 1)  # A -> B
        graph.add_edge(1, 0)  # B -> A
        self.assertTrue(graph.has_cycle())

    def test_has_cycle_3(self):
        """Test has_cycle with 5 vertex and 5 edges, expecting a return of True."""
        graph = Graph()
        for i in range(5):
            graph.add_vertex(str(i))
        graph.add_edge(0, 1)  # 0 -> 1
        graph.add_edge(1, 2)  # 1 -> 2
        graph.add_edge(2, 3)  # 2 -> 3
        graph.add_edge(3, 4)  # 3 -> 4
        graph.add_edge(4, 0)  # 4 -> 0 (Cycle)
        self.assertTrue(graph.has_cycle())


def main():
    """Main function to run tests based on command-line arguments."""
    test_cases = {"registration": TestGetRegistrationPlan, "cycle": TestHasCycle}

    usage_string = (
        "Usage: python3 test_registration.py [test_method_or_function] [test_number]\n"
        "Examples:\n"
        "    python3 test_registration.py cycle 1\n"
        "    python3 test_registration.py cycle 3\n"
        "Valid options for [test_method_or_function]: "
        + ", ".join(test_cases.keys())
        + "\n"
        "Test cases range 1-6 for get_registration_plan(), and 1-3 for has_cycle()."
    )

    if len(sys.argv) > 3:
        print(usage_string)
        return
    if len(sys.argv) == 1:
        unittest.main()
        return
    sys.argv = sys.argv[1:]
    test_name = sys.argv[0]
    if test_name not in test_cases:
        print(
            f"Invalid test name: {test_name}. Valid options are: {', '.join(test_cases.keys())}"
        )
        return
    if len(sys.argv) == 1:
        # Extract test case based on the first command-line argument
        suite = unittest.TestLoader().loadTestsFromTestCase(test_cases[test_name])
    else:
        test_num = sys.argv[1]
        loader = unittest.TestLoader()

        # Load all tests from the test case class
        all_tests = loader.loadTestsFromTestCase(test_cases[test_name])
        suite = unittest.TestSuite()
        # Filter tests that end with 'test_num'
        for test in all_tests:
            if test.id().split(".")[-1].split("_")[-1] == test_num:
                suite.addTest(test)
        if not suite.countTestCases():
            print(usage_string)
            return
    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    main()
