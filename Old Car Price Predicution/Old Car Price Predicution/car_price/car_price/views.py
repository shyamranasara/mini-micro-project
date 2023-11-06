from django.http import HttpResponse
from django.shortcuts import render
from data import pred_price

def index(request):
    return render(request, "index.html")

def result(request):
    print(request.GET.get("car_name"))






    name = request.GET.get("car_name")
    location = request.GET.get("Location")
    year = request.GET.get("Year")
    driven = request.GET.get("Driven")
    fuel = int(request.GET.get("Fuel"))
    owner = int(request.GET.get("Owner"))
    transmission = int(request.GET.get("Transmission"))
    milage = request.GET.get("Milage")
    cc = request.GET.get("cc")
    hp = request.GET.get("hp")
    seats = request.GET.get("Seats")


    # name = request.POST.get("car_name")
    # location = request.POST.get("Location")
    # year = request.POST.get("Year")
    # driven = request.POST.get("Driven")
    # fuel = request.POST.get("Fuel")
    # owner = request.POST.get("Owner")
    # transmission = request.POST.get("Transmission")
    # milage = request.POST.get("Milage")
    # cc = request.POST.get("cc")
    # hp = request.POST.get("hp")
    # seats = request.POST.get("Seats")

    # if(request.POST):
    #     numb = request.POST.dict()
    #     num1 = numb.get("car_name")
    #     num2 = numb.get("Location")
    #     num3 = numb.get("Year")
    #     num4 = numb.get("Driven")
    #     num5 = numb.get("Fuel")
    #     num6 = numb.get("Owner")
    #     num7 = numb.get("Transmission")
    #     num8 = numb.get("Milage")
    #     num9 = numb.get("cc")
    #     num10 = numb.get("hp")
    #     num11 = numb.get("Seats")
        

        
    print(name , location ,fuel , year , driven , owner , transmission, milage ,cc , hp, seats)



        # price = pred_price.pred(num1,num2,num3,num4,num5,num6,num7,num8,num9,num10,num11)
    price = pred_price.pred(name , location , year , driven ,fuel ,owner ,transmission ,milage ,cc ,hp, seats)
    p1= float(price)
    p2 = round(p1 ,2)
    param={
        "Price":p2
    }




    return render(request , "result.html" , param)