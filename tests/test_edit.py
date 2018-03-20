import pytest
import pandas as pd
from pandangas import Network


def test_nodes_type_is_dataframe():
    n = Network()
    assert type(n.nodes) is pd.DataFrame


def test_pipes_type_is_dataframe():
    n = Network()
    assert type(n.pipes) is pd.DataFrame
