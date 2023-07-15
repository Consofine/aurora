from datetime import datetime
from constants import MIN_STRENGTH_THRESHOLD, RESET_TIME_HOURS


class MaxKeeper:
    max_strength = 0.0
    max_set_at = None

    def should_update_strength(self, strength: float):
        return strength > MIN_STRENGTH_THRESHOLD and strength > self.max_strength + 30

    def update_strength(self, strength: float):
        self.max_strength = strength
        self.max_set_at = datetime.now()

    def check_should_clear_max(self):
        if not self.max_set_at:
            return False
        diff = datetime.now() - self.max_set_at
        timespan_in_seconds = 60 * 60 * RESET_TIME_HOURS
        return diff.total_seconds() > timespan_in_seconds

    def maybe_clear_max_strength(self):
        if self.max_set_at and self.check_should_clear_max():
            self.max_set_at = None
            self.max_strength = 0.0
