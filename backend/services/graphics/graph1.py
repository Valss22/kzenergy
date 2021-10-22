from rest_framework.response import Response

from backend.models import Archive
from backend.parsing import parse_number


def get_graph1(get_params) -> dict:
    period = get_params['period']
    emis = get_params['emis']

    pollutants = ['NO2', 'NO', 'SO2', 'CO']
    grhs = ['CO2', 'CH4', 'N2O']

    mass_of_emissions = {}

    def get_total_emis(facility: str) -> float:
        total = 0
        archive = Archive.objects.all()

        if not archive.exists():
            return 0

        if period == 'last':
            archive = [archive.last()]

        def add_total_emis(type_emis: str, elems: list[str]):
            nonlocal total
            fac_data = arch.__dict__['EPWorker'][facility]
            total += fac_data[type_emis]
            for el in elems:
                v = fac_data[el]
                if i == 0:
                    mass_of_emissions[el] = v
                else:
                    mass_of_emissions[el] += v

        i: int = 0
        for arch in archive:
            if emis == 'pollutants':
                add_total_emis('totalEmis', pollutants)
            elif emis == 'grhs':
                add_total_emis('totalGrhs', grhs)
            else:
                total += arch.__dict__['EPWorker'][facility]['energy']
            i += 1

        for key, value in mass_of_emissions.items():
            mass_of_emissions[key] = parse_number(
                round(value / len(archive), 2))

        avg = total / len(archive)
        return parse_number(round(avg, 2))

    response = Response()
    response.data = {'graph1': {}}

    order = {}

    for f in ['compressor', 'powerplant', 'boiler']:
        total = get_total_emis(f)
        response.data['graph1'][f] = {'total': total}
        if emis != 'energy':
            response.data['graph1'][f]. \
                update({'elems': [*mass_of_emissions.values()]})
        order[f] = total

    sorted_order = dict(sorted(order.items(), key=lambda x: x[1]))

    response.data['graph1'].update({'order': [*sorted_order]})

    return response.data
