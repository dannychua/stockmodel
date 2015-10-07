# %% header
# % handle a holding and the related logic
# % date: 7/3/2015

# %%
# % it is a handle class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% not needed


class Holding(object):
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])