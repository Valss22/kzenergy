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
        totalPoll = [parse_number(i.EPWorker[facility]['totalEmis']) for i in archive]
        totalPoll.reverse()
        totalGrhs = [parse_number(i.EPWorker[facility]['totalGrhs']) for i in archive]
        totalGrhs.reverse()
        response['graph2'].update({
            'total1': totalPoll,
            'total2': totalGrhs
        })
    else:
        n: int = 1
        for f in ['compressor', 'powerplant', 'boiler']:
            energyArr = [parse_number(i.EPWorker[f]['energy']) for i in archive]
            energyArr.reverse()
            response['graph2'].update({
                'total' + str(n): energyArr
            })
            n += 1

    return response
