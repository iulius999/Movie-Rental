from src.validators.exceptions import UndoException


class Function:

    def __init__(self, name, *params):
        self._name = name
        self._params = params

    def call(self):
        self._name(*self._params)


class Operation:    # Undo/Redo

    def __init__(self, functions: list):
        self._functions = functions

    def undo(self):
        for function in self._functions:
            function.call()

    def redo(self):
        for function in self._functions:
            function.call()


class UndoService:

    def __init__(self):
        self._stack = []

        # When I call the functions from the undo stack, I must NOT push further operations on the stack
        # Therefore, I need a flag. True - push operation on the stack. False - do not push.
        self._flag = True

    def _is_empty(self):
        if len(self._stack) == 0:
            return True
        return False

    def push(self, operation: Operation):
        if self._flag is False:
            return
        self._stack.append(operation)

    def undo(self):  # pop
        if self._is_empty():
            raise UndoException('Nothing to be undone!')

        operation = self._stack.pop()

        self._flag = False
        operation.undo()
        self._flag = True
