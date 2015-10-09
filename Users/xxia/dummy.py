import numpy

a = numpy.random.normal(2, 5, 100)
print a.shape
amean = numpy.nanmean(a)
print amean

b = numpy.ma.append(a,1000)
print b.size
print b.shape
print b.dtype