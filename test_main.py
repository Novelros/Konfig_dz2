
import unittest
from unittest.mock import patch, MagicMock
from graphviz import Digraph
import main  # Предполагаем, что ваш файл называется show_commits.py

class TestScript(unittest.TestCase):

    @patch("subprocess.run")
    def test_get_commits(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(
            returncode=0,
            stdout="1350c6d0322875e2e58ad6a01bdeaa06ed0c19fe 2023-11-21 21:57:11 Rblba20 Delete ConsoleApplication4-pseudo-doom/thanksgiving-party-master directory\n8772da2ac070e8ed2e2f41259935096ccf981785 2023-11-23 11:47:45 Rblba20 fire and movement with mouse\n"
        )
        repo_path = "repo"
        expected = [
            ("1350c6d0322875e2e58ad6a01bdeaa06ed0c19fe",  "2023-11-21 21:57:11", "Rblba20","Delete ConsoleApplication4-pseudo-doom/thanksgiving-party-master directory"),
            ("8772da2ac070e8ed2e2f41259935096ccf981785", "2023-11-23 11:47:45","Rblba20", "fire and movement with mouse")
        ]
        commits = main.get_commits(repo_path)
       # self.assertEqual(commits, expected)

    def test_build_dependency_graph(self):
        commits = [
            ("1350c6d0322875e2e58ad6a01bdeaa06ed0c19fe","2023-11-21 21:57:11","Rblba20",  "Delete ConsoleApplication4-pseudo-doom/thanksgiving-party-master directory"),
            ("8772da2ac070e8ed2e2f41259935096ccf981785", "2023-11-23 11:47:45","Rblba20",  "fire and movement with mouse")
        ]
        graph = main.build_dependency_graph(commits)
        self.assertIn('0', graph.source)  # Проверяем, существует ли узел первого коммита
        self.assertIn('1', graph.source)  # Проверяем, существует ли узел второго коммита
        self.assertIn("->", graph.source)  # Убеждаемся, что грани присутствуют

    @patch("graphviz.Digraph.render")
    def test_save_graph(self, mock_render):
        graph = Digraph()
        main.save_graph(graph, "output")
        mock_render.assert_called_once_with("output", format="png")

if __name__ == "__main__":
    unittest.main()