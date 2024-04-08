from airport.models import (
    Country,
    City,
    Airport,
    AirplaneType,
    Airplane,
    Crew, Route, Flight
)


def sample_city(**params):
    country = Country.objects.create(name="South Africa")
    default = {
        "name": "Capetown",
        "country": country
    }
    default.update(params)
    return City.objects.create(**default)


def sample_airport(**params):
    default = {
        "name": "Airport",
        "closest_big_city": sample_city()
    }
    default.update(params)
    return Airport.objects.create(**default)


def sample_airplane(**params):
    plane_type = AirplaneType.objects.create(name="Jumbo Jet")
    default = {
        "name": "Boeing",
        "rows": 50,
        "seats_in_row": 6,
        "type": plane_type
    }
    default.update(params)
    return Airplane.objects.create(**default)


def sample_crew(**params):
    default = {
        "first_name": "Boris",
        "last_name": "Barbaris",
    }
    default.update(params)
    return Crew.objects.create(**default)


def sample_route(**params):
    source = sample_airport()
    destination = sample_airport(name="Port")
    default = {
        "source": source,
        "destination": destination,
        "distance": 100
    }
    default.update(params)
    return Route.objects.create(**default)


def sample_main_flight(**params):
    default = {
        "route": sample_route(),
        "airplane": sample_airplane(),
        "departure_time": "2024-03-20 14:00:00",
        "arrival_time": "2024-03-20 15:00:00",
    }
    default.update(params)

    flight = Flight.objects.create(**default)
    flight.crew.add(sample_crew())

    return flight


def sample_secondary_flight(**params):
    source = sample_airport(name="Bulba")
    destination = sample_airport(name="Cartoplya")
    route = sample_route(source=source, destination=destination)
    default = {
        "route": route,
        "airplane": sample_airplane(name="Airbus"),
        "departure_time": "2024-03-20 14:00:00",
        "arrival_time": "2024-03-20 15:00:00",
    }
    default.update(params)

    flight = Flight.objects.create(**default)
    flight.crew.add(sample_crew())

    return flight
