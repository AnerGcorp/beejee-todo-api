from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Task, User
from datetime import timedelta, datetime
import re, tokenlib, time

def index(request):	
	if request.method == 'GET':
		fields = ["username", "status", "email", "text"]
		directions = ['asc' , 'desc']
		
		# params
		sort_field = request.GET.get("sort_field" , "username").lower()
		sort_direction = request.GET.get("sort_direction" , "desc").lower()
		page = request.GET.get("page" , 1)

		try:
			page = int(page)
			if page <= 0:
				page = 1
		except Exception as e:
			page = 1


		# check sort field
		if sort_field not in fields:
			return JsonResponse({'status': 'error' , 'message': 'Некорректное значение для сортировки'}, status=400)

		# check sort direction
		if sort_direction not in directions:
			return JsonResponse({'status': 'error' , 'message': 'Некорректное значение для направление сортировки'}, status=400)

		# fetch total count 
		total_count = Task.objects.all().count()
		result = {'status': "ok", 'tasks' : [] , 'total_task_count' : total_count, 'page': page, 'sort_field': sort_field , 'sort_direction' : sort_direction}


		# fetch tasks
		limit = 3
		offset = (page - 1) * 3

		tasks = Task.objects.order_by(sort_field)[offset: offset + limit]
		# sorting
		if sort_field == 'desc':
			tasks = tasks.reverse()

		for task in tasks:
			result['tasks'].append(task.to_dict())

		return JsonResponse(result)
	else:
		return HttpResponse("Not Allowed" , status=405)

@csrf_exempt
def task_create(request):
	if request.method == "POST":
		username = request.POST.get('username' , None)
		email = request.POST.get('email' , None)
		text = request.POST.get("text" , None)

		# validate input data
		errorMessage = {}
		if username == None:
			errorMessage['username'] = 'Поле является обязательным для заполнения' 
		if not email_valid(email):
			errorMessage['email'] = 'Неверный email'
		if text == None:
			errorMessage['text'] = 'Поле является обязательным для заполнения'
		if errorMessage:
			return JsonResponse({'status': 'error', 'message': errorMessage}, status=400)

		# save task
		task = Task()
		task.username = username
		task.email = email
		task.text = text
		task.save()

		return JsonResponse({'status': 'ok', 'message' : 'Задача успешно добавлена'})
	else:
		return HttpResponse("Not Allowed", status=405)

@csrf_exempt
def login(request):
	if request.method == 'POST':
		username = request.POST.get('username', None)
		password = request.POST.get('password' , None)

		# validation input data
		errorMessage = {}
		if username == None:
			errorMessage['username'] = 'Поле является обязательным для заполнения'
		if password == None:
			errorMessage['password'] = 'Неверный логин или пароль'
		if errorMessage:
			return JsonResponse({'status': 'error', 'message' : errorMessage}, status=400)

		users = User.objects.filter(username=username,password=password)
		if len(users) > 0:
			user = users[0]

			# gen user token
			expire_date_time = datetime.now() + timedelta(hours=24)
			payload = {'user_id': user.id, 'expire': expire_date_time.timestamp()}
			token = tokenlib.make_token(payload, secret="beejee")

			user.token = token
			user.save()

			return JsonResponse({'status': 'ok', 'token': user.token})

		else:
			return JsonResponse({'status': 'error', 'message': {'password' : 'Неверный логин или пароль'}})

	else:
		return HttpResponse('Not Allowed', status=405)

@csrf_exempt
def task_edit(request,id):
	if request.method == 'POST':
		token = request.POST.get('token', None)
		status = request.POST.get('status', 0)
		text = request.POST.get('text', None)

		# validation fields
		errorMessage = {}
		if token == None:
			errorMessage['token'] = 'Токен обязательное поле'

		data = parse_token(token)
		if not data and token != None:
			errorMessage['token'] = 'Токен истёк или неверный'

		if errorMessage:
			return JsonResponse({'status': 'error', 'message': errorMessage}, status=400)



		task = get_object_or_404(Task,pk=id)
		status = int(status)
		if task.text != text:
			if status == 0 or status == 10:
				status += 1
		task.text = text
		task.status = status
		task.save()
		
		return JsonResponse({'status': 'error', 'task': task.to_dict()})
	else:
		return HttpResponse("Not Allowed", status=405)

def email_valid(email):
	if email == None: return False
	regex = re.compile('[^@]+@[^@]+\\.[^@]+')
	return regex.match(email)

def parse_token(token):
	if token == None: return None
	try:
		data = tokenlib.parse_token(token, secret='beejee')
		expire = data['expire']
	except:
		return None
	if time.time() > expire:
		return None
	return data





