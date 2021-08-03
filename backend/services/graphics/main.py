from rest_framework.response import Response

from backend.services.graphics.graph1 import get_graph1
from backend.services.graphics.graph2 import get_graph2


def get_main(request):
    getParams = request.query_params
    response = Response()
    keys = getParams.keys()

    if 'graph2' in keys and 'emis' in keys:
        response.data = get_graph1(getParams)
        response.data.update(get_graph2(getParams))
        return response

    elif 'graph2' in keys:
        response.data = get_graph2(getParams)
        return response

    response.data = get_graph1(getParams)
    return response
