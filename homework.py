from dataclasses import dataclass, fields
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    GET_MESSAGE: ClassVar = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        """Вывод информационного сообщение о выполненной тренировке."""
        return self.GET_MESSAGE.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar = 1000
    LEN_STEP: ClassVar = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration, self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    AVG_SPEED_MULTIPLICATOR: ClassVar = 18
    COEFFICIENT_CALLORIES: ClassVar = 20
    MINUTE_IN_HOUR: ClassVar = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий (бег)."""
        return (
            (self.AVG_SPEED_MULTIPLICATOR * self.get_mean_speed()
             - self.COEFFICIENT_CALLORIES)
            * self.weight / self.M_IN_KM
            * (self.duration * self.MINUTE_IN_HOUR)
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    COEFFICIENT_CALLORIES_1: ClassVar = 0.035
    COEFFICIENT_CALLORIES_2: ClassVar = 0.029
    MINUTE_AT_HOUR: ClassVar = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий (спортивная ходьба)."""
        return (
            (self.COEFFICIENT_CALLORIES_1 * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * self.COEFFICIENT_CALLORIES_2 * self.weight)
            * (self.MINUTE_AT_HOUR * self.duration)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP: ClassVar = 1.38
    COEFFICIENT_CALLORIES_1: ClassVar = 1.1
    COEFFICIENT_CALLORIES_2: ClassVar = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения (плавание)."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий (плавание)."""
        return (
            (self.get_mean_speed()
             + self.COEFFICIENT_CALLORIES_1)
            * self.COEFFICIENT_CALLORIES_2 * self.weight
        )


TRAININGS = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if len(data) == (len(fields(TRAININGS[workout_type]))):
        return (TRAININGS[workout_type])(*data)
    else:
        return 'Eror data'


def main(training: Training) -> None:
    """Главная функция."""
    print((training.show_training_info()).get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
