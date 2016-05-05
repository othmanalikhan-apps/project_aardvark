from django.http import HttpResponse
from .models import Table

import json


def sendTotalTables(request):
    """
    Retrieves all table numbers from the database the sends the results
    to the client in JSON format.

    :return: An HTTP response object containing the table numbers.
    """
    tableNumbers = []
    data = {"tables": tableNumbers}

    if request.method == "GET":
        for table in Table.objects.all():
            tableNumbers.append(table.number)

        data["tables"] = sorted(data["tables"])

    return HttpResponse(json.dumps(data), content_type="application/json")