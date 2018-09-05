title: Linux-杀死进程
date: 2016-07-06 22:06:39
categories: linux
tags: linux
---

### 用ps命令查看进程

### ps -ef
<!--more-->
```
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 7月05 ?       00:00:02 /sbin/init splash
root         2     0  0 7月05 ?       00:00:00 [kthreadd]
root         3     2  0 7月05 ?       00:00:16 [ksoftirqd/0]
root         5     2  0 7月05 ?       00:00:00 [kworker/0:0H]
root         7     2  0 7月05 ?       00:00:18 [rcu_sched]
root         8     2  0 7月05 ?       00:00:00 [rcu_bh]
root         9     2  0 7月05 ?       00:00:00 [migration/0]
root        10     2  0 7月05 ?       00:00:00 [watchdog/0]
root        11     2  0 7月05 ?       00:00:01 [watchdog/1]
root        12     2  0 7月05 ?       00:00:00 [migration/1]
root        13     2  0 7月05 ?       00:00:10 [ksoftirqd/1]
root        15     2  0 7月05 ?       00:00:00 [kworker/1:0H]
root        16     2  0 7月05 ?       00:00:00 [kdevtmpfs]
root        17     2  0 7月05 ?       00:00:00 [netns]
root        18     2  0 7月05 ?       00:00:00 [perf]
root        19     2  0 7月05 ?       00:00:00 [khungtaskd]
root        20     2  0 7月05 ?       00:00:00 [writeback]
root        22     2  0 7月05 ?       00:00:00 [ksmd]
root        23     2  0 7月05 ?       00:00:00 [khugepaged]
root        24     2  0 7月05 ?       00:00:00 [crypto]
root        25     2  0 7月05 ?       00:00:00 [kintegrityd]
root        26     2  0 7月05 ?       00:00:00 [bioset]
root        27     2  0 7月05 ?       00:00:00 [kblockd]
root        28     2  0 7月05 ?       00:00:00 [devfreq_wq]
root        30     2  0 7月05 ?       00:00:00 [kswapd0]
root        31     2  0 7月05 ?       00:00:00 [vmstat]
root        32     2  0 7月05 ?       00:00:00 [fsnotify_mark]
root        42     2  0 7月05 ?       00:00:00 [kthrotld]
root        43     2  0 7月05 ?       00:00:00 [ipv6_addrconf]
root        44     2  0 7月05 ?       00:00:00 [deferwq]
root        79     2  0 7月05 ?       00:00:00 [acpi_thermal_pm]
root        81     2  0 7月05 ?       00:00:00 [ata_sff]
root        82     2  0 7月05 ?       00:00:00 [kpsmoused]
root        90     2  0 7月05 ?       00:00:00 [scsi_eh_0]
root        91     2  0 7月05 ?       00:00:00 [scsi_tmf_0]
root        92     2  0 7月05 ?       00:00:03 [usb-storage]
root        93     2  0 7月05 ?       00:00:00 [scsi_eh_1]
root        94     2  0 7月05 ?       00:00:00 [scsi_tmf_1]
root        95     2  0 7月05 ?       00:00:00 [scsi_eh_2]
root        96     2  0 7月05 ?       00:00:00 [scsi_tmf_2]
root        97     2  0 7月05 ?       00:00:00 [scsi_eh_3]
root        98     2  0 7月05 ?       00:00:00 [scsi_tmf_3]
root        99     2  0 7月05 ?       00:00:00 [scsi_eh_4]
root       100     2  0 7月05 ?       00:00:00 [scsi_tmf_4]
root       101     2  0 7月05 ?       00:00:00 [scsi_eh_5]
root       102     2  0 7月05 ?       00:00:00 [scsi_tmf_5]
root       108     2  0 7月05 ?       00:00:00 [bioset]
root       109     2  0 7月05 ?       00:00:00 [bioset]
root       113     2  0 7月05 ?       00:00:00 [kworker/0:1H]
root       115     2  0 7月05 ?       00:00:00 [bioset]
root       129     2  0 7月05 ?       00:00:00 [md]
root       155     2  0 7月05 ?       00:00:02 [jbd2/sda3-8]
root       156     2  0 7月05 ?       00:00:00 [ext4-rsv-conver]
root       166     2  0 7月05 ?       00:00:00 [kworker/1:1H]
root       199     1  0 7月05 ?       00:00:01 /lib/systemd/systemd-journald
root       210     2  0 7月05 ?       00:00:00 [kauditd]
root       218     1  0 7月05 ?       00:00:00 /sbin/lvmetad -f
root       229     1  0 7月05 ?       00:00:01 /lib/systemd/systemd-udevd
root       304     2  0 7月05 ?       00:00:00 [ktpacpid]
root       313     2  0 7月05 ?       00:00:00 [cfg80211]
root       387     1  0 7月05 ?       00:00:00 /usr/sbin/ModemManager
avahi      388     1  0 7月05 ?       00:00:00 avahi-daemon: running [timilong-
message+   389     1  0 7月05 ?       00:00:20 /usr/bin/dbus-daemon --system --
root       408     1  0 7月05 ?       00:00:00 /usr/sbin/rsyslogd -n
avahi      410   388  0 7月05 ?       00:00:00 avahi-daemon: chroot helper
root       411     1  0 7月05 ?       00:00:00 /usr/sbin/cron -f
root       413     1  0 7月05 ?       00:00:00 /usr/sbin/cupsd -l
root       418     1  0 7月05 ?       00:00:00 /lib/systemd/systemd-logind
root       420     1  0 7月05 ?       00:00:19 /usr/sbin/NetworkManager --no-da
root       422     1  0 7月05 ?       00:00:01 /usr/lib/accountsservice/account
root       493     1  0 7月05 tty1    00:00:00 /sbin/agetty --noclear tty1 linu
root       497     1  0 7月05 ?       00:00:05 /usr/sbin/irqbalance --pid=/var/
root       513     1  0 7月05 ?       00:00:00 /usr/sbin/lightdm
mysql      519     1  0 7月05 ?       00:00:00 /bin/sh /usr/bin/mysqld_safe
root       523     1  0 7月05 ?       00:00:00 /usr/lib/policykit-1/polkitd --n
mysql      929   519  0 7月05 ?       00:00:37 /usr/sbin/mysqld --basedir=/usr 
root       973     1  0 7月05 ?       00:00:00 /usr/sbin/acpid
root       995     1  0 7月05 ?       00:00:02 /sbin/wpa_supplicant -u -s -O /r
root      1085     1  0 7月05 ?       00:00:00 /usr/lib/deepin-daemon/dde-syste
root      1318     1  0 7月05 ?       00:00:04 /usr/lib/upower/upowerd
root      1384     1  0 7月05 ?       00:00:37 /usr/lib/udisks2/udisksd --no-de
root      1490     1  0 7月05 ?       00:00:30 /usr/bin/lastore-daemon
root      8221     2  0 07:55 ?        00:00:00 [irq/28-mei_me]
root      8250   420  0 07:55 ?        00:00:00 /sbin/dhclient -d -q -sf /usr/li
root     10760   513  3 17:41 tty7     00:08:11 /usr/lib/xorg/Xorg -core :0 -sea
root     10815   513  0 17:41 ?        00:00:00 lightdm --session-child 12 19
timilong 10820     1  0 17:41 ?        00:00:00 /lib/systemd/systemd --user
timilong 10822 10820  0 17:41 ?        00:00:00 (sd-pam)
timilong 10827     1  0 17:41 ?        00:00:01 /usr/bin/gnome-keyring-daemon --
timilong 10829 10815  0 17:41 ?        00:00:10 /usr/bin/startdde
timilong 10884     1  0 17:41 ?        00:00:00 /usr/bin/dbus-launch --exit-with
timilong 10885     1  0 17:41 ?        00:00:12 /usr/bin/dbus-daemon --fork --pr
timilong 10894 10829  0 17:41 ?        00:00:00 /usr/bin/ssh-agent /usr/bin/sogo
timilong 10898     1  9 17:41 ?        00:26:23 /usr/bin/fcitx
timilong 10915     1  0 17:41 ?        00:00:02 /usr/bin/dbus-daemon --fork --pr
timilong 10919     1  0 17:41 ?        00:00:00 /usr/bin/fcitx-dbus-watcher unix
timilong 10929     1  0 17:41 ?        00:00:00 /usr/lib/at-spi2-core/at-spi-bus
timilong 10934 10929  0 17:41 ?        00:00:00 /usr/bin/dbus-daemon --config-fi
timilong 10936     1  0 17:41 ?        00:00:01 /usr/lib/at-spi2-core/at-spi2-re
timilong 10952 10829  0 17:41 ?        00:00:02 /usr/bin/deepin-wm-switcher
timilong 10953 10829  0 17:41 ?        00:00:01 /usr/lib/deepin-daemon/dde-osd
timilong 10954 10829  0 17:41 ?        00:00:00 /usr/lib/deepin-daemon/deepin-fi
timilong 10956 10829  0 17:41 ?        00:00:07 /usr/lib/deepin-daemon/dde-sessi
timilong 10975     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfsd
timilong 10985     1  0 17:41 ?        00:00:26 /usr/lib/deepin-daemon/dde-sessi
timilong 10987     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfsd-fuse /run/us
timilong 10989 10952  3 17:41 ?        00:10:42 /usr/bin/deepin-wm --replace
timilong 10991     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfsd-trash --spaw
timilong 11017 10829  0 17:41 ?        00:00:02 /usr/bin/dde-desktop
timilong 11024     1  0 17:41 ?        00:00:00 /usr/lib/dconf/dconf-service
timilong 11037     1  0 17:41 ?        00:01:02 /usr/bin/pulseaudio --start --lo
timilong 11046 10829  1 17:41 ?        00:03:56 /usr/bin/dde-dock
timilong 11050     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfsd-computer --s
timilong 11055     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfs-udisks2-volum
timilong 11058 10829  0 17:41 ?        00:00:01 /usr/bin/dde-launcher
timilong 11076     1  0 17:41 ?        00:00:00 /usr/lib/policykit-1-gnome/polki
timilong 11089     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfs-gphoto2-volum
timilong 11091     1  0 17:41 ?        00:00:00 /usr/bin/lastore-session-helper
timilong 11098     1  0 17:41 ?        00:00:00 /usr/lib/deepin-menu
timilong 11106     1  0 17:41 ?        00:00:00 /usr/lib/deepin-daemon/cloudprin
timilong 11125     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfs-goa-volume-mo
timilong 11140     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfs-mtp-volume-mo
timilong 11151     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfs-afc-volume-mo
timilong 11165 10985  0 17:41 ?        00:00:00 /bin/sh -c syndaemon -i 1 -K -t
timilong 11167 11165  0 17:41 ?        00:00:05 syndaemon -i 1 -K -t
timilong 11181     1  0 17:41 ?        00:00:21 /usr/lib/deepin-api/mousearea
timilong 11189     1  0 17:41 ?        00:00:01 /usr/lib/bamf/bamfdaemon
timilong 11206     1  0 17:41 ?        00:00:00 /usr/lib/x86_64-linux-gnu/gconf/
timilong 11214     1  0 17:41 ?        00:00:18 sogou-qimpanel
timilong 11596     1  0 17:41 ?        00:00:00 sogou-qimpanel-watchdog
timilong 11641     1  0 17:41 ?        00:00:03 /usr/bin/python3 /usr/share/syst
timilong 11880     1  0 17:43 ?        00:00:13 /usr/lib/gnome-terminal/gnome-te
timilong 11885 11880  0 17:43 pts/0    00:00:00 bash
timilong 12412     1  0 17:58 ?        00:00:00 /usr/lib/gvfs/gvfsd-network --sp
root     12428     1  0 17:58 ?        00:00:00 /sbin/mount.ntfs /dev/sda6 /medi
timilong 12443     1  0 17:58 ?        00:00:00 /usr/lib/gvfs/gvfsd-metadata
timilong 12465     1  0 17:58 ?        00:00:00 /usr/lib/gvfs/gvfsd-dnssd --spaw
timilong 12651     1  0 18:06 ?        00:00:00 /usr/lib/gvfs/gvfsd-http --spawn
timilong 14925     1  0 19:52 ?        00:00:07 /usr/bin/dde-control-center date
root     15497     2  0 21:39 ?        00:00:03 [kworker/u16:0]
root     15580     2  0 21:43 ?        00:00:00 [kworker/1:0]
timilong 15665     1  0 21:53 ?        00:00:00 winewrapper.exe --wait-children 
timilong 15671     1  2 21:53 ?        00:00:26 /opt/cxoffice/bin/wineserver
timilong 15675     1  0 21:53 ?        00:00:00 C:\windows\system32\services.exe
timilong 15679     1  0 21:53 ?        00:00:00 C:\windows\system32\winedevice.e
timilong 15687     1  0 21:53 ?        00:00:00 C:\windows\system32\plugplay.exe
timilong 15693     1  0 21:53 ?        00:00:00 C:\windows\system32\winedevice.e
timilong 15699     1  0 21:53 ?        00:00:00 C:\windows\system32\winedevice.e
timilong 15707     1  0 21:53 ?        00:00:00 C:\windows\system32\explorer.exe
timilong 15709     1  0 21:53 ?        00:00:04 C:\Program Files\Tencent\QQ\QQPr
timilong 15764     1  6 21:53 ?        00:00:58 /qdwnd=65616 /hosthwnd=65658 /ho
timilong 16105     1  3 21:54 ?        00:00:33 /opt/google/chrome/chrome https:
timilong 16113 16105  0 21:54 ?        00:00:00 cat
timilong 16114 16105  0 21:54 ?        00:00:00 cat
timilong 16116 16105  0 21:54 ?        00:00:00 /opt/google/chrome/chrome-sandbo
timilong 16117 16116  0 21:54 ?        00:00:00 /opt/google/chrome/chrome --type
timilong 16119 16117  0 21:54 ?        00:00:00 /opt/google/chrome/chrome-sandbo
timilong 16120 16119  0 21:54 ?        00:00:00 /opt/google/chrome/nacl_helper
timilong 16122 16117  0 21:54 ?        00:00:00 /opt/google/chrome/chrome --type
timilong 16161 16105  4 21:54 ?        00:00:36 /opt/google/chrome/chrome --type
timilong 16175 16161  0 21:54 ?        00:00:00 /opt/google/chrome/chrome --type
timilong 16285 16122  2 21:54 ?        00:00:23 /opt/google/chrome/chrome --type
timilong 16303 16122  0 21:54 ?        00:00:02 /opt/google/chrome/chrome --type
timilong 16428 16122  0 21:55 ?        00:00:01 /opt/google/chrome/chrome --type
root     16451     2  0 21:55 ?        00:00:00 [kworker/0:1]
timilong 16460 16122  1 21:55 ?        00:00:10 /opt/google/chrome/chrome --type
root     16662     2  0 21:58 ?        00:00:02 [kworker/u16:1]
root     16663     2  0 21:58 ?        00:00:01 [kworker/u16:2]
root     16667     2  0 22:00 ?        00:00:00 [kworker/0:0]
root     16672     2  0 22:01 ?        00:00:00 [kworker/1:1]
timilong 16694 16122  3 22:02 ?        00:00:12 /opt/google/chrome/chrome --type
root     16736     2  0 22:06 ?        00:00:00 [kworker/1:2]
root     16751     2  0 22:06 ?        00:00:00 [kworker/u16:3]
root     16752     2  0 22:06 ?        00:00:00 [kworker/0:2]
timilong 16771 11885  0 22:07 pts/0    00:00:00 vim linux-杀死?程.md
timilong 16777 16771  0 22:07 ?        00:00:00 /usr/bin/python /home/timilong/.
timilong 16823 11880  1 22:09 pts/1    00:00:00 bash
timilong 16834 16823  0 22:09 pts/1    00:00:00 ps -ef
```

#### ps -aux
```
D        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 7月05 ?       00:00:02 /sbin/init splash
root         2     0  0 7月05 ?       00:00:00 [kthreadd]
root         3     2  0 7月05 ?       00:00:16 [ksoftirqd/0]
root         5     2  0 7月05 ?       00:00:00 [kworker/0:0H]
root         7     2  0 7月05 ?       00:00:18 [rcu_sched]
root         8     2  0 7月05 ?       00:00:00 [rcu_bh]
root         9     2  0 7月05 ?       00:00:00 [migration/0]
root        10     2  0 7月05 ?       00:00:00 [watchdog/0]
root        11     2  0 7月05 ?       00:00:01 [watchdog/1]
root        12     2  0 7月05 ?       00:00:00 [migration/1]
root        13     2  0 7月05 ?       00:00:10 [ksoftirqd/1]
root        15     2  0 7月05 ?       00:00:00 [kworker/1:0H]
root        16     2  0 7月05 ?       00:00:00 [kdevtmpfs]
root        17     2  0 7月05 ?       00:00:00 [netns]
root        18     2  0 7月05 ?       00:00:00 [perf]
root        19     2  0 7月05 ?       00:00:00 [khungtaskd]
root        20     2  0 7月05 ?       00:00:00 [writeback]
root        22     2  0 7月05 ?       00:00:00 [ksmd]
root        23     2  0 7月05 ?       00:00:00 [khugepaged]
root        24     2  0 7月05 ?       00:00:00 [crypto]
root        25     2  0 7月05 ?       00:00:00 [kintegrityd]
root        26     2  0 7月05 ?       00:00:00 [bioset]
root        27     2  0 7月05 ?       00:00:00 [kblockd]
root        28     2  0 7月05 ?       00:00:00 [devfreq_wq]
root        30     2  0 7月05 ?       00:00:00 [kswapd0]
root        31     2  0 7月05 ?       00:00:00 [vmstat]
root        32     2  0 7月05 ?       00:00:00 [fsnotify_mark]
root        42     2  0 7月05 ?       00:00:00 [kthrotld]
root        43     2  0 7月05 ?       00:00:00 [ipv6_addrconf]
root        44     2  0 7月05 ?       00:00:00 [deferwq]
root        79     2  0 7月05 ?       00:00:00 [acpi_thermal_pm]
root        81     2  0 7月05 ?       00:00:00 [ata_sff]
root        82     2  0 7月05 ?       00:00:00 [kpsmoused]
root        90     2  0 7月05 ?       00:00:00 [scsi_eh_0]
root        91     2  0 7月05 ?       00:00:00 [scsi_tmf_0]
root        92     2  0 7月05 ?       00:00:03 [usb-storage]
root        93     2  0 7月05 ?       00:00:00 [scsi_eh_1]
root        94     2  0 7月05 ?       00:00:00 [scsi_tmf_1]
root        95     2  0 7月05 ?       00:00:00 [scsi_eh_2]
root        96     2  0 7月05 ?       00:00:00 [scsi_tmf_2]
root        97     2  0 7月05 ?       00:00:00 [scsi_eh_3]
root        98     2  0 7月05 ?       00:00:00 [scsi_tmf_3]
root        99     2  0 7月05 ?       00:00:00 [scsi_eh_4]
root       100     2  0 7月05 ?       00:00:00 [scsi_tmf_4]
root       101     2  0 7月05 ?       00:00:00 [scsi_eh_5]
root       102     2  0 7月05 ?       00:00:00 [scsi_tmf_5]
root       108     2  0 7月05 ?       00:00:00 [bioset]
root       109     2  0 7月05 ?       00:00:00 [bioset]
root       113     2  0 7月05 ?       00:00:00 [kworker/0:1H]
root       115     2  0 7月05 ?       00:00:00 [bioset]
root       129     2  0 7月05 ?       00:00:00 [md]
root       155     2  0 7月05 ?       00:00:02 [jbd2/sda3-8]
root       156     2  0 7月05 ?       00:00:00 [ext4-rsv-conver]
root       166     2  0 7月05 ?       00:00:00 [kworker/1:1H]
root       199     1  0 7月05 ?       00:00:01 /lib/systemd/systemd-journald
root       210     2  0 7月05 ?       00:00:00 [kauditd]
root       218     1  0 7月05 ?       00:00:00 /sbin/lvmetad -f
root       229     1  0 7月05 ?       00:00:01 /lib/systemd/systemd-udevd
root       304     2  0 7月05 ?       00:00:00 [ktpacpid]
root       313     2  0 7月05 ?       00:00:00 [cfg80211]
root       387     1  0 7月05 ?       00:00:00 /usr/sbin/ModemManager
avahi      388     1  0 7月05 ?       00:00:00 avahi-daemon: running [timilong-
message+   389     1  0 7月05 ?       00:00:20 /usr/bin/dbus-daemon --system --
root       408     1  0 7月05 ?       00:00:00 /usr/sbin/rsyslogd -n
avahi      410   388  0 7月05 ?       00:00:00 avahi-daemon: chroot helper
root       411     1  0 7月05 ?       00:00:00 /usr/sbin/cron -f
root       413     1  0 7月05 ?       00:00:00 /usr/sbin/cupsd -l
root       418     1  0 7月05 ?       00:00:00 /lib/systemd/systemd-logind
root       420     1  0 7月05 ?       00:00:19 /usr/sbin/NetworkManager --no-da
root       422     1  0 7月05 ?       00:00:01 /usr/lib/accountsservice/account
root       493     1  0 7月05 tty1    00:00:00 /sbin/agetty --noclear tty1 linu
root       497     1  0 7月05 ?       00:00:05 /usr/sbin/irqbalance --pid=/var/
root       513     1  0 7月05 ?       00:00:00 /usr/sbin/lightdm
mysql      519     1  0 7月05 ?       00:00:00 /bin/sh /usr/bin/mysqld_safe
root       523     1  0 7月05 ?       00:00:00 /usr/lib/policykit-1/polkitd --n
mysql      929   519  0 7月05 ?       00:00:37 /usr/sbin/mysqld --basedir=/usr 
root       973     1  0 7月05 ?       00:00:00 /usr/sbin/acpid
root       995     1  0 7月05 ?       00:00:02 /sbin/wpa_supplicant -u -s -O /r
root      1085     1  0 7月05 ?       00:00:00 /usr/lib/deepin-daemon/dde-syste
root      1318     1  0 7月05 ?       00:00:04 /usr/lib/upower/upowerd
root      1384     1  0 7月05 ?       00:00:37 /usr/lib/udisks2/udisksd --no-de
root      1490     1  0 7月05 ?       00:00:30 /usr/bin/lastore-daemon
root      8221     2  0 07:55 ?        00:00:00 [irq/28-mei_me]
root      8250   420  0 07:55 ?        00:00:00 /sbin/dhclient -d -q -sf /usr/li
root     10760   513  3 17:41 tty7     00:08:11 /usr/lib/xorg/Xorg -core :0 -sea
root     10815   513  0 17:41 ?        00:00:00 lightdm --session-child 12 19
timilong 10820     1  0 17:41 ?        00:00:00 /lib/systemd/systemd --user
timilong 10822 10820  0 17:41 ?        00:00:00 (sd-pam)
timilong 10827     1  0 17:41 ?        00:00:01 /usr/bin/gnome-keyring-daemon --
timilong 10829 10815  0 17:41 ?        00:00:10 /usr/bin/startdde
timilong 10884     1  0 17:41 ?        00:00:00 /usr/bin/dbus-launch --exit-with
timilong 10885     1  0 17:41 ?        00:00:12 /usr/bin/dbus-daemon --fork --pr
timilong 10894 10829  0 17:41 ?        00:00:00 /usr/bin/ssh-agent /usr/bin/sogo
timilong 10898     1  9 17:41 ?        00:26:23 /usr/bin/fcitx
timilong 10915     1  0 17:41 ?        00:00:02 /usr/bin/dbus-daemon --fork --pr
timilong 10919     1  0 17:41 ?        00:00:00 /usr/bin/fcitx-dbus-watcher unix
timilong 10929     1  0 17:41 ?        00:00:00 /usr/lib/at-spi2-core/at-spi-bus
timilong 10934 10929  0 17:41 ?        00:00:00 /usr/bin/dbus-daemon --config-fi
timilong 10936     1  0 17:41 ?        00:00:01 /usr/lib/at-spi2-core/at-spi2-re
timilong 10952 10829  0 17:41 ?        00:00:02 /usr/bin/deepin-wm-switcher
timilong 10953 10829  0 17:41 ?        00:00:01 /usr/lib/deepin-daemon/dde-osd
timilong 10954 10829  0 17:41 ?        00:00:00 /usr/lib/deepin-daemon/deepin-fi
timilong 10956 10829  0 17:41 ?        00:00:07 /usr/lib/deepin-daemon/dde-sessi
timilong 10975     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfsd
timilong 10985     1  0 17:41 ?        00:00:26 /usr/lib/deepin-daemon/dde-sessi
timilong 10987     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfsd-fuse /run/us
timilong 10989 10952  3 17:41 ?        00:10:42 /usr/bin/deepin-wm --replace
timilong 10991     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfsd-trash --spaw
timilong 11017 10829  0 17:41 ?        00:00:02 /usr/bin/dde-desktop
timilong 11024     1  0 17:41 ?        00:00:00 /usr/lib/dconf/dconf-service
timilong 11037     1  0 17:41 ?        00:01:02 /usr/bin/pulseaudio --start --lo
timilong 11046 10829  1 17:41 ?        00:03:56 /usr/bin/dde-dock
timilong 11050     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfsd-computer --s
timilong 11055     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfs-udisks2-volum
timilong 11058 10829  0 17:41 ?        00:00:01 /usr/bin/dde-launcher
timilong 11076     1  0 17:41 ?        00:00:00 /usr/lib/policykit-1-gnome/polki
timilong 11089     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfs-gphoto2-volum
timilong 11091     1  0 17:41 ?        00:00:00 /usr/bin/lastore-session-helper
timilong 11098     1  0 17:41 ?        00:00:00 /usr/lib/deepin-menu
timilong 11106     1  0 17:41 ?        00:00:00 /usr/lib/deepin-daemon/cloudprin
timilong 11125     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfs-goa-volume-mo
timilong 11140     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfs-mtp-volume-mo
timilong 11151     1  0 17:41 ?        00:00:00 /usr/lib/gvfs/gvfs-afc-volume-mo
timilong 11165 10985  0 17:41 ?        00:00:00 /bin/sh -c syndaemon -i 1 -K -t
timilong 11167 11165  0 17:41 ?        00:00:05 syndaemon -i 1 -K -t
timilong 11181     1  0 17:41 ?        00:00:21 /usr/lib/deepin-api/mousearea
timilong 11189     1  0 17:41 ?        00:00:01 /usr/lib/bamf/bamfdaemon
timilong 11206     1  0 17:41 ?        00:00:00 /usr/lib/x86_64-linux-gnu/gconf/
timilong 11214     1  0 17:41 ?        00:00:18 sogou-qimpanel
timilong 11596     1  0 17:41 ?        00:00:00 sogou-qimpanel-watchdog
timilong 11641     1  0 17:41 ?        00:00:03 /usr/bin/python3 /usr/share/syst
timilong 11880     1  0 17:43 ?        00:00:13 /usr/lib/gnome-terminal/gnome-te
timilong 11885 11880  0 17:43 pts/0    00:00:00 bash
timilong 12412     1  0 17:58 ?        00:00:00 /usr/lib/gvfs/gvfsd-network --sp
root     12428     1  0 17:58 ?        00:00:00 /sbin/mount.ntfs /dev/sda6 /medi
timilong 12443     1  0 17:58 ?        00:00:00 /usr/lib/gvfs/gvfsd-metadata
timilong 12465     1  0 17:58 ?        00:00:00 /usr/lib/gvfs/gvfsd-dnssd --spaw
timilong 12651     1  0 18:06 ?        00:00:00 /usr/lib/gvfs/gvfsd-http --spawn
timilong 14925     1  0 19:52 ?        00:00:07 /usr/bin/dde-control-center date
root     15497     2  0 21:39 ?        00:00:03 [kworker/u16:0]
root     15580     2  0 21:43 ?        00:00:00 [kworker/1:0]
timilong 15665     1  0 21:53 ?        00:00:00 winewrapper.exe --wait-children 
timilong 15671     1  2 21:53 ?        00:00:26 /opt/cxoffice/bin/wineserver
timilong 15675     1  0 21:53 ?        00:00:00 C:\windows\system32\services.exe
timilong 15679     1  0 21:53 ?        00:00:00 C:\windows\system32\winedevice.e
timilong 15687     1  0 21:53 ?        00:00:00 C:\windows\system32\plugplay.exe
timilong 15693     1  0 21:53 ?        00:00:00 C:\windows\system32\winedevice.e
timilong 15699     1  0 21:53 ?        00:00:00 C:\windows\system32\winedevice.e
timilong 15707     1  0 21:53 ?        00:00:00 C:\windows\system32\explorer.exe
timilong 15709     1  0 21:53 ?        00:00:04 C:\Program Files\Tencent\QQ\QQPr
timilong 15764     1  6 21:53 ?        00:00:58 /qdwnd=65616 /hosthwnd=65658 /ho
timilong 16105     1  3 21:54 ?        00:00:33 /opt/google/chrome/chrome https:
timilong 16113 16105  0 21:54 ?        00:00:00 cat
timilong 16114 16105  0 21:54 ?        00:00:00 cat
timilong 16116 16105  0 21:54 ?        00:00:00 /opt/google/chrome/chrome-sandbo
timilong 16117 16116  0 21:54 ?        00:00:00 /opt/google/chrome/chrome --type
timilong 16119 16117  0 21:54 ?        00:00:00 /opt/google/chrome/chrome-sandbo
timilong 16120 16119  0 21:54 ?        00:00:00 /opt/google/chrome/nacl_helper
timilong 16122 16117  0 21:54 ?        00:00:00 /opt/google/chrome/chrome --type
timilong 16161 16105  4 21:54 ?        00:00:36 /opt/google/chrome/chrome --type
timilong 16175 16161  0 21:54 ?        00:00:00 /opt/google/chrome/chrome --type
timilong 16285 16122  2 21:54 ?        00:00:23 /opt/google/chrome/chrome --type
timilong 16303 16122  0 21:54 ?        00:00:02 /opt/google/chrome/chrome --type
timilong 16428 16122  0 21:55 ?        00:00:01 /opt/google/chrome/chrome --type
root     16451     2  0 21:55 ?        00:00:00 [kworker/0:1]
timilong 16460 16122  1 21:55 ?        00:00:10 /opt/google/chrome/chrome --type
root     16662     2  0 21:58 ?        00:00:02 [kworker/u16:1]
root     16663     2  0 21:58 ?        00:00:01 [kworker/u16:2]
root     16667     2  0 22:00 ?        00:00:00 [kworker/0:0]
root     16672     2  0 22:01 ?        00:00:00 [kworker/1:1]
timilong 16694 16122  3 22:02 ?        00:00:12 /opt/google/chrome/chrome --type
root     16736     2  0 22:06 ?        00:00:00 [kworker/1:2]
root     16751     2  0 22:06 ?        00:00:00 [kworker/u16:3]
root     16752     2  0 22:06 ?        00:00:00 [kworker/0:2]
timilong 16771 11885  0 22:07 pts/0    00:00:00 vim linux-杀死?程.md
timilong 16777 16771  0 22:07 ?        00:00:00 /usr/bin/python /home/timilong/.
timilong 16823 11880  1 22:09 pts/1    00:00:00 bash
timilong 16834 16823  0 22:09 pts/1    00:00:00 ps -ef
```

### 用kill命令杀死进程
```
kill -s 9 16122
```
就可以杀死进程号为16122的goole chrome的进程。
其中：-s 9 制定了传递给进程的信号是９，即强制、尽快终止进程。

### 其它方法
#### ps -ef | grep python
把ps的查询结果通过管道给grep查找包含特定字符串的进程。管道符“|”用来隔开两个命令，管道符左边命令的输出会作为管道符右边命令的输入。

#### pgrep
pgrep的p表明了这个命令是专门用于进程查询的grep。
```
pgrep chrome
```

#### pidof
pid of xx，字面翻译过来就是 xx的PID。
```
pidof firefox-bin
```

#### ps -ef | grep firefox | grep -v grep | cut -c 9-15 | xargs kill -s 9

说明：
“grep firefox”的输出结果是，所有含有关键字“firefox”的进程。
“grep -v grep”是在列出的进程中去除含有关键字“grep”的进程。
“cut -c 9-15”是截取输入行的第9个字符到第15个字符，而这正好是进程号PID。
“xargs kill -s 9”中的xargs命令是用来把前面命令的输出结果（PID）作为“kill -s 9”命令的参数，并执行该命令。“kill -s 9”会强行杀掉指定进程

#### pkill
```
pkill -９ firefox
```

#### killall
```
killall -9 firefox
```

### 文章来源如下

[http://blog.csdn.net/andy572633/article/details/7211546](http://blog.csdn.net/andy572633/article/details/7211546)
