from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
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
                var userID = $('#userID').val();
            }
            if ($('#password').val().length === 0){
                $('#pwdError').text('Please enter Password')
                noErrorMsg=false
            }else{
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
                <form action='orderProcessing.html'>
                    <table id='menuTable' border='1'>
                        <tr>
                            <th>Menu ID</th><th>Food</th><th>Food Name</th><th>Price</th><th>Quantity</th>
                        </tr>
                    </table>
                    <input type='submit' name='submit'>
                </form>
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
                                
                                "<td><img src="+item.menuId+".jpg)}}' height='100' width='100'></td>" +
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

if __name__ == "__main__":
    app.run(port=5000, debug=True)
