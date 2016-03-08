---
title: RPi NGINX Webserver
subtitle: Using the NGINX to serve static pages
author: Gary Dalton
date: 6 March 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_nginx.md -o rpi_nginx.html
tags: rpi, setup, guide, secure
---
[Home](index.html)

# Description

NGINX is an open source web server and reverse proxy that excels at large-scale web integration, application security, and web acceleration.

# Next up?

After reading this guide, you may be interested in reading:


# Overview

1. [Install NGINX](#1)
2. [Serve static content](#2)
3. [Conclusion](#Conclusion).


# Procedures

## <a name="1"></a>Install NGINX

+ `sudo apt-get install nginx`
+ Is it running? `sudo service nginx status`
+ Check if it is available,
    - locally, `links http://localhost/`
    - other device, browse to [http://192.168.84.1](http://192.168.84.1)
    - should see the _Welcome to nginx_ page

## <a name="2"></a>Serve static content

Your pi is all set to serve static content. The location of the files is **/var/www/html**.

+ `sudo nano /etc/nginx/sites-available/default`
    - Just after _root /var/www/html;_ add the line
        - `autoindex on;`
+ Add these Raspberry Pi guides
    - `cd /var/www/html`
    - `sudo git clone --branch gh-pages https://github.com/gary-dalton/RaspberryPi-projects.git rpi`
+ Download other resources
    - `mkdir resources`
    - `cd resources`
    - `sudo links https://www.ualberta.ca/~enoch/Readings/The_Art_Of_War.pdf`
    - `sudo wget "http://www.hackerhighschool.org/lessons/HHS_en1_Being_a_Hacker.v2.pdf"`


# <a name="Conclusion"></a>Save the image to a file

Now that you have spent all this time getting your Raspberry Pi set up just so, **save it to an image** for easy reuse. You will still have to change things like usernames, passwords, and hostnames.

Instead of writing a file image to the MicroSD, use the same software to read the MicroSD to a file image. Then when you are ready to spin up your next pi, it will be as easy as, well, pie.
