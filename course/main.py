import os
import pandas as pd
import numpy as np

from scipy.optimize import linprog
from matplotlib import pyplot as plt
from shapely import Polygon



ELEMENTS = ('Se', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'Sn', 'Te', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Hf', 'Os', 'Pt', 'Th')
elements_err = lambda elems: ["e"+e for e in elems]

ELEMENTS_GROUPS = {
    "g1": ["Se", "Sr", "Y", "Nb", "Mo"],
    # "g2": ["Ru", "Rh", "Pd", "Ag"],
    # "g3": ["Cd", "Sn", "Te"],
    # "g4": ["La", "Ce", "Pr", "Nd", "Sm"],
    # "g5": ["Gd", "Dy", "Ho", "Er", "Tm", "Yb", "Hf", "Os", "Pt"],
}

ZR_COL = "Zr"
EUFE_COL = "[Eu/Fe]"


def float_cast(x):
    try:
        return np.float32(x)
    except:
        return np.nan

def read_data(path: str, elements: tuple = ELEMENTS):
    float_cols = list(elements) + elements_err(elements)
    data = pd.read_csv(path, skiprows=[0])
    data[float_cols] = data[float_cols].apply(float_cast)

    return data

def transform_egroup(data: pd.DataFrame, group: list):
    zr_err = elements_err([ZR_COL])[0]
    transformed_data = [
        data[[elem, err, ZR_COL, zr_err, EUFE_COL]].dropna().rename(
            mapper={
                elem: "elem",
                err: "eer",
                ZR_COL: "zr",
                zr_err: "zr_err",
                EUFE_COL: "x"
            },
            axis=1
        )
        for elem, err in zip(group, elements_err(group))]
    
    transformed_data = pd.concat(transformed_data)

    point_value = (transformed_data["elem"] - transformed_data["zr"]).values
    err_value = (transformed_data["eer"] + transformed_data["zr_err"]).values
    x = transformed_data["x"].values

    return x, point_value, err_value

def linreg(x: np.array, y: np.array, y_err: np.array):
    nvars = x.shape[0]
    A_ub = np.zeros([nvars*2, nvars+2])

    A_ub[:, 0] = np.r_[x, -x]
    A_ub[:, 1] = np.r_[np.ones(nvars), -np.ones(nvars)]
    A_ub[:nvars, 2:][np.diag_indices(nvars)] = -y_err
    A_ub[nvars:, 2:][np.diag_indices(nvars)] = -y_err
    
    b_ub = np.r_[y, -y]

    c = np.r_[0, 0, np.ones(nvars)]

    bounds = np.array([(None, None)]*2 + [(0, None)]*nvars)

    return linprog(c, A_ub, b_ub, bounds=bounds)

def plot_linprog(x: np.array, 
                 y: np.array, 
                 y_err: np.array, 
                 b1: float, 
                 b2: float, 
                 title: str,
                 imgpath: str = "./course/doc/img"):
    plt.errorbar(x, y, y_err, marker="o", linestyle="", label="$log \epsilon (X/Zr)$")
    plt.plot(x, x*b1+b2, label="$linreg$")
    plt.legend()
    plt.grid()
    plt.title(title)
    plt.xlabel(EUFE_COL)
    os.makedirs(imgpath, exist_ok=True)
    plt.savefig(os.path.join(imgpath, f"{title}.png"))
    plt.close()

def infoset_bbox(xy: tuple):
    eges = lambda i: np.repeat(xy[i], 2)
    close = lambda t: np.r_[t, t[0]]

    x = close(eges(0))
    y = close(np.roll(eges(1), 1))

    return x, y

def plot_infoset(x: np.array, 
                 y: np.array, 
                 y_err: np.array, 
                 b1: float, 
                 b2: float, 
                 title: str,
                 imgpath: str = "./course/doc/img",
                 lb: float=-1,
                 ub: float=1):
    poligons = [Polygon((
        (lb, -lb * xi + yi - yi_err), 
        (lb, -lb * xi + yi + yi_err), 
        (ub, -ub * xi + yi + yi_err), 
        (ub, -ub * xi + yi - yi_err), 
    )) for xi, yi, yi_err in zip(x, y, y_err)]

    infoset = poligons[0]
    for poligon in poligons[1:]:
        infoset = infoset.intersection(poligon)
    if infoset.is_empty:
        return None, None
    
    minmax = lambda t: np.r_[np.min(t), np.max(t)]
    xy = infoset.exterior.xy
    mmxy = minmax(xy[0]), minmax(xy[1])
    bbox = infoset_bbox(mmxy)
    
    os.makedirs(imgpath, exist_ok=True)
    # for poligon in poligons:
    #     plt.plot(*poligon.exterior.xy)
    plt.plot(*xy, label="infoset borders")
    plt.scatter(np.mean(mmxy[0]), np.mean(mmxy[1]), label="infoset mean point")
    plt.plot(*bbox, linestyle="--", label="infoset bbox")
    plt.xlabel(r"$\beta_1$")
    plt.ylabel(r"$\beta_2$")
    plt.title(f"{title} infoset")
    plt.legend()
    plt.savefig(os.path.join(imgpath, f"{title} infoset.png"))
    plt.close()

    return mmxy

def main():
    data = read_data("data/science.adf1341_sm_data-s1.v2.csv")
    for meta, group in ELEMENTS_GROUPS.items():
        x, y, y_err = transform_egroup(data, group)
        out = linreg(x, y, y_err)
        b1, b2 = out.x[:2]
        plot_infoset(x, y, y_err, b1, b2, " ".join(group))
        plot_linprog(x, y, y_err, b1, b2, " ".join(group))
        
        print(group)
        print(f"(\\beta_1, \\beta_2) = ({b1:.1f}, {b2:.1f})")

        plot_linprog(x, y, 3*y_err, b1, b2, " ".join(group) + " 3sig")
        ib1, ib2 = plot_infoset(x, y, 3*y_err, b1, b2, " ".join(group) + " 3sig")
        out = linreg(x, y, 3*y_err)
        b1, b2 = out.x[:2]

        print(f"(\\beta_1, \\beta_2) = ({b1:.1f}, {b2:.1f})")
        print(f"(\\beta_1, \\beta_2) = ({ib1}, {ib2})")
        print(f"(\\beta_1, \\beta_2) = ({np.mean(ib1):.3f}, {np.mean(ib2):.3f})")
        

if __name__ == '__main__':
    main()
