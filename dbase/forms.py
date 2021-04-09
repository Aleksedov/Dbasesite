from .models import Violation, Case, Article, Place, RestrictionOfVictim, Guilty, TypeOfPersecution
from django import forms

class СaseChoice(forms.Form):
    """
    Формы фильтров для преследований
    """

    """ 
    case_filter = forms.ModelMultipleChoiceField(label='Выбор дел ',
                                            queryset=Case.objects.values_list("name", flat=True),
                                            widget=forms.CheckboxSelectMultiple)
    
    case_filter = forms.ModelChoiceField(label='тестовая форма ',
        queryset=Case.objects.values_list("name", flat=True).distinct(),
        empty_label=None)
    """
    case_choice = [('','---------')]+list((case.id,case.name) for case in Case.objects.all())
    case = forms.ChoiceField(label='Дела ', choices=case_choice, required=False, )

    viol_choice = [('','---------')]+list((viol.id,viol.rights) for viol in Violation.objects.all())
    Violation = forms.ChoiceField(label='Права ', choices=viol_choice, required=False)

    article_choice = [('', '---------')] + list((art.id, art) for art in Article.objects.all())
    article = forms.ChoiceField(label='Cтатья ', choices=article_choice, required=False)

    type_choice = [('', '---------')] + list((type.id, type) for  type in TypeOfPersecution.objects.all())
    type = forms.ChoiceField(label='Преследование ', choices=type_choice, required=False)

class VictimsChoice(forms.Form):
    """
    Формы фильтров для жертв
    """

    place_choise = [('', '---------')] + list((place.id, place.short_name) for place in Place.objects.all())
    place = forms.ChoiceField(label='Места лишения свободы ', choices=place_choise, required=False, )

    restriction_choice = [('', '---------')] + list((rest.id, rest.restriction) for rest in RestrictionOfVictim.objects.all())
    restriction = forms.ChoiceField(label='Ограничения ', choices=restriction_choice, required=False)

class GuiltyChoice(forms.Form):
    """
    Формы фильтров для преследователей
    """

    citizenship_choise = [('', '---------'), ] + list(set((glt.citizenship, glt.citizenship)
                                                          for glt in Guilty.objects.all()))
    citizenship = forms.ChoiceField(label='Гражданство', choices=citizenship_choise, required=False, )

    org_choice = [('', '---------')] + list(set((glt.organization, glt.organization)
                                                          for glt in Guilty.objects.all()))
    organization = forms.ChoiceField(label='Организация ', choices=org_choice, required=False)
