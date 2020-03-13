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
    inputPositionArray = om.MObject()
    inputWeightArray = om.MObject()

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
            'outputWeight', 'ow', om.MFnNumericData.kFloat, 1.0)
        compositeCentroidNode.addAttribute(compositeCentroidNode.outputWeight)

        # output Position
        nAttr = om.MFnNumericAttribute()
        compositeCentroidNode.outputPosition = nAttr.create(
            'outputPosition', 'op', om.MFnNumericData.k3Float, 1.0)
        compositeCentroidNode.addAttribute(compositeCentroidNode.outputPosition)

        # input Weight Array
        nAttr = om.MFnTypedAttribute()
        compositeCentroidNode.inputWeightArray = nAttr.create(
            'inputWeightArray', 'iweights', om.MfnData.kDoubleArray
        )
        compositeCentroidNode.addAttribute(compositeCentroidNode.inputWeightArray)
        compositeCentroidNode.attributeAffects(
            compositeCentroidNode.inputWeightArray, compositeCentroidNode.outputPosition
        )

        # input Position Array
        nAttr = om.MFnTypedAttribute()
        compositeCentroidNode.inputPositionArray = nAttr.create(
            'inputPositionArray', 'ipos', om.MfnData.kPointArray
        )
        compositeCentroidNode.addAttribute(compositeCentroidNode.inputPositionArray)
        compositeCentroidNode.attributeAffects(
            compositeCentroidNode.inputPositionArray, compositeCentroidNode.outputPosition
        )


    def compute(self, plug, dataBlock):
        if(plug == compositeCentroidNode.outputPosition or plug == compositeCentroidNode.outputWeight):
            # dataHandle.data(MObject)をPointArrayDataにして、PointArrayData.arrayで配列を取得
            dataHandle = dataBlock.inputValue(compositeCentroidNode.inputPositionArray)
            _ipdata = om.MFnPointArrayData(dataHandle.data())
            ipoints = _ipdata.array()
            dataHandle = dataBlock.inputValue(compositeCentroidNode.inputWeightArray)
            _iwdata = om.MFnDoubleArrayData(dataHandle.data())
            iweights = _iwdata.array()


            sumW = sum(iweights)
            sumX = 0
            sumY = 0
            sumZ = 0
            
            for point in ipoints:
                sumX += point.x
                sumY += point.y
                sumZ += point.z

            resX = sumX / sumW
            resY = sumY / sumW
            resZ = sumZ / sumW
            
            outHandle = dataBlock.outputValue(compositeCentroidNode.outputPosition)
            outHandle.set3Float([resX,resY,resZ])
            outHandle = dataBlock.outputValue(compositeCentroidNode.outputWeight)
            outHandle.setFloat(sumW)
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
