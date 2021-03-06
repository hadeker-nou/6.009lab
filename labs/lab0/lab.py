# No Imports Allowed!


def backwards(sound):
    result={}
    result["rate"]=sound['rate']
    result["left"]=[sample for sample in reversed(sound['left'])]
    result["right"]=[sample for sample in reversed(sound['right'])]
    return result
    

def mix(sound1, sound2, p):
    result={"left":[],"right":[]}
    if(sound1["rate"]!=sound2["rate"]):
        return None
    result["rate"]=sound1["rate"]
    if(len(sound1["left"])<=len(sound2["left"])):
        leng=len(sound1["left"])
    else:
        leng=len(sound2["left"])
    for i in range(leng):
        new=(sound1["left"][i]*p)+(sound2["left"][i]*(1-p))
        result["left"].append(new)
        new=(sound1["right"][i]*p)+(sound2["right"][i]*(1-p))
        result["right"].append(new)
    return result


def echo(sound, num_echos, delay, scale):
    result={"left":[],"right":[]}
    result["rate"]=sound['rate']
    sample_delay=round(sound["rate"]*delay) 
    output_long=num_echos * sample_delay + len(sound['left'])
    result["left"]=[0]*output_long
    result["right"]=[0]*output_long
    for i in range(num_echos+1):
        for j in range(len(sound["right"])):
            result["right"][j+ (int(sample_delay) * i)] += (sound["right"][j]*(scale**i))
            result["left"][j+ (int(sample_delay) * i)] += (sound["left"][j]*(scale**i))
    return result

        


def pan(sound):
    result={"right":[],"left":[],"rate":sound["rate"]}
    length=len(sound["right"])
    for i in range(length):
        newR=(i/(length-1))
        result["right"].append(newR*sound["right"][i])
        newL=1-newR
        result["left"].append(newL*sound["left"][i])
    return result


def remove_vocals(sound):
    result={"right":[],"left":[],"rate":sound["rate"]}
    for i in range(len(sound["right"])):
        new=sound["left"][i]-sound["right"][i]
        result["left"].append(new)
        result["right"].append(new)
    return result


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct

def load_wav(filename):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    left = []
    right = []
    for i in range(count):
        frame = f.readframes(1)
        if chan == 2:
            left.append(struct.unpack('<h', frame[:2])[0])
            right.append(struct.unpack('<h', frame[2:])[0])
        else:
            datum = struct.unpack('<h', frame)[0]
            left.append(datum)
            right.append(datum)

    left = [i/(2**15) for i in left]
    right = [i/(2**15) for i in right]

    return {'rate': sr, 'left': left, 'right': right}


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, 'w')
    outfile.setparams((2, 2, sound['rate'], 0, 'NONE', 'not compressed'))

    out = []
    for l, r in zip(sound['left'], sound['right']):
        l = int(max(-1, min(1, l)) * (2**15-1))
        r = int(max(-1, min(1, r)) * (2**15-1))
        out.append(l)
        out.append(r)

    outfile.writeframes(b''.join(struct.pack('<h', frame) for frame in out))
    outfile.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    #hello = load_wav('sounds/hello.wav')

    # write_wav(backwards(hello), 'hello_reversed.wav')


    cof = load_wav("sounds/coffee.wav")
    res=remove_vocals(cof)
    write_wav( res , "result_outputs/cof_remove.wav")
    