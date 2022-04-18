def almost_equal(obj1, obj2, exclude_paths=[]):
    """Helper functions for legacy tests"""
    def almost_equal_helper(x, y, path):

        if isinstance(x, dict):
            if not isinstance(y, dict):
                print(f"At path {path}, obj1 was of type dict while obj2 was not")
                return False

            if not set(x.keys()) == set(y.keys()):
                print(f"At path {path}, obj1 has keys\n{x.keys()}\n while obj2 has keys\n{y.keys()}")
                return False

            for key in x.keys():
                current_path = path + [key]
                if current_path not in exclude_paths:
                    if not almost_equal_helper(x[key], y[key], current_path):
                        return False

        elif isinstance(x, list) or isinstance(x, tuple):
            if not( (isinstance(y, list) or isinstance(y, tuple)) and len(x) == len(y)):
                print(f"At path {path}, obj1 is an array and obj2 is either not an array or has different length")
                return False

            for i in range(len(x)):
                if not almost_equal_helper(x[i], y[i], path):
                    return False

        else:
            if not x == y:
                print(f"{x} != {y} at path {path}")
                return False

        return True

    return almost_equal_helper(obj1, obj2, [])
