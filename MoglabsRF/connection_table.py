from labscript import *

from user_devices.FPGA.FPGA_device import FPGA_board, DigitalChannels, AnalogChannels, PRIMARY_IP, SECONDARY_IP, DEFAULT_PORT
from user_devices.unit_conversion.generic_conversion import generic_conversion
from user_devices.FPGA.FPGA_device import FPGA_board, DigitalChannels, AnalogChannels, PRIMARY_IP, SECONDARY_IP, DEFAULT_PORT
from user_devices.red_pitaya_pyrpl_asg_ArQuS.labscript_devices import red_pitaya_pyrpl_asg

#from user_devices.mogdevice import MOGDevice

########################################################################################
# Connected instruments

MogQRF = True
RP = False
########################################################################################################################
# FPGA boards

# Primary board:
primary = FPGA_board(name='primary', ip_address='cora-01', ip_port=DEFAULT_PORT, bus_rate=1e6, num_racks=1,
    worker_args={ # optional arguments. can be changed in GUI. if defined here used at startup, otherwise last settings in GUI are used.
        'outputs': {'output 0': ('sync out', 'low level')}, # required: start trigger for sec. board (default, keep here). other outputs can be added.
        #'ext_clock':False,  # True = use external clock
        #'ignore_clock_loss':True # True = ignore when external clock is lost. Message Box is displayed but board keeps running.
        #'trigger':{}, # no trigger (default)
        #'trigger':{'start trigger':('input 0', 'rising edge')}, # start trigger
        #'trigger':{'start trigger':('input 0', 'rising edge'),'stop trigger':('input 1', 'falling edge'),'restart trigger':('input 0', 'rising edge')}, # start+stop+restart trigger
    })


########################################################################################################################

# Digital Outputs:
#DigitalChannels(name='DO0', parent_device=primary, connection='0', rack=0, max_channels=16)

#DigitalOut  (name='ZS_Shutter', parent_device=DO0, connection=0)
#DigitalOut  (name='MOT2D_Shutter', parent_device=DO0, connection=1)
#DigitalOut  (name='CrossBeams_AOM_on', parent_device=DO0, connection=2)
#DigitalOut  (name='RedPitaya_Ch1_Trigger', parent_device=DO0, connection=3)
#DigitalOut  (name='RedPitaya_Ch2_Trigger', parent_device=DO0, connection=4)

DigitalChannels(name='DO0', parent_device=primary, connection='0', rack=0, max_channels=16)
DigitalOut     (name='ZS_shutter_TTL', parent_device=DO0, connection=0)
DigitalOut     (name='MOT2D_shutter', parent_device=DO0, connection=1)
DigitalOut     (name='CrossedBeams_shutter', parent_device=DO0, connection=2)
DigitalOut     (name='Blue_imaging_ON_OFF', parent_device=DO0, connection=3)
DigitalOut     (name='Blue_imaging_shutter', parent_device=DO0, connection=4)
DigitalOut     (name='MOT_HOR_ON_OFF', parent_device=DO0, connection=5)
DigitalOut     (name='MOT_VER_ON_OFF', parent_device=DO0, connection=6)
DigitalOut     (name='MOT_HOR_shutter', parent_device=DO0, connection=7)
DigitalOut     (name='MOT_VER_shutter', parent_device=DO0, connection=8)
DigitalOut     (name='DOut10', parent_device=DO0, connection=9)
DigitalOut     (name='Green_imaging_ON_OFF', parent_device=DO0, connection=10)



i = 11
while i<16:
    DigitalOut (name=f'Digitaltest{i+1}', parent_device=DO0, connection=i)
    i += 1


#DigitalChannels(name='DO2', parent_device=primary, connection='0x40', rack=0, max_channels=16)
#DigitalOut  (name='MyDigitaltest2', parent_device=DO2, connection=0)

#########################################################################################################################
# Analog Outputs: 
# 16 Analog outputs, each with max two channels
# Old:
#AnalogChannels(name='AO0', parent_device=primary, rack=0, max_channels=2)
#AnalogOut     (name='MOT2D_AOM_percent', parent_device=AO0, connection='0x2', unit_conversion_class=generic_conversion, 
#               unit_conversion_parameters={'unit':'percent', 'equation':'(-0.02063+3.62077*np.tan(0.01724-0.19288*np.sqrt(x/100)+1.39915*x/100))', 'min':0.0, 'max':100.0})
#AnalogOut     (name='AOM_CrossedBeams_percent', parent_device=AO0, connection='0x3', unit_conversion_class=generic_conversion, 
#               unit_conversion_parameters={'unit':'percent', 'equation':'6+x/10', 'min':0.0, 'max':100.0})

AnalogChannels(name='AO1', parent_device=primary, rack=0, max_channels=4)
AnalogOut     (name='Coils_modulation', parent_device=AO1, connection='1')
AnalogOut     (name='BiasCoils_X_modulation', parent_device=AO1, connection='2')
AnalogOut     (name='BiasCoils_Y_modulation', parent_device=AO1, connection='3')
AnalogOut     (name='BiasCoils_Z_modulation', parent_device=AO1, connection='4')


AnalogChannels(name='AO2', parent_device=primary, rack=0, max_channels=4)
AnalogOut     (name='Blue_lock_FM', parent_device=AO2, connection='5')
AnalogOut     (name='MOT2D_lock_FM', parent_device=AO2, connection='6')
AnalogOut     (name='CrossedBeams_FM', parent_device=AO2, connection='7')
AnalogOut     (name='Blue_imaging_FM', parent_device=AO2, connection='8', unit_conversion_class=generic_conversion, 
    unit_conversion_parameters={'unit':'MHz', 'equation':'x/100', 'min':-50, 'max':50})

AnalogChannels(name='AO3', parent_device=primary, rack=0, max_channels=4)
AnalogOut     (name='MOT_HOR_FM', parent_device=AO3, connection='9')
AnalogOut     (name='MOT_HOR_AM', parent_device=AO3, connection='10', unit_conversion_class=generic_conversion, 
    unit_conversion_parameters={'unit':'dV', 'equation':'x/10', 'min':-100, 'max':100})
AnalogOut     (name='MOT_VER_FM', parent_device=AO3, connection='11')
AnalogOut     (name='MOT_VER_AM', parent_device=AO3, connection='12')

AnalogChannels(name='AO4', parent_device=primary, rack=0, max_channels=4)
AnalogOut     (name='AOtest13', parent_device=AO4, connection='13')
AnalogOut     (name='AOtest14', parent_device=AO4, connection='14')
AnalogOut     (name='AOtest15', parent_device=AO4, connection='15')
AnalogOut     (name='AOtest16', parent_device=AO4, connection='16')


AnalogChannels(name='AO5', parent_device=primary, rack=0, max_channels=4)
AnalogOut     (name='AO17', parent_device=AO5, connection='17')
AnalogOut     (name='AO18', parent_device=AO5, connection='18')
AnalogOut     (name='AO19', parent_device=AO5, connection='19')
AnalogOut     (name='AO20', parent_device=AO5, connection='20')

########################################################################################################################
# MOGLABS Quad RF synthesizer. give primary board as parent_device
if MogQRF: 

    from user_devices.MoglabsRF.MOGLabs_QRF import MOGLabs_QRF, QRF_DDS

    # we need one or several DigitalChannels intermediate device(s) for triggering given to QRF_DDS digital_gate as 'device' keyword.
    # note: do not create the channel(s) here since QRF_DDS creates each channel automatically with the 'connection' keyword as channel number.
    # this ensures the user does not set the channel by mistake.
    # parent must be the same board as for QRF.
    # the enable/disable commands are working. maybe this can be employed for triggering of individual channels?
    DigitalChannels(name='DO_QRF', parent_device=primary, connection='21', rack=0, max_channels=16)    
    # define temporarily for testing another intependent digital channel for Trigger of QRF. 
    # this should give a single trigger command for a single channel or for all channels I do not know, 
    # but so far even if I call QRF_0.trigger does not do anything?
    DigitalChannels(name='DO_QRF_1', parent_device=primary, connection='22', rack=0, max_channels=16, clockline=('QRF',True))

    MOGLabs_QRF(name='QRF_0', parent_device=DO_QRF_1, addr='qrf-01', port=7802)
    QRF_DDS(name='Green_imaging_AOM', parent_device=QRF_0, connection='channel 0', table_mode=False, trigger_each_step=False, digital_gate={'device':DO_QRF, 'connection': 0})
    QRF_DDS(name='QRF_Ch2', parent_device=QRF_0, connection='channel 1', table_mode=False, trigger_each_step=False, digital_gate={'device':DO_QRF, 'connection': 1})
    QRF_DDS(name='QRF_Ch3', parent_device=QRF_0, connection='channel 2', table_mode=False, trigger_each_step=False, digital_gate={'device':DO_QRF, 'connection': 2})
    QRF_DDS(name='QRF_Ch4', parent_device=QRF_0, connection='channel 3', table_mode=False, trigger_each_step=False, digital_gate={'device':DO_QRF, 'connection': 3})


########################################################################################################################
# Red Pitaya
if RP: 
    red_pitaya_pyrpl_asg(name='RedPitaya_Ch0', trigger_device=RedPitaya_Ch1_Trigger,trigger_connection=3, ip_addr = 'redpitaya-02', out_channel='out1', peak_volt=1., offset_calib=-1.,trig_duration = 0.01)
    # V2 implemenation of ArQuS RP 
    #red_pitaya_pyrpl_asg(name='RedPitaya_Ch1',output_ch = 'out1',trigger_source = 'ext_positive_edge', trigger_device=RedPitaya_Ch1_Trigger,trigger_connection=3, ip_addr = 'redpitaya-02', waveform='halframp',cycle_duration=100e-3,amplitude=1,offset = 1,cycles_per_burst=1)
    #red_pitaya_pyrpl_asg(name='RedPitaya_Ch2',output_ch = 'out2',trigger_source = 'immediately', trigger_device=RedPitaya_Ch2_Trigger,trigger_connection=4, ip_addr = 'redpitaya-02', waveform='square',cycle_duration=1e-3,amplitude=0.5,offset = 1.0)

## V1 implemenation of ArQuS RP 
# red_pitaya_pyrpl_asg0(name='RedPitaya_Ch1',trigger_device=RedPitaya_Ch1_Trigger,trigger_connection=3, ip_addr = 'redpitaya-02', waveform='sin',cycle_duration=1e-3,amplitude=0.5,offset = 1.0)
# red_pitaya_pyrpl_asg1(name='RedPitaya_Ch2',trigger_device=RedPitaya_Ch2_Trigger,trigger_connection=4, ip_addr = 'redpitaya-02', waveform='dc',cycle_duration=1e-3,amplitude=0.01)

########################################################################################################################
# Experimental sequence
if __name__ == '__main__':

    t = primary.start_time #note: t is not used here
    dt = primary.time_step

    # start sequence
    start()

    # stop sequence
    stop(1.000000 + dt)