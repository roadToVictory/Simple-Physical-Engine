from math import sqrt, degrees, acos
 
# Definition class of Vector in three dimensions
class Vector3D():
 
    # Set coordinates of Vector
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # setters
    def setx(self, nx): self.x = float(nx)
    def sety(self, ny): self.y = float(ny)        
    def setz(self, nz): self.z = float(nz) 


    # check the equality of Vectors
    def __eq__(self, other):
        if self.x == other.x and self.y==other.y and self.z==other.z:
            return True
        else: return False

    #create a copy of itself
    def __copy__(self):
        return Vector3D(self.x, self.y, self.z)

    # magnitude of Vectors
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
 
    # add of two Vectors
    def __add__(self, oth):
        return Vector3D(self.x + oth.x, self.y + oth.y, self.z + oth.z)
 
    # subtract of two Vectors
    def __sub__(self, oth):
        return Vector3D(self.x - oth.x, self.y - oth.y, self.z - oth.z)
 
    # dot product of two Vectors
    def __xor__(self, oth):
        return self.x * oth.x + self.y * oth.y + self.z * oth.z
 
    # Method to calculate the cross product of two Vectors
    def __mul__(self, oth):
        # return np.cross(self.array, oth.array)
        return Vector3D(self.y * oth.z - self.z * oth.y,
                        self.z * oth.x - self.x * oth.z,
                        self.x * oth.y - self.y * oth.x)

    # normalization of Vector
    def normalization(self):
        return Vector3D(self.x/self.length(),self.y/self.length(),self.z/self.length())

    #get cordinates by brackets operators where x is 1, y is 2,z is 3
    def __getitem__(self, key):
        key=max(min(key,3),1)
        if(key==1):
            return self.x
        elif(key==2):
            return self.y
        else:
            return self.z
    
    # representation of Vector
    def __str__(self):
        return '[%s, %s, %s]' % (self.x, self.y, self.z)

    #static method create Vector3D from single data chunk
    @staticmethod
    def toVector(arr):
        return Vector3D(arr[1],arr[2],arr[3])

    def reverse(self):
        return Vector3D(-self.x,-self.y,-self.z)

#calculate the degree between two Vectors
def angle(a, b):
	m = a.x*b.x + a.y*b.y + a.z*b.z
	return degrees( acos( m / (a.length() * b.length()) ) )

#return distance between two Points
def distance(p1, p2):
    return sqrt((p2.x-p1.x)**2 + (p2.y-p1.y)**2 + (p2.z-p1.z)**2)

