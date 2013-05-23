#coding = 'utf-8'
from django.contrib.auth import authenticate,login,logout  
  
def login_view(request):      
    user = authenticate(username=request.POST['username'], password=request.POST['password'])  
    if user is not None:  
        login(request, user)      
        print request.user    
        return list_product(request)  
    else:  
        return store_view(request)  
  
def logout_view(request):  
    logout(request)  
    return store_view(request) 
