from requests import get

urlc = 'http://testus.neotelecom.kg/api.php?key=aspergilus&cat=task&action=get_list&state_id=11&employee_id='
urln = 'http://testus.neotelecom.kg/api.php?key=aspergilus&cat=employee&action=get_data&id='
urlf = 'http://testus.neotelecom.kg/api.php?key=aspergilus&cat=employee&action=get_employee_id&data_typer=name&data_value='
urls1 = 'http://testus.neotelecom.kg/api.php?key=aspergilus&cat=employee&action=check_pass&login='
urls2 = '&pass='
urls3 = '&action=get_employee_id&data_typer=login&data_value='

def parsing(id_, name):
	if name == 'count':
		response = get(urlc + str(id_)).json()
		return response['count']
	elif name == 'names':
		response = get(urln + str(id_)).json()
		return response['data'][str(id_)]['name']
	elif name == 'for_name':
		response = get(urlf + str(id_)).json()
		return response['id']
	elif name == 'sign':
		response = get(urls1 + id_[0] + urls2 + id_[1] + urls3 + id_[0]).json()
		try:
			return response['id']
		except KeyError:
			return 'none'