import csv
import os

valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]

 
class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        try:
            self.carrying = float(carrying)
        except ValueError:
            self.carrying = 0.0

    def __repr__(self):
        return str(self.get_photo_file_ext())

    def get_photo_file_ext(self):
        _, ext = os.path.splitext(self.photo_file_name)
        return ext

    @classmethod
    def is_valid(cls, brand, passenger_seats_count, photo_file_name, _, carrying, extra):
        if type(brand) != str or not len(brand):
            return False
        file_name, ext = os.path.splitext(photo_file_name)
        if ext not in valid_extensions or not file_name:
            return False
        try:
            if float(carrying) <= 0.0:
                return False
        except ValueError:
            return False
        if cls == Car:
            try:
                passengers = int(passenger_seats_count)
                if passengers <= 0:
                    return False
            except ValueError:
                return False
        elif cls == SpecMachine:
            if not len(extra) or not len(brand):
                return False

        return True


class Car(CarBase):
    def __init__(self,  brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "car"
        try:
            self.passenger_seats_count = int(passenger_seats_count)
        except ValueError:
            self.passenger_seats_count = 0

    @classmethod
    def args_for_init(cls, brand, passengers, photo, carrying):
        return [brand, photo, carrying, passengers]


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "truck"
        self.body_height = 0.0
        self.body_length = 0.0
        self.body_width = 0.0

        flag = False
        dimensions = body_whl.split("x")
        if len(dimensions) == 3:
            for i, v in enumerate(["length", "width", "height"]):
                try:
                    if float(dimensions[i]) <= 0.0:
                        flag = True
                    else:
                        self.__dict__[f"body_{v}"] = float(dimensions[i])
                except (ValueError, IndexError):
                    flag = True
        if flag:
            self.body_height = 0.0
            self.body_length = 0.0
            self.body_width = 0.0

    def __str__(self):
        return f"{self.car_type} {self.brand} {self.photo_file_name}" \
               f"{self.body_length}*{self.body_width}*{self.body_height} {self.carrying}"
    
    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width

    @classmethod
    def args_for_init(cls, brand, photo, whl, carrying):
        return [brand, photo, carrying, whl]


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "spec_machine"
        self.extra = extra
        pass

    @classmethod
    def args_for_init(cls, brand, photo, carrying, extra):
        return [brand, photo, carrying, extra]


cars_map = {
    "car": Car,
    "truck": Truck,
    "spec_machine": SpecMachine
}

args_map = {
    "car": [1, 2, 3, 5],
    "truck": [1, 3, 4, 5],
    "spec_machine": [1, 3, 5, 6]
}


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=",")
        next(reader)  # пропускаем заголовок
        for row in reader:
            try:
                elements = row[0].split(";")
                args = []
                for i, v in enumerate(elements):
                    if i in args_map[elements[0]]:
                        args.append(v)
                
                car_type = elements[0]
                car_func = cars_map[car_type]
                
                if car_func.is_valid(*elements[1::]):
                    car_list.append(car_func(*car_func.args_for_init(*args)))
            except (IndexError, KeyError):
                pass
    return car_list


if __name__ == "__main__":
    print(get_car_list("/home/igor/Projects/hello/cars.csv"))
