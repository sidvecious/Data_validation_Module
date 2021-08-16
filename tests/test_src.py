"""
Example pytest script:
you are looking for setup / teardown methods? py.test has fixtures:
    http://doc.pytest.org/en/latest/fixture.html
you find examples below
"""

import pytest


@pytest.yield_fixture
def one():
    print("setup")
    yield 1
    print("teardown")


def test_something(one):
    assert one == 1
