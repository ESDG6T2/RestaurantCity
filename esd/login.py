from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder="img")
CORS(app)

@app.route('/login')
def login():
    output='''<html>
    <head>
        <title>Login Page</title>
        <!-- jquery google CDN -->
        <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script>
    </head>
    <body>
        <form id='loginForm' action='mainPage' method='POST'>
            <table>
                <tr>
                    <td>UserID:</td><td><input id='userID' type='text' name='userID'></td><td id='userIdError'></td>
                </tr>
                <tr>
                    <td>Password:</td><td><input id='password' type='password' name='pwd'></td><td id='pwdError'></td>
                </tr>
            </table>
            <input type='submit' name='submitBtn'><div id='error'></div>
        </form>
    </body>
    <script>

        $("#loginForm").submit(async (event) => {
            //Prevents screen from refreshing when submitting
            
            event.preventDefault();
            var noErrorMsg= true;
            if ($('#userID').val().length === 0){
                $('#userIdError').text('Please enter User ID')
                noErrorMsg=false;
            }else{
                $('#userIdError').text('')
                var userID = $('#userID').val();
            }
            if ($('#password').val().length === 0){
                $('#pwdError').text('Please enter Password')
                noErrorMsg=false
            }else{
                $('#pwdError').text('')
                var pwd = $('#password').val();
            }
            if (noErrorMsg){
                var serviceURL = "http://127.0.0.1:5001/user";
                try {
                    const response =
                    await fetch(
                    serviceURL, { method: 'POST',headers: {
                        'Content-Type': 'application/json'
                        }, body:  JSON.stringify({userId :userID ,password:pwd}) 
                    });
                    const data = await response.json();
                    if (!response.ok){
                        $('#error').text(data.message);
                    }else{
                        $("#loginForm").unbind('submit').submit();
                    }
                    
                } catch (error) {
                        // Errors when calling the service; such as network error, 
                        // service offline, etc
                        // showError
                        $('#error').text('Server Error, please try again later.<br />'+error);
                    
                } 
            }

        })
    </script>
</html>'''
    return output

@app.route('/mainPage', methods=['POST'])
def mainPage():
    # retrieve value from form
    userID=request.form.get('userID')
    password=request.form.get('pwd')

    output='''
    <html>
        <head>
            <!-- jquery google CDN -->
            <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script>
        </head>
        <body>
            <h1>Restaurant City</h1>
            Welcome,'''+userID+'''
            <div id="main-container"">
                <form action='orderProcessing' method='POST'>
                    <input type='hidden' name='userID' value='''+str(userID)+'''>
                    <table id='menuTable' border='1'>
                        <tr>
                            <th>Menu ID</th><th>Food</th><th>Food Name</th><th>Price</th><th>Quantity</th>
                        </tr>
                    </table>
                    <input type='submit' name='submit'>
                </form>
                <h1>Locate Us!</h1>
                <iframe width="600" height="450" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/search?q=Stamford Road, SMU School of Information Systems, Singapore&key=AIzaSyCpukJ8bc2TwSB-4IuGp1sUjuZEF4-VVms" allowfullscreen></iframe>
            </div>
        </body>
    </html>
    <script>
        function showError(message) {
            // Hide the table and button in the event of error
            $('#menuTable').hide();

            // Display an error under the main container
            $('#main-container')
                .append("<label>"+message+"</label>");
        }
        $(async() => {           
                // Change serviceURL to your own
                var serviceURL = "http://127.0.0.1:5001/menu";
            
                try {
                    const response =
                    await fetch(
                    serviceURL, { method: 'GET' }
                    );
                    const data = await response.json();
                    var menu = data.Menu; //the arr is in data.menu of the JSON data
                    console.log(menu)
                    // array or array.length are falsy
                    if (!menu || !menu.length) {
                        showError('Menu list empty or undefined.')
                    } else {
                        // for loop to setup all table rows with obtained book data
                        var rows = "";
                        for (const item of menu) {
                            eachRow =
                                "<td>" + item.menuId + "</td>" +
                                
                                "<td><img src='img/"+item.menuId+".jpg' height='100' width='100'></td>" +
                                "<td>" + item.foodName + "</td>" +
                                "<td>" + item.price + "</td>"+
                                "<td> <select name="+item.menuId+">";
                                for (i=0;i<=20;i++){
                                    eachRow+='<option value='+i+'>'+i+'</option>';
                                }
                                eachRow+="</select></td>";
                            rows += "<tr>" + eachRow + "</tr>";
                        }
                        // add all the rows to the table
                        $('#menuTable').append(rows);
                    }
                } catch (error) {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    showError
                    ('There is a problem retrieving books data, please try again later.<br />'+error);
            
            } // error
        });
    </script>'''

    return output

@app.route('/orderProcessing', methods=['POST'])
def OrderProcessing():
    # retrieve value from form
    userID=request.form.get('userID')
    requestField=request.values
    menuID={}
    for key,item in requestField.items():
        if key[0]=='F' and item!='0':
            menuID[key]=item
    output='''
    <html>
        <head>
            <!-- jquery google CDN -->
            <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script>
        </head>
        <body>
            <h1>Restaurant City</h1>
            <div id="main-container"">
                <form id='orderForm' action='Summary' method='POST'>
                    <input id='userID' type='hidden' name='userID' value='''+str(userID)+'''>
                    <table id='OrderTable' border='1'>
                        <tr>
                            <th>Menu ID</th><th>Food</th><th>Food Name</th><th>Price</th><th>Quantity</th><th>Subtotal</th>
                        </tr>
                    </table>
                    <table id='particulars'>
                        <tr>
                            <th>Billing Address</th><td><input id='billingAddress' type='text' name='billingAddress'></td><td id='billingAddressError'></td>
                        </tr>
                        <tr>
                            <th>Postal Code</th><td><input id='postalCode' type='text' name='postalCode'></td><td id='postalCodeError'></td>
                        </tr>
                        <tr>
                            <th>Contact of Person</th><td><input id='contactNo' type='text' name='contactNo'></td><td id='contactNoError'></td>
                        </tr>
                    </table>
                    <input type='submit' name='submitBtn'>
                </form>
            </div>
        </body>
    </html>
    <script>
        var MenuList={};'''
    for key,item in menuID.items():
        output+='''MenuList[\''''+key+'''\']='''+item+''';'''
    output+='''
        function showError(message) {
            // Hide the table and button in the event of error
            $('#OrderTable').hide();

            // Display an error under the main container
            $('#main-container')
                .append("<label>"+message+"</label>");
        }
        $(async() => {           
                // Change serviceURL to your own
                var serviceURL = "http://127.0.0.1:5001/menu";
                
                try {
                    const response =
                    await fetch(
                    serviceURL, { method: 'GET' }
                    );
                    const data = await response.json();
                    var menu = data.Menu; //the arr is in data.menu of the JSON data
                    // array or array.length are falsy
                    if (!menu || !menu.length) {
                        showError('Menu list empty or undefined.')
                    } else {
                        // for loop to setup all table rows with obtained book data
                        var rows = "";
                        var totalAmt=0.0;
                        var l=0;

                        for (const item of menu) {
                            if (item.menuId in MenuList){
                                eachRow =
                                    "<td>" + item.menuId + "</td>" +
                                    "<td><img src='img/"+item.menuId+".jpg' height='100' width='100'></td>" +
                                    "<td>" + item.foodName + "</td>" +
                                    "<td>" + item.price + "</td>"+
                                    "<td>"+MenuList[item.menuId]+"</td>"+
                                    "<td>"+MenuList[item.menuId]*item.price+"</td>";
                                totalAmt+=MenuList[item.menuId]*item.price
                                rows += "<tr>" + eachRow + "</tr>";
                            };   
                            l++;
                        }
                        if (rows==''){
                            rows+="<tr><th colspan='6'>No item selected</th></tr>";
                        }
                        rows+="<tr><th colspan='5' align='right'>Total Amount</th><td>$"+totalAmt+"</td></tr>";
                        // add all the rows to the table
                        $('#OrderTable').append(rows);
                    }
                } catch (error) {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    showError
                    ('Server Error, please try again later.<br />'+error);
            
            } // error
        });
        $("#orderForm").submit(async (event) => {
            //Prevents screen from refreshing when submitting
            var userID=$('#userID').val();
            event.preventDefault();
            var noErrorMsg= true;
            if ($('#billingAddress').val().length === 0){
                $('#billingAddressError').text('Please enter your billing address')
                noErrorMsg=false;
            }else{
                $('#billingAddressError').text('')
                var billingAddress = $('#billingAddress').val();
            }
            if ($('#postalCode').val().length === 0){
                $('#postalCodeError').text('Please enter Postal Code')
                noErrorMsg=false
            }else{
                $('#postalCodeError').text('')
                var postalCode = $('#postalCode').val();
            }
            if ($('#contactNo').val().length === 0){
                $('#contactNoError').text('Please enter Contact No')
                noErrorMsg=false
            }else{
                $('#contactNoError').text('')
                var contactNo = $('#contactNo').val();
            }
            if (noErrorMsg){
                var serviceURL = "http://127.0.0.1:5001/order";
                try {
                    const response =
                    await fetch(
                    serviceURL, { method: 'POST',headers: {
                        'Content-Type': 'application/json'
                        }, body:  JSON.stringify({userId :userID ,menuItem:MenuList, billingAddress:billingAddress, postalCode:postalCode, contactNo:contactNo}) 
                    });
                    const data = await response.json();
                    if (!response.ok){
                        showError(data.message);
                    }else{
                        $("#orderForm").unbind('submit').submit();
                    }
                    
                } catch (error) {
                        // Errors when calling the service; such as network error, 
                        // service offline, etc
                        showError('Server Error, please try again later.<br />'+error);
                } 
            }
        })
    </script>
    '''
    return output

if __name__ == "__main__":
    app.run(port=5000, debug=True)
