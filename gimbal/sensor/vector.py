# -*- coding: utf-8 -*-

'''
Created on 18/02/2016

@author: david
'''
from copy import deepcopy
from math import cos, sin, sqrt, copysign

class Vector(object):

    @staticmethod
    def _det3x3(matrix):
        
        det = 0.0
        
        for inc in range(3):
            m = 1.0
            for r in range(3):                            
                
                c = (r + inc)%3                
                m *= matrix[r][c]                
            
            det += m
            
        for inc in range(3):
            m = 1.0
            for r in range(3):
                
                c = 2 - (r + inc)%3                
                m *= matrix[r][c]
            
            det -= m

        return det
       
    
    @staticmethod
    def _replaceCoeffs(coeffs, terms, column):
        
        m = deepcopy(coeffs)
        
        for row in range(3):
            m[row][column] = terms[row]
        
        return m
    
    
    @staticmethod
    def _resolveCramer(coeffs, terms):
        
        div = Vector._det3x3(coeffs)
        
        mx = Vector._replaceCoeffs(coeffs, terms, 0)
        my = Vector._replaceCoeffs(coeffs, terms, 1)
        mz = Vector._replaceCoeffs(coeffs, terms, 2)
        
        dx = Vector._det3x3(mx)
        dy = Vector._det3x3(my)
        dz = Vector._det3x3(mz)
        
        x = dx/div
        y = dy/div
        z = dz/div
        
        return [x,y,z]
    
    @staticmethod
    def _descomposeVector(modulus, angles):
        '''
        Descompose a vector according rotation angles in radians
        
        @param modulus: Modulus (length) of the vector
        @param angles: Rotation angles in radians of the XY-plane
        '''
        cosx = cos(angles[0])
        cosy = cos(angles[1])
        
        sin2x = sin(angles[0])**2
        sin2y = sin(angles[1])**2
        cos2y = cosy**2
        
        modulus2 = modulus * modulus
        
        t1 = modulus2 * sin2y
        t2 = modulus2 * cos2y
        t3 = modulus2 * sin2x
        
        coeffs = [[1.0, sin2y, 0.0], [0.0, cos2y, 1.0], [sin2x, 1.0, 0.0]]
        terms = [t1, t2, t3]
        
        #Returns x², y², z²
        desc = Vector._resolveCramer(coeffs, terms)
        
        for i in range(3):
            desc[i] = sqrt(desc[i])

        #Choose the right solution depending of the passed angles sign
        desc[0] = copysign(desc[0], angles[1])
        #Positive axis-X angle makes negative motion along Y direction
        desc[1] = copysign(desc[1], -angles[0]) 
        if cosx < 0.0 or cosy < 0.0 or modulus < 0.0:
            desc[2] = -desc[2]        
        
        return desc

    
    @staticmethod
    def rotateVectorByAngle(vector, angle):
        '''
        Rotates a 2-dimensional vector

        @param vector: 2-dimensional vector
        @param angle: angle in radians to rotate
        '''

        return Vector.rotateVector(vector, sin(angle), cos(angle))
    

    @staticmethod
    def rotateVector(vector, sine, cosine):
        '''
        Rotates a 2-dimensional vector

        @param vector: 2-dimensional vector
        @param sine: sine of the angle to rotate
        @param cosine: cosine of the angle to rotate
        '''

        x = vector[0] * cosine - vector[1] * sine
        y = vector[0] * sine + vector[1] * cosine

        return [x, y]
    

    @staticmethod
    def _applyRotation(rotationMatrix, vector):
        '''
        rotation matrix's order must be [3,3] and vector order must be [3]
        This restriction is not chequed due to performance.
        
        @param rotationMatrix: matrix's order [3, 3]
        @param vector: vector's order [3]        
        '''
        
        product = [0.0]*3
        
        for row in range(3):
            for col in range(3):
        
                product[row] += rotationMatrix[row][col] * vector[col]
                
        return product
                

    @staticmethod
    def rotateVector3D(vector, angles):
        '''
        Rotates a 3D-vector
        @param vector: 3D vector as [x,y,z]
        @param angles: Rotation angles as radians within 3-dimensions [pitch, roll, yaw]
        '''
        
        cosx = cos(angles[0])
        sinx = sin(angles[0])
        
        cosy = cos(angles[1])
        siny = sin(angles[1])
        
        cosz = cos(angles[2])
        sinz = sin(angles[2])
        
        rotationMatrixX = [[1.0, 0.0, 0.0],[0.0, cosx, -sinx],[0.0, sinx, cosx]] 
        rotationMatrixY = [[cosy, 0.0, siny],[0.0, 1.0, 0.0],[-siny, 0.0, cosy]]
        rotationMatrixZ = [[cosz, -sinz , 0.0],[sinz, cosz, 0.0],[0.0, 0.0, 1.0]]
        
        #Rotate on X-axis
        vector = Vector._applyRotation(rotationMatrixX, vector)
        #Rotate on Y-axis
        vector = Vector._applyRotation(rotationMatrixY, vector)
        #Rotate on Z-axis
        vector = Vector._applyRotation(rotationMatrixZ, vector)
        
        return vector
    
