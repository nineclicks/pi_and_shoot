# Pi & Shoot

Install `ffmpeg`. Uses ffmpeg to convert png to whatever the framebuffer format is. fbi command was causing problems.

Screen is constantly calibrating, just touch all four corners the first time your run before using the menu.

Add user to gpio group, replace `user` with your username

```
sudo adduser user gpio
```

Add line to visudo, replace `user` with your username

```
user ALL=(ALL) NOPASSWD: /sbin/poweroff, /sbin/reboot, /sbin/shutdown
```
