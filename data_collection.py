# sanic import module
from sanic import text, Blueprint, json as Response, Sanic
from sanic.log import logger
from sanic.response import json
# general ins
import aiomysql
import json
import random
from twilio.rest import Client

    
#user_details_api
async def user_details(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #data request
    data = request.json
    #insert into db
    try:
        query = "INSERT INTO user_details (email_id,first_name,last_name,pass_word,phone_number,created_by,last_updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values=(data['email_id'],data['first_name'],data['last_name'],data['pass_word'],data['phone_number'],data['created_by'],data['last_updated_by'])
        #Execute the query
        await operator_my.execute(query, values)
        #Commit the changes
        await mysql_db.commit()
        return Response({'status':'success',"data":True,"msg":'Data inserted'},status = 200)
    except Exception as e:
        #Handle any errors that occur during the insertion
        return Response.json({'error': str(e)}, status=500)
    finally:
        # closing mysql connectors
        await operator_my.close()
        mysql_db.close()
        
 
#user_login_api
async def user_login(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #data request
    email_id= request.json.get('email_id')
    pass_word=request.json.get('pass_word')
    #search the data into db  
    data=await operator_my.execute(f"select email_id,pass_word from user_details where email_id='{email_id}' and pass_word='{pass_word}'")
    # closing mysql connectors
    await operator_my.close()
    mysql_db.close()
    if data==0:
        return Response({"status":"Failure","data":False,"msg":"Invalid username or password"},status = 500)
    else:
        return Response({'status':'success',"data":True,"msg":"Login Successfully"},status = 200)

   
#particular_user_info_api
async def user_info(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #data request
    email_id= request.json.get('email_id')
    #search the data into db  
    data=await operator_my.execute(f"select *from user_details where email_id='{email_id}'")  
    data = [json.loads(json.dumps([dict(zip(map(lambda x:x[0], operator_my.description),row)) for row in await operator_my.fetchall()],default = str))]
    # closing mysql connectors
    await operator_my.close()
    mysql_db.close()
    #login logic
    if len(data)== 0:
        return Response({"status":"Failure","data":False,"msg":"Invalid username or password"},status = 500)
    else:
        return Response({'status':'success',"data":True,"details":data},status = 200)
    
#overall_user_info_api
async def overall_info(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #user_id= request.json.get('user_id')
    #search the data into db  
    await operator_my.execute(f"select *from user_details")  
    data = [json.loads(json.dumps([dict(zip(map(lambda x:x[0], operator_my.description),row)) for row in await operator_my.fetchall()],default = str))]
    # closing mysql connectors
    await operator_my.close()
    mysql_db.close()
    #login logic
    if len(data)== 0:
        return Response({"status":"Failure","data":False,"msg":"No record found"},status = 500)
    else:
        return Response({'status':'success',"data":True,"details":data},status = 200)
        
    
#password_update_api
async def password_reset(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #data request
    email_id= request.json.get('email_id')
    old_password= request.json.get('pass_word')
    new_password=request.json.get('new_password')
    #search the data into db 
    try:  
        data= await operator_my.execute(f"select email_id,pass_word from user_details where email_id='{email_id}'and pass_word='{old_password}'")
        #update the data into db 
        if data == 1:
            mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
            operator_my = await mysql_db.cursor()
            await operator_my.execute(f"update user_details set pass_word='{new_password}' where email_id='{email_id}'")
            await mysql_db.commit()
            return Response({'status':'success',"data":True,"msg":'Password Updated'},status = 200)
        else:
            return Response({"status":"Failure","data":False,"msg":"Invalid username or password"},status = 500)
    except Exception as e:
        #Handle any errors that occur during the insertion
        return Response.json({'error': str(e)}, status=500)
    finally:
        # closing mysql connectors
        await operator_my.close()
        mysql_db.close()
       
#user_details_api
async def delete_user(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #data request
    email_id= request.json.get('email_id')
    data = await operator_my.execute(f"select  * user_details where email_id='{email_id}'")
    if data == 0:
        return Response({"status":"Failure","data":False,"msg":"Invalid username or password"},status = 500)
    else :
        try:
            host,port,username,password = list(request.app.config.database.values())
            # connecting to database
            mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
            operator_my = await mysql_db.cursor()
            await operator_my.execute(f"delete from user_details where email_id='{email_id}'")
            #Commit the changes
            await mysql_db.commit()
            return Response({'status':'success',"data":True,"msg":'Data inserted'},status = 200)
        except Exception as e:
            #Handle any errors that occur during the insertion
            return Response.json({'error': str(e)}, status=500)
        finally:
            # closing mysql connectors
            await operator_my.close()
            mysql_db.close()
            
            
#forgot_password_api   
async def forgot_password(request):
    temp=0
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #data request
    email_id= request.json.get('email_id')
    phone_number=request.json.get('phone_number')
    #search the data into db  
    await operator_my.execute(f"select phone_number from user_details where email_id='{email_id}' and phone_number='{phone_number}'")  
    data = [json.loads(json.dumps([dict(zip(map(lambda x:x[0], operator_my.description),row)) for row in await operator_my.fetchall()],default = str))]
    print(data)
    # closing mysql connectors
    await operator_my.close()
    mysql_db.close()
    #forgot logic
    if len(data) == 0:
        return Response({"status":"Failure","data":False,"msg":"No Email or Phone Number found"},status = 500)
    # Send OTP through phone
    else:
        #genrate OTP 
        otp=''.join([str(random.randint(0,9)) for i in range(6)])
        #store the OTP in temporary variable to compare
        global n
        n = otp
        #Send OTP
        account_sid = '____twilio account SID ____'
        auth_token = '______twilio auth token_________'
        client = Client (account_sid, auth_token)
        msg= client.messages.create(body = f"Your OTP is {otp}",from_="______ twilio number_______",to='data')
        return Response({'status':'success',"data":True,"msg":"OTP is sended to Phone number"},status = 200)
      
#otp_verfiy_api   
async def otp_verfiy(request):
    otp_number= request.json.get('otp_number')
    #function calling
    to_verfiy(otp_number)
    
    #otp_verfiy_function
    def to_verfiy(otp_number):
        if otp_number == 123455:
            return Response({'status':'success',"data":True,"msg":""},status = 200)
        else:
            return Response({"status":"Failure","data":False,"msg":"Invalid OTP Enter valid OTP"},status = 500)   

#fan_details_api
async def fan_status(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #user_id= request.json.get('user_id')
    #search the data into db  
    await operator_my.execute(f"select *from fan_details where stauts:'Active'")  
    data = [json.loads(json.dumps([dict(zip(map(lambda x:x[0], operator_my.description),row)) for row in await operator_my.fetchall()],default = str))]
    # closing mysql connectors
    await operator_my.close()
    mysql_db.close()
    #login logic
    if len(data)== 0:
        return Response({"status":"Failure","data":False,"msg":"No record found"},status = 500)
    else:
        return Response({'status':'success',"data":True,"details":data},status = 200)
    
#cooling_pad_status_api
async def cooling_pad_status(request):
    host,port,username,password = list(request.app.config.database.values())
    # connecting to database
    mysql_db = await aiomysql.connect(host=host, port=port,user=username, password=password,db = "zogx_test")
    operator_my = await mysql_db.cursor()
    #user_id= request.json.get('user_id')
    #search the data into db  
    await operator_my.execute(f"select *from heater_details where stauts:'Active'")  
    data = [json.loads(json.dumps([dict(zip(map(lambda x:x[0], operator_my.description),row)) for row in await operator_my.fetchall()],default = str))]
    # closing mysql connectors
    await operator_my.close()
    mysql_db.close()
    #login logic
    if len(data)== 0:
        return Response({"status":"Failure","data":False,"msg":"No record found"},status = 500)
    else:
        return Response({'status':'success',"data":True,"details":data},status = 200)