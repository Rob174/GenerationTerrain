# Progress

✔️ done and tested ; 🔨 done not tested ; ⏲️ in progress ; ⏳ waiting for other scripts to finish ; 🚩 problem ; 🐛 bug ; 〰️ ok does the job but maybe to improve ; 🛑 pause ; 🛰️ release
## Monday Aug 23 2021
[24e6ea9](https://github.com/Rob174/GenerationTerrain/tree/24e6ea92df7289ef404dfca2929ca113fd54e3a6)

- ✔ Rivers read and extract points 
- ✔ Raster read

# Friday Aug 27 2021
[f2925e3](https://github.com/Rob174/GenerationTerrain/tree/f2925e35c026f099b39c03ccb451b252e61da8cb)

Cache rivers : convert to images

- ✔ First version GenerationTerrain.pstat
- ✔ Optimized version avoiding PIL np switch GenerationTerrain2.pstat
- ✔ Optimized version avoiding too many invtransform get GenerationTerrain5.pstat
- ✔ Dump rivers into HDF5 dataset (stored as images matching elevation map locations)

# Saturday Aug 28 2021
[1ce65c1](https://github.com/Rob174/GenerationTerrain/tree/1ce65c198794006569cb0a9d1ad39a959db4dfcd)

- ✔ Create datasets objects to use hdf5 files 
- ✔ Operation Pipeline
- 🔨 Check if cycles
- ✔ Check if more than 2 outputs
- ✔ Test graph1 build_graph
- ✔ Test graph1 execute

# Sunday Aug 29 2021
[070f95c](https://github.com/Rob174/GenerationTerrain/tree/070f95c3de5c5c9ae601e8faaa71a0273e11548d)

- ✔ Tests HDF5Dataset
- ✔ Test RiversDataset
- ✔ Test graph graphviz
- ✔ Improving initialization check of FolderInfos.py
- ✔ geotiff to hdf5

✔️ done and tested ; 🔨 done not tested ; ⏲️ in progress ; ⏳ waiting for other scripts to finish ; 🚩 problem ; 🐛 bug ; 〰️ ok does the job but maybe to improve ; 🛑 pause ; 🛰️ release

## TODO

- View rivers on elevation maps
- extract mountains drawing from dem
- filter dem 
  - no mountain = useless
  - rivers cut due to border line