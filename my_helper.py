"""Some help functions for Meep simulations.

"""


import math
import cmath
import sys
import datetime
import re

##############################
##### write data into a file
##############################
def matrix_output(fname,data,fmt,sig=None,onScreen=True):
    """Write data to a file and/or to screen.  
    
    Parameters
    -----------

    fname : string

      file name. If fname=None, it won't save to any file.

    data : 2D data array

    fmt : string
    
      data format, for example, fmt='{:0.4f}'

    sig : string

      the label before each line of data

    onScreen: bool

      switch for screen display
  
    Returns
    -----------
    None
    """

    n1=data.shape[0]
    n2=data.shape[1]
    ss=''
 
    for i in range(n1):
        line=''
        if sig is not None:
            line+=sig+":"
        for j in range(n2):
            if line:
                line+=", "
            line+=fmt.format(data[i,j])
        if i<n1-1:
            ss+=line+"\n"
        else:
            ss+=line
  
    if fname:
        with open(fname, "w") as fout:
            print(ss,file=fout)
    if onScreen:
        print(ss)
   


###############################################
#### convert number of second into a readable string
###############################################
def nice_sec2str(x):
    """Convert the number of seconds to a nice readable string  
    
    Parameters
    -----------

    x : number

      the number of seconds

    Returns
    -----------
    string

     A nice readable string
    """
    sec=datetime.timedelta(seconds=x)
    d = datetime.datetime(1,1,1) + sec
    unit=["days","hours","minutes","seconds"]
    if d.day<3:
        unit[0]="day"
    if d.hour<2:
        unit[1]="hour"
    if d.minute<2:
        unit[2]="minute"
    if d.second<2:
        unit[3]="second"

    if (d.day>1):
        ss="{:d} {} {:d} {} {:d} {} {:d} {} ".format(
            d.day-1,unit[0],d.hour,unit[1], 
            d.minute,unit[2], d.second,unit[3])
    elif (d.hour>0):
        ss="{:d} {} {:d} {} {:d} {} ".format(
            d.hour,unit[1], 
            d.minute,unit[2], d.second,unit[3])
    elif (d.minute>0):
        ss="{:d} {} {:d} {} ".format(
            d.minute,unit[2], d.second,unit[3])
    else:
       ss="{:d} {} ".format(d.second,unit[3])
 
    return ss


##############################
#### replace strings in a file
##############################
def file_re_sub(fname1,fname2,*argv):  
    """ Replace strings in a file.

    Parameters
    -----------

    fname1 : string

      file name of the original file

    fname2 : string

      The new file name after the string substitute

    *argv : a list of two-element tuples
    
      ( regular expression to be replaced, new string)

    Returns
    -----------
    None

    """
    with open(fname1, "rt") as fin:
        fin=open(fname1, 'rt')
        lines=fin.readlines()
        fin.close()

        for i,line in enumerate(lines):
            for pair in argv:
                line=re.sub(pair[0],pair[1],line)
            lines[i]=line
    
        fout=open(fname2, 'wt')
        fout.write("".join(lines))
        fout.close()



##############################
#### add a line to a file
##############################
def file_add_line(fname1,fname2,newline='',
                before=None,after=None,number=None):
    """Add a line to a file.

    Parameters
    -----------

    fname1 : string

      file name of the original file

    fname2 : string

      The new file name after the string insertions

    before : a regular expression
    
      insert right before the first line which matchs the regular expression

    after : a regular expression
    
      insert right after the first line which matchs the regular expression
    
    number : integer

      insert at the line number. All the conditions have to be
      satisfied if more than one conditions are defined.

    Returns
    -----------
    None

    """
    # before and after are regular expression
    # number is an interger
    # if before,after and number are not None, 
    # all the condition must be satisfied
    with open(fname1, "rt") as fin:
        fin=open(fname1, 'rt')
        lines=fin.readlines()
        fin.close()
    
        # find before or after, the first match
        number1=None
        number2=None
        for i,line in enumerate(lines):
            if before is not None and re.search(before, line):
                if number1 is None:
                    number1=i
            if after is not None and re.search(after, line):
                if number2 is None:
                    number2=i
        # print(number1)
        # print(number2)
        # check condition
        idx=number
        if idx is not None:
            if number1 is not None and (number1-idx)!=0:
                idx=None
        elif number1 is not None:
            idx=number1

        if idx is not None:
            if number2 is not None and (number2-idx)!=-1:
                idx=None
        elif number2 is not None:
            idx=number2+1
            
        # write the line
        if idx!=None:
            lines.insert(idx,newline+'\n')
       
        fout=open(fname2, 'wt')
        fout.write("".join(lines))
        fout.close()


########################
###### round-up, 
########################
# round_up(x,b)/b is a integer
def round_up(x, b=1): 
    """Round up a number. 

    round_up(x,b) is the smallest number which makes round_up(x,b)/b
    an integer. b=1 is the ordinary round-up; round_up(3.54,0.2)=3.6.

    Parameters
    -----------
    x : number

      The number to be rounded up 
    
    b : number 
    
      Round-up base. Fine control of the result.
    
    Returns
    -----------
    number
      round_up result

    """
    return math.ceil(x/b)*b
