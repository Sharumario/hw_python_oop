from dataclasses import dataclass, astuple, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        """Вывод информационного сообщение о выполненной тренировке."""
        return self.MESSAGE.format(*astuple(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM = 1000
    M_IN_HOUR = 60
    LEN_STEP = 0.65

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
            str(type(self))[17:-2],
            self.duration, self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER = 18
    SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий (бег)."""
        return (
            (
                self.SPEED_MULTIPLIER
                * self.get_mean_speed()
                - self.SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.M_IN_HOUR)
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий (спортивная ходьба)."""
        return (
            (
                self.WEIGHT_MULTIPLIER_1
                * self.weight
                + (self.get_mean_speed() ** 2
                    // self.height
                   )
                * self.WEIGHT_MULTIPLIER_2
                * self.weight
            )
            * (self.M_IN_HOUR
               * self.duration
               )
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    SPEED_SHIFT = 1.1
    SPEED_MULTIPLIER = 2
    LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения (плавание)."""
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий (плавание)."""
        return (
            (
                self.get_mean_speed()
                + self.SPEED_SHIFT
            )
            * self.SPEED_MULTIPLIER
            * self.weight
        )


TRAININGS = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}
KEY_ERROR_MESSAGE = (
    'Получено не корректное имя класса: "{}". '
)
TYPE_ERROR_MESSAGE = (
    'Количество аргументов класса {} не корректно. '
    'Получено {} аргумента. Ожидалось {} аргумента.'
)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAININGS:
        raise ValueError(KEY_ERROR_MESSAGE.format(workout_type))
    if len(data) != len(fields(TRAININGS[workout_type])):
        raise (TypeError(
            TYPE_ERROR_MESSAGE.format(
                workout_type,
                len(data),
                len(fields(TRAININGS[workout_type]))))
               )
    return TRAININGS[workout_type](*data)


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
