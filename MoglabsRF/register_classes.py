#####################################################################
#####################################################################
from labscript_devices import register_classes

blacs_tab = 'user_devices.MoglabsRF.MOGLabs_QRF.MOGLabs_QRF_Tab'
runviewer_parser = 'user_devices.MoglabsRF.MOGLabs_QRF.RunviewerClass'
register_classes(
    'MOGLabs_QRF',
    BLACS_tab=blacs_tab,
    runviewer_parser=None
)


