########################## THE TOON LAND DLC ##########################
# Filename: __init__.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# Initializes the Toon Land DLC. Do not modify.
####

# This method is used to prevent potential hackers from accessing the
# various Toon Land modules. All work will be done in this namespace.
priv_namespace = {
    '__version__':'v0.1.4.4',
    '__filebase__':'mods\\TL_Cookies',
    '__modulebase__':'mods\\TL_Cookies\\toonland',
    '__admin__':True,
    '__dev__':True
}
exec('from __main__ import *', priv_namespace)
execfile('%s\\security\\HackerCrypt.py' % (
    priv_namespace.get('__modulebase__')), priv_namespace)
exec('HackerCrypt = HackerCrypt()', priv_namespace)
exec('HackerCrypt.setMagic("[TL-Cookies]")', priv_namespace)
exec('HackerCrypt.setKey("Initializing Toon Land...")', priv_namespace)
execfile('%s\\__par__.py' % priv_namespace.get('__filebase__'), priv_namespace)
del priv_namespace # Block potential hackers from accessing this namespace.