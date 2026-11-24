from machine import ADC, Pin, PWM

class LightNode:
    def __init__(self, adc_pin=34, pwm_pin=25, dark=200, bright=3550):
        self.adc = ADC(Pin(adc_pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.pwm = PWM(Pin(pwm_pin), freq=1000)
        self.pwm.duty_u16(0)
        self.dark = dark
        self.bright = bright

    def read_raw(self, samples=10):
        total = 0
        for _ in range(samples):
            total += self.adc.read()
        return total / samples

    def read_pct(self):
        raw = self.read_raw()
        pct = (raw - self.dark) / (self.bright - self.dark) * 100.0
        return max(0.0, min(100.0, pct))

    def set_duty(self, duty):
        clamped = max(0, min(65535, int(duty)))
        self.pwm.duty_u16(clamped)
        return clamped
