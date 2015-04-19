import re

class ValueLib(object):
    def _increment(self, start=0):
        val = start
        while True:
            val += 1
            yield val

    def incrementer(self, start=0):
        self.inc = self._increment(start)
        return self.inc.next()

    @staticmethod
    def repeat_string(char, size):
        return char*size

    def random_string(self, size):
        pass

    def count(self, num):
        for i in xrange(num):
            yield i

    def run_function(self, func_str):
        match = re.match("([\w_]+)\((|[\W\d\w\,]+)\)", func_str)
        if match == None:
            print "Couldn't match a regex!"
            return False
        else:
            func, argstr = match.groups()

        try:
            if argstr == "":
               return self.__getattribute__(func)()
            else:
                # evaluate the arg string to create code passable to the
                # funciton
                args = eval(argstr)

                # if multiple args are passed in eval returns a tuple,
                # which needs to be expanded using the * syntax
                if isinstance(args, tuple):
                    return self.__getattribute__(func)(*args)
                else:
                    return self.__getattribute__(func)(args)

        except AttributeError:
            print "Invalid function call: %s" % (func)
            return False

vlib = ValueLib()

