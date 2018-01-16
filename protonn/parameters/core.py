import protonn
import inspect
import ast


class _Tracker:
    """singleton class here to keep track of all parameters"""
    def __init__(self):
        self.params = []


def view(scope):
    """this function shold be used as a decorato"""

    print("test")
    return scope


def observe(x, stack_level=1):
    """register single variable for tracking"""

    # print('value', x)
    frame_info = inspect.getouterframes(inspect.currentframe())[stack_level]
    #  caller_path = frame_info[1]  # frame_info.filename
    caller_line = frame_info[2]  # lineno
    caller = frame_info[0]  # frame
    code = inspect.getsource(caller)
    print(code, caller_line)
    call_line = code.splitlines()[caller_line - 1].strip()
    syntax = ast.parse(call_line)
    var_name = None
    for node in ast.walk(syntax):
        if isinstance(node, ast.Call) and node.func.id == 'observe':
            var_name = node.args[0].id
    if var_name is None:
        raise ValueError(ast.dump(syntax))
    return var_name


def dump(path):
    print("dumping parameters:")
    d = protonn.parameters._parameters
    for param in d:
        print(param, d[param])
