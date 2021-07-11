def validate_role(value: str) -> bool:
    role_choices = ['objWorker', 'chemWorker', 'miningWorker', 'EPWorker']
    if value not in role_choices:
        return False
    return True


def validate_gas_name(value: str) -> bool:
    gas_names = ['sweetGas']
    if value not in gas_names:
        return False
    return True
