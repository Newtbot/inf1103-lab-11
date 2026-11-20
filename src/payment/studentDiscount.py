from .percentageDiscount import PercentageDiscount


class StudentDiscount(PercentageDiscount):
    """Applies a fixed 20% student discount."""

    def __init__(self) -> None:
        super().__init__(20)
