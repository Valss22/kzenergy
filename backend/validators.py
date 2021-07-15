

def validate_role(value: str) -> bool:
    role_choices = ['compressor', 'powerplant', 'boiler',
                    'chemical', 'mining', 'EPWorker']
    if value not in role_choices:
        return False
    return True


