import time

class TurtleHare:
    def __init__(self, *args, **kwargs):
        self.function = kwargs.get('function')

    def measure(self, function, *args):
        print('\nMeasuring execution time with TurtleHare ...')
        print('Print statements of executed function below:')
        print('--------------------------------------------\n')
        start = time.time()
        self.function(*args)
        end = time.time()
        print('\n---------------------------------------------')
        print('End of print statements of executed function.')
        print('Final execution measurement:')
        print(f'    In seconds: {end - start}')

    class static:
        @staticmethod
        def measure(function, *args):
            print('\nMeasuring execution time with TurtleHare ...')
            print('Print statements of executed function below:')
            print('--------------------------------------------\n')
            start = time.time()
            function(*args)
            end = time.time()
            print('\n---------------------------------------------')
            print('End of print statements of executed function.')
            print('Final execution measurement:')
            print(f'    In seconds: {end - start}')
