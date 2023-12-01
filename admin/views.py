from django.shortcuts import render

# Create your views here.
def dashboard_screen_view(request):
	print(request.headers)
	return render(request, "dashboard.html", {})

def table_screen_view(request):
	print(request.headers)
	return render(request, "table.html", {})