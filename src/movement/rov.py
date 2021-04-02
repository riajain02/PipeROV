from motor import Motor

class ROV:
    def __init__(self):
        left_front = Motor()
        right_front = Motor()
        left_back = Motor()
        right_back = Motor()
    
    def drive_fwd(self, speed):
        left_front.change_speed(speed)
        right_front.change_speed(speed)
        left_back.change_speed(speed)
        right_back.change_speed(speed)
    
    def drive_rev(self, speed):
        left_front.change_speed(speed)
        right_front.change_speed(speed)
        left_back.change_speed(speed)
        right_back.change_speed(speed)