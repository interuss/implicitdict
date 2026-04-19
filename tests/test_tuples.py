from __future__ import annotations

import json
from datetime import datetime
from typing import Tuple, Optional, Self

import pytest

from implicitdict import ImplicitDict, StringBasedDateTime, StringBasedTimeDelta


class WithTuples(ImplicitDict):
    all_floats: tuple[float, float]
    big_tuple: Tuple[str, str]
    mixed_values: Optional[tuple[str, float]]
    nested_tuples: Optional[tuple[tuple[float, int], str]]
    nested_self: Optional[tuple[str, Self]]
    times: Optional[tuple[StringBasedDateTime, StringBasedTimeDelta]]
    lists: Optional[tuple[list[tuple[str, float]], str | None]]
    dicts: Optional[dict[int, tuple[str, dict[str, int]]]]
    long_tuple: Optional[tuple[bool, str, int, float, list[str], dict[str, str], tuple[int, int, int]]]

    @staticmethod
    def example_values() -> dict[str, WithTuples]:
        return {
            "fully_defined": WithTuples(
                all_floats=(1.23, 4.56),
                big_tuple=("foo", "bar"),
                mixed_values=("foo", 7),
                nested_tuples=((9.87, 3), "foo"),
                nested_self=("foo", WithTuples(all_floats=(0, 0), big_tuple=("", ""))),
                times=(StringBasedDateTime(datetime.now()), StringBasedTimeDelta("1h")),
                lists=([("foo", 10), ("bar", 100)], None),
                dicts={42: ("1", {"foo": 9}), 314: ("a", {"bar": 7})},
                long_tuple=(False, "foo", 8888, 1e7, [], {}, (1, 2, 3)),
            )
        }


def test_nominal():
    data = WithTuples.example_values()["fully_defined"]
    assert "all_floats" in data
    assert "big_tuple" in data
    assert "mixed_values" in data
    assert "nested_tuples" in data
    assert "nested_self" in data
    assert "times" in data
    assert "lists" in data
    assert "dicts" in data
    assert "long_tuple" in data
    s = json.dumps(data)
    assert "all_floats" in s
    assert "big_tuple" in s
    assert "mixed_values" in s
    assert "nested_tuples" in s
    assert "nested_self" in s
    assert "times" in s
    assert "lists" in s
    assert "dicts" in s
    assert "long_tuple" in s
    decoded = ImplicitDict.parse(json.loads(s), WithTuples)
    assert decoded == data
    assert decoded.times[0].datetime
    assert decoded.times[1].timedelta


def test_wrong_element_count():
    with pytest.raises(ValueError, match="3 values"):
        ImplicitDict.parse(json.loads('{"all_floats":[0,1,2],"big_tuple":["",""]}'), WithTuples)
