import csv, os
from biothings.utils.dataload import dict_sweep, unlist

def package_restr_dict(dictionary):
    _d = {}
    _d['ndc'] = {}
    _d['ndc']['package'] = {}

    for key in dictionary:
        if key is None:
            continue
        if key == 'PRODUCTID':
            _d.update({'_id':dictionary[key]})
            _d['ndc'].update({'product_id':dictionary[key]})
        elif key == 'NDCPACKAGECODE':
            _d['ndc']['package'].update({key.lower():dictionary[key]})
        elif key == 'PACKAGEDESCRIPTION':
            _d['ndc']['package'].update({key.lower():dictionary[key]})
        else:
            _d['ndc'].update({key.lower():dictionary[key]})
    return _d

def product_restr_dict(dictionary):
    _d = {}
    _d['ndc'] = {}
    for key in dictionary:
        if key is None:
            continue
        if key == 'PRODUCTID':
            _d.update({'_id':dictionary[key]})
            _d['ndc'].update({'product_id':dictionary[key]})
        else:
            _d['ndc'].update({key.lower():dictionary[key]})
    return _d

def convert_to_unicode(dictionary):
    for key, val in dictionary.items():
        if isinstance(val, str):
            dictionary[key] = str(val)
        elif isinstance(val, dict):
            convert_to_unicode(val)
    return dictionary

def load_products(_file):
    f = open(_file,'r',encoding="latin1")
    reader = csv.DictReader(f,dialect='excel-tab')
    for row in reader:
        _dict = product_restr_dict(row)
        _dict = convert_to_unicode(dict_sweep(_dict))
        _dict["_id"] = _dict["ndc"]["productndc"]
        yield _dict

def load_packages(_file):
    f = open(_file,'r',encoding='latin1')
    reader = csv.DictReader(f,dialect='excel-tab')
    for row in reader:
        _dict = package_restr_dict(row)
        _dict = unlist(dict_sweep(_dict))
        _dict["_id"] = _dict["ndc"]["productndc"]
        yield _dict

def load_data(data_folder, drugbank_col=None):
    package_file = os.path.join(data_folder,"package.txt")
    product_file = os.path.join(data_folder,"product.txt")
    assert os.path.exists(package_file), "Package file doesn't exist..."
    assert os.path.exists(product_file), "Product file doesn't exist..."
    package_ndc = {}
    inchi_key = {}
    for doc in load_packages(package_file):
        package_ndc.setdefault(doc["_id"],[]).append(doc["ndc"])
    for doc in load_products(product_file):
        packages = package_ndc.get(doc["_id"],[])
        if packages:
            doc["ndc"]["package"] = []
            for pack in packages:
                # remove keys used for the merge (duplicates, already in product
                pack.pop("product_id",None)
                pack.pop("productndc",None)
                doc["ndc"]["package"].append(pack)
            if len(doc["ndc"]["package"]) == 1:
                doc["ndc"]["package"] = doc["ndc"]["package"].pop() # to dict
        ik = find_inchi_key(doc,drugbank_col)
        if ik:
            # IK found, but other productndc could also match the same
            # IK so we keep them in a list
            inchi_key.setdefault(ik,[]).append(doc["ndc"])
            continue
        else:
            # No IK found, we'll just return the doc as-is
            yield doc
    for ik,ndclist in inchi_key.items():
        if len(ndclist) == 1:
            ndclist = ndclist.pop() # back to single dict
        yield {"_id": ik, "ndc": ndclist}

def find_inchi_key(doc,drugbank_col):
    if not drugbank_col:
        return
    d = drugbank_col.find_one({"drugbank.products.ndc_product_code":doc["ndc"]["productndc"]})
    if d and d["drugbank"].get("inchi_key"):
        _id = d["drugbank"]["inchi_key"]
        return _id
    else:
        return

