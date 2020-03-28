def config(filename=None):

    import flood.models
    flood.models.config()
    flood.models.create_tables()