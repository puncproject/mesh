# mesh
Unstructed meshes for use in simulations with e.g. PUNC, PUNC++ or PTetra.

The naming convention for the meshes are chosen to be unusually verbose since otherwise it has proven hard to remember exactly what each mesh is. The meshes are subdivided by folders into 1D, 2D and 3D meshes. In addition, some meshes may be 2D surfaces embedded in a 3D mesh. These are in the subfolder `surface`. The naming convention for the files is

```
<something>_in_<some_exterior_boundary>.geo
```
where `<something>` refers to what's inside the domain, e.g. "four circles", a "circle and a square" or just that the mesh is "nonuniform" in the sense that it has varying resolution throughout the domain (useful for testing Voronoi methods). One can also emphasize for instance _what_ sphere it is, say, the one in the Laframboise paper, by calling it `laframboise_sphere`. This makes the mesh more specific (less general) and in a certain sense more important since it indicates that this is not just something for a demo but possibly something for an actual simulation which may end up in a publication.

`<some_exterior_boundary>` is, obviously, the shape of the exterior boundary (e.g. a cube). If it is periodic, this should be indicated (e.g. `periodic_cube`).

Meshes which have different resolutions but which are otherwise identical may be suffixed by `_res` and a number, the higher the number the finer the resolution. 
