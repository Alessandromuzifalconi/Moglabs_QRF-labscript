# Imports:
import numpy as np
from labscript_utils import import_or_reload
from labscript import start, stop, add_time_marker, LabscriptError, AnalogOut, DigitalOut
from user_devices.FPGA.FPGA_device import FPGA_board, DigitalChannels, AnalogChannels, PRIMARY_IP, SECONDARY_IP, DEFAULT_PORT, AO_MIN, AO_MAX
from user_devices.unit_conversion.generic_conversion import generic_conversion

# Import connection table so that it remains updated
import_or_reload('labscriptlib.arqus_experiment.connection_table')


from labscriptlib.arqus_experiment.connection_table import primary #, secondary

t = primary.start_time 
dt = primary.time_step



# precise ramp by Andi

def precise_ramp(t, duration, initial, final, rate, name):
	"""
	linear ramp with fixed sample rate.
	intermediate points are kept constant.
	this allows interleaved ramps without time collisions.
	"""
	#print(name,t)
	if initial   > AO_MAX: initial = AO_MAX
	elif initial < AO_MIN: initial = AO_MIN
	if final     > AO_MAX: final   = AO_MAX
	elif final   < AO_MIN: final   = AO_MIN
	if isinstance(t, np.ndarray):
	    return np.where(t < duration, initial + np.floor(t*rate)/rate*(final-initial)/duration, [final]*len(t))
	else:
	    if t < duration: return initial + np.floor(t*rate)/rate*(final-initial)/duration
	    else:            return final

def MOT_parameters (time):
	MOT_HOR_ON_OFF.go_high(time)
	MOT_VER_ON_OFF.go_high(time)
	time += dt
	MOT_HOR_AM.constant(time, Ampl_MOT_HOR)
	time += dt
	MOT_HOR_FM.constant(time, Freq_MOT_HOR)
	time += dt
	MOT_VER_AM.constant(time, Ampl_MOT_VER)
	time += dt
	MOT_VER_FM.constant(time, Freq_MOT_VER)
	time += dt
	return time

def Imaging (time, t_exposure, shutter_delay = 0.1):

	Blue_imaging_ON_OFF.go_low(time-shutter_delay)
	Blue_imaging_shutter.go_high(time-shutter_delay)
	time += shutter_delay
	Blue_imaging_ON_OFF.go_high(time)
	time += t_exposure
	# Camera click should go here
	Blue_imaging_ON_OFF.go_low(time)
	Blue_imaging_shutter.go_low(time + dt)
	time += shutter_delay 
	Blue_imaging_ON_OFF.go_high(time)
	return time


def TestQRF (time, freq, ampl):

	Green_imaging_AOM.setfreq(time,freq)
	Green_imaging_AOM.setamp(time,ampl)
	Green_imaging_AOM.setphase(time,0.0)
	"""
	QRF_Ch2.setfreq(time,20)
	QRF_Ch2.setamp(time,0.0)
	QRF_Ch2.setphase(time,0.0)
	
	QRF_Ch3.setfreq(time,20)
	QRF_Ch3.setamp(time,0.0)
	QRF_Ch3.setphase(time,0.0)	

	QRF_Ch4.setfreq(time,20)
	QRF_Ch4.setamp(time,0.0)
	QRF_Ch4.setphase(time,0.0)
	"""
	return time



	return ()
if __name__ == '__main__':

	# start sequence
	start()
	print(f'Minimum time step: {dt}')


	t += dt
	# Turn on AOMs
	Blue_imaging_ON_OFF.go_high(t)

	# Opens shutters
	MOT2D_shutter.go_high(t)
	CrossedBeams_shutter.go_high(t)
	MOT_HOR_shutter.go_high(t)
	MOT_VER_shutter.go_high(t)



	# Set MOT parameters
	t = MOT_parameters(t+dt)
	t += dt

	# Set QRF green imaging parameters
	t += TestQRF (t+dt, 80.0, 10.0)
	t += TestQRF (t+dt, 25.0, 5.0)

	Green_imaging_ON_OFF.go_high(t)
	Green_imaging_ON_OFF.go_low(t+dt)

	# CMOT
	t += t_start_CMOT
	MOT2D_shutter.go_low(t)
	CrossedBeams_shutter.go_low(t)
	t += dt
	

	"""
	rate: true output rate, i.e. the rate of change of the output
	1/rate must be an integer multiple of channels*t_ch_offset with channels = number of channels which change in parallel 
	t_ch_offset: time slot per channel (integer multiple of dt, minimum dt)
	samplerate: time resolution of the ramp. labscript rounds all output times to this resolution therefore this must be <= 1/t_ch_offset

	"""
	# list of analog outputs changing in parallel
	ao_list = [MOT_HOR_FM,MOT_HOR_AM,MOT_VER_FM,MOT_VER_AM]
	channels = len(ao_list)
	t_ch_offset = dt # time offset between channel
	t_offset = {}
	for i, channel in enumerate (ao_list):
		t_offset[channel.name] = i*t_ch_offset
		#print(f'Channel {i} ({channel.name}) time slot {t_offset[channel.name]*1e6} us')

	analog_ramp_rate = 1/(channels*t_ch_offset)

	MOT_HOR_FM.customramp(t+t_offset[MOT_HOR_FM.name], function = precise_ramp, initial = Freq_MOT_HOR, final= Freq_CMOT_HOR, duration=t_ramp_CMOT, samplerate = 1/t_ch_offset, rate = analog_ramp_rate, name = 'MOT_HOR_Freq_ramp'  )
	MOT_HOR_AM.customramp(t+t_offset[MOT_HOR_AM.name], function = precise_ramp, initial =  Ampl_MOT_HOR, final= Ampl_CMOT_HOR, duration=t_ramp_CMOT, samplerate = 1/t_ch_offset, rate = analog_ramp_rate, name = 'MOT_HOR_Ampl_ramp')
	MOT_VER_FM.customramp(t+t_offset[MOT_VER_FM.name],function = precise_ramp, initial = Freq_MOT_VER, final= Freq_CMOT_VER, duration=t_ramp_CMOT, samplerate = 1/t_ch_offset, rate = analog_ramp_rate, name = 'MOT_VER_Freq_ramp'  )
	MOT_VER_AM.customramp(t+t_offset[MOT_VER_AM.name], function = precise_ramp, initial =  Ampl_MOT_VER, final= Ampl_CMOT_VER, duration=t_ramp_CMOT, samplerate = 1/t_ch_offset, rate = analog_ramp_rate, name = 'MOT_VER_Ampl_ramp')

	# shortest time after ramp finished
	t+= (channels-1)*t_ch_offset+t_ramp_CMOT+dt


	# Shut down MOT
	MOT_HOR_ON_OFF.go_low(t)
	MOT_VER_ON_OFF.go_low(t)
	MOT_HOR_shutter.go_low(t)
	MOT_VER_shutter.go_low(t)


	t += t_wait
	# Turn on MOT AOMs
	MOT_HOR_ON_OFF.go_high(t)
	MOT_VER_ON_OFF.go_high(t)

	# Image
	t += t_imaging
	Imaging(t, t_exposure,shutter_delay = dt)
	
	Green_imaging_ON_OFF.go_high(t)
	Green_imaging_ON_OFF.go_low(t+dt)


	
	Green_imaging_ON_OFF.go_high(t_end_experiment-3*dt)
	Green_imaging_ON_OFF.go_low(t_end_experiment-2*dt)
	MOT_VER_ON_OFF.go_low(t_end_experiment-dt)

	# stop sequence
	stop(t_end_experiment)
