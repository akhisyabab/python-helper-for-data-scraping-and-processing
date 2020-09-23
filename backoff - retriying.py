# see more at https://pypi.org/project/backoff/

import backoff
import requests
import time

# Re-usable decorator with exponential wait.
backoff_retriying = backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
    ),
    max_tries=5,
)


@backoff_retriying
def get_url():
    print('Getting url test.....')
    time.sleep(5)
    raise requests.exceptions.ConnectionError


if __name__ == '__main__':
    get_url()