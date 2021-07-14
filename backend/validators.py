

def validate_role(value: str) -> bool:
    role_choices = ['objWorker', 'chemWorker', 'miningWorker', 'EPWorker']
    if value not in role_choices:
        return False
    return True


