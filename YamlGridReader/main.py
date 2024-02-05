import itertools
import yaml 
import re 
import copy

class YamlGridReader:

    def __init__(self, yaml_path=None, yaml_dict=None, ignore_list=[]):
        if yaml_dict is not None:
            self.contents = yaml_dict
        elif yaml_path is not None:
            with open(yaml_path, 'r') as f:
                self.contents = yaml.safe_load(f)
        self.nogrid = []
        self.ignore_list = ignore_list

    def flatten_dict(self, d, parent_key='', sep='.'):
        """Flatten a nested dictionary, optionally skipping specified keys."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if new_key in self.ignore_list:
                self.nogrid.append({new_key:v})
            elif isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def listify_dict(self, d):
        dc = copy.deepcopy(d)
        for k,v in d.items():
            if isinstance(v, str) and "," in v:
                v = v.split(",")
                if re.search(r'(\.\d*|\d+e[+-]\d+)', v[0]):
                    v = [float(vi) for vi in v]
                elif re.search(r'^[+-]?\d+$', v[0]):
                    v = [int(vi) for vi in v]
            elif not isinstance(v, list):
                v = [v]
            dc[k] = v
        return dc

    def unflatten_dict(self, dictionary, separator='.'):
        """Reconstructs nested dictionaries from flat ones."""
        result_dict = {}
        for ng in self.nogrid:
            dictionary.update(ng)
        for key, value in dictionary.items():
            parts = key.split(separator)
            d = result_dict
            for part in parts[:-1]:
                if part not in d:
                    d[part] = {}
                d = d[part]
            d[parts[-1]] = value
        return result_dict
    
    def main(self):
        flattened = self.flatten_dict(self.contents)
        listed = self.listify_dict(flattened)
        combinations = list(itertools.product(*listed.values()))
        flat_dicts = [dict(zip(listed.keys(), values)) for values in combinations]
        param_list = [self.unflatten_dict(d) for d in flat_dicts]
        return param_list
    
    @classmethod
    def FromPath(cls, yaml_path, ignore_list=[]):
        return cls(yaml_path=yaml_path, ignore_list=ignore_list).main()
        
    @classmethod
    def FromDict(cls, yaml_dict, ignore_list=[]):
        return cls(yaml_dict=yaml_dict, ignore_list=ignore_list).main()