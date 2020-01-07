"""
Some functions which uses and extends meep 
"""
import numpy as np
# import meep as mp
import math
import cmath
import sys
import datetime
import re


##############################
#### define a flux region
##############################
def FluxRegion_box(x1,x2,y1,y2,z1,z2,loc):
    """ 

    Create a mp.FluxRegion objuect from  a box face.

    Parameters
    -----------
    x1,x2,y1,y2,z1,z2 : numbers
      (x1,y1,z1) and (x2,y2,z2) define two end points of a space diagonal
    
    loc: string 
    
      loc is one of ('X+','X-','Y+','Y-','Z+','Z-') which indicates
      the face. The face of ('X-','Y-','Z-') has negative weight.

    Returns
    -----------
    mp.FluxRegion
      a Meep FluxRegion object so that we can calcuatet the power flow.

    """
    # giving the coordinate of the points, return flux region
    fx=abs(x1-x2)
    fy=abs(y1-y2)
    fz=abs(z1-z2)
    
    cx=(x1+x2)/2
    cy=(y1+y2)/2
    cz=(z1+z2)/2
    
    if loc=="X+":
        center=mp.Vector3(max(x1,x2),cy,cz)
        size=mp.Vector3(0,fy,fz)
        weight=1
    elif loc=="X-":
        center=mp.Vector3(min(x1,x2),cy,cz)
        size=mp.Vector3(0,fy,fz)
        weight=-1
    elif loc=="Y+":
        center=mp.Vector3(cx,max(y1,y2),cz)
        size=mp.Vector3(fx,0,fz)
        weight=1
    elif loc=="Y-":
        center=mp.Vector3(cx,min(y1,y2),cz)
        size=mp.Vector3(fx,0,fz)
        weight=-1
    elif loc=="Z+":
        center=mp.Vector3(cx,cy,max(z1,z2))
        size=mp.Vector3(fx,fy,0)  
        weight=1     
    elif loc=="Z-":
        center=mp.Vector3(cx,cy,min(z1,z2))
        size=mp.Vector3(fx,fy,0)    
        weight=-1 
    else:
        sys.exit("Flux region setting is wrong")

    return mp.FluxRegion(center=center,size=size,weight=weight)

###############################################
#### define flux region from box length and center
###############################################
def FluxRegion_box_Center(x,y,z,c,loc):
    """

    Create a mp.FluxRegion objuect from  a box face.

    Parameters
    -----------
    x,y,z : numbers
      (x,y,z) are the dimentions along the three directions
    c: mp.Vector3
      The center of the box

    loc: string 

      loc is one of ('X+','X-','Y+','Y-','Z+','Z-') which indicates
      the face.The face of ('X-','Y-','Z-') has negative weight.

    Returns
    -----------
    mp.FluxRegion
      a Meep FluxRegion object so that we can calcuatet the power flow.

    """
    x1=c.x-abs(x)/2
    x2=c.x+abs(x)/2
    y1=c.y-abs(y)/2
    y2=c.y+abs(y)/2
    z1=c.z-abs(z)/2
    z2=c.z+abs(z)/2
    return FluxRegion_box(x1,x2,y1,y2,z1,z2,loc)


###############################################
#### create 6 flux regions from a box defined by corners
###############################################
def FluxRegions_Box_Corner(x1,x2,y1,y2,z1,z2):

    """Create a list of six mp.FluxRegion objects from all the six faces of a
    box befined by the two corners.

    Parameters
    -----------
    x1,x2,y1,y2,z1,z2 : numbers
   
      (x1,y1,z1) and (x2,y2,z2) define two end points of a space diagonal
  
    Returns
    -----------
    a list of mp.FluxRegion objects

      a list of Meep FluxRegion objects in the order of
      ('X+','X-','Y+','Y-','Z+','Z-')

    """
    frx1=FluxRegion_box(x1,x2,y1,y2,z1,z2,"X+")
    frx2=FluxRegion_box(x1,x2,y1,y2,z1,z2,"X-")
    fry1=FluxRegion_box(x1,x2,y1,y2,z1,z2,"Y+")
    fry2=FluxRegion_box(x1,x2,y1,y2,z1,z2,"Y-")
    frz1=FluxRegion_box(x1,x2,y1,y2,z1,z2,"Z+")
    frz2=FluxRegion_box(x1,x2,y1,y2,z1,z2,"Z-")
    return [frx1,frx2,fry1,fry2,frz1,frz2]

###############################################
#### create of 6 flux regions from a box defined by the size and center
###############################################
def FluxRegions_Box_Center(x,y,z,center):

    """

    Create a list of six mp.FluxRegion objects from all the six faces
    of a box defined by the size and center.

    Parameters
    -----------

    x,y,z : numbers
      (x,y,z) are the dimentions along the three directions
  
    c: mp.Vector3
      The center of the box
  
    Returns
    -----------
    a list of mp.FluxRegion objects

      a list of Meep FluxRegion objects in the order of
      ('X+','X-','Y+','Y-','Z+','Z-')

    """

    c=center
    x1=c.x-abs(x)/2
    x2=c.x+abs(x)/2
    y1=c.y-abs(y)/2
    y2=c.y+abs(y)/2
    z1=c.z-abs(z)/2
    z2=c.z+abs(z)/2
    frx1=FluxRegion_box(x1,x2,y1,y2,z1,z2,"X+")
    frx2=FluxRegion_box(x1,x2,y1,y2,z1,z2,"X-")
    fry1=FluxRegion_box(x1,x2,y1,y2,z1,z2,"Y+")
    fry2=FluxRegion_box(x1,x2,y1,y2,z1,z2,"Y-")
    frz1=FluxRegion_box(x1,x2,y1,y2,z1,z2,"Z+")
    frz2=FluxRegion_box(x1,x2,y1,y2,z1,z2,"Z-")
    return [frx1,frx2,fry1,fry2,frz1,frz2]


###############################################
#### create of 6 flux regions from a cube
###############################################
def FluxRegions_Cube_Center(l,center):

    """

    Create a list of six mp.FluxRegion objects from all the six faces
    of a cube (an equilateral cuboid) defined by the size and center.

    Parameters
    -----------

    l : number
      edge length
  
    center: mp.Vector3
      The center of the box
  
    Returns
    -----------
    a list of mp.FluxRegion objects

      a list of six Meep FluxRegion objects in the order of
      ('X+','X-','Y+','Y-','Z+','Z-')

    """

    return FluxRegions_Box_Center(l,l,l,center)


###############################################
def FluxRegions_Box2D_Center(lx,ly,center):
    """Create a list of four mp.FluxRegion objects from all the four sides
    of a 2D box defined by the size and center.

    Parameters
    -----------

    lx,ky : numbers
      dimentions along the two directions
  
    center: mp.Vector3
      The center of the box
  
    Returns
    -----------
    a list of mp.FluxRegion objects

      a list of four Meep FluxRegion objects in the order of
      ('X+','X-','Y+','Y-'). The weight is 1 for all the sides.

    """

    x1=center.x-abs(lx)/2
    x2=center.x+abs(lx)/2
    y1=center.y-abs(ly)/2
    y2=center.y+abs(ly)/2

    frx1=mp.FluxRegion(center=mp.Vector3(x1,(y1+y2)/2,0),
                      size=mp.Vector3(0,abs(y2-y1),0))
    frx2=mp.FluxRegion(center=mp.Vector3(x2,(y1+y2)/2,0),
                      size=mp.Vector3(0,abs(y2-y1),0))

    fry1=mp.FluxRegion(center=mp.Vector3((x1+x2)/2,y1,0),
                      size=mp.Vector3(abs(x2-x1),0,0))
    fry2=mp.FluxRegion(center=mp.Vector3((x1+x2)/2,y2,0),
                       size=mp.Vector3(abs(x2-x1),0,0))

    return [frx1,frx2,fry1,fry2]

###############################################
#### calculate flux box center and size with restriction
###############################################
def FluxBox1D_helper(size,xsrc,xmin=None,xmax=None):

    """

    Calculate the size and center of a 1D box based on some restrictions. 

    Parameters
    -----------

    size : number 

      The desired box size. The actual box size is equal
      to or less than the desired size

    xsrc: number

      The coordinae of the source. The 1D box should cover the source.
      
    xmin,xmax: numbers

      The boundaries of the boxes. The 1D box can not exceed the
      boundaries.
  
    Returns
    -----------
    (number, number)
    
      the box size and the central cooridnate of the 1D box
    
    """
    
    if xmin is None:
        xmin=xsrc-10*size
    if xmax is None:
        xmax=xsrc+10*size

    if (xmax-xmin)<2*size:
        lx=(xmax-xmin)/2
        xbox=xsrc/2+xmin/4+xmax/4
    else:
        lx=size
        if (xsrc-xmin)<lx:
            xbox=(xsrc+xmin)/2+lx/2
        elif (xmax-xsrc)<lx:
            xbox=(xsrc+xmax)/2-lx/2
        else:
            xbox=xsrc
    return (lx,xbox)


def FluxBox2D(size,src,xmin=None,xmax=None,ymin=None,ymax=None):

    """

    Calculate the size and center of a 2D box based on some restrictions. 

    Parameters
    -----------

    size : number 

      The desired box size. The actual box size is equal
      to or less than the desired size

    src: mp.Vector3

      The coordinae of the source. The box should cover the source.
      
    xmin,xmax,ymin,ymax: numbers

      The boundaries of the boxes. 
  
    Returns
    -----------
    (number, mp.Vector3)
    
      the box size and the central cooridnate of the box
    
    """

    lx,xbox=FluxBox1D_helper(size,src.x,xmin,xmax)
    ly,ybox=FluxBox1D_helper(size,src.y,ymin,ymax)
    return (min(lx,ly),mp.Vector3(xbox,ybox,0))
    
def FluxBox3D(size,src,xmin=None,xmax=None,
              ymin=None,ymax=None,
              zmin=None,zmax=None):

    """

    Calculate the size and center of a 3D box based on some restrictions. 

    Parameters
    -----------

    size : number 

      The desired box size. The actual box size is equal
      to or less than the desired size

    src: mp.Vector3

      The coordinae of the source. The box should cover the source.
      
    xmin,xmax,ymin,ymax,zmin,zmax : numbers

      The boundaries of the boxes. 
  
    Returns
    -----------
    (number, mp.Vector3)
    
      the box size and the central cooridnate of the box
    
    """
  
    lx,xbox=FluxBox1D_helper(size,src.x,xmin,xmax)
    ly,ybox=FluxBox1D_helper(size,src.y,ymin,ymax)
    lz,zbox=FluxBox1D_helper(size,src.z,zmin,zmax)

    return (min(lx,ly,lz),mp.Vector3(xbox,ybox,zbox))


###############################################
#### force meep to demonstrate information on time
###############################################
def my_flush_step(sim):
    """
    
    Flush stdout and force meep to display the message on time

    Parameters
    -----------

    sim : Meep simulation
  
  
    Returns
    -----------
    None


    """
    t=datetime.datetime.now()
    print("My flush: "+str(t))
    sys.stdout.flush()


##############################
#### calculate an array of centers based on thicknesses 
##############################
def center_from_thickness(ds,x0):

    """
    
    Calculate the central coordinates from a list of thickness

    Parameters
    -----------

    ds : a list of numbers

      Thickness of a series layers

    x0 : number
      
      The coordinate of the bottom surface of the first layer
  
    Returns
    -----------
    a list of numbers
    
      The central coordinates of all the layers
      

    """

    ds=np.array(ds)
    return np.array([np.sum(ds[0:i+1]) for i in range(ds.size)])-ds/2+x0


