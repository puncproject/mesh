
import dolfin as df
import subprocess
import os
import numpy as np

def create_mesh(fname, dim):
    subprocess.call(['gmsh -%d %s.geo' %(dim, fname)], shell=True)
    
    assert os.path.exists(fname + '.msh')
    # assert all(os.path.exists(f) for f in (fname+'.msh',
    #                                     fname + '_facet_region.msh',
    #                                     fname + '_physical_region.msh'))
def convert_msh_to_xml(fname, dim):
    subprocess.call(['dolfin-convert %s.msh %s.xml'%(fname, fname)], shell=True)

    assert os.path.exists(fname + '.xml')
    # assert all(os.path.exists(f) for f in (fname + '.xml',
    #                                     fname + '_facet_region.xml',
    #                                     fname + '_physical_region.xml'))

def convert_xml_to_hdf5(fname):
    mesh = df.Mesh(fname + ".xml")
    if os.path.exists(fname + '_physical_region.xml'):
        subdomains = df.MeshFunction(
            "size_t", mesh, fname + "_physical_region.xml")
    if os.path.exists(fname + '_facet_region.xml'):
        boundaries = df.MeshFunction("size_t", mesh, fname + "_facet_region.xml")
    hdf = df.HDF5File(mesh.mpi_comm(), fname + ".h5", "w")
    hdf.write(mesh, "/mesh")
    if os.path.exists(fname + '_physical_region.xml'):
        hdf.write(subdomains, "/subdomains")
    if os.path.exists(fname + '_facet_region.xml'):
        hdf.write(boundaries, "/boundaries")

def get_dim(fname):
    geometric_shapes = ["Line", "Surface", "Volume"]
    found = [False]*3

    with open(fname+'.geo') as f:
        f = f.readlines()

    for line in f:
        for i, shape in enumerate(geometric_shapes):
            if shape in line:
                found[i] = True

    dim = max([j+1 for j, truth in enumerate(found) if truth])
    print("dim: ", dim)
    return dim


if __name__ == '__main__':
    
    import sys
    from datetime import datetime
    fname = sys.argv[1]


    if os.path.exists(os.path.abspath(fname)+'.geo'):
        dim = get_dim(fname)
        geo_mtime = os.path.getmtime(os.path.abspath(fname) + '.geo')
        g_mtime = datetime.fromtimestamp(geo_mtime)
        print("geo-file exists and was last modified at ", g_mtime)
        if os.path.exists(os.path.abspath(fname) + '.msh'):
            msh_mtime = os.path.getmtime(os.path.abspath(fname) + '.msh')
            if msh_mtime < geo_mtime:
                print("msh-file has not been updated.")
                print("Creating a new mesh.")
                create_mesh(fname, dim)
            else:
                print("msh-file exists and it's up to date.")
            if os.path.exists(os.path.abspath(fname) + '.xml'):
                xml_mtime = os.path.getmtime(os.path.abspath(fname) + '.xml')
                if xml_mtime < msh_mtime:
                    print("xml-file has not been updated.")
                    print("Generating a new xml-file")
                    convert_msh_to_xml(fname, dim)
                else:
                    print("xml-file exists and it's up to date.")
                if os.path.exists(os.path.abspath(fname) + '.h5'):
                    h5_mtime = os.path.getmtime(os.path.abspath(fname) + '.h5')
                    if h5_mtime < xml_mtime:
                        print("h5-file has not been updated.")
                        print("Generating a new h5-file")
                        convert_xml_to_hdf5(fname)
                    else:
                        print("h5-file exists and it's up to date.")
                else:
                    print("Generating a new h5-file")
                    convert_xml_to_hdf5(fname)
            else:
                print("Generating a new xml-file")
                convert_msh_to_xml(fname, dim)
                print("Generating a new h5-file")
                convert_xml_to_hdf5(fname)
        else:
            print("Creating the mesh")
            create_mesh(fname, dim)
            print("Generating a new xml-file")
            convert_msh_to_xml(fname, dim)
            print("Generating a new h5-file")
            convert_xml_to_hdf5(fname)
    else:
        print("geo-file does not exists in folder.")
