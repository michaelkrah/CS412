from django.shortcuts import render

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter

from datetime import date


import plotly
import plotly.graph_objects as go


# Create your views here.

class VotersListView(ListView):
  '''View to display list of voter data.'''

  template_name = 'voter_analytics/voters.html'
  model = Voter
  context_object_name = 'voters'

  paginate_by = 100

  def get_context_data(self, **kwargs: any):
      '''add data to the context object, including graphs'''

      context = super().get_context_data(**kwargs)

      birth_years = [i for i in range(1924, 2007)]
      context['birth_years'] = birth_years

      return context



  def get_queryset(self) -> QuerySet[any]:
    qs = super().get_queryset()

    if "affiliation" in self.request.GET:
      affiliation = self.request.GET['affiliation']
      if affiliation:
        qs = Voter.objects.filter(party=affiliation)
    
    min_birth = self.request.GET.get('min_birth')
    if min_birth:
      min_birth = date(int(min_birth), 1, 1)
      qs = qs.filter(date_of_birth__gte=min_birth)


    max_birth = self.request.GET.get('max_birth')
    if max_birth:
      max_birth = date(int(max_birth), 1, 1)
      qs = qs.filter(date_of_birth__lte=max_birth)

    voter_score = self.request.GET.get("voter_score")
    if voter_score:
      voter_score = int(voter_score)
      qs = qs.filter(voter_score=voter_score)
 
    if self.request.GET.get('v20state') == 'true':
        qs = qs.filter(v20state=True)
    if self.request.GET.get('v21town') == 'true':
        qs = qs.filter(v21town=True)
    if self.request.GET.get('v21primary') == 'true':
        qs = qs.filter(v21primary=True)
    if self.request.GET.get('v22general') == 'true':
        qs = qs.filter(v22general=True)
    if self.request.GET.get('v23town') == 'true':
        qs = qs.filter(v23town=True)


    return qs


class VoterDetailView(DetailView):
   '''show a detailed view for one voter'''

   template_name = 'voter_analytics/voter_detail.html'
   model = Voter
   context_object_name = 'v'


class Graphs(ListView):
  '''Display necessary graphs'''
  template_name = 'voter_analytics/graphs.html'
  model = Voter
  context_object_name = 'voters'

  paginate_by = 100

  def get_context_data(self, **kwargs: any):
      '''add data to the context object, including graphs'''

      context = super().get_context_data(**kwargs)

      filtered_queryset = self.get_queryset()

      birth_years = [i for i in range(1924, 2007)]
      context['birth_years'] = birth_years

      x_age_dic = {}
      x_age = []
      y_age = []

      x_party_dic = {}
      x_party = []
      y_party = []

      x_election = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
      y_election = [0, 0, 0, 0, 0]

      for entry in filtered_queryset:
        year = entry.get_birth_year()
        party = entry.party
        election_history = entry.get_election_history()

        if year in x_age_dic:
           x_age_dic[year] += 1
        else:
           x_age_dic[year] = 1
          
        if party in x_party_dic:
           x_party_dic[party] += 1
        else:
           x_party_dic[party] = 1

        for i in range(5):
           if election_history[i]:
              y_election[i] += 1
           

      for key in x_age_dic:
         x_age.append(key)
      for i in x_age:
         y_age.append(x_age_dic[i])

      for key in x_party_dic:
         x_party.append(key)
      for i in x_party:
         y_party.append(x_party_dic[i])

      n = 0
      for i in y_age:
         n += i

      fig = go.Figure(data=[go.Bar(x=x_age, y=y_age)],
          layout=go.Layout(title=f"Number of Voters Born Each Year (n = {n})"))
      graph_hist = plotly.offline.plot(fig, auto_open=False, output_type='div')
      
      context['graph_hist'] = graph_hist

      fig = go.Figure(data=[go.Pie(labels=x_party, values=y_party)],
                      layout=go.Layout(title=f"Number of Voters in Each Party (n = {n})"))

      pie_div = plotly.offline.plot(fig, auto_open=False, output_type='div')
      context['pie_div'] = pie_div

      fig = go.Figure(data=[go.Bar(x=x_election, y=y_election)],
          layout=go.Layout(title=f"Number of Voters in Each Election (n = {n})"))
      election_hist = plotly.offline.plot(fig, auto_open=False, output_type='div')
      
      context['election_hist'] = election_hist
      


      return context



  def get_queryset(self) -> QuerySet[any]:
    qs = super().get_queryset()

    if "affiliation" in self.request.GET:
      affiliation = self.request.GET['affiliation']
      if affiliation:
        qs = Voter.objects.filter(party=affiliation)
    
    min_birth = self.request.GET.get('min_birth')
    if min_birth:
      min_birth = date(int(min_birth), 1, 1)
      qs = qs.filter(date_of_birth__gte=min_birth)


    max_birth = self.request.GET.get('max_birth')
    if max_birth:
      max_birth = date(int(max_birth), 1, 1)
      qs = qs.filter(date_of_birth__lte=max_birth)

    voter_score = self.request.GET.get("voter_score")
    if voter_score:
      voter_score = int(voter_score)
      qs = qs.filter(voter_score=voter_score)
 
    if self.request.GET.get('v20state') == 'true':
        qs = qs.filter(v20state=True)
    if self.request.GET.get('v21town') == 'true':
        qs = qs.filter(v21town=True)
    if self.request.GET.get('v21primary') == 'true':
        qs = qs.filter(v21primary=True)
    if self.request.GET.get('v22general') == 'true':
        qs = qs.filter(v22general=True)
    if self.request.GET.get('v23town') == 'true':
        qs = qs.filter(v23town=True)


    return qs
