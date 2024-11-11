from django.db import models

# Create your models here.

class Voter(models.Model):
  '''class to represent an individual voter and how they voted in Newton'''

  # *    Last Name
  # *    First Name
  # *    Residential Address - Street Number
  # *    Residential Address - Street Name
  # *    Residential Address - Apartment Number
  # *    Residential Address - Zip Code
  # *    Date of Birth
  # *    Date of Registration
  # *    Party Affiliation
  # *    Precinct Number

  last_name = models.TextField()
  first_name = models.TextField()
  street_number = models.TextField()
  street_name = models.TextField()
  apartment_number = models.TextField()
  zip_code = models.IntegerField()
  
  date_of_birth = models.DateField()
  date_of_registration = models.DateField()
  party = models.TextField()
  precinct_number = models.TextField()

  # *    v20state
  # *    v21town
  # *    v21primary
  # *    v22general
  # *    v23town

  v20state = models.BooleanField()
  v21town = models.BooleanField()
  v21primary = models.BooleanField()
  v22general = models.BooleanField()
  v23town = models.BooleanField()

  voter_score = models.IntegerField()


  def __str__(self):
    '''return a string representation'''
    return f'{self.first_name} {self.last_name} ({self.voter_score})'
  
  def get_election_history(self):
    return [self.v20state, self.v21town, self.v21primary, self.v22general, self.v23town]
  
  def get_birth_year(self):
    return self.date_of_birth.year 

def load_data():
  '''load the data from a csv file'''
  Voter.objects.all().delete()

  filename = "C:/Users/Michael/Downloads/newton_voters.csv"

  f = open(filename)
  headers = f.readline()
  count = 0
  try:
    for line in f:
      fields = [field.strip() for field in line.split(',')]
      fields = [True if f == "TRUE" else False if f == "FALSE" else f for f in fields]
      voter = Voter(
          last_name=fields[1],
          first_name=fields[2],
          street_number=fields[3],
          street_name=fields[4],
          apartment_number=fields[5],
          zip_code=fields[6],
          date_of_birth=fields[7],
          date_of_registration=fields[8],
          party=fields[9],
          precinct_number=fields[10],
          v20state=fields[11],
          v21town=fields[12],
          v21primary=fields[13],
          v22general=fields[14],
          v23town=fields[15],
          voter_score=fields[16]
          )
        
        
        
      voter.save()
      if count % 25 == 0:
        print(f"Successfully saved {voter}")
      count = count + 1
  except:
    print(f"An error occured: {voter}")
  