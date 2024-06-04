# Weblogic Cluster provisioning

Repository contains everything to provision a Weblogic Cluster on any RedHat 7+ based system..

- [1. Requirements](#1-requirements)
  - [1.1. Proxy requirements](#1-1-proxy-requirements)
- [2. Configuration](#2-configuration)
  - [2.1 Installers configuration](#2-1-installers-configuration)
- [3. Testing configuration](#3-testing-configuration)
- [4. Installation](#4-installation)
- [5. Uninstall](#5-uninstall)
- [6. Cluster maintanace tasks](#6-cluster-maintanace-tasks)

<br>

## 1. Requirements

**System requirements**:
- 1 VM with minimums of 2 cpus and 4GB RAM (HDD size is on your preference) for AdminServer
- 1 - ∞ VMs with minimum of 2 cpus and 8GB RAM each (HDD size is on your preference) for Managed Servers
- static IPs on all VMs
- supported linux OS: RedHat/CentOS 7/8, Oracle Linux 7/8, Rocky 8, AlmaLinux 8

**Workstation requirements**:
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

**Additional requirements**:
- NFS share for shared domain on all hosts, mounted on: `/u01/oracle`
- [VMs and Workstation requirements](docs/requirements.md)

### 1.1. Proxy requirements

Access to following external resources are required:

- Access to OS repository (yum/apt)
- Access to Python packages (*.python.org, *.pypi.org, *.pythonhosted.org)
- Access to Oracle Java and Middleware installer download (*.oracle.com)

<br>

## 2. Configuration

- Create copy of `inventory/default` directory and name it after your environment, example: `inventory/<environment>`.
- Edit your environment `inventory.ini` file by filling out environment servers configuration values.
- Edit your environment `all.yml` file by filling out environment specific configuration values (also see [2.1 Installers](#21-installers)).
- Edit your environment `all-vault.yml` file by filling out environment specific secrets.

> NOTE: Encrypt the `all-vault.yaml` file using `ansible-vault encrypt inventory/<environment>/group_vars/all/all-vault.yml` and providing secure password.

### 2.1 Installers configuration

> NOTE: Instructions for downloading and configuring installers.

Download [Linux x64 Compressed Archive](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html) and place `tar.gz` archive to:

```
./roles/jdk/files/jdk-8u371-linux-x64.tar.gz
```

Also set archive name (ex. `jdk-8u371-linux-x64.tar.gz`) as value for variable in your environments [all.yml](inventory/default/group_vars/all/all.yml#L2) file.

```yml
jdk_installer_archive: 'jdk-8u371-linux-x64.tar.gz'
```

Download [Generic Installer for Oracle WebLogic Server 12.2.1.4](https://www.oracle.com/middleware/technologies/weblogic-server-installers-downloads.html), extract archive and place generic `jar` installer to:

```
./roles/wls/files/fmw_12.2.1.4.0_wls_lite_generic.jar
```

Also set installer name (ex. `fmw_12.2.1.4.0_wls_lite_generic.jar`) as value for variable in your environments [all.yml](inventory/default/group_vars/all/all.yml#L5) file.

```yml
fmw_installer: 'fmw_12.2.1.4.0_wls_lite_generic.jar'
```

<br>

## 3. Testing configuration

Before installation you can test connection to your VMs using [check.yml](playbooks/check.yml) playbook.

Simply run:

```shell
ansible-playbook -i inventory/<environment>/inventory.ini playbooks/check.yml --ask-vault-pass
```

Output should look like this:

> NOTE: If playbook ran with no errors, then you are ready to begin installation.

```shell
...
TASK [debug] **********************************************************************
ok: [wl-admin] =>
  msg:
  - 'os_family: RedHat'
  - 'distribution: AlmaLinux'
  - 'major_version: 8'
ok: [wl-node-01] =>
  msg:
  - 'os_family: RedHat'
  - 'distribution: AlmaLinux'
  - 'major_version: 8'
ok: [wl-node-02] =>
  msg:
  - 'os_family: RedHat'
  - 'distribution: AlmaLinux'
  - 'major_version: 8'
...
```

<br>

## 4. Installation

Playbook to install and configure Weblogic cluster.

```shell
ansible-playbook -i inventory/<environment>/inventory.ini playbooks/setup.yml --ask-vault-pass
```

Will configure the cluster based on provided configuration in inventory files.

:exclamation: Weblogic console URL after installation: http://<admin_host_ip>:{{ admin_server_port }}/console

<br>

## 5. Uninstall

Playbook to uninstall Weblogic cluster.

```shell
ansible-playbook -i inventory/<environment>/inventory.ini playbooks/reset.yml
```

Will uninstall the Weblogic cluster and reboot the machines.

## 6. Cluster maintanace tasks

Playbook to update some parts of Cluster or Domain configuration

```shell
ansible-playbook -i inventory/<environment>/inventory.ini playbooks/update.yml -t <tag>
```

Will update specific part of configuration.

Currently available tags:

| Category | File Path | Tag | Description |
|----------|-----------|-----|-------------|
| Update | [playbooks/update.yml](playbooks/update.yml) | `ssl` | Will update Managed server SSL certificate and do SSL reset. |