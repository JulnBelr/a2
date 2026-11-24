class PID:
    def __init__(self, kp, ki, kd, out_min=0.0, out_max=65535.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.out_min = out_min
        self.out_max = out_max
        self.integral = 0.0
        self.prev_error = 0.0
        self.first_run = True

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0
        self.first_run = True

    def update(self, setpoint, measurement, dt):
        if dt <= 0:
            return 0.0

        error = setpoint - measurement

        # Proportional
        p_term = self.kp * error

        # Derivative (skip kick on very first sample)
        if self.first_run:
            d_term = 0.0
            self.first_run = False
        else:
            d_term = self.kd * ((error - self.prev_error) / dt)

        # Integral with conditional clamping (anti-windup)
        candidate_integral = self.integral + error * dt
        i_term = self.ki * candidate_integral
        raw_out = p_term + i_term + d_term

        if self.out_min <= raw_out <= self.out_max:
            self.integral = candidate_integral
        else:
            i_term = self.ki * self.integral
            raw_out = p_term + i_term + d_term

        self.prev_error = error
        return max(self.out_min, min(self.out_max, raw_out))
