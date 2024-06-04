# VMs and Workstation requirements

> Requirements for all cluster VMs and administrator workstation.

<hr>

- [1. On VMs](#1-on-vms)
  - [1.1 OS user](#1-1-os-user)
  - [1.2 Sudoers file](#1-2-sudoers-file)
- [2. On ansible workstation (admin node)](#2-on-ansible-workstation-admin-node)
  - [2.1 Generate SSH keys](#2-1-generate-ssh-keys)
  - [2.2 SSH folder and file permissions](#2-2-ssh-folder-and-file-permissions)
  - [2.3 Setup passwordless SSH](#2-3-setup-passwordless-ssh)

<br>

## 1. On VMs

### 1.1 OS user

Create new OS user for a ansible tasks on all cluster VMs:

Debian/Ubuntu

```shell
sudo adduser ansible
```

RedHat/Rocky

```shell
sudo useradd ansible
```

```shell
sudo passwd ansible
```

<br>

### 1.2 Sudoers file

Add newly created user to sudoers file (for passwordless sudo):

```shell
sudo su -
```

```shell
echo -e "\n# Allow without a password\nansible        ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers
```

```shell
exit
```

<br>

## 2. On ansible workstation (admin node)

### 2.1 Generate SSH keys

Create required directory

```shell
mkdir -p ~/.ssh/
```

Generate new SSH key:

```shell
ssh-keygen -f ~/.ssh/id_rsa -N ""
```

<br>

### 2.2 SSH folder and file permissions

```shell
chmod 700 ~/.ssh
```

```shell
chmod 644 ~/.ssh/id_rsa.pub
```

```shell
chmod 600 ~/.ssh/id_rsa
```

```shell
chmod 600 ~/.ssh/authorized_keys
```

### 2.3 Setup passwordless SSH

Distribute the SSH public key to all servers:

- use newly created user for ansible tasks:

```shell
ssh-copy-id ansible@127.0.0.11
```

SSH without password

```shell
ssh ansible@127.0.0.11
```