from exif import Image
import warnings


warnings.simplefilter(action='ignore')


def get_location(image_file: str= ''):
    """
    Принимает файл, обрабатывает фотографию и возвращает широту и долготу если они есть в метаданных.
    :param url: path to file
    :return: if nothing in url: None
             if metadata include geo: latitude, latitude_ref, longitude, longitude_ref
             else: str: 'Location is not available'
    """
    if image_file == '':
        return
    try:
        palm_1_image = image_file
    except:
        return "Cannot hadnle this file."

    image_members = dir(palm_1_image)
    if ('gps_latitude' or 'gps_latitude_ref' or 'gps_longitude' or 'gps_longitude_ref') in image_members:
        latitude = palm_1_image.get('gps_latitude', default= None)
        longitude = palm_1_image.get('gps_longitude', default= None)
        longitude_formatted = f'{int(longitude[0]) + int(longitude[1])/60 + int(longitude[2])/3600}'
        latitude_formatted = f'{int(latitude[0]) + int(latitude[1])/60 + int(latitude[2])/3600}'
        return latitude_formatted, longitude_formatted
    return ('Location is not available from EXIF')
