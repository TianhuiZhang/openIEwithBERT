import numpy as np
import os



# POS num = 1+49+1
def get_random_mat():
    pos = {"num": 51, "dim": 5, "max": 10, "min": 0}

    posrand = np.random.uniform(pos["min"], pos["max"], (pos["num"], pos["dim"]))

    save_path = os.path.join(os.getcwd(), "")
    posfile = os.path.join(save_path, "pos_mat.npy")
    np.save(posfile, posrand)

    loader = np.load(posfile)
    print(loader)

get_random_mat()