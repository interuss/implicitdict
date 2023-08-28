import json

from implicitdict import ImplicitDict

import pytest
from .test_types import MassiveNestingData


def _get_correct_value() -> MassiveNestingData:
    return json.loads(json.dumps(MassiveNestingData.example_value()))


def test_stacktrace():
    obj_dict = _get_correct_value()
    obj_dict["bar"] = "wrong kind of value"
    with pytest.raises(ValueError, match=r"^At bar:"):
        ImplicitDict.parse(obj_dict, MassiveNestingData)

    obj_dict = _get_correct_value()
    obj_dict["bar"] = []
    with pytest.raises(TypeError, match=r"^At bar:"):
        ImplicitDict.parse(obj_dict, MassiveNestingData)

    obj_dict = _get_correct_value()
    obj_dict["bar"] = {}
    with pytest.raises(TypeError, match=r"^At bar:"):
        ImplicitDict.parse(obj_dict, MassiveNestingData)

    obj_dict = _get_correct_value()
    obj_dict["children"] = "this gets treated as a list"
    with pytest.raises(ValueError, match=r"^At children\[0]:"):
        ImplicitDict.parse(obj_dict, MassiveNestingData)

    obj_dict = _get_correct_value()
    obj_dict["children"] = 0
    with pytest.raises(ValueError, match=r"^At children:"):
        ImplicitDict.parse(obj_dict, MassiveNestingData)

    obj_dict = _get_correct_value()
    obj_dict["children"][0]["bar"] = "wrong kind of value"
    with pytest.raises(ValueError, match=r"^At children\[0].bar:"):
        ImplicitDict.parse(obj_dict, MassiveNestingData)

    obj_dict = _get_correct_value()
    obj_dict["children"][1]["children"] = False
    with pytest.raises(ValueError, match=r"^At children\[1].children:"):
        ImplicitDict.parse(obj_dict, MassiveNestingData)

    obj_dict = _get_correct_value()
    obj_dict["children"][1]["children"][0]["children"][2]["children"] = 2
    with pytest.raises(ValueError, match=r"^At children\[1].children\[0].children\[2].children:"):
        ImplicitDict.parse(obj_dict, MassiveNestingData)
