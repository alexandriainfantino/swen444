# swen444
# Gradebook

## Installation
Install pip (may need to run with `sudo`)
```
easy_install pip
```

Install Flask (may need to run with `sudo`)
```
pip install Flask
```

Install the project:

If you'd like to clone the repository from github:
```
git clone git@github.com:alexandriainfantino/swen444.git
```
or
```
git clone https://github.com/alexandriainfantino/swen444.git
```
Alternatively, if you'd like to download the zip, click `Clone or Download`, and click `Download Zip`. Then unzip the zip-file in the desired directory.

## Python version 2.7

### To run
Navigate into the directory that was just downloaded or unzipped (should be named `swen444`), and execute one of the following commands, where `[port number]` is an optional desired port number for the server to listen to:  
```
python donatoro.py [port number]
```
Next, open a web browser and go to `127.0.0.1:5000` if the port number is not specified, or `127.0.0.1:[port number]`, replacing `[port number]` wiht the port number passed in as a parameter.

There is also a hosted version of Donatoro available at [vm343f.se.rit.edu:5500](http://vm343f.se.rit.edu:5500/) for the remainder of the 2017 Spring semester.

##Default Login Info
###Login as a Charity Representative:
**Email**: charity@charity.com

**Password**: Password1

###Login as Donor:
**Email**: Johnny.Bravo@gmail.com

**Password**: Password

## [Official Flask Documentation](http://flask.pocoo.org)

## Currently Unsupported Features
1. Donors following charities.
2. Donors rating charities.
3. On the charity home page, the 'Timeline' and 'New Post' links do not function.
4. On login page, 'Remember Me' does not function.
5. Input validation. Some forms do not prompt user that field should be filled in before submitting. Others, such as email fields, do not enforce uniqueness.

##Available For Demonstration
1. Graphs on charity statistic page are modelled of hardcoded data instead of donation data.

## Bugs
1. On 'Profile - Payment' page, Alabama is automatically selected as the state for the new credit card.
