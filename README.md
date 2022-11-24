# uniwa-announcements-email
This python script gets new announcements from "http://www.ice.uniwa.gr/feed/" and sends them via email to a list of emails in a database.

For this to work you need to have a .env file containing the following environmental variables:
1. database-url: the url of the used database
2. database-key: the key of the used database
3. sender-email: the email you want to be used to send said emails
4. sender-password: the password of the before mentioned sender email

Extra information:
- The database must be of supabase postgreSQL type (see line 55 to change)
- The email must be of gmail type (see line 77 to change)

This project was a spur of the moment idea I ended up spending the day on.
Was some great python practise as well!
