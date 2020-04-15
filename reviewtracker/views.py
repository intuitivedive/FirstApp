from django.shortcuts import render
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from random import randint
from time import sleep
from django.http import HttpResponse


now = datetime.now()


fixedstring_1 = 'https://www.amazon.in/product-reviews/'
fixedstring_2 = '/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent&pageNumber=1'

def inputform(request):
    return render(request,'input.html')

def reviewtracker(request):
    asin=request.GET['asin']
    daycount=int(request.GET['daycount'])
    url = fixedstring_1 + asin + fixedstring_2
    try:
        html=urlopen(url)
    except:
        output='asin not found'
        return HttpResponse(output)
    soup = BeautifulSoup(html.read(),"html.parser");
    reviewsection = soup.findAll("div", {"data-hook": "review"}) 
    if (not reviewsection):
        output='no reviews found'
        return HttpResponse(output)
    count=0
    results=[]
    for section in reviewsection:
        rating = section.find("span", {"class": "a-icon-alt"}).replace('out of 5 stars','')
        review_date = section.find("span",{"data-hook":"review-date"})
        review_comment = section.find("span",{"data-hook":"review-body"})
        review_date_formatted = datetime.strptime(review_date.getText().replace('Reviewed in India on ',''), '%d %B %Y')
        if(review_date_formatted>(now-timedelta(days=daycount))):
            output=[asin,review_date.getText().replace('Reviewed in India on ',''),rating.getText(),review_comment.getText()]
            results.append(output)
            count+=1
        else:
            if(count==0):
                output='no reviews found during this period'
                return HttpResponse(output)
                break
    #return HttpResponse(result)
    return render(request,'output.html',{'results':results})