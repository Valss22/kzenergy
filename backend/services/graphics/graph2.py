from backend.models import Archive
from backend.parsing import parse_number


def get_graph2(get_params) -> dict:
    facility = get_params['graph2']

    archive = Archive.objects.filter().order_by('-id')[:6]

    labels = [i.EPWorker['date'].split()[0] for i in archive]
    labels.reverse()
    response: dict = {
        'graph2': {
            'labels': labels,
        }
    }

    if facility != 'energy':
        total_poll = [parse_number(i.EPWorker[facility]['totalEmis']) for i in archive]
        total_poll.reverse()
        total_grhs = [parse_number(i.EPWorker[facility]['totalGrhs']) for i in archive]
        total_grhs.reverse()
        response['graph2'].update({
            'total1': total_poll,
            'total2': total_grhs
        })
    else:
        n: int = 1
        for f in ['compressor', 'powerplant', 'boiler']:
            energy_arr = [parse_number(i.EPWorker[f]['energy']) for i in archive]
            energy_arr.reverse()
            response['graph2'].update(
                {'total' + str(n): energy_arr}
            )
            n += 1

    return response
