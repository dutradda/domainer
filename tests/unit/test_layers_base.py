import pytest
from domainer.exceptions import DomainerError
from domainer.layers.data.repositories import BaseRepository


def test_init_error():
    with pytest.raises(DomainerError):
        BaseRepository(None, None)
