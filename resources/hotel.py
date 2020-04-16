from flask_restful import Resource, reqparsefrom models.hotel import HotelModelhoteis = [    {        'hotel_id': 'alpha',        'nome': 'Alpha Hotel',        'estrelas': 4.3,        'diaria': 420.34,        'cidade': 'Rio de Janeiro'    },    {        'hotel_id': 'bravo',        'nome': 'Bravo Hotel',        'estrelas': 4.8,        'diaria': 540.00,        'cidade': 'São Pualo'    },    {        'hotel_id': 'coco',        'nome': 'Coco Hotel',        'estrelas': 3.4,        'diaria': 330.54,        'cidade': 'Belo Horizonte'    }]class Hoteis(Resource):    def get(self):        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}class Hotel(Resource):    argumentos = reqparse.RequestParser()    argumentos.add_argument('nome')    argumentos.add_argument('estrelas')    argumentos.add_argument('diaria')    argumentos.add_argument('cidade')    @staticmethod    def get(hotel_id):        hotel = HotelModel.find_hotel(hotel_id)        if hotel:            return hotel.json()        return {'message': 'Hotel not found.'}, 404 # not found    @staticmethod    def post(hotel_id):        if HotelModel.find_hotel(hotel_id):            return {"message": "Hotel ID '{}' already exists.".format(hotel_id)}, 400 #Bad request        dados = Hotel.argumentos.parse_args()        hotel_objeto = HotelModel(hotel_id, **dados)        HotelModel.save_hotel(hotel_objeto)        return hotel_objeto.json()    @staticmethod    def put(hotel_id):        dados = Hotel.argumentos.parse_args()        hotelFounded = HotelModel.find_hotel(hotel_id)        if hotelFounded:            hotelFounded.update_hotel(**dados)            hotelFounded.save_hotel()            return hotelFounded.json(), 200        hotel_objeto = HotelModel(hotel_id, **dados)        hotel_objeto.save_hotel()        return hotel_objeto.json(), 201    @staticmethod    def delete(hotel_id):       hotel = HotelModel.find_hotel(hotel_id)       if hotel:           return {'message': 'Hotel deleted.'}       return {'message': 'Hotel not found.'}