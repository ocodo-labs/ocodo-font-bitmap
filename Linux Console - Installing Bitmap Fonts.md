# Linux Console : Installing Bitmap Fonts

This page covers installation and persistent configuration of PSF/PSFU bitmap fonts on major Linux distributions.

e.g. ocodo-mono-dotzero-13x24.psfu

- from https://github.com/ocodo-labs/ocodo-mono-dotzero-bitmap/releases/tag/1.0.2 
  - https://github.com/ocodo-labs/ocodo-mono-dotzero-bitmap/releases/download/1.0.2/ocodo-mono-dotzero-13x24.psfu
  - Note if you are on a 4k TV at couch distance 60px Y/Height is good. 

The general process is:

1. Install the font in the distribution's console-font directory.
2. Test it with `setfont` - only from a console e.g. <kbd>Ctrl+Alt+<kbd>3</kbd>.
3. Configure the distribution's normal console-font mechanism.

 ## Debian / Ubuntu

 Debian-family systems using `console-setup` normally use:

```
/usr/share/consolefonts/
```

 Install the font:

```
sudo install -m 0644 ocodo-mono-dotzero-13x24.psfu /usr/share/consolefonts/
```

Test it:

```
sudo setfont /usr/share/consolefonts/ocodo-mono-dotzero-13x24.psfu
```

Persistent configuration is handled by:

```
/etc/default/console-setup
```

The easiest way to configure it is:

```
sudo dpkg-reconfigure console-setup
```

 For a custom font, set `FONT` to the installed font filename:

```
FONT="ocodo-mono-dotzero-13x24.psfu"
```

 Apply the configuration:

```
sudo setupcon
```

 Debian's `console-setup` also supports `FONTFACE` and `FONTSIZE` for fonts supplied by the package system.

 ## Fedora / RHEL / CentOS Stream / Rocky / Alma

 The Red Hat family uses `kbd` and `systemd-vconsole-setup`.

 Console fonts are normally installed in:

```
/usr/lib/kbd/consolefonts/
```

Install the font:

```
sudo install -m 0644 ocodo-mono-dotzero-13x24.psfu /usr/lib/kbd/consolefonts/
```

Test it:

```
sudo setfont ocodo-mono-dotzero-13x24.psfu
```

Persistent configuration:

```
/etc/vconsole.conf
```

Set:

```
FONT=ocodo-mono-dotzero
```

 For example:

```
KEYMAP=us
FONT=ocodo-mono-dotzero
```

 ## Arch Linux

 Arch uses `kbd`.

 Console fonts are normally installed in:

```
/usr/share/kbd/consolefonts/
```

 Install:

```
sudo install -m 0644 ocodo-mono-dotzero-13x24.psfu /usr/share/kbd/consolefonts/
```

 Test:

```
sudo setfont ocodo-mono-dotzero
```

 Persistent configuration:

```
/etc/vconsole.conf
```

 Set:

```
FONT=ocodo-mono-dotzero
```

 For example:

```
KEYMAP=us
FONT=ocodo-mono-dotzero
```

 ## openSUSE / SUSE Linux Enterprise

 SUSE systems using `kbd` normally use:

```
/usr/share/kbd/consolefonts/
```

 Install and test:

```
sudo install -m 0644 ocodo-mono-dotzero-13x24.psfu /usr/share/kbd/consolefonts/
sudo setfont ocodo-mono-dotzero
```

 On current systemd-based installations, configure:

```
/etc/vconsole.conf
```

 with:

```
FONT=ocodo-mono-dotzero
```

 Older installations may instead use:

```
/etc/sysconfig/console
```

 If `/etc/vconsole.conf` is already used by the system, prefer it.

 ## Alpine Linux

 Alpine uses OpenRC.

 Console fonts are normally installed in:

```
/usr/share/consolefonts/
```

 Install `kbd` if necessary:

```
sudo apk add kbd
```

 Install and test:

```
sudo install -m 0644 ocodo-mono-dotzero-13x24.psfu /usr/share/consolefonts/
sudo setfont /usr/share/consolefonts/ocodo-mono-dotzero-13x24.psfu
```

 Persistent configuration is handled by the `consolefont` service.

 Edit:

```
/etc/conf.d/consolefont
```

 and set:

```
consolefont="ocodo-mono-dotzero-13x24.psfu"
```

 Enable the service:

```
sudo rc-update add consolefont boot
```

 Apply it immediately:

```
sudo rc-service consolefont start
```

 ## Gentoo

 Gentoo installations using OpenRC use the `consolefont` service.

 Console fonts are normally under:

```
/usr/share/kbd/consolefonts/
```

 Install `kbd` if necessary:

```
sudo emerge --ask sys-apps/kbd
```

 Install and test:

```
sudo install -m 0644 ocodo-mono-dotzero-13x24.psfu /usr/share/kbd/consolefonts/
sudo setfont ocodo-mono-dotzero
```

 Persistent configuration:

```
/etc/conf.d/consolefont
```

 Set:

```
consolefont="ocodo-mono-dotzero"
```

 Enable the service:

```
sudo rc-update add consolefont boot
```

 ## Void Linux

 Void uses runit and configures the console through:

```
/etc/rc.conf
```

 Console fonts are normally under:

```
/usr/share/kbd/consolefonts/
```

 Install and test:

```
sudo install -m 0644 ocodo-mono-dotzero-13x24.psfu /usr/share/kbd/consolefonts/
sudo setfont ocodo-mono-dotzero
```

 Set the persistent font in `/etc/rc.conf`:

```
FONT=ocodo-mono-dotzero
```

 ## Slackware

 Slackware uses its `rc.font` startup mechanism.

 Console fonts are normally under:

```
/usr/share/kbd/consolefonts/
```

 Install and test:

```
sudo install -m 0644 ocodo-mono-dotzero-13x24.psfu /usr/share/kbd/consolefonts/
sudo setfont ocodo-mono-dotzero-13x24.psfu
```

 Persistent configuration:

```
/etc/rc.d/rc.font
```

 For example:

```
#!/bin/sh

setfont ocodo-mono-dotzero-13x24.psfu
```

 Make the script executable:

```
sudo chmod +x /etc/rc.d/rc.font
```

 `setconsolefont` can also be used to select an installed font.

 ## NixOS

 NixOS handles console fonts declaratively.

 For a font provided by `kbd`:

```
{
  console.font = "Lat2-Terminus16";
}
```

 Apply the configuration:

```
sudo nixos-rebuild switch
```

 The font name normally omits its path and file extension.

 For custom fonts, make the font available through the Nix store and reference it from the NixOS configuration rather than installing it directly under `/usr/share`.

 ## Other systemd distributions

 For distributions using `systemd-vconsole-setup` and `kbd`, the usual arrangement is:

```
/usr/share/kbd/consolefonts/
/etc/vconsole.conf
```

 Install and test:

```
sudo install -m 0644 ocodo-mono-dotzero-13x24.psfu /usr/share/kbd/consolefonts/
sudo setfont ocodo-mono-dotzero
```

 Then configure:

```
FONT=ocodo-mono-dotzero
```

 The console-font directory is distribution-specific. Existing fonts supplied by the distribution are a reliable indication of the correct location.

 ## Finding the console-font directory

 If the distribution's location is unclear:

```
find /usr/share/kbd/consolefonts \
     /usr/lib/kbd/consolefonts \
     /usr/share/consolefonts \
     -maxdepth 1 -type f 2>/dev/null
```

 Use the directory containing the distribution's existing `.psf`, `.psfu`, or compressed console fonts.

 ## Quick reference

 | Family | Console font directory | Persistent configuration |
| --- | --- | --- |
| Debian / Ubuntu | `/usr/share/consolefonts/` | `/etc/default/console-setup` |
| Fedora / RHEL | `/usr/lib/kbd/consolefonts/` | `/etc/vconsole.conf` |
| Arch | `/usr/share/kbd/consolefonts/` | `/etc/vconsole.conf` |
| openSUSE / SLE | `/usr/share/kbd/consolefonts/` | `/etc/vconsole.conf` |
| Alpine | `/usr/share/consolefonts/` | `/etc/conf.d/consolefont` |
| Gentoo | `/usr/share/kbd/consolefonts/` | `/etc/conf.d/consolefont` |
| Void | `/usr/share/kbd/consolefonts/` | `/etc/rc.conf` |
| Slackware | `/usr/share/kbd/consolefonts/` | `/etc/rc.d/rc.font` |
| NixOS | Nix store | `configuration.nix` |
