import math

c1 = 1.70158
c2 = c1 * 1.525
c3 = c1 + 1
c4 = (2 * math.pi) / 3
c5 = (2 * math.pi) / 4.5
n1 = 7.5625
d1 = 2.75


class EaseManager:
    @staticmethod
    def ease_func(easeType: str, t: float) -> float:
        if easeType == Ease.LINEAR:
            return t
        elif easeType == Ease.IN_SINE:
            return 1 - math.cos((t * math.pi) / 2)
        elif easeType == Ease.OUT_SINE:
            return math.sin((t * math.pi) / 2)
        elif easeType == Ease.IN_OUT_SINE:
            return 0.5 * (1 - math.cos((t * math.pi)) / 2)
        elif easeType == Ease.IN_QUAD:
            return t * t
        elif easeType == Ease.OUT_QUAD:
            return t * (2 - t)
        elif easeType == Ease.IN_OUT_QUAD:
            return 2 * t * t if t < 0.5 else 1 - math.pow(-2 * t + 2, 2) / 2
        elif easeType == Ease.IN_CUBIC:
            return t * t * t
        elif easeType == Ease.OUT_CUBIC:
            return (t - 1) * (t - 1) * (t - 1) + 1
        elif easeType == Ease.IN_OUT_CUBIC:
            return 4 * t * t * t if t < 0.5 else 1 - math.pow(-2 * t + 2, 3) / 2
        elif easeType == Ease.IN_QUART:
            return t * t * t * t
        elif easeType == Ease.OUT_QUART:
            return 1 - math.pow(1 - t, 4)
        elif easeType == Ease.IN_OUT_QUART:
            return 8 * t * t * t * t if t < 0.5 else 1 - math.pow(-2 * t + 2, 4) / 2
        elif easeType == Ease.IN_QUINT:
            return t * t * t * t * t
        elif easeType == Ease.OUT_QUINT:
            return 1 + math.pow(t - 1, 5)
        elif easeType == Ease.IN_OUT_QUINT:
            return (
                16 * t * t * t * t * t if t < 0.5 else 1 - math.pow(-2 * t + 2, 5) / 2
            )
        elif easeType == Ease.IN_EXPO:
            return 0 if t == 0 else math.pow(2, 10 * t - 10)
        elif easeType == Ease.OUT_EXPO:
            return 1 if t == 1 else 1 - math.pow(2, -10 * t)
        elif easeType == Ease.IN_OUT_EXPO:
            return (
                0
                if t == 0
                else (
                    1
                    if t == 1
                    else (
                        math.pow(2, 20 * t - 10) / 2
                        if t < 0.5
                        else (2 - math.pow(2, -20 * t + 10)) / 2
                    )
                )
            )
        elif easeType == Ease.IN_CIRC:
            return 1 - math.sqrt(1 - t * t)
        elif easeType == Ease.OUT_CIRC:
            return math.sqrt(1 - (t - 1) * (t - 1))
        elif easeType == Ease.IN_OUT_CIRC:
            return (
                1 - math.sqrt(1 - math.pow(2 * t, 2)) / 2
                if t < 0.5
                else (math.sqrt(1 - math.pow(-2 * t + 2, 2)) + 1) / 2
            )
        elif easeType == Ease.IN_BACK:
            return c3 * t * t * t - c1 * t * t
        elif easeType == Ease.OUT_BACK:
            return 1 + c3 * math.pow(t - 1, 3) + c1 * math.pow(t - 1, 2)
        elif easeType == Ease.IN_OUT_BACK:
            return (
                math.pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2) / 2
                if t < 0.5
                else (math.pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2
            )
        elif easeType == Ease.IN_ELASTIC:
            return (
                0
                if t == 0
                else (
                    1
                    if t == 1
                    else -math.pow(2, 10 * t - 10) * math.sin((t * 10 - 10.75) * c4)
                )
            )
        elif easeType == Ease.OUT_ELASTIC:
            return (
                0
                if t == 0
                else (
                    1
                    if t == 1
                    else math.pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1
                )
            )
        elif easeType == Ease.IN_OUT_ELASTIC:
            return (
                0
                if t == 0
                else (
                    1
                    if t == 1
                    else (
                        -math.pow(2, 10 * t - 10) * math.sin((20 * t - 11.125) * c5) / 2
                        if t < 0.5
                        else math.pow(2, -10 * t) * math.sin((20 * t - 11.125) * c5) / 2
                        + 1
                    )
                )
            )
        elif easeType == Ease.IN_BOUNCE:
            return 1 - EaseManager.ease_out_bounce(1 - t)
        elif easeType == Ease.OUT_BOUNCE:
            return EaseManager.ease_out_bounce(t)
        elif easeType == Ease.IN_OUT_BOUNCE:
            return (
                1 - EaseManager.ease_out_bounce(1 - 2 * t)
                if t < 0.5
                else (1 + EaseManager.ease_out_bounce(2 * t - 1)) / 2
            )
        else:
            return t

    def ease_out_bounce(t: float) -> float:
        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            return n1 * (t - 1.5 / d1) * t + 0.75
        elif t < 2.5 / d1:
            return n1 * (t - 2.25 / d1) * t + 0.9375
        else:
            return n1 * (t - 2.625 / d1) * t + 0.984375


class Ease:
    LINEAR = "linear"
    IN_SINE = "in_sine"
    OUT_SINE = "out_sine"
    IN_OUT_SINE = "in_out_sine"
    IN_QUAD = "in_quad"
    OUT_QUAD = "out_quad"
    IN_OUT_QUAD = "in_out_quad"
    IN_CUBIC = "in_cubic"
    OUT_CUBIC = "out_cubic"
    IN_OUT_CUBIC = "in_out_cubic"
    IN_QUART = "in_quart"
    OUT_QUART = "out_quart"
    IN_OUT_QUART = "in_out_quart"
    IN_QUINT = "in_quint"
    OUT_QUINT = "out_quint"
    IN_OUT_QUINT = "in_out_quint"
    IN_EXPO = "in_expo"
    OUT_EXPO = "out_expo"
    IN_OUT_EXPO = "in_out_expo"
    IN_CIRC = "in_circ"
    OUT_CIRC = "out_circ"
    IN_OUT_CIRC = "in_out_circ"
    IN_ELASTIC = "in_elastic"
    OUT_ELASTIC = "out_elastic"
    IN_OUT_ELASTIC = "in_out_elastic"
    IN_BACK = "in_back"
    OUT_BACK = "out_back"
    IN_OUT_BACK = "in_out_back"
    IN_BOUNCE = "in_bounce"
    OUT_BOUNCE = "out_bounce"
    IN_OUT_BOUNCE = "in_out_bounce"
