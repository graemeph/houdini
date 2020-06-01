node = hou.selectedNodes()[0]
print node
it = node.parm('num_materials').eval()
print it
store_mat = []

for i in range(it):
    curMat = node.parm('shop_materialpath' + str(i+1)).eval()
    s = curMat.split('/')
    newMat = '/mat/' + str(s[-1])
    node.parm('shop_materialpath' + str(i+1)).set(newMat)
    store_mat.append(newMat)
    
    
#import to lops
############################

doLop = hou.ui.displayMessage("Do LOPS import too?", buttons=('Ok', 'Cancel', ), title='lop')

if doLop == 0:
    wrangle = node.createOutputNode("attribwrangle", "paths")
    wrangle.parm('class').set(1)
    wrangle.parm('snippet').set("s[]@groups = detailintrinsic(0, 'primitivegroups');\n" + "foreach(string g; @groups){\n" + "    if(inprimgroup(0, g, @primnum) == 1){\n" + "        s@gatt = g;\n" + "    }\n" + "}\n\n" + "s@usdprimpath = sprintf(\"/root/%d\", s@gatt);\ns@path=s@usdprimpath;")
    
    
    stage = hou.node("/stage")
    import_tree = stage.createNode("sopimport", "import_tree")
    import_tree.parm('soppath').set(wrangle.path())
    import_tree.parm('enable_kindschema').set(1)
    import_tree.parm('kindschema').set('nestedgroup')
    x = stage.createNode("xform", "roate_90")
    x.parm("primpattern").set("/*")
    x.parm('rx').set(-90)
    x.parmTuple('p').set([0,0,0])
    x.setFirstInput(import_tree)
    
    mat = stage.createNode("materiallibrary", "tree_materials")
    mat.setFirstInput(x)
    mat.setGenericFlag(hou.nodeFlag.Display, 1)
    stage.layoutChildren()
    
    matNodes = []
    
    for m in store_mat:
        this = hou.node(m)
        matNodes.append(this)
        
    #print matNodes
    
    hou.copyNodesTo(matNodes, mat)
    
    mat.parm('fillmaterials').pressButton()
    
    amount = mat.parm("materials").eval()
    
    for a in range(amount):
        matPath = mat.parm('matnode' + str(a+1)).eval()
        mat.parm('geopath' + str(a+1)).set('/root/' + str(matPath) + '_group')
    
    mat.setSelected(1)
    
    
