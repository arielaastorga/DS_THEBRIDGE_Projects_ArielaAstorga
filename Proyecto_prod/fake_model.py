class FakeApartmentPriceModel:
    def __init__(self):
        self.neighbourhood_map = {
            "Sol": 1.35,
            "Universidad": 1.20,
            "Justicia": 1.25,
            "Salamanca": 1.50,
            "Centro": 1.30
        }
        self.room_type_map = {
            "Entire home/apt": 1.40,
            "Private room": 0.75,
            "Shared room": 0.50,
            "Hotel room": 1.60
        }
        self.base_price = 25

    def predict_one(self, neighbourhood, room_type, minimum_nights,
                    number_of_reviews, availability_365, number_of_reviews_ltm):
        n_factor = self.neighbourhood_map.get(neighbourhood, 1.00)
        r_factor = self.room_type_map.get(room_type, 1.00)

        price = (
            self.base_price
            + minimum_nights * 1.8
            + number_of_reviews * 0.15
            + availability_365 * 0.12
            + number_of_reviews_ltm * 0.8
        ) * n_factor * r_factor

        return round(price, 2)