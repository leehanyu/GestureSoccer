# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 13:12:04 2018

@author: graes
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 11:51:01 2018

@author: graes
"""
import numpy as np


def getPoint(tip,n1,n2,n3,w1):
    n = 5.0
    Xm = (tip[0]+n1[0]+n2[0]+n3[0]+w1[0])/n
    Ym = (tip[1]+n1[1]+n2[1]+n3[1]+w1[1])/n
    Zm = (tip[2]+n1[2]+n2[2]+n3[2]+w1[2])/n
    
    Sxx = (tip[0]**2+n1[0]**2+n2[0]**2+n3[0]**2+w1[0]**2)/n - Xm**2
    Syy = (tip[1]**2+n1[1]**2+n2[1]**2+n3[1]**2+w1[1]**2)/n - Ym**2
    Szz = (tip[2]**2+n1[2]**2+n2[2]**2+n3[2]**2+w1[2]**2)/n - Zm**2
    Sxy = (tip[0]*tip[1]+n1[0]*n1[1]+n2[0]*n2[1]+n3[0]*n3[1]+w1[0]*w1[1])/n - Xm*Ym
    Sxz = (tip[0]*tip[2]+n1[0]*n1[2]+n2[0]*n2[2]+n3[0]*n3[2]+w1[0]*w1[2])/n - Xm*Zm
    Syz = (tip[2]*tip[1]+n1[2]*n1[1]+n2[2]*n2[1]+n3[2]*n3[1]+w1[2]*w1[1])/n - Zm*Ym
    
    theta = 0.5*np.arctan(2*Sxy/(Sxx - Syy))
    cos2 = np.cos(theta)**2
    sin2 = np.sin(theta)**2
    cos1 = np.cos(theta)
    sin1 = np.sin(theta)
    
    K11 = (Syy + Szz)*cos2+(Sxx+Szz)*sin2-2*Sxy*cos1*sin1
    K22 = (Syy + Szz)*sin2+(Sxx+Szz)*cos2+2*Sxy*cos1*sin1
    K12 = -1*Sxy*(cos2-sin2)+(Sxx-Syy)*cos1*sin1
    K10 = Sxz*cos1+Syz*sin1
    K01 = Syz*cos1-Sxz*sin1
    K00 = Sxx + Syy
    
    c2 = -1*(K00 + K11 + K22)
    c1 = K00*K11 + K00*K22 + K11*K22 - K01*K01 - K10*K10
    c0 = K01*K01*K11 + K10*K10*K22 - K00*K11*K22
    
    p = c1 - (1/3.0)*c2*c2
    q = (2.0/27)*c2**3 - (1.0/3)*c1*c2 + c0
    R = 0.25*q*q + (1.0/27)*p**3
    
    if R > 0:
        delta2 = (-1.0/3)*c2 + (-0.5*q+np.sqrt(R))**(1.0/3) + (-0.5*q-np.sqrt(R))**(1.0/3)
    else:
        rho = np.sqrt((-1.0/27)*p**3)
        phi = np.arccos(-1.0*q/(2*rho))
        delta2 = np.min([(-1/3.0)*c2+2*rho**(1.0/3)*np.cos(phi/3.0),
                         (-1/3.0)*c2+2*rho**(1.0/3)*np.cos((phi+2*np.pi)/3.0),
                         (-1/3.0)*c2+2*rho**(1.0/3)*np.cos((phi+4*np.pi)/3.0)])
    
    a = ((-1.0*K10)/(K11-delta2))*cos1 + (K01/(K22-delta2))*sin1
    b = ((-1.0*K10)/(K11-delta2))*sin1 + ((-1.0*K01)/(K22-delta2))*cos1
    u = (1.0/(1+a*a+b*b))*((1+b*b)*Xm - a*b*Ym + a*Zm)
    v = (1.0/(1+a*a+b*b))*(-1.0*a*b*Xm + (1+a*a)*Ym + b*Zm)
    w = (1.0/(1+a*a+b*b))*(a*Xm + b*Ym + (a*a+b*b)*Zm)
    
    nx = a/np.sqrt(a*a + b*b + 1.0)
    ny = b/np.sqrt(a*a + b*b + 1.0)
    nz = -1.0/np.sqrt(a*a + b*b + 1.0)
    
    vector = np.array([nx,ny,nz])
    start = np.array([Xm,Ym,Zm])
#    print start
#    print vector
    
    mag = -Zm / nz
    x = Xm + nx*mag
    y = Ym + ny*mag
    
    print (x, y)
    return (x,y)

#print getPoint((0.0,0.0,0.0),(0.0,1.0,1.0),(0.0,1.9,2.0),(0.0,3.0,3.1),(0.0,4.2,3.9))