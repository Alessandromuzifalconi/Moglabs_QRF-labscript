#####################################################################
#####################################################################

# Just copied for now-> Not finished yet! Ale


from labscript_devices import register_classes

blacs_tab = 'user_devices.MoglabsRF.MOGLabs_XRF021.MOGLabs_XRF021Tab'
runviewer_parser = 'user_devices.MoglabsRF.MOGLabs_XRF021.RunviewerClass'
register_classes(
    'MOGLabs_XRF021',
    BLACS_tab=blacs_tab,
    runviewer_parser=runviewer_parser
)


