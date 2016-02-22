from django.shortcuts import render, get_object_or_404
from table.models import Table

# Create your views here.
def table_list(request, id):
	context = {
		"table": get_object_or_404(Table, pk=id)
	}

	return render (request, 'table/table_list.html', context)