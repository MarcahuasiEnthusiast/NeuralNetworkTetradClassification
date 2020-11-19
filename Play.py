import time
import rtmidi

ADN = [['61576266', '55596266', '55596064', '57606367'],
         ['54596370', '56596368', '57616468', '59636468'],
         ['57606465', '58626367', '57586265', '59606467'],
         ['50535760', '52535760', '53575862', '53555861'],
         ['55606265', '55576165', '57616266', '57596266'],
         ['50576064', '52566064', '55596064', '54576062'],
         ['52596064', '50596064', '48576264', '52555960'],
         ['58606367', '59626567', '60636768', '59626567'],
         ['54555962', '53565962', '55576062', '54566062'],
         ['55596264', '55576064', '54575962', '56586264'],
         ['53576062', '54566063', '54555962', '55576062'],
         ['55586265', '55586063', '55566063', '53566063'],
         ['55586265', '55586063', '55566063', '53566063'],
         ['55576064', '52545762', '53555760', '50555954']]

chordProgression = ['48606567', '48566370', '57596165', '49516468']

# ALEATORIO ['58506061', '59486271', '55596958', '48675067']
# ['57616266', '55596266', '55596064', '57606367']
# ['49455054', '43475054', '43474852', '45485155']

def numConcat(num1, num2):
    num1 = str(num1)
    num2 = str(num2)
    num1 += num2
    return int(num1)

def playADN(data):
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    print(available_ports)
    print(available_ports, "\n")

    # Attempt to open the port
    if available_ports:
        midiout.open_port(2)
    else:
        midiout.open_virtual_port("My virtual output")

    for k in range(len(data)):
        print("Iteracion: ", k+1)
        for i in range (len(data[k])):
            #note on
            try:
                a = numConcat(data[k][i][0], data[k][i][1])
                b = numConcat(data[k][i][2], data[k][i][3])
                c = numConcat(data[k][i][4], data[k][i][5])
                d = numConcat(data[k][i][6], data[k][i][7])
                print(a, b, c, d)
            except:
                print(a, b, c)
                pass
            try:
                midiout.send_message([0x90, a, 127])
                midiout.send_message([0x90, b, 127])
                midiout.send_message([0x90, c, 127])
                midiout.send_message([0x90, d, 127])
            except:
                pass
            time.sleep(2.0)
            #note off
            try:
                a = (0x80, a, 0)
                b = (0x80, b, 0)
                c = (0x80, c, 0)
                d = (0x80, d, 0)
            except:
                pass
            try:
                midiout.send_message(a)
                midiout.send_message(b)
                midiout.send_message(c)
                midiout.send_message(d)
            except:
                pass

    del midiout

def playChordProgression(data):

    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    print(available_ports, "\n")

    # Attempt to open the port
    if available_ports:
        midiout.open_port(3)
    else:
        midiout.open_virtual_port("My virtual output")
    for j in range(10):
        for i in range(len(data)):
            # note on
            try:
                a = numConcat(data[i][0], data[i][1])
                b = numConcat(data[i][2], data[i][3])
                c = numConcat(data[i][4], data[i][5])
                d = numConcat(data[i][6], data[i][7])
                print(a, b, c, d)
            except:
                print(a, b, c)
                pass
            try:
                midiout.send_message([0x90, a, 127])
                midiout.send_message([0x90, b, 127])
                midiout.send_message([0x90, c, 127])
                midiout.send_message([0x90, d, 127])
            except:
                pass
            time.sleep(2.0)
            # note off
            try:
                a = (0x80, a, 0)
                b = (0x80, b, 0)
                c = (0x80, c, 0)
                d = (0x80, d, 0)
            except:
                pass
            try:
                midiout.send_message(a)
                midiout.send_message(b)
                midiout.send_message(c)
                midiout.send_message(d)
            except:
                pass
    del midiout

#playADN(ADN)
playChordProgression(chordProgression)

