import re
import os.path
import csv


def camel_to_snake(string):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower() 

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)
        self.car_type = camel_to_snake(self.__class__.__name__)


    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_lwh):
        super().__init__(brand, photo_file_name, carrying)

        body_lwh = to_valid_lwh(body_lwh)
        self.body_length = body_lwh[0]
        self.body_width = body_lwh[1]
        self.body_height = body_lwh[2]


    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def is_valid_format(filename):
    formats = ['.png', '.jpg', '.jpeg', '.gif']
    for format in formats:
        if format == os.path.splitext(filename)[1] and os.path.splitext(filename)[0]:
            return True
    return False

def is_digit(carrying):
    try:
        float(carrying)
        return True
    except ValueError:
        return False

def is_valid_class(car_type):
    car_types = ['car', 'spec_machine', 'truck']
    for type in car_types:
        if car_type == type:
            return True
    return False

def to_valid_lwh(body_lwh):
    try:
        body_lwh = body_lwh.split('x')
        if len(body_lwh) == 3:
            for i in range(3):
                is_digit(body_lwh[i])
                body_lwh[i] = float(body_lwh[i])
        else:
            raise ValueError
    except ValueError:
        body_lwh = [0.0, 0.0, 0.0]
    return body_lwh

def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename, encoding='utf-8') as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        for row in reader:
            if len(row) == 7:
                if row[0] and row[1] and row[3] and row[5]:
                    if is_valid_format(row[3]) and is_digit(row[5]):
                        if row[0] == 'car':
                            if row[2].isdigit() and not row[4] and not row[6]:
                                car_list.append(Car(row[1], row[3],  row[5], row[2]))
                            else:
                                pass
                        elif row[0] == 'truck':
                            if not row[2] and not row[6]:
                                car_list.append(Truck(row[1], row[3],  row[5], row[4]))
                            else:
                                pass
                        elif row[0] == 'spec_machine':
                            if row[6] and not row[2] and not row[4]:
                                car_list.append(SpecMachine(row[1], row[3],  row[5], row[6]))
                            else:
                                pass
                        else:
                            pass
                pass
            else:
                pass

    return car_list
