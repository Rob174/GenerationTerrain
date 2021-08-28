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
- ⏳ Dump rivers into HDF5 dataset (stored as images matching elevation map locations)

# Saturday Aug 28 2021
[f2925e3](https://github.com/Rob174/GenerationTerrain/tree/f2925e35c026f099b39c03ccb451b252e61da8cb)

- 🔨 Create datasets objects to use hdf5 files 
- 🔨 Operation Pipeline
- 🔨 Check if cycles
- 🔨 Check if more than 2 outputs

✔️ done and tested ; 🔨 done not tested ; ⏲️ in progress ; ⏳ waiting for other scripts to finish ; 🚩 problem ; 🐛 bug ; 〰️ ok does the job but maybe to improve ; 🛑 pause ; 🛰️ release

## TODO

- Use raster to superpose rivers
- View rivers on elevation maps