---
title: Adafruit Raspberry Pi repository
subtitle: DEPRECATED
author: Gary Dalton
date: 7 September 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_ada_repo.md -o rpi_ada_repo.html
tags: rpi, adafruit, repository
---
[Home](index.html)

# Description

*DEPRECATED: I NO LONGER USE THIS PROCEDURE*

(optional) The [Adafruit repository](https://learn.adafruit.com/apt-adafruit-com/overiew) provides access to the most recent node packages and to a few other goodies useful to makers.

1. Become root, `sudo -i`.
2. Add the repository to the sources file, `echo "deb http://apt.adafruit.com/raspbian/ release main" >> /etc/apt/sources.list`. Replace _release_ with the current stable release. In Jan2016, it is jessie.
3. Add the repository key, `wget -O - -q https://apt.adafruit.com/apt.adafruit.com.gpg.key | apt-key add -`.
4. `apt-get update`.
5. Exit root, `exit`.
