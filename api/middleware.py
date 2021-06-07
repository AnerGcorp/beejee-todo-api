from django.http import HttpResponse, JsonResponse

class FilterMiddleware(object):

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)


	def process_view(self, request, view_func, view_args, view_kwargs):
		if request.method == "GET" and request.path == "/api/":
			developer_name = request.GET.get("developer" , None)
			if developer_name == None:
				return JsonResponse({'status': 'error', 'message' :'Не передано имя разработчика'})
		return None