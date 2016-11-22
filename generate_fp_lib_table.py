#!env python2
import os

isdir = os.path.isdir
join = os.path.join
cur_dir = os.path.abspath(os.path.dirname(__file__))

lst = [x[:-len('.pretty')] for x in os.listdir(cur_dir) if isdir(join(cur_dir, x)) and x.endswith('.pretty')]

template='  (lib (name {name})(type KiCad)(uri ${KISYSMOD}/{name}.pretty)(options "")(descr "The way you like them."))'

print "(fp_lib_table"
print '\n'.join([template.replace('{name}', x) for x in lst])

####
# Feel free to add your custom lib here

# print '  (lib (name MyFootprint)(type KiCad)(uri ${KIPRJMOD}/../../../kicad-mylib/myworks/my_footprint.pretty)(options "")(descr ""))'


####

print ")"

# overwrite ~/.config/kicad/fp-lib-table
