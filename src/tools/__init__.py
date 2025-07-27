import pkgutil
import importlib
import inspect
from tools.base_tool import BaseTool

def get_all_tools():
    tool_dict = {}
    for loader, module_name, _ in pkgutil.iter_modules(__path__):
        if module_name == "base_tool":
            continue
        module = importlib.import_module(f"{__name__}.{module_name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseTool) and obj is not BaseTool:
                instance = obj()
                tool_dict[instance.name] = instance
    return tool_dict