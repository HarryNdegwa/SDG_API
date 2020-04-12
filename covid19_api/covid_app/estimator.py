import math


class Estimator(object):

  def __init__(self,data=None):
    if data:
      self.input_data = data
    else:
      self.input_data = {}

    self.reported_cases = self.input_data.get("reportedCases")

    # sets the day instance variable
    self.period_normaliser_to_days()

    # sets the factor instance variable
    self.period_factor_calculator()

    # sets projected_infections_estimation instance variable
    self.get_projected_number_of_infections()

    # sets projected_severe_infections_estimation instance variable
    self.get_projected_number_of_severe_infections()

    self.available_beds = math.ceil(0.35*self.input_data.get("totalHospitalBeds"))

    if self.input_data["region"]["avgDailyIncomePopulation"] >= 1:
      self.majority_earning_population_fraction = self.input_data["region"]["avgDailyIncomePopulation"]/100
    else:
      self.majority_earning_population_fraction = self.input_data["region"]["avgDailyIncomePopulation"]


    self.average_daily_income = self.input_data["region"]["avgDailyIncomeInUSD"]


  def get_current_infected_estimation(self):
    if self.reported_cases != None:
      return self.reported_cases*10
    return 0


  def get_severe_current_infected_estimation(self):
    if self.reported_cases != None:
      return self.reported_cases*50
    return 0


  def period_normaliser_to_days(self):
    days = "days"
    weeks = "weeks"
    months = "months"
    days_in_a_week = 7
    days_in_a_month = 30

    period_type = self.input_data.get("periodType")
    elapse_time = self.input_data.get("timeToElapse")

    if str(period_type).casefold() == days.casefold():
      self.days = elapse_time
      return self.days
    elif str(period_type).casefold() == weeks.casefold():
      self.days = elapse_time*days_in_a_week
      return self.days
    elif str(period_type).casefold() == months.casefold():
      self.days = elapse_time*days_in_a_month
      return self.days


  def period_factor_calculator(self):
    infections_to_double_period_in_days = 3
    days = self.period_normaliser_to_days()
    self.factor = days//infections_to_double_period_in_days
    return self.factor


  def get_projected_number_of_infections(self):
    current_infections_estimation = self.get_current_infected_estimation()
    self.projected_infections_estimation = current_infections_estimation*(2**self.factor)
    return self.projected_infections_estimation 


  def get_projected_number_of_severe_infections(self):
    current_severe_infections_estimation = self.get_severe_current_infected_estimation()
    self.projected_severe_infections_estimation = current_severe_infections_estimation*(2**self.factor)
    return self.projected_severe_infections_estimation


  def get_infection_cases_to_hospitalize_estimation(self):
    return int(0.15*self.projected_infections_estimation)


  def get_projected_infection_cases_to_hospitalize_estimation(self):
    return int(0.15*self.projected_severe_infections_estimation)


  def get_available_beds_for_infection_cases(self):
    to_hospitalize_estimation = self.get_infection_cases_to_hospitalize_estimation()
    if self.available_beds >= to_hospitalize_estimation:
      return self.available_beds
    return self.available_beds - to_hospitalize_estimation


  def get_available_beds_for_projected_infection_cases(self):
    to_hospitalize_estimation = self.get_projected_infection_cases_to_hospitalize_estimation()
    if self.available_beds >= to_hospitalize_estimation:
      return self.available_beds
    return self.available_beds - to_hospitalize_estimation

  def get_infection_cases_to_require_icu(self):
    return int(0.05*self.projected_infections_estimation)


  def get_projected_infection_cases_to_require_icu(self):
    return int(0.05*self.projected_severe_infections_estimation)


  def get_infection_cases_to_require_ventilators(self):
    return int(0.02*self.projected_infections_estimation)


  def get_projected_infection_cases_to_require_ventilators(self):
    return int(0.02*self.projected_severe_infections_estimation)


  def get_money_economy_is_likely_to_loose_on_infections(self):
    amount = (self.projected_infections_estimation*self.majority_earning_population_fraction*self.average_daily_income)//self.days
    return int(amount)


  def get_money_economy_is_likely_to_loose_on_projected_infections(self):
    amount = (self.projected_severe_infections_estimation*self.majority_earning_population_fraction*self.average_daily_income)//self.days
    return int(amount)





def estimator(data):
  input_data = data
  my_estimator = Estimator(input_data)
  data = {
    "data":input_data,
    "impact":{
      "currentlyInfected":my_estimator.get_current_infected_estimation(),
      "infectionsByRequestedTime":my_estimator.get_projected_number_of_infections(),
      "severeCasesByRequestedTime":my_estimator.get_infection_cases_to_hospitalize_estimation(),
      "hospitalBedsByRequestedTime":my_estimator.get_available_beds_for_infection_cases(),
      "casesForICUByRequestedTime":my_estimator.get_infection_cases_to_require_icu(),
      "casesForVentilatorsByRequestedTime":my_estimator.get_infection_cases_to_require_ventilators(),
      "dollarsInFlight":my_estimator.get_money_economy_is_likely_to_loose_on_infections()
    },
    "severeImpact":{
      "currentlyInfected":my_estimator.get_severe_current_infected_estimation(),
      "infectionsByRequestedTime":my_estimator.get_projected_number_of_severe_infections(),
      "severeCasesByRequestedTime":my_estimator.get_projected_infection_cases_to_hospitalize_estimation(),
      "hospitalBedsByRequestedTime":my_estimator.get_available_beds_for_projected_infection_cases(),
      "casesForICUByRequestedTime":my_estimator.get_projected_infection_cases_to_require_icu(),
      "casesForVentilatorsByRequestedTime":my_estimator.get_projected_infection_cases_to_require_ventilators(),
      "dollarsInFlight":my_estimator.get_money_economy_is_likely_to_loose_on_projected_infections()
    }
  }
  return data




