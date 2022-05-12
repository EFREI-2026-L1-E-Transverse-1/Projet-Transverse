import math

radius = 160

def conversionRadian(theta):
    return theta * math.pi / 180

def conversionDegree(theta):
    return theta * 180 / math.pi

def recupPente(p1, p2):
    if p1[0] == p2[0]:
        m = conversionRadian(90)
    else:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    return m

def recupAngleDePente(gradient):
    return math.atan(gradient)

def recupAngle(pos, origin):
    m = recupPente(pos, origin)
    thetaRad = recupAngleDePente(m)
    theta = round(conversionDegree(thetaRad), 2)
    return theta

def recupPosCirconf(theta, origin):
    theta = conversionRadian(theta)
    x = origin[0] + radius * math.cos(theta)
    y = origin[1] + radius * math.sin(theta)
    return (x, y)
