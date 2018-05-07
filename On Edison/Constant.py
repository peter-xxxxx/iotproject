class const(object):
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value

const.FREQUENCY  = 200       # Hz
const.AVGTIME    = 3         # number of sampling times over which we take average
const.CALTIMES   = 200       # number of sampling times for calibration
const.G          = 9.802     # Gravity acceleration value in New York City
const.SAMPLETIME = 1.0 / (const.FREQUENCY * const.AVGTIME)

GyrBias = [0, 0, 0]
