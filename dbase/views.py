from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import *
from .forms import СaseChoice, VictimsChoice, GuiltyChoice

def get_attr (obj):
	# добавление только существующих атрибутов объекта
	obj_attr = []
	for attr in obj.__dict__.keys():
		if attr in ('_state', 'id', 'photo','name') or type((obj.__dict__[attr])) is 'int':
			continue
		if (obj.__dict__[attr]):
			obj_attr.append(obj.__dict__[attr])
	return obj_attr

def filter_persecutios(request):
	"""
	фильтрация преследований на основании фильтров переданных в запросе "request"
	"""
	pers_list = Perseqution.objects.all().order_by("date")
	if request.method == 'GET': return pers_list
	if request.POST['case']:
		# сбор преследований в деле
		case = Case.objects.filter(id=request.POST['case'])[0]
		pers_list = Perseqution.objects.filter(case=case)

	if request.POST['Violation']:
		# сбор преследований в которых нарушались заданные права
		viol = Violation.objects.filter(id=request.POST['Violation'])[0]
		pers_list = set(ViP.persecution for ViP in ViolationInPersecution.objects.filter(rights=viol)
							 if ViP.persecution in pers_list)

	if request.POST['article']:
		# сбор преследований в которых применялась статья
		art = Article.objects.filter(id=request.POST['article'])[0]
		pers_list = set(AiP.persecution for AiP in ArticlesInPersecution.objects.filter(article=art)
							if AiP.persecution in pers_list)

	if request.POST['type']:
		# сбор преследований в которых применялась статья
		type = TypeOfPersecution.objects.filter(id=request.POST['type'])[0]
		pers_list = set(pers for pers in pers_list
							if pers.type_of_pers == type)

	return pers_list

def index(request):
	return render(request, 'dbase/index.html')

def victims(request):
	form = СaseChoice()
	vic_form = VictimsChoice()
	if request.method == 'POST':
		print (request.POST.keys())
		vict_rest = Victim.objects.all() #полный список который будет уменьшаться по мере прохождения фильтров
		filtr_set = []
		for filtr in request.POST.keys():
			if filtr in ('csrfmiddlewaretoken') : continue
			print (filtr)
			if request.POST[filtr]:
				filtr_set.append(filtr)
		if filtr_set:
			pers_list = filter_persecutios(request)
			vict_rest = set(pers.victim for pers in pers_list)

		if 'place' in filtr_set:
			# фильтрация жертв по месту лишения свободы
			place = Place.objects.filter(id=request.POST['place'])[0]
			vict_rest = set(vict for vict in vict_rest
							if vict.place == place)

		if 'restriction' in filtr_set:
			# фильтрация текущей жертв по мере пресечения
			restriction = RestrictionOfVictim.objects.filter(id=request.POST['restriction'])[0]
			vict_rest = set(vict for vict in vict_rest
							if vict.restriction == restriction)

	elif request.method == 'GET':
		vict_rest = Victim.objects.all()

	context = {'head':'Пострадавшие','list_of_pers':vict_rest,
			   'form': form, 'vic_form': vic_form}
	return render(request, 'dbase/victims.html', context)

def guiltys(request):
	form = СaseChoice()
	glt_form = GuiltyChoice()
	if request.method == 'POST':
		guity_rest = Guilty.objects.all()  # полный список который будет уменьшаться по мере прохождения фильтров
		filtr_set = []
		for filtr in request.POST.keys():
			if filtr in ('csrfmiddlewaretoken'): continue
			if request.POST[filtr]:
				filtr_set.append(filtr)
		if filtr_set:
			pers_list = filter_persecutios(request)
			guity_rest = set(pers.guilty for pers in GuiltyInPersecutions.objects.all()
							   if pers.perseqution in pers_list)

		if request.POST['citizenship']:
			# фильтрация виновных по гражданству
			guity_rest =  set(guity for guity in guity_rest if guity.citizenship == request.POST['citizenship'])

		if request.POST['organization']:
			# фильтрация виновных по гражданству
			guity_rest =  set(guity for guity in guity_rest if guity.organization == request.POST['organization'])

	elif request.method == 'GET':
		guity_rest = Guilty.objects.all()
	data ={'head':'Виновные','list_of_pers':guity_rest,
		   'form': form, 'glt_form':glt_form}
	return render(request, 'dbase/guiltys.html',data)

def cases(request):
	form = СaseChoice()
	list_of_pers = Case.objects.all()
	data ={'head':'Дела','list_of_pers':list_of_pers, 'form': form}
	return render(request, 'dbase/cases.html',data)

class VictimDetailView(generic.DetailView):
	model = Victim
	template_name = 'dbase/victim_home.html'
	contex_object_name = 'victim'

	def get_context_data(self, **kwargs):
		form = СaseChoice()
		obj = self.object
		# collecting information about persecutions of victim
		vic_in_persecution = Perseqution.objects.filter(victim=obj)
		#vic_in_persecution = set(pers for pers in Perseqution.objects.all().order_by('date')
		#						 if pers.victim == obj)

		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		context['persequtions_list'] = vic_in_persecution
		context['form'] = form
		return context

	def post(self, request, *args, **kwargs):
		form = СaseChoice()
		self.object = self.get_object()
		context = self.get_context_data(**kwargs)
		filtred_pers = filter_persecutios(request)
		context['persequtions_list'] = (pers for pers in context['persequtions_list'] if pers in filtred_pers)
		context['form'] = form
		return self.render_to_response(context=context)

class GuiltyDetailView(generic.DetailView):
	model = Guilty
	queryset = Guilty.objects.all()
	template_name = 'dbase/guilty_home.html'
	contex_object_name = 'guilty'

	def get_context_data(self, **kwargs):
		obj = self.object
		# добавление только существующих атрибутов объекта
		obj_attr = get_attr(obj)
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		gul_in_persecution = set(pers for pers in GuiltyInPersecutions.objects.all()
						if pers.guilty == obj)
		context['persequtions_list'] = gul_in_persecution
		context['obj_attr'] = obj_attr
		return context

class CaseDetailView(generic.DetailView):
	model = Case
	queryset = Case.objects.all()
	template_name = 'dbase/case_home.html'
	contex_object_name = 'case'

	def get_context_data(self, **kwargs):
		obj = self.object
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		vict_in_case = set(pers.victim for pers in Perseqution.objects.all()
						if pers.case == obj)
		context['Victim_list'] = vict_in_case
		return context

class PersDetailView(generic.DetailView):
	model = Perseqution
	template_name = 'dbase/perseс_home.html'
	contex_object_name = 'persecution'

	def get_context_data(self, **kwargs):
		obj = self.object
		obj.articles = (AiP.article for AiP in ArticlesInPersecution.objects.all()
						if AiP.persecution == obj)

		obj.violation = (ViP.rights for ViP in ViolationInPersecution.objects.all()
						 if ViP.persecution == obj)

		GiP = (glt.guilty for glt in GuiltyInPersecutions.objects.all()
			   if glt.perseqution == obj)

		context = super().get_context_data(**kwargs)
		context['GiP_list'] = GiP
		return context

# Create your views here.
