from math import sqrt, cos, acos, degrees, radians, erf
import sys

def cosine_rule(a, b, C):
    """ Given two side lengths and the size of the angle not opposite to either side,
        calculate the angle opposite to the second side length by the cosine rule. """

    # apply cosine rule to calculate c, the length to the closest goalpost
    c = sqrt( a**2 + b**2 - 2*a*b*cos(C) )

    # apply cosine rule to calculate A, the angle subtended by half the goalmouth
    B = acos( (a**2 - b**2 + c**2) / (2*a*c) )

    return B

def difficulty(angle, distance):
    """ Given the angle from the midpoint of the goalmouth, calculate the
        angle of opportunity, theta. """
    
    if distance == 0:
        print "You cannot kick a goal from on the boundary line!"
        sys.exit()

    b = 3.2         # gap between goalposts
    a = distance
   
    # the side close to the goalpost 
    C1 = radians(90 - angle)
    B1 = cosine_rule(a, b, C1)
    
    # the side further from the goalpost 
    C2 = radians(90 + angle)
    B2 = cosine_rule(a, b, C2)
    
    return degrees(B1 + B2)

def cdf(x):
    """ Cumulative distribution function for the standard normal distribution. """
    return (1.0 + erf(x / sqrt(2.0))) / 2.0

def probability(difficulty, stdev):
    """ Calculate the probability of a successful set shot, assuming the
        angle of the kick is normally distributed about the centre of the
        goal (zero) with standard deviation stdev. """

    # standardise the random variable 
    x = difficulty/stdev

    # now return P( -x/2 < 0 < x/2 ), ie. the probability that the random variable
    # falls in an interval of width x centred on 0
    return cdf(x/2) - cdf(-x/2)

    # 68 degrees at 27 metres = 43%, according to channel 7

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: afl.py ANGLE DISTANCE [STDEV]\n"
        sys.exit()

    angle, distance = float(sys.argv[1]), float(sys.argv[2])
    print "Set shot taken from {} degree angle at a distance of {} metres.".format(angle, distance)
    if len(sys.argv) == 3: stdev = 5
    else: stdev = float(sys.argv[3])
    print "Player standard deviation: {} degrees".format(stdev)
    print "=========================="

    angle_of_opportunity = difficulty(angle, distance)
    print "Angle of opportunity: {:.1f} degrees".format(angle_of_opportunity)
    print "Probability of goal: {:.2f}%".format(probability(angle_of_opportunity, stdev)*100)
