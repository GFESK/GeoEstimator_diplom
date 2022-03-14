from struct import unpack


marker_mapping = {
    0xffd8: "Start of Image",
    0xffc4: "Define Huffman Table",
    0xffd9: "End of Image"
}

class JPEG:
    def __init__(self, image_file):
        self.img_data = image_file


    def decode(self):
        data = self.img_data
        f = self.img_data
        n = 0
        if b'Photoshop' in f:
            n=1
        elif b'CDEFGH' in f:
            n=2
        k = 0
        while (True):
            marker, = unpack(">H", data[0:2])
            if marker_mapping.get(marker) == "Define Huffman Table":
                k+=1
            if marker == 0xffd8:
                data = data[2:]
            elif marker == 0xffd9:
                if k <= 2 and n == 1:
                    return "Photo uploaded from Instagram."
                elif k > 2 and n == 2:
                    return "Photo uploaded from VKontakte."
                else:
                    return "Photo uploaded from unknown social network"
            elif marker == 0xffda:
                data = data[-2:]
            else:
                lenchunk, = unpack(">H", data[2:4])
                data = data[2 + lenchunk:]
            if len(data) == 0:
                break
