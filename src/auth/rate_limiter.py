from src.redis_client import redis_client, try_command

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_TIME = 60  # 鎖定時間
ATTEMPT_RESET_TIME = 600  # 登入失敗重置時間


def check_lockout(username: str):
    lockout_key = f"lockout:{username}"
    result = try_command(redis_client.exists, lockout_key)
    return result


def reset_failed_attemps(username: str):
    failed_attempts_key = f"failed_attempts:{username}"
    try_command(redis_client.delete, failed_attempts_key)


def record_failed_attempt(username: str):
    failed_attempts_key = f"failed_attempts:{username}"
    lockout_key = f"lockout:{username}"

    lua_script = """
    local failed_attempts_key = KEYS[1]
    local lockout_key = KEYS[2]
    local ATTEMPT_RESET_TIME = ARGV[1]
    local MAX_FAILED_ATTEMPTS = ARGV[2]
    local LOCKOUT_TIME = ARGV[3]

    local attempts = redis.call('INCR', failed_attempts_key)
    redis.call('EXPIRE', failed_attempts_key, ATTEMPT_RESET_TIME)

    if tonumber(attempts) >= tonumber(MAX_FAILED_ATTEMPTS) then
        redis.call('SETEX', lockout_key, LOCKOUT_TIME, 'LOCKED')
    end
    return attempts
    """

    script = redis_client.register_script(lua_script)
    attemps = try_command(
        script,
        keys=[failed_attempts_key, lockout_key],
        args=[ATTEMPT_RESET_TIME, MAX_FAILED_ATTEMPTS, LOCKOUT_TIME],
    )
    return attemps
