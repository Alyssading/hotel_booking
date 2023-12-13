import datetime

from django.shortcuts import render


# Viewing function
def index(request):
    if request.method == 'GET':
        checkin = datetime.datetime.today()
        print(checkin)
        checkout = checkin + datetime.timedelta(days=1)
        date_range = f'{checkin.strftime("%Y/%m/%d")} - {checkout.strftime("%Y/%m/%d")}'
        # The view function returned a template through the render method:index.html
        return render(request, 'index.html', {'default_date_range': date_range})


def hotel_list(request):
    print(request.GET)
