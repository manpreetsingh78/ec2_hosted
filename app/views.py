import json
from django.shortcuts import render,redirect
from .models import City,address
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def search_button_execution(search_query,lat,long):
    import requests
    from .token_generate import tokengenerate
    token = tokengenerate()
    headers ={
    'authority': 'www.bigbasket.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    f = requests.get('https://www.bigbasket.com/',headers=headers)


    cok = f.cookies.items()
    cookie = ''
    for item in cok:
        data = list(item)
        cookie += data[0] + "=" + data[1] + ";"
        if data[0] == '_bb_aid':
            cookie += '_bb_vid' + "=" + data[1] + ";"
    print(cookie)
    headers ={
    'authority': 'www.bigbasket.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'cookie': f'{cookie}',
    }

    f = requests.get(f'https://www.bigbasket.com/skip_explore/?c=1000046&l=0&s=0&n=/',headers=headers)
    cok = f.cookies.items()
    cookie = ''
    for item in cok:
        data = list(item)
        cookie += data[0] + "=" + data[1] + ";"
        if data[0] == '_bb_aid':
            cookie += '_bb_vid' + "=" + data[1] + ";"
    print(cookie)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'{cookie}',
        'Host': 'www.bigbasket.com',
        'Referer': 'https://www.bigbasket.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    # get_places = f'https://www.bigbasket.com/places/v1/places/autocomplete/?inputText={search_query}&token={token}'

    # r = requests.get(get_places,headers=headers)
    # print(r.text)
    # json_data = r.json()

    # place_id = str(json_data['predictions'][0]['placeId'])
    # desc = str(json_data['predictions'][0]['description'])
    # print(place_id)
    # print(desc)

    # get_lat_long_url = f'https://www.bigbasket.com/places/v1/places/address?placeId={place_id}&token={token}'

    # r = requests.get(get_lat_long_url,headers=headers)

    # json_data = r.json()
    # lat = json_data['lat']
    # long = json_data['lng']
    # print(lat)
    # print(long)

    set_address_url = 'https://www.bigbasket.com/mapi/v4.1.0/set-current-address/'
    postdata = f'transient=1&src=2&referrer=other&lat={lat}&lng={long}&area=Baner'
    f = requests.post(set_address_url,headers=headers,data=postdata)
    print(f.text)
    cok = f.cookies.items()
    cookie = ''
    for item in cok:
        data = list(item)
        cookie += data[0] + "=" + data[1] + ";"
        if data[0] == '_bb_aid':
            cookie += '_bb_vid' + "=" + data[1] + ";"
    print(cookie)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'{cookie}',
        'Host': 'www.bigbasket.com',
        'Referer': 'https://www.bigbasket.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    
    r = requests.get(f'https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug={search_query}&page=1',headers=headers)

    # print(r.text)
    return r.text


def fetch_address_by_city(city_unique_id):
    from time import time
    print("Fetching Started")
    import requests
    header = {
    'authority': 'www.bigbasket.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'cookie': '''bb_cid=1; _bb_vid="NzIwNDM1NTg3MQ=="; _bb_tc=0; _client_version=2590; _bb_rdt="MzExNjU1NTc4Ng==.0"; _bb_rd=6; sessionid=v3uu8l9ursk5cat56a1cjzwiucedu2bl; _gid=GA1.2.785627896.1664443464; bigbasket.com=36847bad-10db-46d5-8a70-c62859258577; adb=0; bbscc=2; jedi=2; _gcl_au=1.1.1485070885.1664443466; ufi=1; csrftoken=fE4pz6iu8ReVigmiCEfJZE2KjtUs2aNs4anV8B1auLxQCdCi612rCMo7wcFrxMXy; _vz=viz_63356e0d8fe28; _vz=; _sp_van_encom_hid=3273; _bb_hid=3274; _sp_bike_hid=3271; _bb_visaddr="fEhTUiBMYXlvdXQgU2VjdG9yIDMsIEhTUiBDbHViIHJvYWQgTmVhciBOZXcgYm9ybiBifDEyLjkwOTM1MjAwMTg4OTI4fDc3LjY0MzM2MjgxMDgyODk5fDU2MDEwMnw="; _bb_aid="Mjk4MTQ2NTA2Ng=="; x-channel=web; _bb_bb2.0=1; _bb_sa_ids=10215; isPwaPilot=true; bb2_enabled=true; csurftoken=l8vNMg.NzIwNDM1NTg3MQ==.1664445973551.0faFB4OeUVOgWwVs/OjmqGEpCnIoGDzNgRK8vGL6hWs=; isRedirectedFromTCP=false; tneuSessionId=2e77df2d-8a43-4683-833e-0df61eb9b911; _ga_FRRYG5VKHX=GS1.1.1664445957.2.1.1664446694.0.0.0; _ga=GA1.2.216632993.1664443464; ts=2022-09-29 10:18:15.982''',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    t1 = time()
    counter = 0
    for i in range(97,123):
        for y in range(97,123):
            ar = str(chr(i)+chr(y))
            print(ar)
            r = requests.get(f'https://www.bigbasket.com/bbplacessearch/getplaces/?term={ar}&city_id={city_unique_id}',headers=header)
            # print(r.text)
            import json
            address_data = []
            json_data = json.loads(r.text)
            for j in range(10):
                try:
                    pincode = str(json_data['response']['results'][j]['pincode'])
                    addresss = str(json_data['response']['results'][j]['display_name'])
                    latitude = float(json_data['response']['results'][j]['location'][1])
                    longitude = float(json_data['response']['results'][j]['location'][0])
                    addresss = str(json_data['response']['results'][j]['display_name'])
                    full_ = addresss + " " + pincode
                    print(full_)
                    print(latitude)
                    print(longitude)
                    if pincode in address_data:
                        continue
                    city_idd = City.objects.get(id=1)
                    addres = full_
                    try:
                        add_obj = address(city_id=city_idd,address_field = addres,lat=latitude,long=longitude)
                        add_obj.save()
                        print("Data added;- ",city_idd,addres)
                        counter += 1
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
    t2 = time()
    print(t2-t1)
    return counter

@login_required(login_url='/admin')
def homepage(request):
    if request.method == 'GET':
        return render(request,"index.html")
    elif request.method == 'POST':
        search_query = str(request.POST.get("search_query"))
        lat = request.POST.get("lat")
        long = request.POST.get("long")
        print(lat)
        print(long)
        search_query =search_query.strip().replace(" ","%20")
        print(search_query)
        result = search_button_execution(search_query,lat,long)
        result = json.loads(str(result))
        # result = result['tabs'][0]['product_info']['products']
        print(result)
        item_name_data =[]
        brand_data =[]
        category_data =[]
        weight_data =[]
        price_data =[]
        image_data =[]
        try:

            for i in range(24):
                item_name = result['tabs'][0]['product_info']['products'][i]['desc']
                brand = result['tabs'][0]['product_info']['products'][i]['brand']['name']
                category = result['tabs'][0]['product_info']['products'][i]['category']['tlc_name']
                weight = result['tabs'][0]['product_info']['products'][i]['w']
                price = "Rs." + result['tabs'][0]['product_info']['products'][i]['pricing']['discount']['mrp'] 
                image = result['tabs'][0]['product_info']['products'][i]['images'][0]['s']
                if len(result['tabs'][0]['product_info']['products'][i]['children']) > 0:
                    for k in range(len(result['tabs'][0]['product_info']['products'][i]['children'])):
                        weight = weight + " & " + result['tabs'][0]['product_info']['products'][i]['children'][k]['w']
                        price = price + " & " + "Rs." +  result['tabs'][0]['product_info']['products'][i]['children'][k]['pricing']['discount']['mrp']


                item_name_data.append(item_name)
                brand_data.append(brand)
                category_data.append(category)
                price_data.append(price)
                weight_data.append(weight)
                image_data.append(image)
        except:
            pass
        mylist = zip(item_name_data, brand_data,category_data,weight_data,price_data,image_data)
        items_found = result['tabs'][0]['product_info']['total_count']
        context = {
            'mylist': mylist,
            'items_found': items_found,
            'no_of_pages': no_of_pages,
        }


        return render(request,"results.html",
            context
            )



def search_results(request):
    if is_ajax(request=request):
        game = request.POST.get('game')
        if len(game) < 3:
            return JsonResponse({})
        print(game)
        qs = address.objects.filter(address_field__icontains=game)
        print(qs)
        if len(qs) > 0 and len(game) > 0:
            data = []
            for pos in qs:
                item = {
                    'pk':pos.pk,
                    'address':pos.address_field,
                    'lat':pos.lat,
                    'long':pos.long
                }
                data.append(item)
            res = data
        else:
            res = "Not found"
        return JsonResponse({'data':res})
    return JsonResponse({})



def fetch_address_of_city(request):
    city = City.objects.get(id=1)
    city_u_id = city.city_unique_id
    data_address = fetch_address_by_city(city_u_id)
    print(data_address)
    
    return HttpResponse(f'<p>SuccessFull {data_address}</p>')

