class Jupiter:
  def __init__(self, period, x_location, y_location, start_time):
    self.period=period
    self.x_location=x_location
    self.y_location=y_location
    self.start_time=start_time
  def orbit(self, timestep):
    #update attributes of the jupiter objects with new location after timestep