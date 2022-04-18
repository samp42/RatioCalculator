class Wheel:
    def __init__(self, name, diameter_in, friction_coeff):
        self.name = name
        self.diameterIn = diameter_in
        self.diameterM = diameter_in * 0.0254
        self.frictionCoeff = friction_coeff
