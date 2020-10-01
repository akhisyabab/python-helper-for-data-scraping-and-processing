import backoff


# Re-usable decorator with exponential wait.
backoff_retriying = backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(
       ConnectionError
    ),
    max_tries=3,
)


def sampel_func():
    raise ConnectionError