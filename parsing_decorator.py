import functools
from inspect import signature

class DiceRollParser(object):
    def __call__(self, token: str) -> int:
        magic_goop = r"(\d+d\d+)"
        match = re.search(magic_goop, token)
        
        if not match:
            raise ValueError('DiceRolls should be formatted as [die amount]d[dice faces]')

        roll_split = match.groups()[0].split('d')

        die_amount = int(roll_split[0])
        dice_faces = int(roll_split[1])

        if die_amount > 20 or dice_faces > 100:
            raise ValueError('DiceRolls does not accept numbers that high')

        total = 0

        for _ in range(die_amount):
            total += random.randint(1, dice_faces)

        return total


class StatParser(object):
    def __call__(self, token: str) -> str:
        token = token.lower()

        if token not in player.valid_stat_names:
            raise ValueError(f'Stats should be one of: {player.valid_stat_names}')

        return token


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

@require_args(str, int, BoolParser()):
def foo(some_str, some_int, some_bool):
  pass

"""
      
def require_args(*args):
    """ Require these arguments. They will be passed to the function as the types provided inside the kwarg 'parsed_args'. """
    
    # Id love to make these kwargs so they can be retrived by name,
    # but the Python specs don't reliably allow for that since
    # we can't rely on dictionaries to be in order (even in Python3)
    def require_arg(func):
        sig = signature(func)
        needed_parameters = len(args) + 2  # Magic number. Anticipates base command trigger word?
        actual_parameters = len(sig.parameters)
        if actual_parameters < needed_parameters:
            raise AttributeError(f'Decorated function {func} does not accept the correct about of parameters. Needed {needed_parameters}, actual {actual_parameters}')

        @functools.wraps(func)
        def wrapper(self, message):
            # Get the actual and required parameter counts
            tokens = message.content.split()
            require_count = len(args)

            # Send error message if counts dont match
            if len(tokens) - 1 < require_count:
                print(f'Insufficient arguments to command. {require_count} needed.')
                return

            # Parse only as many tokens as requested as requested type
            parsed_args = []
            for i, arg in enumerate(tokens[1:needed_parameters-1]):
                try:
                    parsed_args.append(args[i](arg))
                except Exception as e:
                    print(f'Error in parsing argument "*{arg}*" as a "*{args[i]}*". Error:\n{e}')
                    return
            
            func(self, message, *parsed_args)

        return wrapper
    
    return require_arg
