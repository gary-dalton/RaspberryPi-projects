---
title: SSH Hints and Advanced
subtitle: Advanced usage with hints and tricks for leveraging SSH
author: Gary Dalton
date: 6 March 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html ssh.md -o ssh.html
tags: rpi, setup, guide, secure, ssh
---
[Home](index.html)

# Description

SSH is very important for improved security when connecting to your pi. There are some unusual problems that may occur which are addressed in the _Hints_ section. The _Advanced and Optional_ section provides guidance to some more advanced SSH settings and methods. Some of these are for improved security and should not really be considered optional.

# Overview

## Advanced and Optional Overview

1. [Improving security](#1)
2. [Basic SSHd configuration](#2)
3. [SSH key authentication](#3)
4. [Public key SSHd configuration](#4)

## Hints Overview

### <a name="Chrome"></a>Chrome Browser App

+ [Remove SSH known_hosts](#Chrome_01)

# Advanced and Optional Procedures

## <a name="1"></a>Improving security

Some general rules to security are:

* Do not use default passwords
* Use multifactor authentication
* Do not provide shell access unless it is needed
* Do not provide services you do not need
* Do not needlessly expose services
* Apply security patches
* Prevent physical access
* Use quality cryptology

## <a name="2"></a>Basic SSHd configuration

There are a few SSHd configuration changes that will improve SSH security. Since SSHd is likely a service you do want to provide and it gives shell access, this is important.

+ Edit the configuration file, `sudo nano /etc/ssh/sshd_config`
+ Change the following:
```
PermitRootLogin no
```
+ Add the following:
```
AllowUsers pi
# Even better if you use a non-default user
```

## <a name="3"></a>SSH key authentication

Using public key authentication will greatly improve your SSHd security but sometimes seems complicated. Do it anyways.

### Linux

1. Generate a password protected key pair, `ssh-keygen`.
2. You will be asked the name of the key file and the password to unlock the key. I usually name my key file according to the system it is used to connect to. The process should look something like this:
```
Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa): /home/user/.ssh/id_rsa_hostname
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/user/.ssh/id_rsa_hostname.
Your public key has been saved in /home/user/.ssh/id_rsa_hostname.pub.
The key fingerprint is:
ac:6a:0f:32:2e:bd:aa:3d:46:cc:c0:21:cc:68:47:40 user@computer
The key's randomart image is:
+---[RSA 2048]----+
|=Eo.             |
|o= .             |
|+ o              |
|..     .         |
| +      S        |
|  +    .         |
| oo . .          |
|.o+o.o           |
|++++...          |
+-----------------+
```
3. Copy your public key to the pi, `ssh-copy-id -i ~/.ssh/id_rsa_hostname.pub pi@hostname.local`.
4. You should see something like the following and also be asked for your password.

```
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
pi@hostname.local's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'pi@hostname.local'"
and check to make sure that only the key(s) you wanted were added.
```

* Go ahead and `ssh 'pi@hostname.local`. You should be asked for the password for your key.

An excellent resource for learning more is from [archlinux](https://wiki.archlinux.org/index.php/SSH_keys)

### Windows PuTTY

1. Start **PuTTYgen**
2. Change the _Number of bits in a generated key_ to 2048.
3. Click **Generate** to generate a new key pair.
4. Add a password to the _Key passphrase_ and _Confirm passphrase_.
5. Save your public and private keys. The private key should not be shared but the public key may be freely shared.
6. On the pi,
    - `mkdir ~/.ssh`
    - `nano ~/.ssh/authorized_keys`.
7. Copy the public key from the Windows PuTTYgen box and paste it into the authorized_keys file on your pi. Save the file.
8. Close PuTTYgen.
9. Open PuTTY.
10. Save a new session named _hostname_ and put _hostname.local_ in the Host Name box.
11. From the configuration Categories, select Connection >> SSH >> Auth.
12. Browse to select the private key you created earlier for authentication.
13. Save the session.
14. Test by clicking Open.
15. You should be required to enter in the username to log in with and also the password used to protect the key.

**NOTE: Do not lose your private keys. Once the next configuration steps are complete, your private key and password are required to login remotely.** You will still be able to login from the console or with a keyboard and monitor.

## <a name="4"></a>Public key SSHd configuration

Time now to only allow remote logins using public key authentication. This configuration is on your pi.

1. Open the file, `sudo nano /etc/ssh/sshd_config`
2. Add the following lines to the file and save:
```
PasswordAuthentication no
ChallengeResponseAuthentication no
UsePAM no
PubkeyAuthentication yes
```
3. Reload the sshd configuration, `sudo service sshd reload`
4. Test by trying to login without the key file.

# Hints

### <a name="Chrome_01"></a>Remove SSH known_hosts

_for Chrome app Secure Shell_

When working with pies in a closed network, there are times when the host identification will change. When that happens, attempts to connect using the Secure Shell app will fail with the following message:

    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
    Someone could be eavesdropping on you right now (man-in-the-middle attack)!
    It is also possible that a host key has just been changed.
    The fingerprint for the ECDSA key sent by the remote host is
    d6:be:12:7e:22:23:c3:e1:56:30:d6:cd:65:b7:ab:42.
    Please contact your system administrator.
    Add correct host key in /.ssh/known_hosts to get rid of this message.
    Offending ECDSA key in /.ssh/known_hosts:7
    ECDSA host key for xxxxxxxxxxxxx.yyy.au has changed and you have requested strict checking.
    Host key verification failed.
    NaCl plugin exited with status code 255.
    (R)econnect, (C)hoose another connection, or E(x)it?

This can only be fixed by removing the offending key. Make note of the number shown at the end of the line, _Offending ECDSA key in /.ssh/known_hosts:7_. That number depends on your system and is the index of the offending key.

+ Open the JavaScript console, `CTRL +Shift +J`
+ Enter `term_.command.removeKnownHostByIndex(INDEX);` into the console. Replace _INDEX_ by the index of your offending key.
+ Clear all host keys with `term_.command.removeAllKnownHosts();`

_from [gaggl](https://www.gaggl.com/2015/07/chromeos-removing-ssh-known_hosts-from-chromebook/)_
