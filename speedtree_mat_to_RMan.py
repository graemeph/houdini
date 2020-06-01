import hou
import menutools

tex = hou.ui.displayMessage("add renderman .tex to filename? You'll need to make sure to convert with RM Texture manager. This is best for LOPs", buttons=('Ok', 'Cancel', ), title='.tex')

nodes = hou.selectedNodes()
mat = hou.node('/mat')
pxrNodes = []

for n in nodes:
    print n.path()
    pxrMat = menutools.createBxdf("pxrsurface")
    pxrNode = hou.node('/mat/' + str(pxrMat))
    
    pxrNodes.append(pxrNode)
    stMat = hou.node(n.path())
    
    name = stMat.name()
    type = name.split('_')[0].lower()
    print type
    
    ## colour map
    texCol = stMat.parm('ColorMap').eval()
    
    if texCol != "":
        col = pxrNode.createNode('pxrtexture', 'col')
        srf = hou.node(col.parent().path() + '/pxrsurface1')
        srf.setInput(2, col, 0)
        
        if tex == 1:
            col.parm('filename').set(texCol)
        else:
            col.parm('filename').set(str(texCol) + ".tex")
        
        if type == "leaf":
            srf.parm('diffuseDoubleSided').set(1)
            srf.parm('diffuseTransmitGain').set(0.5)
            srf.parmTuple('diffuseTransmitColor').set([0.025, 0.084, 0.025])
                
    ## opacity map
    texOpac = stMat.parm('OpacityMap').eval()
    
    if texOpac != "":
        opac = pxrNode.createNode('pxrtexture', 'opac')
        srf = hou.node(opac.parent().path() + '/pxrsurface1')
        srf.setInput(96, opac, 1)
                
        if tex == 1:
            opac.parm('filename').set(texOpac)
        else:
            opac.parm('filename').set(str(texOpac) + '.tex')
        
        
    ## normal map
    texN = stMat.parm('NormalMap').eval()
    
    if texN != "":
        n = pxrNode.createNode('pxrnormalmap', 'normal')
        srf = hou.node(n.parent().path() + '/pxrsurface1')
        srf.setInput(94, n, 0)
        
        if tex == 1:
            n.parm('filename').set(texN)
        else:
            n.parm('filename').set(str(texN) + '.tex')
        
        
        scale = stMat.parm('NormalScale').eval()
        n.parm('bumpScale').set(scale)
        
    ## gloss map
    texGloss = stMat.parm('GlossMap').eval()
    
    if texGloss != "":
        gloss = pxrNode.createNode('pxrtexture', 'Gloss')
        to = pxrNode.createNode('pxrtofloat3')
        srf = hou.node(gloss.parent().path() + '/pxrsurface1')
        
        if type != 'leaf':
            srf.setInput(19, to, 0)
        else:
            srf.setInput(28, to, 0)
            srf.parm('clearcoatFresnelMode').set(2)
            srf.parm('clearcoatRoughness').set(0.6)
        
        to.setInput(0, gloss, 1)
        
        if tex == 1:
            gloss.parm('filename').set(texGloss)
        else:
            gloss.parm('filename').set(str(texGloss) + '.tex')
        
        
    ## subsurface amount map
    texSSSa = stMat.parm('SubsurfaceAmountMap').eval()
    
    if texSSSa != "":
        sssa = pxrNode.createNode('pxrtexture', 'SSS_Amount')
        srf = hou.node(sssa.parent().path() + '/pxrsurface1')
        srf.setInput(69, sssa, 1)
        
        if tex == 1:
            sssa.parm('filename').set(texSSSa)
        else:
            sssa.parm('filename').set(str(texSSSa) + '.tex')
        
        
    ## subsurface map
    texSSS = stMat.parm('SubsurfaceMap').eval()
    
    if texSSS != "":
        sss = pxrNode.createNode('pxrtexture', 'SSS')
        srf = hou.node(sss.parent().path() + '/pxrsurface1')
        srf.setInput(70, sss, 0)
        
        if tex == 1:
            sss.parm('filename').set(texSSS)
        else:
            sss.parm('filename').set(str(texSSS) + '.tex')
                    
    pxrNode.layoutChildren()
        
for idx, val in enumerate(pxrNodes):
    print(idx, val)
    val.setName(str(nodes[idx]))
    
    
