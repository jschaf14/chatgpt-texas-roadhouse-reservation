# chatgpt-texas-roadhouse-reservation
I used only code from ChatGPT to make this.

What it does:

This is a Texas Roadhouse reservation maker for the current day. Currently if you decided around 2:00 PM that you want to eat there with 4 people at 7:00 PM you would have to start checking the wait times around 4:30 PM and continually check them until eventually the wait time linus up with when you want to arrive. This is a tiresome process that a lot of the times has high unpredictability that might make you miss your mark. With this program it will do the checking and reserve for you so that all you have to think about is when you show up. It currently checks every 5 minutes but you can make it more often if your texas roadhouse wait times are more volatile.

How to run:

Navigate to the directory

run `source env/bin/activate` for Linux/Mackbook or run `.\env\Scripts\activate` on a windows

run `python -m http.server 8000` to spin up the frontend

run `python backend.py` to spin up the backend

Then navigate to localhost:8000 and input all the information needed for your reservation and leave the app running on your comupter until you get a text and email from texas roadhouse. 

***There is no validation please put in a valid email address and a 10-digit phone number! If these are wrong you won't be able to make your reservation!***

If you show up 15 minutes before or after your reservation time you should be able to text HERE back to them and be seated quickly.
