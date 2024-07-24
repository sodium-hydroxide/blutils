"""Tools for serializing and deserializing objects to json"""
#region Frontmatter
import json
from typing import Any, Callable
from numpy import ndarray, array
from pandas import Series, DataFrame

#endregion

#region Mainmatter
def json_ndarray(to_jason: bool = True) -> (
        Callable[[ndarray], dict[str, Any]]
        | Callable[[dict[str, Any]], ndarray]
        ):
    """Serialize and deserialize numpy ndarray to json"""
    def serialize(obj: ndarray) -> dict[str, Any]:
        return {
            "values":obj.tolist(),
            "dtype": str(obj.dtype),
            "extended_json_type":"ndarray"
        }
    def deserialize(obj: dict[str, Any]) -> ndarray:
        out = array(obj["values"], dtype=obj["dtype"])
        return out
    if to_jason:
        return serialize
    return deserialize

def json_series(to_jason: bool = True) -> (
        Callable[[Series], dict[str, Any]]
        | Callable[[dict[str, Any]], Series]
        ):
    """Serialize and deserialize pandas series to json"""
    def serialize(obj: Series) -> dict[str, Any]:
        return {
            "values":obj.to_dict(),
            "extended_json_type":"series"
        }
    def deserialize(obj: dict[str, Any]) -> Series:
        out = Series(obj["values"])
        return out
    if to_jason:
        return serialize
    return deserialize

def json_dataframe(to_jason: bool = True)-> (
        Callable[[DataFrame], dict[str, Any]]
        | Callable[[dict[str, Any]], DataFrame]
        ):
    """Seriealize and deserialize pandas dataframe to json"""
    def serialize(obj: DataFrame) -> dict[str, Any]:
        return {
            "values":obj.to_dict(),
            "extended_json_type":"dataframe"
        }
    def deserialize(obj: dict[str, Any]) -> DataFrame:
        out = DataFrame(obj["values"])
        return out
    if to_jason:
        return serialize
    return deserialize

class JSONExtendedEncoder(json.JSONEncoder):
    """Extension to json encoder for complex data types"""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, ndarray): return json_ndarray()(obj) #type: ignore
        if isinstance(obj, DataFrame): return json_dataframe()(obj) #type: ignore
        if isinstance(obj, Series): return json_series()(obj)# type: ignore
        try: out = super().default(obj)
        except: raise NotImplementedError(
            f"Objects of type: {type(obj)} cannot be serialized by "
            "json or the extended version at this time."
        )
        else: return out

def json_dump(obj: Any) -> str:
    """Convert python object to json

    Extension to json.dumps for the following extended types:
    - numpy ndarray
    - pandas dataframe
    - pandas series

    Parameters
    ----------
    obj : Any
        Object that you wish to be serialized. Must be one of the base types or
        one of the extended types.

    Returns
    -------
    str
        JSON encoding for object.

    Raises
    ------
    NotImplementedError
        Object is not one of the base types that can be serialized by
        JSON, or it is not one of the extended types that can be serialized
        by JSON.
    """
    out = json.dumps(obj, cls=JSONExtendedEncoder)
    return out

def json_load(json_str: str) -> Any:
    """Convert json string to python object

    Extension to json.loads for the following extended types:
    - numpy ndarray
    - pandas dataframe
    - pandas series

    Parameters
    ----------
    json_str : str
        String containing json serialized object

    Returns
    -------
    Any
        Deserialized object. Must be one of the base types supported by json or
        one of the extended types

    Raises
    ------
    NotImplementedError
        Object is not one of the base types that can be serialized by
        JSON, or it is not one of the extended types that can be serialized
        by JSON.
    """
    obj = json.loads(json_str)
    if not isinstance(obj, dict): return obj
    if not "extended_json_type" in obj: return obj
    deserialization = {
        "ndarray": json_ndarray(to_jason=False),
        "series": json_series(to_jason=False),
        "dataframe": json_dataframe(to_jason=False)
    }
    json_type = obj["extended_json_type"]
    try: out = deserialization[json_type]
    except: raise NotImplementedError(
        f"Objects of type: {type(obj)} cannot be deserialized by "
        "json or the extended version at this time."
    )
    else: return out

#endregion

#region Backmatter
__all__=[
    json_dump.__name__,
    json_load.__name__
]
#endregion
