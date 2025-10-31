import pytest
from confidant.sorter import Sorter


@pytest.fixture
def sorter():
    return Sorter()


def test_contains_standup_phrase(sorter):
    assert sorter._contains_standup_phrase("this is a standup bit")
    assert sorter._contains_standup_phrase("this is a stand-up bit")
    assert sorter._contains_standup_phrase("this is a stand up bit")
    assert not sorter._contains_standup_phrase("this is a normal sentence")
    assert sorter._contains_standup_phrase("standup is the first word")
    assert sorter._contains_standup_phrase("first few words contain standup")
    assert not sorter._contains_standup_phrase(
        "this sentence is longer than twelve words and the keyword doesn't appear until later. standup"
    )
