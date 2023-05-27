import time

from fastai.vision.all import *
import matplotlib.pyplot as plt
from torchvision.models import vgg13, resnet34, googlenet, alexnet
import warnings

warnings.simplefilter(action='ignore')
import yellowbrick as yb
from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score
import os


class SklearnWrapper(BaseEstimator):
    _estimator_type = "classifier"
    target_type_ = "BINARY"

    def __init__(self, model):
        self.model = model
        self.classes_ = [0, 1]

    def fit(self, X, y):
        pass

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))

    def get_new_preds(self, X):
        # new_to = self.model.dls.valid_ds.new(X)
        # new_to.conts = new_to.conts.astype(np.float32)
        # new_dl = self.model.dls.valid.new(new_to)
        with self.model.no_bar():
            test_dl = self.model.dls.test_dl(X)  # Create a test dataloader
            preds, _, dec_preds = self.model.get_preds(dl=test_dl, with_decoded=True)  # Make predictions on it
            # preds, dec_preds = self.model.get_preds()
        return (preds, dec_preds)

    def predict_proba(self, X):
        return self.get_new_preds(X)[0].numpy()

    def predict(self, X):
        return self.get_new_preds(X)[1].numpy()


# label function
def label_func1(f):
    return f[:-4].split('_')[-1]


# main train function
def run_train(tiles_path, tile_size_, model):
    """
    run train
    :param tiles_path: tiles path
    :param tile_size_: pixel
    :param model: transfer larning model
    :return:None
    """
    # x = "/home/bio1/DPlearning/NHSC_grid/NHSC_grid_level0_200_224_224"
    tile_size = tile_size_[0]
    # make result file
    res_dir = tiles_path + "_result_resize" + str(tile_size) + "_" + model
    os.makedirs(res_dir, exist_ok=True)
    os.chdir(res_dir)

    path = Path(tiles_path)
    # path.ls()
    files = get_image_files(path, recurse=True)
    # len(files)

    splits = RandomSplitter(valid_pct=0.2)(range_of(files))
    if model == "alexnet" and tile_size == 50:
        dls = ImageDataLoaders.from_name_func(path, files, label_func=label_func1, item_tfms=Resize(224),
                                              splits=splits)
    else:
        dls = ImageDataLoaders.from_name_func(path, files, label_func=label_func1, item_tfms=Resize(tile_size),
                                              splits=splits)

    # dls.valid_ds.items[:3]

    X_train = dls.train.items
    X_test = dls.valid.items
    dics = {'normal': 1, 'cancer': 0}
    y_train = np.array([dics[label_func1(x.name)] for x in X_train])
    y_test = np.array([dics[label_func1(x.name)] for x in X_test])

    dls.c
    dls.show_batch()
    # plt.show()
    plt.savefig("batch.pdf")
    # model = ["resnet34", "alexnet", "vgg13", "googlenet"]
    # choose different model
    if model == "resnet34":
        learn = vision_learner(dls, resnet34, metrics=[accuracy, error_rate])
    if model == "alexnet":
        learn = vision_learner(dls, alexnet, metrics=[accuracy, error_rate])
    if model == "vgg13":
        learn = vision_learner(dls, vgg13, metrics=[accuracy, error_rate])
    if model == "googlenet":
        learn = vision_learner(dls, googlenet, metrics=[accuracy, error_rate])
    start = time.time()
    # train
    learn.fine_tune(2)

    print(f"train time: {time.time() - start}")

    # learn.export(os.path.join(res_dir, "learn.pkl"))

    # show learning result
    learn.show_results()
    # plt.show()
    plt.savefig('show_result.pdf')

    interp = Interpretation.from_learner(learn)
    interp.plot_top_losses(9, figsize=(15, 10))
    plt.savefig('interpretation.pdf')
    # plt.show()
    # learn = load_learner("learn.pkl")
    plt.clf()
    # classification report
    wrapped_learn = SklearnWrapper(learn)

    classes = list(learn.dls.vocab)
    visualizer = yb.classifier.ClassificationReport(wrapped_learn, classes=classes, support=True,
                                                    title="classification Report")
    visualizer.score(X_test, y_test)
    visualizer.show(outpath="classificationReport.pdf")
    # prediction error
    plt.clf()

    visualizer = yb.classifier.ClassPredictionError(wrapped_learn, classes=classes, title="Class Prediction Error")
    visualizer.score(X_test, y_test)
    visualizer.show(outpath="ClassPredictionError.pdf")

    # auc
    plt.clf()
    visualizer = yb.classifier.ROCAUC(wrapped_learn,
                                      classes=classes,
                                      size=[1300, 600],
                                      title="AUC")
    visualizer.score(X_test, y_test)
    visualizer.show(outpath="ROCAUC.pdf")



def run_each_model(train_path, tiles):
    """
    run each model
    :param train_path: tiles path
    :param tiles: tiles
    :return: None
    """
    model = ["resnet34", "alexnet", "vgg13", "googlenet"]
    for line in model:
        print(f"train model: {line}")
        print(f"train pixel: {tiles[0]}")
        run_train(train_path, tiles, line)


def run(manifest_dir):
    """
    run benchmark
    :param manifest_dir: manifest dir
    :return: None
    """
    # manifest_dir = "/home/bio1/workdata/Benchmark_WSI/Benchmark/manifest"
    BASE_DIR = os.path.abspath(os.path.join(manifest_dir, ".."))

    for line in os.listdir(manifest_dir):
        project = line.strip().split('_')[2].replace(".txt", "")
        print(f"Start train {line}")
        case_path = os.path.join(BASE_DIR, "Data", project)
        case_id = os.path.join(manifest_dir, line)
        p_level = "max"
        for tile_size in [(50, 50), (125, 125), (224, 224)]:
            BASE_PATH = os.path.join(BASE_DIR, 'Tiles', project) + '/Grid_level' + p_level + "_" + '_'.join(
                [str(tile_size[0]), str(tile_size[1])])
            run_each_model(BASE_PATH, tile_size)
        print(f"Train {line} completed")

if __name__ == '__main__':
    manifest = sys.argv[1]
    run(manifest)
