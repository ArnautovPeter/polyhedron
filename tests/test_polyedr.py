import unittest
from unittest.mock import patch, mock_open
from shadow.polyedr import Polyedr


class TestPolyedr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        fake_file_content = """200.0	45.0	45.0	30.0
8	4	16
-0.5	-0.5	0.5
-0.5	0.5	0.5
0.5	0.5	0.5
0.5	-0.5	0.5
-0.5	-0.5	-0.5
-0.5	0.5	-0.5
0.5	0.5	-0.5
0.5	-0.5	-0.5
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5"""
        fake_file_path = 'data/holey_box.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

    def test_num_vertexes(self):
        self.assertEqual(len(self.polyedr.vertexes), 8)

    def test_num_facets(self):
        self.assertEqual(len(self.polyedr.facets), 4)

    def test_num_edges(self):
        self.assertEqual(len(self.polyedr.edges), 16)

    # У фигура с 1 гранью нет затененных, а значит и
    # удовлетворяющих условиям ребер нет
    def test_sum_porjecion_len_01(self):
        polyedr = Polyedr('data/square.geom')
        pl = polyedr.get_projection_len()
        self.assertEqual(pl, 0)

    # Одна грань полностью затеняется другой, но все ребра нижней
    # грани не удовлетворяют условиям
    def test_sum_projection_len_02(self):
        polyedr = Polyedr('data/two_squares1.geom')
        pl = polyedr.get_projection_len()
        self.assertAlmostEqual(pl, 0)

    # Одна грань полностью затеняется другой. Все ребра нижней грани
    # удовлетворяют условиям, длина всех нижних ребер равна 2
    def test_sum_projection_len_03(self):
        polyedr = Polyedr('data/two_squares2.geom')
        pl = polyedr.get_projection_len()
        self.assertAlmostEqual(pl, 8)

    # Одна грань полностью затеняется 2 ребра другой, но не полностью
    def test_sum_projection_len_04(self):
        polyedr = Polyedr('data/two_squares3.geom')
        pl = polyedr.get_projection_len()
        self.assertAlmostEqual(pl, 0)

    # Одна грань полностью затеняется другой. Два ребра нижней грани
    # удовлетворяют условиям, длина всех нижних ребер равна 2
    def test_sum_projection_len_05(self):
        polyedr = Polyedr('data/two_squares4.geom')
        pl = polyedr.get_projection_len()
        self.assertAlmostEqual(pl, 4)
