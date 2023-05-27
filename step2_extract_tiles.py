import sys
from histolab.slide import Slide
import os
from histolab.tiler import GridTiler


def check_dim(org_dim, tile_size):
    """
    check dimension
    :param org_dim: original dimension
    :param tile_size: tile size
    :return:
    """
    tem = []
    for line in range(len(tile_size)):
        if tile_size[line] > org_dim[line]:
            tem.append(org_dim[line])
        else:
            tem.append(tile_size[line])
    return tuple(tem)


# extract tile and labeled
def extract_random_5050(info, BASE_PATH, case_path, p_level, tile_size):
    """
    extract tiles
    :param info: add labels
    :param BASE_PATH: base path
    :param case_path: case path
    :param p_level: p level
    :param tile_size: tiles size
    :return:
    """
    cals = info[1].split('-')[3][:2]
    if cals == '01':
        sub_folder = 'cancer'
    else:
        sub_folder = 'normal'
    process_path = os.path.join(BASE_PATH, sub_folder)

    path_ = os.path.join(case_path, info[0], info[1])
    nhsc_slide = Slide(path_, processed_path=process_path)
    print(f"Slide name: {nhsc_slide.name}")
    try:
        print(nhsc_slide.level_magnification_factor())
    except:
        print("null")
    if p_level == "max":
        levels = nhsc_slide.levels[-1]
    elif p_level == '0':
        levels = nhsc_slide.levels[0]
    print(levels)

    # low dim
    org_dim = nhsc_slide.level_dimensions(level=levels)
    check_tile_size = check_dim(org_dim, tile_size)

    suf = info[0] + "_" + sub_folder + ".png"

    grid_tiles_extractor = GridTiler(
        tile_size=check_tile_size,
        level=levels,
        check_tissue=True,  # default
        pixel_overlap=0,  # default
        prefix="",  # save tiles in the "grid" subdirectory of slide's processed_path
        suffix=suf  # default
    )
    grid_tiles_extractor.locate_tiles(
        slide=nhsc_slide,
        scale_factor=64,
        alpha=64,
        outline="#046C4C",
    )
    try:
        grid_tiles_extractor.extract(nhsc_slide)
    except:
        print('error')


def extract_each_wsi(cases, BASE_PATH, case_path, p_level, tile_size):
    """
    extract each wsi
    :param cases: case id
    :param BASE_PATH: base dir
    :param case_path: cast path
    :param p_level: p level
    :param tile_size: tile size
    :return: None
    """
    for line in cases:
        # print(f"extract tiles from {line}")
        tem = line.strip().split('\t')
        extract_random_5050(info=tem, BASE_PATH=BASE_PATH, case_path=case_path, p_level=p_level, tile_size=tile_size)


def run(manifest_dir):
    """
    run extracted tiles
    :param manifest_dir: dir
    :return: None
    """
    # manifest_dir = "/home/bio1/workdata/Benchmark_WSI/Benchmark/manifest"
    BASE_DIR = os.path.abspath(os.path.join(manifest_dir, ".."))

    for line in os.listdir(manifest_dir):
        project = line.strip().split('_')[2].replace(".txt", "")
        print(f"Start extract tiles from {line}")
        case_path = os.path.join(BASE_DIR, "Data", project)
        case_id = os.path.join(manifest_dir, line)
        p_level = "max"
        for tile_size in [(50, 50), (125, 125), (224, 224)]:
            os.makedirs(os.path.join(BASE_DIR, 'Tiles', project), exist_ok=True)
            BASE_PATH = os.path.join(BASE_DIR, 'Tiles', project) + '/Grid_level' + p_level + "_" + '_'.join(
                [str(tile_size[0]), str(tile_size[1])])
            cases = open(case_id).readlines()[1:]
            extract_each_wsi(cases, BASE_PATH, case_path, p_level, tile_size)
        print(f"Extract tiles from {project} completed.")


if __name__ == '__main__':
    manifest = sys.argv[1]
    run(manifest)
