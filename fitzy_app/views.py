import math
from django.utils import timezone
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import UserInfo
from .models import NutritionalData
from decimal import Decimal


def home(request):
    return render(request,'home.html')

def handle_login(request):
   if request.method=="POST":
      email=request.POST.get('email')
      password=request.POST.get('password')
      user=authenticate(request,username=email,password=password)

      if user is not None:
          login(request, user)
          messages.success(request, "Logged In Successfully")
          return redirect('home')
         
      else:
        messages.error(request,"Enter Valid Username Or Password")
        return redirect('home')
   return render(request,'home.html')  

def handle_signup(request):
   if request.method=='POST':
      firstname=request.POST.get('f_name')
      lastname=request.POST.get('l_name')
      email=request.POST.get('email1')
      pass1=request.POST.get('pass1')
      pass2=request.POST.get('pass2')
      if User.objects.filter(email=email).exists():
         messages.error(request,"Email Already In Use...")
         return redirect('home')
      if pass1!=pass2:
         messages.error(request,"Passwords Didn't Matched")
         return redirect('home')
      else:    
       user=User.objects.create_user(username=email,first_name=firstname,last_name=lastname,email=email,password=pass2)
       messages.success(request,"Account Created Successfully")
       login(request,user)
       return redirect('user_info_form')
   return render(request,'home.html')    

def handle_logout(request):
     logout(request)
     messages.warning(request,"Logged Out Successfully")
     return redirect('home')

def calc_protein(weight,activity_level):
   al={
             'Sedentary':0.8,
             'Lightly Active':1,
             'Moderately Active':1.4,
             'Very Active':1.7,
             'Super Active':2
          }
   protein=round(weight*al[activity_level])
   return protein

def calc_calorie(goal,weight,height_cm,age,activity_level,gender):
        al = {
            'Sedentary': 1.2,
            'Lightly Active': 1.375,
            'Moderately Active': 1.55,
            'Very Active': 1.725,
            'Super Active': 1.9
        }

        weight = float(weight)
        height_cm = float(height_cm)
        age = int(age)

        if (gender == 'Male'):
            bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
        
       
        tdee = bmr * al[activity_level]
       
        if (goal == 'Maintain'):
            calorie_req = round(tdee)
       
        elif (goal == 'Lose Weight'):
            calorie_req =round(tdee - 500)
        
        else:
            calorie_req =round(tdee + 500)
  
        return calorie_req   

def calc_bmi(weight,height_m):
     bmi =round(weight / (height_m * height_m),1)  
     return bmi   
        
   
def check_reset_data(userinfo):
   print(1)
   last_updated_date=userinfo.date_update
   date_today=timezone.localdate()
   if(date_today!=last_updated_date):
      userinfo.protein_eaten=0
      userinfo.calorie_eaten=0
      userinfo.nutrition={}
      userinfo.date_update=date_today
      userinfo.save()


def user_info_form(request):
     if request.method=='POST':
        gender=request.POST.get('gender')
        age=request.POST.get('age')
        weight=float(request.POST.get('weight'))
        height_m=float(request.POST.get('height_m'))
        height_cm=float(request.POST.get('height_cm'))
        activity_level=request.POST.get('activity_level')
        goal=request.POST.get('goal')
        userinfo=UserInfo.objects.create(user=request.user,gender=gender,age=age,weight=weight,h1=height_m,h2=height_cm,activity_level=activity_level,goal=goal)
        protein=calc_protein(weight,activity_level)
        calorie=calc_calorie(goal,weight,height_cm,age,activity_level,gender)
        bmi=calc_bmi(weight,height_m)
        userinfo.bmi_req=bmi
        userinfo.calorie_req=calorie 
        userinfo.protein_req=protein
        userinfo.save()
        return redirect('home')
      
     return render(request,'user_info_form.html')
 
def handle_update(request,path):
  
    if request.method=='POST':
        gender=request.POST.get('gender')
        age=request.POST.get('age')
        weight=float(request.POST.get('weight'))
        height_m=float(request.POST.get('height_m'))
        height_cm=float(request.POST.get('height_cm'))
        activity_level=request.POST.get('activity_level')
        goal=request.POST.get('goal')
        protein=calc_protein(weight,activity_level)
        calorie=calc_calorie(goal,weight,height_cm,age,activity_level,gender)
        bmi=calc_bmi(weight,height_m)
        UserInfo.objects.filter(user=request.user).update(gender=gender,age=age,weight=weight,h1=height_m,h2=height_cm,activity_level=activity_level,protein_req=protein,calorie_req=calorie,bmi_req=bmi)
        messages.success(request,'Information Updated')
        if path == 'home':
         return redirect('home')
        else:
         return redirect(f'/{path}/')
    userinfo=UserInfo.objects.get(user=request.user)
    
    return render(request,'update_form.html',{'userinfo':userinfo,'current_path': path})


def handle_protein(request):
    check_info_btn = False
    add_food_btn = False
    flag = False
    protein = 0
    calorie = 0
    dishname = ""
    serving=""

    if request.method == "POST":
        userinfo = UserInfo.objects.get(user=request.user)
        dishname = request.POST.get("dishname").strip()
        sub_btn = request.POST.get("sub_btn") 
        nutrition = userinfo.nutrition or {}
        food = NutritionalData.objects.filter(food_name=dishname).first()

        if food:
            protein = food.protein
            calorie = food.calorie
            serving=food.serving_size
            
            if sub_btn == 'check_info':
                check_info_btn = True
            
            else:
                add_food_btn = True
                p_val = float(protein)
                c_val = float(calorie)
                if food.food_name in nutrition:
                    nutrition[food.food_name] = {
                        'protein': round(p_val+ nutrition[food.food_name]['protein'],1),
                        'calorie': round(c_val + nutrition[food.food_name]['calorie'],1),
                        'serving_size': serving,
                        'qty':nutrition[food.food_name]['qty']+1
                    }
                else:
                    nutrition[food.food_name] = {
                        'protein': round(float(protein), 1),
                        'calorie': round(float(calorie), 1),
                        'serving_size': serving,
                        'qty':1
                    }
                
                userinfo.nutrition = nutrition
                userinfo.protein_eaten = round(float(userinfo.protein_eaten) + p_val, 1)
                userinfo.calorie_eaten = round(float(userinfo.calorie_eaten) + c_val, 1)
                userinfo.save()
        else:
            flag = True
            messages.error(request, "Enter Proper Dishname Or Try Different Name")

    if request.user.is_authenticated:
        userinfo = UserInfo.objects.get(user=request.user)

        if not check_info_btn and not add_food_btn and not flag:
            check_reset_data(userinfo)
            userinfo.refresh_from_db()

        food_nutri = userinfo.nutrition.items()
        
        if userinfo.protein_req > 0:
            protein_width = (userinfo.protein_eaten / userinfo.protein_req) * 100
        else:
            protein_width = 0

        if check_info_btn:
            return render(request, 'protein.html', {
                'userinfo': userinfo,
                'food_nutri': food_nutri,
                'protein_width': protein_width,
                'protein': protein,
                'dishname': dishname,
                'serving_size':serving,
                'flag': True
            })

        return render(request, 'protein.html', {
            'userinfo': userinfo,
            'food_nutri': food_nutri,
            'protein_width': protein_width
        })

    return render(request, 'protein.html')
  
def handle_bmi(request):
   if request.method == "POST":
         weight=float(request.POST.get("weight"))
         h1=float(request.POST.get("height_m"))
      
         bmi =calc_bmi(weight,h1)
         bmi=calc_bmi(weight,h1)
         rem_class=True

         if request.user.is_authenticated:
            userinfo=UserInfo.objects.get(user=request.user)
            userinfo.h1=h1
            userinfo.h2=h1*100
            userinfo.weight=weight
            userinfo.bmi_req=bmi
            userinfo.protein_req=calc_protein(userinfo.weight,userinfo.activity_level)
            userinfo.calorie_req=calc_calorie(userinfo.goal,userinfo.weight,userinfo.h2,userinfo.age,userinfo.activity_level,userinfo.gender)
            userinfo.save()
         else:
            
            return render(request,'bmi.html',{'calculated_bmi':bmi,'rem_class':rem_class})

   if request.user.is_authenticated:
       userinfo=UserInfo.objects.get(user=request.user)
       return render(request,'bmi.html',{'userinfo':userinfo})

  
   return render(request,'bmi.html')

def handle_calorie(request):
      check_info_btn=False
      add_food_btn=False
      flag=False
      calorie=0
      protein=0
      dishname=""
      serving=""
      if request.method == "POST":
         userinfo=UserInfo.objects.get(user=request.user)
         dishname = request.POST.get("dishname").strip()
         sub_btn = request.POST.get("sub_btn")
        
         nutrition = userinfo.nutrition or {}
         nutritional_data=NutritionalData.objects.all()
         food = NutritionalData.objects.filter(food_name=dishname).first()
         
         if food:
            protein = food.protein
            calorie = food.calorie
            serving=food.serving_size
            if sub_btn=='check_info':
                check_info_btn=True
            else:
               add_food_btn=True
               p_val = float(protein)
               c_val = float(calorie)
               if food.food_name in nutrition:
                  nutrition[food.food_name] = {
                           'protein': round(p_val+nutrition[food.food_name]['protein'],1),
                           'calorie': round(c_val+nutrition[food.food_name]['calorie'],1),
                           'serving_size': serving,
                           'qty':nutrition[food.food_name]['qty']+1
                     }
               else:
                  nutrition[food.food_name] = {
                           'protein': round(protein,1),
                           'calorie': round(calorie,1),
                           'serving_size': serving,
                           'qty':1
                     }
               userinfo.nutrition = nutrition
               userinfo.protein_eaten = round(float(userinfo.protein_eaten) + p_val, 1)
               userinfo.calorie_eaten = round(float(userinfo.calorie_eaten) + c_val, 1)
               userinfo.save()
         else:
            flag=True
            messages.error(request,"Enter Proper Dishname Or Try Different Name")
         
   
            

      if request.user.is_authenticated:
         userinfo=UserInfo.objects.get(user=request.user)

         if check_info_btn == False and add_food_btn == False and flag == False: 
              check_reset_data(userinfo)
              userinfo.refresh_from_db()

         food_nutri = userinfo.nutrition.items()
         
         calorie_width = (userinfo.calorie_eaten / userinfo.calorie_req) * 100

         if  check_info_btn:
            return render(request,'calorie.html',{'userinfo':userinfo,'food_nutri':food_nutri,'calorie_width': calorie_width,'calorie':calorie,'dishname':dishname,'serving_size':serving,'flag':check_info_btn})

         
         return render(request,'calorie.html',{'userinfo':userinfo,'food_nutri':food_nutri,'calorie_width': calorie_width})          
      
      return render(request,'calorie.html')
  



def handle_delete(request,item_name,path):
    
    userinfo=UserInfo.objects.get(user=request.user)
    dish_nutri=userinfo.nutrition[item_name]
    protein=0
    calorie=0
    
    for items in dish_nutri:
         if(items=='protein'):
           protein=Decimal(dish_nutri[items])
         elif (items=='calorie'):
           calorie=Decimal(dish_nutri[items])
   
    protein_eaten=userinfo.protein_eaten
    calorie_eaten=userinfo.calorie_eaten
    protein_eaten-=protein
    calorie_eaten-=calorie
    userinfo.protein_eaten=protein_eaten
    userinfo.calorie_eaten=calorie_eaten
    del userinfo.nutrition[item_name]
    userinfo.save()

    if "CalculateCalorie" in path:
      return redirect('handle_calorie')
    else:
      return redirect('handle_protein')
    

def delete_account(request):

     user=request.user
     user.delete()
     messages.success(request, "Account Deleted")
     return redirect('home')
  