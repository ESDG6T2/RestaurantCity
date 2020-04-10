# How to deploy docker#
# Before you begin,
    1) make sure docker is installed
	2) run docker as administator
	3) run WampServer as administator
	4) create an alias on WampServer to this directory. You may follow the guide in the link: https://www.techrepublic.com/blog/smb-technologist/create-aliases-on-your-wamp-server/
    5) Go to phpmyadmin and import all SQL files in the sql folder.

# directory
./cart/
    cart.py (microservice)
    Dockerfile
    requirements.txt
./delivery/
    delivery.py (microservice)
    Dockerfile
    requirements.txt
./feedback/
    feedback.py (microservice)
    Dockerfile
    requirements.txt
./menu/
    menu.py (microservice)
    Dockerfile
    requirements.txt
./monitoring/
    monitoring.py (microservice)
    Dockerfile
    requirements.txt
./order/
    order.py (microservice)
    Dockerfile
    requirements.txt
./order_flask/
    order_flask.py (microservice)
    Dockerfile
    requirements.txt
./payment/
    payment.py (microservice)
    Dockerfile
    requirements.txt
./paypal_app/
    paypal_app.py (microservice)
    Dockerfile
    requirements.txt
    ./templates
        index.html
./rabbitmq/
    Dockerfile (to build rabbitmq image)
./sql
    cart.sql (cart db)
    feedback.sql (feedback db)
    menu.sql (menu db)
    order.sql (order db)
    user_creation.sql (create db user into order to access the db)
./telegram_bot
    telegram_bot.py (microservice)
    Dockerfile
    requirements.txt
./templates (all the webpages, css, img, and vendor)
./docker-compose.yml
./README.txt
	
# Begin
- Open cmd and locate to the directory of this README file
- Enter the cmd "docker-compose up --build" to start docker compose file
- It will take sometime during the first time
- After you see all of the docker logs in the command prompt, this means that your docker network is running.
e.g. 
delivery_1      |  * Serving Flask app "delivery" (lazy loading)
delivery_1      |  * Environment: production
delivery_1      |    WARNING: This is a development server. Do not use it in a production deployment.
delivery_1      |    Use a production WSGI server instead.
delivery_1      |  * Debug mode: on
delivery_1      |  * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
delivery_1      |  * Restarting with stat
delivery_1      |  * Debugger is active!
delivery_1      |  * Debugger PIN: 121-799-828

- open the webpages from the template folder in the current directory (./template)
./template/restaurant_ui.html for customer ordering UI
./template/delivery_ui.html for driver UI
./template/business_ui.html for restaurant business side UI

# Now you can access all of the webpages #
- For Paypal Account
    - Username: gladwin@test.com
    - Password: gladwinn
- For telegram bot (NOTE: Only one user can be running telegram_bot microservice at a time. If the Telegram Bot is not replying messages, it means that someone else is running the microservice)
    - @restaurant_city_bot
    - Press start
    - type /check_status
    - should see this reply : Please enter your userid starting with @ (e.g. @userid)
    - type @a (a is our preset userid for this project as we are not doing account management)
    - should see this reply : a list of message on the order items (check against the database to ensure that it is the same)
- NOTICE
    - sometimes there might be a slight lag after you select "Continue to checkout" in the cart tab. It is suppose to lead you to paypal payment page, but we have notice a certain
        lag in one of our tester's laptop (out of 6) and it will display an error related to "decoder.... error". There is two different ways to fix it: 1)Wait for awhile and try a few times
        2)re run the docker-compose.yml (Ctrl+C and docker-compose down)

* For Testers *
* Run through the full process to check for any bugs or error and report it in the group.
* Do checks for all 3 UI

# How to stop docker #
- open the docker-compose command prompt window that is running and press ctrl C to stop the containers. Wait for all container status to display done and it should 
    allow you to enter a input
- IMPORTANT STEP: type docker-compose down to delete all container and network from docker (might slow down some of your computer if you didn't stop it P.S. Happened to me LOL)

# THE END #



