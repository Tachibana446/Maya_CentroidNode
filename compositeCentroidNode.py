# -*- coding: utf-8 -*-
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as OpenMayaUI
import sys

# Use Api 2.0


def maya_useNewAPI():
    pass


class compositeCentroidNode(om.MPxNode):
    id = om.MTypeId(0x7f005)
    name = 'compositeCentroidNode'
    inputArray = om.MObject()

    # Child Attribute
    inputWeight = om.MObject()
    inputPosition = om.MObject()

    # Output Attributes
    outputPosition = om.MObject()
    outputWeight = om.MObject()

    def __init__(self):
        om.MPxNode.__init__(self)

    @staticmethod
    def creator():
        return compositeCentroidNode()

    @staticmethod
    def initialize():
        # output Weight
        nAttr = om.MFnNumericAttribute()
        compositeCentroidNode.outputWeight = nAttr.create(
            'outputWeight', 'ow', om.MFnNumericData.kFloat, 0.0)
        compositeCentroidNode.addAttribute(compositeCentroidNode.outputWeight)

        # output Position
        nAttr = om.MFnNumericAttribute()
        compositeCentroidNode.outputPosition = nAttr.create(
            'outputPosition', 'op', om.MFnNumericData.k3Float, 1.0)
        compositeCentroidNode.addAttribute(
            compositeCentroidNode.outputPosition)

        # input child
        nAttr = om.MFnNumericAttribute()
        compositeCentroidNode.inputWeight = nAttr.create(
            "weight", "w", om.MFnNumericData.kFloat, 0)
        nAttr.readable = True
        nAttr = om.MFnNumericAttribute()
        compositeCentroidNode.inputPosition = nAttr.create(
            "position", "p", om.MFnNumericData.k3Float)
        nAttr.readable = True

        # input Array
        cAttr = om.MFnCompoundAttribute()
        compositeCentroidNode.inputArray = cAttr.create("inputArray", "ia")
        cAttr.array = True
        cAttr.readable = False
        cAttr.indexMatters = False
        cAttr.addChild(compositeCentroidNode.inputWeight)
        cAttr.addChild(compositeCentroidNode.inputPosition)
        cAttr.readable = True
        cAttr.usesArrayDataBuilder = True
        compositeCentroidNode.addAttribute(compositeCentroidNode.inputArray)
        compositeCentroidNode.attributeAffects(
            compositeCentroidNode.inputArray, compositeCentroidNode.outputPosition
        )

    def compute(self, plug, dataBlock):
        arrayDataHandle = dataBlock.inputArrayValue(
            compositeCentroidNode.inputArray
        )

        # sum of Weghts and Displacement * Weight.
        sumW = 0
        sumX = 0
        sumY = 0
        sumZ = 0

        for _i in range(len(arrayDataHandle)):
            # now Value of Array DataHandle
            v = arrayDataHandle.inputValue()
            wHandle = v.child(compositeCentroidNode.inputWeight)
            w = wHandle.asFloat()
            pHandle = v.child(compositeCentroidNode.inputPosition)
            p = pHandle.asFloat3()

            sumW += w
            sumX += p[0] * w
            sumY += p[1] * w
            sumZ += p[2] * w
            # next Value of Array DataHandle
            arrayDataHandle.next()

        # calc each Displacement 
        resX = 0
        resY = 0
        resZ = 0
        if(sumW != 0):
            resX = sumX / sumW
            resY = sumY / sumW
            resZ = sumZ / sumW

        outhandle = dataBlock.outputValue(
            compositeCentroidNode.outputPosition
        )
        outhandle.set3Float(resX, resY, resZ)
        outhandle = dataBlock.outputValue(
            compositeCentroidNode.outputWeight
        )
        outhandle.setFloat(sumW)
        dataBlock.setClean(plug)


def initializePlugin(obj):
    mplugin = om.MFnPlugin(obj)
    try:
        mplugin.registerNode(compositeCentroidNode.name, compositeCentroidNode.id,
                             compositeCentroidNode.creator, compositeCentroidNode.initialize, om.MPxNode.kDependNode)
    except:
        sys.stderr.write('Failed to register node: %s' %
                         compositeCentroidNode.name)
        raise


def uninitializePlugin(obj):
    mplugin = om.MFnPlugin(obj)
    try:
        mplugin.deregisterNode(compositeCentroidNode.id)
    except:
        sys.stderr.write('Failed to uninitialize node: %s' %
                         compositeCentroidNode.name)
        pass
