from linsys import LinearSystem
from plane import Plane
from vector import Vector

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form
if not (t[0] == p1 and
                t[1] == p2):
    print 'test case 1 failed'

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form
if not (t[0] == p1 and
                t[1] == Plane(constant_term='1')):
    print 'test case 2 failed'

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p4 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
# skip 1
# swap #2 and #3
# add #2-#1 -> 0,0,-2=2
# swap #2 and #3 1,1,1=1;0,1,0=2;0,0,-2=2;1,0,-2=2
# swap #2 and #4
# add #2-#1 -> 0,-1,-3=1
# add #2+#4 -> 0,0,-3,3

# 0,2=2;0,3=3
# 0,3-2*3/2=3-3/2*2


# skip 1
# skip 2
# add -1*#1 + #3 -> 0,0,-2=2
# add -1*#3 + #4 -> 0,-1,-1=-1
# add 1*#2 + #4 -> 0,0,-1=1
# add -1*#3 + #4 -> 0,0,1,-1
# add 1*#3 + #4 -> 0,0,-1=-2
# add -1*#3 + #4 -> 0,0,1,-1
s = LinearSystem([p1,p2,p3,p4])
t = s.compute_triangular_form
print s
print t
if not (t[0] == p1 and
                t[1] == p2 and
                t[2] == Plane(normal_vector=Vector(['0','0','-2']), constant_term='2') and
                t[3] == Plane()):
    print 'test case 3 failed'

p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','-1','1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','2','-5']), constant_term='3')
s = LinearSystem([p1,p2,p3])
t = s.compute_triangular_form
if not (t[0] == Plane(normal_vector=Vector(['1','-1','1']), constant_term='2') and
                t[1] == Plane(normal_vector=Vector(['0','1','1']), constant_term='1') and
                t[2] == Plane(normal_vector=Vector(['0','0','-9']), constant_term='-2')):
    print 'test case 4 failed'
