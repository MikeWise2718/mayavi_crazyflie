import numpy as np 
import pandas as pd
from mayavi import mlab 
from tvtk.api import tvtk

sdir = 'data//'

pdf  = pd.read_csv(sdir+"crazyflie-parts.csv")
cdf  = pd.read_csv(sdir+"crazyflie-components.csv")
ptdf = pd.read_csv(sdir+"crazyflie-points.csv")
vidf = pd.read_csv(sdir+"crazyflie-vertidx.csv")

def getcolor(pdf,idx,rootname):
    r = pdf.at[idx,rootname+'.r']
    g = pdf.at[idx,rootname+'.g']
    b = pdf.at[idx,rootname+'.b']
    return((r,g,b))

for index, comp in cdf.iterrows():
    partid = comp['partid' ]

    pidx = np.argmax(pdf.partid==partid)
    amb = getcolor(pdf,pidx,'amb' )
    spc = getcolor(pdf,pidx,'spc' )
    dif = getcolor(pdf,pidx,'dif' )
    ems = getcolor(pdf,pidx,'ems' )
    alf = pdf.at[pidx,'amb.a']

    # subset the data frames to the part we need
    pt1df = ptdf[ ptdf.partid==partid ]
    vi1df = vidf[ vidf.partid==partid ]

    m11 = comp['rot.11']
    m12 = comp['rot.12']
    m13 = comp['rot.13']
    m21 = comp['rot.21']
    m22 = comp['rot.22']
    m23 = comp['rot.23']
    m31 = comp['rot.31']
    m32 = comp['rot.32']
    m33 = comp['rot.33']

    # transform order is scale, rotate, then translate
    scax = comp['sca.x']*pt1df.x
    scay = comp['sca.y']*pt1df.y
    scaz = comp['sca.z']*pt1df.z

    px = m11*scax + m12*scay + m13*scaz + comp['trn.x']
    py = m21*scax + m22*scay + m23*scaz + comp['trn.y']
    pz = m31*scax + m32*scay + m33*scaz + comp['trn.z']

    # zip up the column indexes into triangles
    #   note that the minus one is because mayavi has zero-based indices for meshes
    tris = [[v1,v2,v3] for v1,v2,v3 in zip(vi1df.v1-1,vi1df.v2-1,vi1df.v3-1)]

    # sadly we can do nothing with the specular and emissive colors
    mesh = mlab.triangular_mesh(px,py,pz, tris, color=amb, opacity=alf )

# now show evertyhing
mlab.show()