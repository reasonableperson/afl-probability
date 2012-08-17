include Math

def cosine_rule(side_a, side_b, angle_C)
    # Given two side lengths and the size of the angle not opposite to either side,
    # calculate the angle opposite to the second side length by the cosine rule

    # apply cosine rule to calculate c, the length to the closest goalpost
    side_c = sqrt( side_a**2 + side_b**2 - 2*side_a*side_b*cos(angle_C) )
    # apply cosine rule to calculate A, the angle subtended by half the goalmouth
    angle_B = acos( (side_a**2 - side_b**2 + side_c**2) / (2*side_a*side_c) )

    return angle_B
end

def angle_of_opportunity(observed_angle, distance)
    # Given the angle from the midpoint of the goalmouth, calculate the
    # angle of opportunity, theta.
    
    raise "You cannot kick a goal from on the boundary line!" if distance == 0

    side_a, side_b = distance, 3.2 # 3.2 metres = distance between goalposts

    # methods to convert degrees <=> radians
    def radians(degrees) return degrees/180 * PI end
    def degrees(radians) return radians/PI * 180 end
   
    # the side close to the goalpost 
    angle_C1 = radians(90 - observed_angle)
    angle_B1 = cosine_rule(side_a, side_b, angle_C1)
    
    # the side further from the goalpost 
    angle_C2 = radians(90 + observed_angle)
    angle_B2 = cosine_rule(side_a, side_b, angle_C2)
    
    return degrees(angle_B1 + angle_B2)
end

def probability(observed_angle, distance, stdev)
    # Calculate the probability of a successful set shot, assuming the
    # angle of the kick is normally distributed about the centre of the
    # goal (zero) with standard deviation stdev.
    # Returned as a percentage.

    angle_of_opportunity = angle_of_opportunity(observed_angle, distance)

    # Cumulative distribution function for the standard normal distribution. """
    def cdf(x); return (1.0 + erf(x / sqrt(2.0))) / 2.0; end

    # standardise the random variable 
    x = angle_of_opportunity / stdev

    # now return P( -x/2 < 0 < x/2 ), ie. the probability that the random variable
    # falls in an interval of width x centred on 0
    return (cdf(x/2) - cdf(-x/2)) * 100
end

# handle arguments
if ARGV.length < 2; abort("Usage: afl.py ANGLE DISTANCE [STDEV]\n\n"); end
angle, distance, stdev = ARGV.map { |x| x.to_f }
unless stdev; stdev = 5.0; end

print "Set shot taken from #{angle} degree angle at a distance of #{distance} metres.\n"
print "Player standard deviation: #{stdev} degrees\n"
print "==========================\n"

print "Probability of goal: %.2f\%\n" % probability(angle, distance, stdev)
