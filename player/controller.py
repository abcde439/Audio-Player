class PlayerController:
  def __init__(self):
    self.running = True
    self.paused = False

  def pause(self):
    self.paused = True

  def resume(self):
    self.paused = False

  def stop(self):
    self.running = False
