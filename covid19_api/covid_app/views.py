import time

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

from .estimator import estimator
from .serializers import CovidDataSerializer


def process_covid_data(data):
    output = {
        "region":{
            "name":data["region_name"],
            "avgAge":float(data["average_age"]),
            "avgDailyIncomeInUSD":float(data["average_daily_income"]),
            "avgDailyIncomePopulation":float(data["average_daily_income_population"])
        },
        "periodType":data["period_type"],
        "timeToElapse":int(data["time_to_elapse"]),
        "reportedCases":int(data["reported_cases"]),
        "population":int(data["population"]),
        "totalHospitalBeds":int(data["total_hospital_beds"])
    }

    return output




def request_logger(func):
    def wrapper(*args,**kwargs):
        request = args[1]
        request_method = request.method
        request_path = request.get_full_path()[:-1]
        start_time = time.time()
        response = func(*args,**kwargs)
        duration = int((time.time()-start_time)*1000)
        status = response.status_code
        line = f"{request_method}\t\t{request_path}\t\t{status}\t\t{duration}ms\n"
        with open("covid_app/log.txt","a+") as log_file:
            log_file.write(line)

        return response
    return wrapper


class PostCovidDataView(APIView):

    @request_logger
    def get(self,request,format=None):
        return Response({})

    @request_logger
    def post(self,request,format=None):
        serializer = CovidDataSerializer(data=request.data)
        if serializer.is_valid():
            estimated_data = estimator(process_covid_data(request.data))
            return Response(estimated_data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class PostCovidXMLDataView(APIView):

    renderer_classes = [XMLRenderer,]


    @request_logger
    def get(self,request,format=None):
        return Response({})

    @request_logger
    def post(self,request,format=None):
        serializer = CovidDataSerializer(data=request.data)
        if serializer.is_valid():
            estimated_data = estimator(process_covid_data(request.data))
            return Response(estimated_data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class GetLogsView(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "log.html"

    @request_logger
    def get(self,request,format=None):
        logs = []
        with open("covid_app/log.txt","r") as log_file:
            for line in log_file:
                logs.append(line)
        return Response({"logs":logs})




