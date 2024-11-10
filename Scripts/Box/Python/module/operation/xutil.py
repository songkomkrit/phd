import os
import shutil
import json
import pandas as pd

# Create directory (if not exist)
def create_dir(dir):
    '''
        Usage: create directory (if not exist)
        Required arguments:
            dir: directory name
    '''
    
    try: os.makedirs(dir)
    except FileExistsError: pass


# Copy single file
def copy(srcpath, destpath):
    '''
        Usage: copy single file
        Required arguments:
            srcpath: source pathname
            destpath: destination pathname
    '''
    
    # Split path into directory and file
    srcdir, srcfile = os.path.split(srcpath) # source
    destdir, destfile = os.path.split(destpath) # destination
    
    # Create destination directory (if not exist)
    create_dir(destdir)

    # Copy source file into destination folder (filename unchanged)
    shutil.copy2(srcpath, destdir) # preserve file metadata
    
    # Rename copied file to correct destination filename
    os.rename(f"{destdir}/{srcfile}", destpath)


# Find maximum value of dictionary and key set
def max_dictval(dc):
    '''
        Usage: find maximum value of dictionary and all of its corresponding keys
        Required arguments:
            dc: dictionary
        Outputs:
            kmax: set of all keys of maximum value
            vmax: maximum value
    '''
    
    kmax = set()
    vmax = dc[next(iter(dc))] # value of first key
    for k, v in dc.items():
        if v > vmax:
            vmax = v
            kmax = {k}
        elif v == vmax:
            kmax.add(k)
    
    return kmax, vmax


# Find interval index of specific value from list of real-line splits
def itvpos(x, splits, closed='neither'):
    '''
        Usage: find interval index of specific value from array of real-line splits
        Required arguments:
            x: specific value of interest
            splits: list of real line splits
            closed: whether intervals are closed on left-side, right-side or neither ('left', 'right', 'neither')
        Outputs:
            interval index of specific input value
    '''

    if closed == 'left': # [_, s), [s, _)
        for i, s in enumerate(splits):
            if x < s: return i
    elif closed == 'neither': # (_, s), (s, _)
        for s in splits:
            if x == s:
                raise Exception(f"Open intervals are chosen but input value {x} is at split value {s}")
        closed = 'right' # Now it is safe to extend to (_, s], (s, _]

    if closed == 'right': # (_, s], (s, _]
        for i, s in enumerate(splits):
            if x <= s:
                return i

    # Last interval
    return i + 1


# Import dictionary from JSON file
def import_dict(jsonpath):
    '''
        Usage: parse JSON data into dictionary
        Required arguments:
            jsonpath: JSON filepath (usually metadata filepath)
        Outputs:
            dictionary
    '''
    
    with open(jsonpath) as file:
    	contents = file.read()

    # JSON data is parsed into dictionary
    return json.loads(contents)


# Export dataframe with nonduplicate entries
def nondup(df, ndcols, intcols=list(), intdtype='Int16'):
    '''
        Usage: export dataframe with nonduplicate entries
        Required arguments:
            df: dataframe
            ndcols: two-dimensional multilevel column lists with nonduplicate entries
        Optional arguments:
            intcols: integer columns (default: empty list)
            intdtype: Pandas integer data type (default: 'Int16' or pd.Int16Dtype())
        Outputs: same dataframe but without duplicate entries
    '''
    
    dfn = df.copy(deep=True)
    for i in range(len(ndcols),0,-1): # iterate over multilevel column lists with nonduplicate entries
        ccols = [f for cols in ndcols[0:i] for f in cols]
        dfn.loc[dfn[ccols].duplicated(), ccols] = pd.NA
    for col in intcols:
        dfn[col] = pd.array(dfn[col], dtype=intdtype)

    return dfn