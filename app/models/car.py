from pydantic import BaseModel


class Car(BaseModel):
    id: int

    make: str
    model: str
    display_name: str

    segment: str

    price_lakh: float

    fuel_type: str
    transmission: str

    seating: int

    safety: int          # 1-5
    comfort: int         # 1-10
    mileage: int         # 1-10
    features: int        # 1-10
    performance: int     # 1-10
    reliability: int     # 1-10