from ma import ma
from models.option import OptionModel


class OptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:

        model = OptionModel

        dump_only = ("id")
        include_fk = True
        load_instance = True

    
