import mmap
import struct

class MySharedMemory(object):

    """
    引数：共有ファイル名,フォーマット文字(structのやつ)
    対応フォーマット文字：{'c','b','B','?','h','H','i','I','l','L','f','q','Q','d'}
    参照：http://docs.python.jp/2/library/struct.html
    """
    def __init__(self, FNAME, formatcharacter):
        self._FNAME = FNAME
        self._unitInfo(formatcharacter)

        self._map = mmap.mmap( -1, 1000, self._FNAME )

    def __del__(self):
        self.closeMap()

    """
    フォーマット文字から型のサイズを取得
    """
    def _unitInfo(self,formatcharacter):
        self._formatcharacter = formatcharacter

        if formatcharacter in {'c','b','B','?'}:
            self._unitSize = 1
        elif formatcharacter in {'h','H'}:
            self._unitSize = 2
        elif formatcharacter in {'i','I','l','L','f'}:
            self._unitSize = 4
        elif formatcharacter in {'q','Q','d'}:
            self._unitSize = 8

    def setData(self, data, offset):
        self._map.seek( offset * self._unitSize )
        self._map.write( struct.pack( self._formatcharacter, data))

    def getData(self, offset):
        self._map.seek( offset * self._unitSize )

        return struct.unpack(
            self._formatcharacter,
            self._map.read(self._unitSize))[0]

    def closeMap(self):
        self._map.close()


if __name__ == '__main__':
    FNAME = "testmap"
    shmem = MySharedMemory( FNAME, 'f')

    myNum = int(shmem.getData(0) + 1)
    shmem.setData( myNum, 0 )

    print("My process number => ",myNum )

    while True:
        for index in range( 1, int(shmem.getData(0)) + 1):
            print("Process {} says => {}", index, shmem.getData(index))
        input_str = input("Input : ")

        if "exit" in input_str:
            break

        shmem.setData(float(input_str),myNum)
