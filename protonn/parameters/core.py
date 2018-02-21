"""Core functionality of protoNN."""

import ast
import collections.abc
import inspect
import logging
import textwrap
import typing as t

import static_typing as st
import typed_ast.ast3 as typed_ast3
import typed_astunparse

import protonn

_LOG = logging.getLogger(__name__)


def flatten_sequence(sequence: t.MutableSequence[t.Any]) -> None:
    """Transform a given list of lists into a flat list in-place."""
    assert isinstance(sequence, collections.abc.MutableSequence), type(sequence)
    for i, elem in enumerate(sequence):
        if isinstance(elem, collections.abc.MutableSequence):
            for value in reversed(elem):
                sequence.insert(i, value)
            del sequence[i + len(elem)]


def flatten_syntax(syntax: t.Union[ast.AST, t.MutableSequence[t.Any]]) -> None:
    """Flatten all lists of lists within the given syntax in-place."""
    if isinstance(syntax, (ast.Module, ast.FunctionDef, ast.ClassDef,
                           ast.For, ast.While, ast.If, ast.With,
                           ast.Try, ast.ExceptHandler,
                           ast.AsyncFunctionDef, ast.AsyncFor, ast.AsyncWith)):
        for node in syntax.body:
            flatten_syntax(node)
        flatten_sequence(syntax.body)
        return
    if isinstance(syntax, (ast.For, ast.While, ast.If, ast.Try,
                           ast.AsyncFor)):
        for node in syntax.orelse:
            flatten_syntax(node)
        flatten_sequence(syntax.orelse)
        return
    if isinstance(syntax, ast.Try):
        for node in syntax.handlers:
            flatten_syntax(node)
        # flatten_sequence(syntax.handlers)  # unnecessary
        for node in syntax.finalbody:
            flatten_syntax(node)
        flatten_sequence(syntax.finalbody)
        return
    if not isinstance(syntax, collections.abc.MutableSequence):
        return
    for node in syntax:
        flatten_syntax(node)
    flatten_sequence(syntax)


class Observed:

    """To be used in type hints."""

    pass


def _observe(alias, obj, attr):
    value = getattr(obj, attr)
    _LOG.debug('observing %s from %s -- value is %s', attr, obj, value)
    protonn.parameters._parameters[alias] = value


def view(scope):
    """Use this as a decorator for functions with observed values."""

    _LOG.debug("parameters.core.view got a scope to handle")

    # parse the srouruce and register all type-hinted vars

    frame_info = inspect.getouterframes(inspect.currentframe())[1]
    caller_frame = frame_info[0]
    globals_ = caller_frame.f_globals
    locals_ = caller_frame.f_locals

    code = inspect.getsource(scope)
    code = textwrap.dedent(code)
    syntax = typed_ast3.parse(code)
    function = syntax.body[0]
    # decorators = function.decorator_list
    function.decorator_list = []
    function = st.augment(function, locals_=locals_, globals_={**globals_, **globals()})

    # _LOG.warning('%s', function._local_vars)
    for var_name, var_types in function._local_vars.items():
        for var_type in var_types:
            if var_type is Observed or isinstance(var_type, Observed):
                raise NotImplementedError('local variables currently cannot be observed')

    instrumented_targets = {}

    # _LOG.warning('%s', function._nonlocal_assignments)
    for target, var_types in function._nonlocal_assignments.items():
        for var_type in var_types:
            if var_type is Observed or isinstance(var_type, Observed):
                assert isinstance(target, typed_ast3.Attribute), type(target)
                obj = typed_astunparse.unparse(target.value).strip()
                attr = target.attr
                _LOG.debug('assignment to %s of %s within %s will be instrumented',
                           attr, obj, function.name)
                obj_attr = typed_astunparse.unparse(target).strip()
                # instrumented_targetstarget)
                instrumented_targets[obj_attr] = (obj, attr)
                protonn.parameters._parameters[obj_attr] = None

    #return scope

    class Instrumenter(st.ast_manipulation.RecursiveAstTransformer[ast]):

        def visit_node(self, node):
            if not isinstance(node, ast.Assign) or len(node.targets) != 1 \
                    or not isinstance(node.targets[0], ast.Attribute):
                return node
            obj_attr = typed_astunparse.unparse(node.targets[0]).strip()
            if obj_attr not in instrumented_targets:
                # _LOG.warning('discarding candidate %s', obj_attr)
                return node
            obj, attr = instrumented_targets[obj_attr]
            instrumentation = ast.parse('protonn.parameters.core._observe({}, {}, {})'
                                        .format(repr(obj_attr), obj, repr(attr)), mode='eval')
            return [node, ast.Expr(instrumentation.body)]

    syntax = ast.parse(code)
    function = syntax.body[0]
    function.decorator_list = []
    function = Instrumenter(fields_first=True).visit(function)
    # transcriber = st.ast_manipulation.AstTranscriber[typed_ast3, ast]()
    # syntax = transcriber.visit(syntax)
    flatten_syntax(syntax)
    _LOG.debug('%s', typed_astunparse.dump(function))
    syntax = ast.fix_missing_locations(syntax)
    expression = compile(syntax, '<instrumented-function>', 'exec')
    empty_locals_ = {}
    eval(expression, globals_, empty_locals_)
    assert len(empty_locals_) == 1
    return next(iter(empty_locals_.values()))

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
