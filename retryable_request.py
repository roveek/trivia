from typing import Optional, Union

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def retryable_request(retries: Optional[Union[int, Retry]] = 1, *,
                      session: Session = None,
                      backoff_factor: float = None) -> Session:
    """Возвращает объект Session, который способен повторять запрос указанное число раз.

    :param retries: Количество повторов.
    :param session: Объект сессии.
    :param backoff_factor: Увеличивающаяся задержка между повторами.
    """
    assert retries is None or isinstance(retries, (int, Retry))

    retries = 1 if retries is None else retries
    backoff_factor = 0 if backoff_factor is None else backoff_factor
    session = Session() if session is None else session

    if isinstance(retries, int):
        retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor)
    else:
        retry = retries
    adapter = HTTPAdapter(max_retries=retry)

    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session
