import ast
import functools
import shlex
from inspect import signature


class BoolParser(object):
    def __call__(self, token: str) -> bool:
        token = token.lower()

        valid_falses = ['0', 'false', 'f', 'off']
        valid_trues = ['1', 'true', 't', 'on']

        val = None

        if token in valid_trues:
            val = True
        elif token in valid_falses:
            val = False

        if val is None:
            raise ValueError(f'{token} is not a valid boolean value.')

        return val       
      
"""
Example usage:

@require_args(str, int, BoolParser())
def foo(some_str, some_int, some_bool):
  pass

"\tone two three" 4 false

"""

def require_args(*args):
    """ Require these arguments. They will be passed to the function as the types provided inside the kwarg 'parsed_args'. """
    
    # Id love to make these kwargs so they can be retrived by name,
    # but the Python specs don't reliably allow for that since
    # we can't rely on dictionaries to be in order (even in Python3)
    def require_arg(func):
        sig = signature(func)

        self_ref_count = 0
        if '.' in func.__qualname__:
            self_ref_count = 1

        needed_parameters = len(args) + 1 + self_ref_count # +1 to fit the original string
        actual_parameters = len(sig.parameters)
        if actual_parameters < needed_parameters:
            raise AttributeError(f'Decorated function {func} does not accept the correct about of parameters. Needed {needed_parameters}, actual {actual_parameters}')

        if self_ref_count:
            @functools.wraps(func)
            def wrapper(self, message):
                # Get the actual and required parameter counts
                # Hack to get input() to allow escape characters
                tokens = shlex.split(str(ast.literal_eval(shlex.quote(message))))
                # If the input is coming from code (ie. literal strings) use the following line instead
                # tokens = shlex.split(message)
                require_count = len(args) - self_ref_count

                # Send error message if counts dont match
                if len(tokens) < require_count:
                    print(f'Insufficient arguments to command. {require_count} needed.')
                    return

                # Parse only as many tokens as requested as requested type
                parsed_args = []
                for i, arg in enumerate(tokens):
                    try:
                        parsed_args.append(args[i](arg))
                    except Exception as e:
                        print(f'Error in parsing argument "*{arg}*" as a "*{args[i]}*". Error:\n{e}')
                        return
                
                func(self, message, *parsed_args)

            return wrapper
        else:
            @functools.wraps(func)
            def wrapper(message):
                # Get the actual and required parameter counts
                tokens = shlex.split(str(ast.literal_eval(shlex.quote(message))))
                # tokens = shlex.split(message)
                require_count = len(args)

                # Send error message if counts dont match
                if len(tokens) < require_count:
                    print(f'Insufficient arguments to command. {require_count} needed.')
                    return

                # Parse only as many tokens as requested as requested type
                parsed_args = []
                for i, arg in enumerate(tokens):
                    try:
                        parsed_args.append(args[i](arg))
                    except Exception as e:
                        print(f'Error in parsing argument "*{arg}*" as a "*{args[i]}*". Error:\n{e}')
                        return
                
                func(message, *parsed_args)

            return wrapper
    
    return require_arg

if __name__ == "__main__":

    class A:
        @require_args(int)
        def bar(self, ogs: str, i: int):
            print(f'Input: "{ogs}"')
            print('Parsed:', i)
    
    @require_args(str, int, BoolParser())
    def foo(original_str: str, some_str: str, some_int: int, some_bool: bool):
        print(f'Input: "{original_str}"')
        print('Parsed:', some_str, some_int, some_bool)

    a = A()
    foo(input('function-> '))
    a.bar(input('method-> '))
