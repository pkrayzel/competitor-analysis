from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class ProductInformation:
    """
    Class with detail information about product
    """
    price: float = 0.0      # EUR only for now
    title: str = ""

    # dimensions
    width: float = 0.0          # cm
    height: float = 0.0         # cm
    depth: float = 0.0          # cm
    diameter: float = 0.0          # cm
    seat_height: float = 0.0    # cm

    # other
    material: str = ""
    color: str = ""

