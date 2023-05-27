# **Benchmarking transfer learning methods for whole silde classification in TCGA project**
Benchmark the transfer learning methods for each TCGA sub-project.

### Dependents
* Python3 environment.
* Download [gdc-client](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool) and add to environment.
* Download and install [openslide](https://openslide.org/).


#### Python packages
```angular2html
pandas==1.4.3
pillow==8.4.0
matplotlib==3.5.2
scipy==1.8.0
numpy==1.22.3
openslide-python
fastai==2.7.9
histolab==0.5.1
```

### Benchmark workflow

1. clone benchmark from github
```angular2html
$git clone

```
2. Get abs path

```angular2html

$cd Benchmark_WSI_TCGA

```
```angular2html

$pwd

```
3. input the `manifest_samll` abs path.

* step1: Obtain TCGA sub-project WSIs

```angular2html

$python  step1_obtain_data.py /home/bio1/workdata/Benchmark_WSI/Benchmark/manifest_small

```
* step2: Extract and label tiles 
```angular2html

$python step2_extract_tiles.py /home/bio1/workdata/Benchmark_WSI/Benchmark/manifest_small

```
* setp3: training TCGA sub-project

```angular2html
$python step3_train.py /home/bio1/workdata/Benchmark_WSI/Benchmark/manifest_small
```

### The small test structure

```angular2html
--main
    --manifest_small
        --gdc_manifest.2022-08-25_KIRC.txt
        --gdc_manifest.2022-08-25_OV.txt
    --Data
        --KIRC
            --9dab4412-5c93-49c2-9ee6-2d2ba1a9950d
            --688fd165-1980-42c0-b1d7-2175f9ad141f
            --a54ed845-eb46-402a-bceb-e89d3fce5c76
            --fc12ffe5-deda-4dfd-8a2b-72eb224d2688
        --OV
            --366afb00-82d3-48a4-83bc-6c91740a96d4
            --a9b1a354-8a8d-419b-be9c-3928f88c052f
            --b5a9f9f8-0313-4c44-af71-d2562354f4fb
            --ecdcf444-f6e9-40df-899b-efd996795c79
    --Tiles
        --KIRC
            --Grid_levelmax_50_50
            --Grid_levelmax_50_50_result_resize50_alexnet
            --Grid_levelmax_50_50_result_resize50_googlenet
            --Grid_levelmax_50_50_result_resize50_resnet34
            --Grid_levelmax_50_50_result_resize50_vgg13
            --Grid_levelmax_125_125
            --Grid_levelmax_125_125_result_resize125_alexnet
            --Grid_levelmax_125_125_result_resize125_googlenet
            --Grid_levelmax_125_125_result_resize125_resnet34
            --Grid_levelmax_125_125_result_resize125_vgg13
            --Grid_levelmax_224_224
            --Grid_levelmax_224_224_result_resize224_alexnet
            --Grid_levelmax_224_224_result_resize224_googlenet
            --Grid_levelmax_224_224_result_resize224_resnet34
            --Grid_levelmax_224_224_result_resize224_vgg13
        --OV
            --Grid_levelmax_50_50
            --Grid_levelmax_50_50_result_resize50_alexnet
            --Grid_levelmax_50_50_result_resize50_googlenet
            --Grid_levelmax_50_50_result_resize50_resnet34
            --Grid_levelmax_50_50_result_resize50_vgg13
            --Grid_levelmax_125_125
            --Grid_levelmax_125_125_result_resize125_alexnet
            --Grid_levelmax_125_125_result_resize125_googlenet
            --Grid_levelmax_125_125_result_resize125_resnet34
            --Grid_levelmax_125_125_result_resize125_vgg13
            --Grid_levelmax_224_224
            --Grid_levelmax_224_224_result_resize224_alexnet
            --Grid_levelmax_224_224_result_resize224_googlenet
            --Grid_levelmax_224_224_result_resize224_resnet34
            --Grid_levelmax_224_224_result_resize224_vgg13
```