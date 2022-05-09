
class product:
    def __init__(self,tp=10):
        self.totalproducts=tp
        
    def searchproducts(self,prod_name): #if we want to search particular product
        self.prod_name=prod_name
        with open('products.txt','r')as m:  #opening file having product details other than stock
            n=m.readlines()
            for line in n:
                t=eval(line)
                if self.prod_name in t:
                    return t    #returning product name, price and product id of the searched product
            if self.prod_name not in t :
                print()
                print('we have no product of this name') #in case person exits the add items corner or the searched item in not present in the list
                return None
            m.close()
            
            
    def chkstock(self,n): #if we need to check stock only
        self.prod_name=n
        with open('stock.txt','r')as tl: #opening file having stock of products
            st=tl.readlines()      #reading file
            for line in st:
                op=eval(line)
                if self.prod_name in op:
                    return op[self.prod_name]  #returning stock of the searched product
            if self.prod_name not in op:  # if searched product name cannot be found in the defined list
                return None  
        
        
    def chkproductdetails(self,prod_name): #if we want to know all details of product with stock
        ta=product.searchproducts(self,prod_name)
        if ta==None:
            print('no stock!')
        elif ta!=None:
            print('product=',self.prod_name)
            print('price=',ta[1])
            print('product_ID=',ta[2])
            fs=product.chkstock(self,prod_name)   #calling chkstock function to have stock of the searched product
            if fs!=None:
                print('stock is=',fs)
        
            
    def additems(self): #for updating products
        for i in range(self.totalproducts):
            print()
            name=input('enter name of product=')  #taking input details of the new items to add to the list
            price=float(input('enter unit price='))
            stock=int(input('enter stock of this product='))
            id_=int(input('enter product ID='))
            print()
            dic={name:stock}
            with open('stock.txt','a')as g:  #storing stock as dictionary in seperate file
                g.write(str(dic)+'\n')
                g.close()
            with open('products.txt','a')as f: #storing product name, price and product id in another file
                p=[name,price,id_]
                p=str(p)
                f.write(p+'\n')
                f.close()





class ShoppingCart(product):
    items_info={}  #each product information with quantity
    items_price={}  # price according to the quantity of each product in the cart
    price_tot=0  #subtotal of the cart
    
    def showproducts(self): #function to show products list of items when the user wants to buy products
        with open('products.txt')as f: 
            lst=[]  #getting the product details to write them in a proper way
            x=f.readlines()   #reading whole file
            for line in x:
                j=line.split(',')
                lst.append(j)
            f.close()
            print('AVAILABLE PRODUCTCS')
            print('Here are the products with their prices!')
            print('choose from the following items')
            print()  # adding print statements to present the application in a beautiful manner
            for i in range(len(lst)):
                first=str(lst[i][0])
                print('product',i+1,'='+first.replace('[',''),end='') #printing list of items in a better way with every product's price
                print('and price is'+lst[i][1])

                
    def additems(self):  #adding items in the cart
        ShoppingCart.showproducts(self)  # calling function to show list of products first to the user
        delete={}  #initializaing dictionary to update the items stock and write new dictionary in the file
        while True:
            print()
            print('you will be taken to main display if we dont have the required product available\nOR if you want to exit by yourself enter q or Q')
            print()
            print('enter product name to add item in the cart')
            a=input()
            b=super().searchproducts(a)  #search for the product first to check it's presence in the list
            if b==None or a=='q' or a=='Q':
                print('Taking you to the main display\nThankyou')
                print()
                break
            elif b!=None:
                print()
                print('product='+' '+b[0].replace('[',''))      
                print('price of'+' '+b[0].replace('[','')+' is'+' '+str(b[1]))     # after selecting product showing individual price for each product so the user would be known of price of product he is going to choose at every step
                print()
                try:
                    pq=int(input('enter required quantity='))   # taking input required quantity of the selected item
                except ValueError:    #exception if the user entered quantity other than in numbers
                    print('input only digits!')
                    break  
                mn=super().chkstock(a)   # calling function to check stock of the product (or availability) so to proceed further 
                if mn!=None:
                    if pq>mn or mn==0:
                        print('we have only'+str(mn)+b[0].replace('[',''))
                    else:
                        mnn=mn-pq  # minus the quantity bought by the user from the total quantity
                        dictionary={a:mnn}   # creating dictionary with the stock left to update it in the file
                        with open('stock.txt','r')as tk:
                            tp=tk.readlines()
                            for line in tp:
                                oy=eval(line)
                                delete.update(oy)  #taking all the products and their sock dictionary in this variable so we can delete and update in it and write in the file
                            tk.close()
                            delete.pop(self.prod_name)  #deleting that selected product 
                            delete.update(dictionary)  #updating product with the left wtock
                            with open('stock.txt','w')as z:  # opening file to write the updated stock dictionary in the file
                                for item in delete.items():
                                    kk='{'+"'"+item[0]+"'"+':'+str(item[1])+'}' 
                                    z.write(kk+'\n')
                                z.close()
                                lo=pq*b[1]  #calculating price for each product (quantity of each product * price for that product)
                                quantity={a:lo}  #taking in dictionary so we could update the above initialized dictionary
                                ShoppingCart.items_price.update(quantity)  #updating price per product dictionary
                                ShoppingCart.price_tot+=lo   # adding prices of the added products for subtotal
                                dictionary1={a:pq}   # taking in dictionary quantity of each product
                                if a in ShoppingCart.items_info: # in case if you have added before the same product so it would increase this time 
                                    tst=ShoppingCart.items_info[a]
                                    dictionary1={a:pq+tst}   #taking in same dictionary so if we have added some quantity before
                                ShoppingCart.items_info.update(dictionary1) #updating the above initialized dictionary for products and their quantity
                                print('subtotal=',round(ShoppingCart.price_tot,2))  #printing subtotal 
                
    def removeitem(self):
        remove={}   # initializing empty dictionary to have the previously contents in the stock file and rewrite them after updating 
        print('your current cart'+str(ShoppingCart.items_info))   #showing it so it will be easy for user to remove item by seeing the cart
        print()
        if ShoppingCart.items_info!={}:
            a=input('enter product name to be removed=') 
            for k in range(len(ShoppingCart.items_info)):
                if a in ShoppingCart.items_info:
                    c=ShoppingCart.items_info[a]   # searching for the product in the cart
                    print('for this item, you have added '+str(c)+' quantity in the cart') # informing user about the quantity of the product he added in the cart and wants to remove
                    print()
                    dd=int(input('enter quantity to remove='))
                    if dd>c:
                        print('ERROR!\nyou are removing more than the items you added')  # if user tries to remove more quantity than he had put in the cart
                        break
                    elif dd==0 or dd<0:
                        print('you dont want to remove anything?\ntaking you to the main display')  #if user enters 0 in the quantity to remove
                        print()
                        break
                    elif dd<c or dd==c:
                        left=c-dd  # calcualting left quantity after removing the desired quantity of the product
                        if left==0:
                            ShoppingCart.items_info.pop(a)
                            for s in range(len(ShoppingCart.items_price)):
                                if a in ShoppingCart.items_price:
                                    ShoppingCart.items_price.pop(a)  # thats the user removed all the quantity of the mentioned product
                        else:
                            f={a:left}  # some quantity left after removing the desired quantity, placing in dictionary so that it can be updated in the stock and product information dictionary
                            for tu in range(len(ShoppingCart.items_info)):
                                if a in ShoppingCart.items_info:
                                    ShoppingCart.items_info.pop(a)     #first removing the quantity present before
                                    ShoppingCart.items_info.update(f)  #updating dictionary with the new quantity
                                    break
                        mm=super().searchproducts(a)            #calling searchproducts function to know price of the removed product so we can subtract the price of the removed quantity
                        if mm=='None':
                            print('taking you to the main display!')
                            break
                        else:
                            mm=float(mm[1])
                            lp=dd*mm     # removed quantity price
                            lt=left*mm    # price of left quantity in the cart
                            fg={a:lt}      #making dictionary to update in the cart after removing desired quantity
                            for q in range(len(ShoppingCart.items_price)):
                                    if a in ShoppingCart.items_price:
                                        ShoppingCart.items_price.pop(a)  # removing already present quantity 
                                        ShoppingCart.items_price.update(fg) # updating quantity in the dictionary
                                        break
                            ShoppingCart.price_tot-=lp  # subtracting from subtotal
                            fst=super().chkstock(a)  # calling this function to update stock 
                            if fst!=None:
                                add=fst+dd   #adding into the stock available as the user has removed desired quantity
                                dictionaryy={a:add}  # making dictionary so to update the stock
                                with open('stock.txt','r')as tp:  # opening stock file to have all the contents 
                                    ts=tp.readlines()
                                    for line in ts:
                                        ozz=line.strip()
                                        ozz=eval(ozz)
                                        remove.update(ozz)  # storing contents of the file in above initialized dictionary 
                                    tp.close()
                                    remove.pop(self.prod_name)  # removing that particular product whose stock has chnaged
                                    remove.update(dictionaryy)  # finally updating it with the updated stock
                                    with open('stock.txt','w')as yz:  # again opening to write the updated dictionary of the products with the updated stock
                                        for item in remove.items():
                                            jk='{'+"'"+item[0]+"'"+':'+str(item[1])+'}'
                                            yz.write(jk+'\n')
                                        yz.close()
                                    print('items in cart right now are'+str(ShoppingCart.items_info)+' products and their quantity ')   #showing it again after removing items so that user can see he has reemoved that product
                                    print()
                                    break
                else:
                    print('we have no product of this name')
                    break
        else:
            print('Your cart is empty\nTaking you to the main display')
            print()

            
class useraccount:
    def enterinfo(self):
        self.n=input('enter your first name=')   # taking user's personal information for creating account
        self.m=input('enter your last name=')
        self.e=input('enter your email address=')
        self.address=input('enter address=')
        self.password=input('enter a strong password=')
        with open('userinfo.txt','a')as k:   
            l=[self.n,self.m,self.e,self.address]
            l=str(l)
            k.write(l+'\n')        # writing personal information only in this file for each user
            k.close()
        return [self.n,self.m,self.e,self.address]

    
    def accountholderslist(self):
        lst=[]  # initializing list to hold information for every account holder
        count=0  # for the serial number of the account holders
        with open('userinfo.txt','r')as accholder: 
            ach=accholder.readlines()
            for line in ach:
                bcd=line.strip()
                bcd=bcd.split(',')
                lst.append(bcd)
            print('S:NO   FIRST NAME  LAST NAME      EMAIL                                 ADDRESS')
            for record in lst:
                count+=1
                print(f'{count:10}{record[0]:20}{record[1]:20}{record[2]:30}{record[3]:35}')
                print()




class checkout:
    def cartdetails(self):
        gh=ShoppingCart()
        f=gh.items_info
        p=gh.items_price
        r=gh.price_tot
        return f,p,r

    
    def clearcart(self):  # function will be called after checkout so the cart could become empty
        sh=ShoppingCart()
        ShoppingCart.items_info={}
        ShoppingCart.items_price={}
        ShoppingCart.price_tot=0


    def history(self):
        print('do you want to check out?')
        abc=input('enter yes or YES to checkout')   # providing option to user so if he still wants to add/remove any product
        if abc=='yes' or abc=='YES':
            lo=checkout.cartdetails(self)
            if lo!=({}, {}, 0):  # if the user wants to checkout even after having empty cart
                v=useraccount()
                indi_info=v.enterinfo()   # calling function of user account class so user can create account at checkout
                print()
                print('details of products you bought')   # printing all the details of the cart after shopping 
                print('products with their quantity'+str(lo[0]))
                print('each product at the rate of'+str(lo[1]))
                print('your total amount='+str(lo[2]))
                print()
                with open('individualrecords.txt','a')as d: 
                    lm=[indi_info,lo[0],lo[1],lo[2]]
                    lm=str(lm)
                    d.write(lm+'\n')          # writing records for each user with his all information and shopping history when he check 
                    d.close()
                    d=checkout.clearcart(self)  # calling function to clear cart
            else:
                print('your cart is empty\ncan\'t checkout')
                return
        else:
            return



class interface:
    def __init__(self):
        print('WELCOME TO ONLINE SHOPPING STORE')
        print('***************************************')
        while True:
            print('ENTER\n1:to add items in the cart\n2: to remove item from the cart(if your cart is already empty you will be taken back here to main display)\n3: to view current cart\n4: to checkout\n5: to search particular user shopping history and other information\n6: to view list of account holders\n7:  to enter in administration account to add products to the list(you will be required password)\n8: to search any product details for admin only( password required)\n9: to check stock of any product (password required, for admin only)\n10: to exit the application')
            print()
            try:
                number=int(input('enter number='))
                print()
                if number==1:   # to add items
                    sc=ShoppingCart()
                    sc.additems()
                elif number==2:   # to remove items
                    sc=ShoppingCart()
                    sc.removeitem()
                elif number==3:   # to view cart
                    sc=ShoppingCart()
                    x=sc.items_info
                    y=sc.items_price
                    z=sc.price_tot
                    print('items in cart right now are (product with quantity)=',x)
                    print('price per product present in your cart=',y)  # includes price for the quantity of each product present in the cart
                    print('sub total uptill now=',z)
                    print() 
                elif number==4:      # to chekout
                    sc=checkout()
                    sc.history()
                elif number==5:   # when anyone wants to search for particular person history
                    nametosearch=input('enter name to search history=')
                    with open('individualrecords.txt','r')as individual:
                        rec=individual.readlines()
                        for line in rec:
                            w=line.strip()
                            w=eval(line)
                            for i in range(len(w)):
                                if nametosearch in w[0]:
                                    print('USER DETAILS!')      # printing user information first 
                                    print('name:'+nametosearch+w[0][1])
                                    print('email:'+w[0][2])
                                    print('address:'+w[0][3])
                                    print()
                                    print('SHOPPING HISTORY')   # then printing shopping history 
                                    print('products and their quantity=',w[1])
                                    print('prices per product you bought=',w[2])
                                    print('total bill=',w[3])
                                    break
                elif number==6:  # to view list of account holders
                    j=useraccount()
                    j.accountholderslist()
                elif number==7:    # to add new products 
                    e=input('enter password to login to administration account=')
                    if e=='HAJRA072':
                        try:
                            total=int(input('enter number of products to add in the list='))
                            pr=product(total)
                            pr.additems()
                        except:
                            print('enter only integers!')
                    else:
                        print('SORRY! unauthorized login')
                elif number==8:    # to search details for any product
                    e=input('enter password to login to administration account=')
                    if e=='HAJRA072':
                        name=input('enter name of product to search for=')
                        print()
                        gt=product()
                        gt.chkproductdetails(name)
                        print()
                    else:
                        print('SORRY! unauthorized login')
                elif number==9:        # to check only stock of any product
                    login=input('enter password to login to administration account=')
                    if login=='HAJRA072':      # only admin knows this password 
                        stock=input('enter product to check stock for=')
                        print()
                        cst=product()
                        kp=cst.chkstock(stock)
                        print('stock of the given product is=',kp)
                        print()
                elif number==10:
                    sc=checkout()
                    cart=sc.cartdetails()  # calling this function to know if the cart is empty or not 
                    if cart!=({}, {}, 0):   # when user tries to exit application with filled shopping cart
                        print('you can\'t checkout!\nyour cart should be empty')
                        print()
                    else:
                        print('THANKYOU for choosing us!')
                        feedback=input('leave your feedback here=')
                        break
            except ValueError:
                print('enter digits only!')
                
c=interface()
