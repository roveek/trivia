from typing import Optional, Tuple, Union

Number = Union[int, float]


class RequestTimeout:
    """
    Хранит и возвращает таймауты для использования в библиотеке requests.
    https://2.python-requests.org/en/master/user/advanced/#timeouts
    """

    def __init__(self,
                 read: Union[Number, Tuple[Number, Number]] = None,
                 connect: Number = None,
                 *, coefficient: Number = None):
        """Инициализация класса.

        :param read: Общее время выполнения запроса, включая получение данных.
        :param connect: Время подключения к серверу.
        :param coefficient: Коэффициент (множитель) применяемый к read и connect таймаутам.
        """
        if isinstance(read, tuple) and len(read) == 2:
            connect, read = read

        assert read is None or isinstance(read, (int, float))
        assert connect is None or isinstance(connect, (int, float))
        assert coefficient is None or isinstance(coefficient, (int, float))

        self._read: Optional[Number] = read
        try:
            if connect > read:
                connect = read
        except (TypeError, ValueError):
            pass
        self._connect: Optional[Number] = connect
        self._coefficient = coefficient

    def __str__(self) -> str:
        return f'{self.read}'

    def __repr__(self):
        return f'{self.__class__.__name__}(read={self._read}, ' \
            f'connect={self._connect}, coefficient={self._coefficient})'

    @property
    def read(self) -> Optional[Number]:
        if self._read is None:
            return None
        return self._read * (self._coefficient or 1)

    @property
    def connect(self) -> Optional[Number]:
        if self._connect is None:
            return None
        return self._connect * (self._coefficient or 1)

    @property
    def tuple(self) -> Tuple[Number, Number]:
        """Возвращает таймауты в форме tuple(connect_timeout, read_timeout)."""
        return self.connect, self.read

    @property
    def timeout(self) -> Union[None, int, float, Tuple[Number, Number]]:
        if self.read and self.connect:
            return self.tuple
        else:
            return self.read

    def coefficient(self, coeff: Number) -> 'RequestTimeout':
        """Возвращает экземпляр класса с установленным коэффициентом."""
        return self.__class__(read=self._read, connect=self._connect, coefficient=coeff)

    def copy(self, *,
             read: Union[Number, Tuple[Number, Number]] = None,
             connect: Number = None,
             coefficient: Number = None
             ) -> 'RequestTimeout':
        """Создаёт копию объекта с возможностью заменить любое из хранимых значений."""
        return self.__class__(read=self._read if read is None else read,
                              connect=self._connect if connect is None else connect,
                              coefficient=self._coefficient if coefficient is None else coefficient)


if __name__ == '__main__':

    t = RequestTimeout(5)
    print('1:', f'{t!r}', '=', t.timeout)

    tt = t.coefficient(.7)
    print('2:', f'{tt!r}', '=', tt.timeout)
