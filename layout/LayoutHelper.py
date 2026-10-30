#     Generated Using https://codebeautify.org/json-to-python-pojo-generator
# To use this code, make sure you
# Should be called popo instead as we are generating plain old python objects here
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = RecordLayouts_from_dict(json.loads(json_string))

from enum import Enum
from typing import List, Optional, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class AttributeType(Enum):
    DATE = "date"
    DATE1 = "date1"
    DATE2 = "date2"
    FLOAT = "float"
    FLOT = "flot"
    INT = "Int"
    LOC1 = "loc1"
    LOC2 = "loc2"
    LOC3 = "loc3"
    LOC4 = "loc4"
    STR = "Str"
    YYYYMMDD = "YYYYMMDD"


class Repeats(Enum):
    N = "N"
    Y = "Y"

class RecordLayout:
    name: str
    description: str
    record_key: str
    parent: str
    repeats: Repeats
    offsets: List[int]
    attributes: List[str]
    attribute_type: Optional[List[AttributeType]]
    primary_key: str
    foreign_key: str
    record_length: int
    root_key: str
    root: str
    attribute_t_ype: Optional[List[AttributeType]]

    def __init__(self, name: str, description: str, record_key: str, parent: str, repeats: Repeats, offsets: List[int], attributes: List[str], attribute_type: Optional[List[AttributeType]], primary_key: str, foreign_key: str, record_length: int, root_key: str, root: str, attribute_t_ype: Optional[List[AttributeType]]) -> None:
        self.name = name
        self.description = description
        self.record_key = record_key
        self.parent = parent
        self.repeats = repeats
        self.offsets = offsets
        self.attributes = attributes
        self.attribute_type = attribute_type
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.record_length = record_length
        self.root_key = root_key
        self.root = root
        self.attribute_t_ype = attribute_t_ype

    @staticmethod
    def from_dict(obj: Any) -> 'RecordLayout':
        assert isinstance(obj, dict)
        name = from_str(obj.get("Name"))
        description = from_str(obj.get("Description"))
        record_key = from_str(obj.get("RecordKey"))
        parent = from_str(obj.get("Parent"))
        repeats = Repeats(obj.get("Repeats;"))
        offsets = from_list(from_int, obj.get("Offsets"))
        attributes = from_list(from_str, obj.get("Attributes"))
        attribute_type = from_union([lambda x: from_list(AttributeType, x), from_none], obj.get("AttributeType"))
        primary_key = from_str(obj.get("Primary_Key"))
        foreign_key = from_str(obj.get("Foreign_Key"))
        record_length = from_int(obj.get("RecordLength"))
        root_key = from_str(obj.get("Root_Key"))
        root = from_str(obj.get("Root"))
        attribute_t_ype = from_union([lambda x: from_list(AttributeType, x), from_none], obj.get("AttributeTYpe"))
        return RecordLayout(name, description, record_key, parent, repeats, offsets, attributes, attribute_type, primary_key, foreign_key, record_length, root_key, root, attribute_t_ype)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Name"] = from_str(self.name)
        result["Description"] = from_str(self.description)
        result["RecordKey"] = from_str(self.record_key)
        result["Parent"] = from_str(self.parent)
        result["Repeats;"] = to_enum(Repeats, self.repeats)
        result["Offsets"] = from_list(from_int, self.offsets)
        result["Attributes"] = from_list(from_str, self.attributes)
        result["AttributeType"] = from_union([lambda x: from_list(lambda x: to_enum(AttributeType, x), x), from_none], self.attribute_type)
        result["Primary_Key"] = from_str(self.primary_key)
        result["Foreign_Key"] = from_str(self.foreign_key)
        result["RecordLength"] = from_int(self.record_length)
        result["Root_Key"] = from_str(RootKey, self.root_key)
        result["Root"] = from_str(Root, self.root)
        result["AttributeTYpe"] = from_union([lambda x: from_list(lambda x: to_enum(AttributeType, x), x), from_none], self.attribute_t_ype)
        return result


# The below class and methods have been renamed 
class RecordLayouts:
    name: str
    type: str
    schema: str
    root_record_key: str
    buffer_size:int
    record_layouts: List[RecordLayout]

    def __init__(self, name: str, schema:str, type: str, root_record_key: str, buffer_size:int,record_layouts: List[RecordLayout]) -> None:
        self.name = name
        self.type = type
        self.schema = schema
        self.root_record_key = root_record_key
        self.record_layouts = record_layouts
        self.buffer_size = buffer_size

    @staticmethod
    def from_dict(obj: Any) -> 'RecordLayouts':
        assert isinstance(obj, dict)
        name = from_str(obj.get("Name"))
        type = from_str(obj.get("Type"))
        schema = from_str(obj.get("Schema"))
        root_record_key = from_str(obj.get("RootRecordKey"))
        buffer_size = from_int(obj.get("BufferSize"))
        record_layouts = from_list(RecordLayout.from_dict, obj.get("RecordLayouts"))
        return RecordLayouts(name, schema,type, root_record_key,buffer_size, record_layouts)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Name"] = from_str(self.name)
        result["Schema"] = from_str(self.schema)
        result["Type"] = from_str(self.type)
        result["RootRecordKey"] = from_str(self.root_record_key)
        result["BufferSize"] = from_int(self.buffer_size)
        result["RecordLayouts"] = from_list(lambda x: to_class(RecordLayout, x), self.record_layouts)
        return result


def RecordLayouts_from_dict(s: Any) -> RecordLayouts:
    return RecordLayouts.from_dict(s)


def RecordLayouts_to_dict(x: RecordLayouts) -> Any:
    return to_class(RecordLayouts, x)