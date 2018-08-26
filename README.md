# WP Google Maps Bulk Editor

This repository provides the capability of making bulk changes to maps in WP Google Maps. It was developed to satisfy a client's need to make identical, but considerable changes to every map in her WordPress site, while the developer did not have access to that sites backend. The scripts contained here automate that process.

## To get data

* Run a local server: `python3 -m http.server --bind localhost --cgi 8000`
* Go to the webpage where the form is you'd like to retrieve data from
* Change the form action to send the data to http://localhost:8000/cgi-bin/get-form-data.py
* Submit the form (you will be redirected to a view of the json)
* The form data will be loaded in /data/formData.csv

## To update the data

* Open a CSV editor to make your changes for the bulk upload (ie. Microsoft Excel, LibreOffice Calc, or Google Sheets)
* The CSV maps values to their HTML form name. You may need to inspect the form page to find the input name.
* Change the fields you want to update (the script does not allow you to bulk update the Map Title)

## Create an environments file

* USERNAME = WordPress admin username
* PASSWORD = WordPress admin password
* LOGIN_URL = WordPress login URL (\<base site URL\>/wp-login.php)
* MAPS_URL = WP Maps url for the website (\<base site URL\>/wp-admin/admin.php?page=wpgmp_manage_map)

## To Run the Script

* Open a terminal
* Run `python3 WP-Maps-Editor.py`