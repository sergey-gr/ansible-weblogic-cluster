# Connect to WebLogic admin server
connect('{{ weblogic_admin }}', '{{ weblogic_admin_pass}}', '{{ hostvars[groups['wl_admin'][0]]['ansible_ssh_host'] }}:{{ admin_server_port }}')

# Creates a user configuration file and an associated key file
# https://docs.oracle.com/middleware/1213/wls/WLSTC/reference.htm#GUID-54FB0DCB-62F4-4BA7-8D34-4E2BEE698EF7
storeUserConfig('{{ domain_home }}/config/{{ oracle_user }}-WebLogicConfig.properties', '{{ domain_home }}/config/{{ oracle_user }}-WebLogicKey.properties')

# ==> Usage
# connect("userConfigFile='<path_to_config_file>', userKeyFile='<path_to_key_file>','t3://<admin_ip>:7001')

disconnect()
exit()