from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework import status
from bs4 import BeautifulSoup
from lxml import html
from .models import *
from .serializers import *
import json
import re
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from django.utils.encoding import smart_str
from urllib import parse



class ApiIndexView(APIView):

    def get(self,request,*args, **kwargs):
        return JsonResponse({'status':"OK"})

    def clean_data(self):

        data = {}
        
        for k, v in self.request.data.items():
            clean = re.compile('>.*?<')
            texts = re.sub(clean,'><',v)
            data.update({k:texts})
        return data

    def get_attribute_from_html(self, data):
        result = {}
        tag_name = []
        for key, value in data.items():
            if "url" != key:
                pars = BeautifulSoup(value, "html.parser").find()
                if pars.get("id", False):
                    parsed_data = "#" + pars.get("id")
                    result[key] = parsed_data 
                elif pars.get("src", False):
                    parsed_data = "@" + pars.get("src")
                    result[key] = parsed_data + '|' + pars.name
                elif pars.get("class", False):
                    parsed_data = "." + " ".join(pars.get("class"))
                    result[key] = parsed_data
                elif pars.get('itemprop', False):
                    parsed_data = "&" + pars.get("itemprop")
                    result[key] = parsed_data + "|" + pars.name
                elif pars.get('href', False):
                    parsed_data = "^" + pars.get("href")
                    result[key] = parsed_data + "|" + pars.name
                else:
                    tag_name.append(key)
            else:
                result[key] = value
        if tag_name:
            return [result, tag_name]
        return result

    def post(self, request, *args, **kwargs):
        
        clean_data = self.clean_data()
        data = self.get_attribute_from_html(clean_data)

        if isinstance(data, dict):
            product = ProductTag.objects.create() 
            product.name = data.get("url")
            product.bulk_insert(**data)
            try:
                product.save()
            except:
                print(data)
            return JsonResponse({'data': data})
        else:
            result = data[0]

            for tag in data[1]:
                result[tag] = self.request.data[tag]
            product = ProductTag.objects.create()
            print(result.get("url"))
            product.name = result.get("url")
            product.bulk_insert(**result)
            product.save()
            return JsonResponse({'data': result})
            


class ScraperView(generic.View):

    def scrapper(self, url, data):
        result = {}
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        pars = BeautifulSoup(driver.page_source, "html.parser")
        for obj in data:
            key, value, tag_name = obj.get("field"), obj.get("value"), obj.get("tag_name")

            if value.startswith("."):
                
                result[key] = pars.find_all(tag_name, {"class": value[1:]})[0].text if pars.find_all(tag_name, {"class": value[1:]}) else "yoxdu"
                
            elif value.startswith("@"):
                result[key] = driver.find_element_by_xpath('//*[@src="{}"]'.format(value[1:])).get_attribute("src")
                
            elif value.startswith("&"):
                result[key] = driver.find_element_by_xpath('//*[@itemprop="{}"]'.format(value[1:])).text

            elif value.startswith("^"):
                result[key] = driver.find_element_by_xpath('//*[@href="{}"]'.format(value[1:])).text
                
                

            elif value.startswith("<"):
                pars = BeautifulSoup(value, "html.parser").find()
            
                result[key] = driver.find_elements_by_xpath("//{}".format(pars.name))[0].text
                 
            elif value.startswith("#"):
                result[key] = pars.find_all(tag_name, {"id": value[1:]})[0].text if pars.find_all(tag_name, {"id": value[1:]}) else "yoxdu"

        driver.quit()
        return result

    def get(self, request, *args, **kwargs):

        url = request.GET.get("url") 
        prs_url = parse.urlsplit(url)
        
        data = ProductTag.objects.filter(name__icontains=prs_url.netloc).last() 
        obj = ProductSerializers(data)
        latest_result = self.scrapper(url, obj.data.get("product_tags"))
        return JsonResponse({"status":"OK", "data": latest_result})
